#
# spec file for package glusterfs
#
# Copyright (c) 2015 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           glusterfs
# %%global prereltag rc1
Version:        5.7%{?prereltag}
Release:        100
Summary:        Aggregating distributed file system
License:        GPL-2.0 or LGPL-3.0+
Group:          System/Filesystems
Url:            http://gluster.org/

#Git-Clone:	git://github.com/gluster/glusterfs
#Git-Clone:	git://github.com/fvzwieten/lsgvt
Source:         http://download.gluster.org/pub/gluster/glusterfs/4.0/%version/%name-%version.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  fdupes
BuildRequires:  flex
BuildRequires:  libaio-devel
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  python3-devel
BuildRequires:  readline-devel
BuildRequires:  liburcu-devel >= 0.7
BuildRequires:  sqlite3-devel
BuildRequires:  glib2-devel
BuildRequires:  libattr-devel
BuildRequires:  libacl-devel
BuildRequires:  rdma-core-devel
BuildRequires:	libtirpc-devel
BuildRequires:	rpcgen
%if 0%{?sles_version} == 11
BuildRequires:  fuse-devel >= 2.6.5
BuildRequires:  libuuid-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
%else
BuildRequires:  pkgconfig(fuse) >= 2.6.5
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(uuid)
%endif
%if 0%{?suse_version} >= 1210
BuildRequires:  systemd
%endif
Requires:       python3
Requires:	python3-requests
Requires:	libglusterfs0 = %{version}
Requires:	libgfapi0 = %{version}
Requires:	libgfchangelog0 = %{version}
Requires:	libgfrpc0 = %{version}
Requires:	libgfxdr0 = %{version}

%description
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file system.
GlusterFS is one of the most sophisticated file systems in terms of
features and extensibility. It borrows a powerful concept called
Translators from GNU Hurd kernel. Much of the code in GlusterFS is in
user space and easily manageable.

%package -n libgfapi0
Summary:        GlusterFS API library
Group:          System/Libraries

%description -n libgfapi0
GlusterFS is a clustered file-system capable of scaling to several
petabytes.

%package -n libgfchangelog0
Summary:        GlusterFS volume changelog translator library
Group:          System/Libraries

%description -n libgfchangelog0
GlusterFS is a clustered file-system capable of scaling to several
petabytes.

The goal of this volume translator is to capture changes performed on
a GlusterFS volume. The translator needs to be loaded on the server
(bricks) and captures changes in a plain text file inside a
configured directory path (controlled by the "changelog-dir"
directive).

%package -n libgfrpc0
Summary:        GlusterFS Remote Procedure Call library
Group:          System/Libraries

%description -n libgfrpc0
GlusterFS is a clustered file-system capable of scaling to several
petabytes.

%package -n libgfxdr0
Summary:        GlusterFS's External Data Representation library
Group:          System/Libraries

%description -n libgfxdr0
GlusterFS is a clustered file-system capable of scaling to several
petabytes.

%package -n libglusterfs0
Summary:        GlusterFS's core library
Group:          System/Libraries

%description -n libglusterfs0
GlusterFS is a clustered file-system capable of scaling to several
petabytes.


%package devel
Summary:        Development files for glusterfs
Group:          Development/Libraries/C and C++
Requires:       %name = %version
Requires:       libgfapi0 = %version
Requires:       libgfchangelog0 = %version
Requires:       libgfrpc0 = %version
Requires:       libgfxdr0 = %version
Requires:       libglusterfs0 = %version
Requires:       libuuid-devel
Requires:       libacl-devel

%description devel
GlusterFS is a clustered file-system capable of scaling to several
petabytes.

This package provides development files such as headers and library
links.

%prep
%setup -q -n %{name}-%{version}

%build
[ ! -e gf-error-codes.h ] && ./autogen.sh
%configure --disable-static --enable-gnfs
# This section is not parallel safe or so due to bison/lex
make V=1 %{?_smp_mflags};

%install
b="%buildroot";
make install DESTDIR="$b" docdir="%_docdir/%name"
find "$b/%_libdir" -type f -name "*.la" -delete;

mkdir -p "$b/%_localstatedir/log"/{glusterd,glusterfs,glusterfsd};

# The things seemingly forgotten by make install.
# - Manually populate devel dirs
mkdir -p "$b/%_includedir/%name";
install -pm0644 libglusterfs/src/*.h "$b/%_includedir/%name/";
# - hekafs wants this:
mkdir -p "$b/%_includedir/%name"/{rpc,server};
install -pm0644 rpc/rpc-lib/src/*.h rpc/xdr/src/*.h \
	"$b/%_includedir/%name/rpc/";
install -pm0644 xlators/protocol/server/src/*.h \
	"$b/%_includedir/%name/server/";
# - init script; there is no SuSE-release in the build env
mkdir -p "$b/%_initrddir";
install -pm0755 extras/init.d/glusterd-SuSE "$b/%_initrddir/glusterd";
# - wrapper umount script?
# - logrotate entry
mkdir -p "$b/%_localstatedir/log/%name";
# - vim syntax

# - state
mkdir -p "$b/%_localstatedir/lib/glusterd";
perl -i -pe \
	's{^(\s*option working-directory )\S+}{$1 %_localstatedir/lib/glusterd}g' \
	"$b/%_sysconfdir/%name/glusterd.vol";

# Clean, but must NOT remove .la from dirs not searched by
# default, thus maxdepth.
find "$b/%_libdir" -maxdepth 1 -type f -name "*.la" -delete;

# W: wrong-file-end-of-line-encoding
perl -i -pe 's{\x0d\x0a}{\x0a}gs' %_docdir/%name/glusterfs-mode.el;

%if 0%{?_unitdir:1}
mkdir -p "$b/%_unitdir";
rm -Rf "$b/%_initddir"
ln -s service "$b/%_sbindir/rcglusterd"
%else
ln -s "%_initddir/glusterd" "$b/%_sbindir/rcglusterd"
%endif
chmod u-s "$b/%_bindir/fusermount-glusterfs"
%fdupes %buildroot/%_prefix

%if 0%{?suse_version} >= 1210
%pre
%service_add_pre glusterd.service
%service_add_pre glustereventsd.service
%service_add_pre glusterfssharedstorage.service
%endif

%post
%if 0%{?suse_version} >= 1210
%service_add_post glusterd.service
%service_add_post glustereventsd.service
%service_add_post glusterfssharedstorage.service
%else
%fillup_and_insserv -f glusterd
%endif

%preun
%if 0%{?suse_version} >= 1210
%service_del_preun glusterd.service
%service_del_preun glustereventsd.service
%service_del_preun glusterfssharedstorage.service
%else
%stop_on_removal glusterd
%endif

%postun
%if 0%{?suse_version} >= 1210
%service_del_postun glusterd.service
%service_del_postun glustereventsd.service
%service_del_postun glusterfssharedstorage.service
%else
%insserv_cleanup
%restart_on_update glusterd
%endif

%post   -n libgfapi0 -p /sbin/ldconfig
%postun -n libgfapi0 -p /sbin/ldconfig
%post   -n libgfchangelog0 -p /sbin/ldconfig
%postun -n libgfchangelog0 -p /sbin/ldconfig
%post   -n libgfrpc0 -p /sbin/ldconfig
%postun -n libgfrpc0 -p /sbin/ldconfig
%post   -n libgfxdr0 -p /sbin/ldconfig
%postun -n libgfxdr0 -p /sbin/ldconfig
%post   -n libglusterfs0 -p /sbin/ldconfig
%postun -n libglusterfs0 -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir %_sysconfdir/%name
%config(noreplace) %_sysconfdir/%name/glusterd.vol
%config(noreplace) %_sysconfdir/%name/glusterfs-logrotate
%config %_sysconfdir/%name/*
%config %_sysconfdir/%name/*.example
%config %_sysconfdir/%name/*-logrotate
%config %_sysconfdir/%name/eventsconfig.json
%_bindir/glusterfind
%_bindir/fusermount-glusterfs
/sbin/mount.%name
%_libexecdir/%name/
%_libdir/%name/
%_libdir/libgfdb.so.*
%exclude %_libdir/libgfdb.so
%_sbindir/gluster*
%_sbindir/gf_attach
%_sbindir/glfsheal
%_sbindir/rcglusterd
%_sbindir/gcron.py
%_sbindir/gfind_missing_files
%_sbindir/snap_scheduler.py
%_sbindir/conf.py
%_datadir/glusterfs/
%_mandir/man*/*
%_docdir/%name
%_localstatedir/lib/glusterd
%_localstatedir/log/%name
%python3_sitelib/gluster*
%if 0%{?_unitdir:1}
%_unitdir/glusterd.service
%_unitdir/glustereventsd.service
%_unitdir/glusterfssharedstorage.service
%else
%_initddir/glusterd*
%endif
%_prefix/lib/ocf

%files -n libgfapi0
%defattr(-,root,root)
%_libdir/libgfapi.so.0*

%files -n libgfchangelog0
%defattr(-,root,root)
%_libdir/libgfchangelog.so.0*

%files -n libgfrpc0
%defattr(-,root,root)
%_libdir/libgfrpc.so.0*

%files -n libgfxdr0
%defattr(-,root,root)
%_libdir/libgfxdr.so.0*

%files -n libglusterfs0
%defattr(-,root,root)
%_libdir/libglusterfs.so.0*

%files devel
%defattr(-,root,root)
%_includedir/%name
%_libdir/*.so
%_libdir/pkgconfig/*.pc

%changelog
* Tue Apr 17 2019 kkeithle at redhat.com
- GlusterFS 5.7 GA
* Tue Apr 9 2019 kkeithle at redhat.com
- GlusterFS 5.6 GA
* Fri Mar 15 2019 kkeithle at redhat.com
- GlusterFS 5.5 GA
* Tue Mar 5 2019 kkeithle at redhat.com
- GlusterFS 5.4 GA
* Thu Jan 17 2019 kkeithle at redhat.com
- GlusterFS 5.3 GA
* Thu Dec 13 2018 kkeithle at redhat.com
- GlusterFS 5.2 GA
* Wed Nov 14 2018 kkeithle at redhat.com
- GlusterFS 5.1 GA
* Thu Oct 18 2018 kkeithle at redhat.com
- GlusterFS 5.0 GA
* Fri Sep 19 2018 kkeithle at redhat.com
- GlusterFS 4.1.5 GA
* Thu Sep 6 2018 kkeithle at redhat.com
- GlusterFS 4.1.4 GA
* Tue Sep 4 2018 kkeithle at redhat.com
- GlusterFS 4.1.3, create /var/run/gluster/metrics
* Mon Aug 27 2018 kkeithle at redhat.com
- GlusterFS 4.1.3 GA
* Wed Jul 25 2018 kkeithle at redhat.com
- GlusterFS 4.1.2 GA
* Fri Jun 29 2018 kkeithle at redhat.com
- GlusterFS 4.1.1 GA
* Wed Jun 13 2018 kkeithle at redhat.com
- GlusterFS 4.1.0 GA
* Thu Apr 26 2018 kkeithle at redhat.com
- GlusterFS 4.0.2 GA
* Wed Mar 21 2018 kkeithle at redhat.com
- GlusterFS 4.0.1 GA
* Mon Mar 12 2018 kkeithle at redhat.com
- GlusterFS 4.0.0 GA (v4.0.0-2 respin)
* Tue Mar 6 2018 kkeithle at redhat.com
- GlusterFS 4.0.0 GA
* Sat Jan 20 2018 kkeithle at redhat.com
- GlusterFS 3.13.2 GA
* Thu Dec 21 2017 kkeithle at redhat.com
- GlusterFS 3.13.1 GA
* Sat Dec 2 2017 kkeithle at redhat.com
- GlusterFS 3.13.0 GA
* Fri Dec 1 2017 kkeithle at redhat.com
- GlusterFS 3.12.3, python-request_s_, w/o python-jwt
* Mon Nov 13 2017 kkeithle at redhat.com
- GlusterFS 3.12.3 GA
* Fri Oct 13 2017 kkeithle at redhat.com
- GlusterFS 3.12.2 GA
* Fri Sep 29 2017 kkeithle at redhat.com
- GlusterFS 3.12.1 w/ BZ 1495858
* Mon Sep 11 2017 kkeithle at redhat.com
- GlusterFS 3.12.1 GA
* Wed Aug 30 2017 kkeithle at redhat.com
- GlusterFS 3.12.0 GA
* Mon Aug 21 2017 kkeithle at redhat.com
- GlusterFS 3.11.3 GA
* Fri Jul 21 2017 kkeithle at redhat.com
- GlusterFS 3.11.2 GA
* Wed Jun 28 2017 kkeithle at redhat.com
- GlusterFS 3.11.1 GA
* Tue May 30 2017 kkeithle at redhat.com
- GlusterFS 3.11.0 GA
* Mon May 15 2017 kkeithle at redhat.com
- GlusterFS 3.10.2 GA
* Fri Mar 31 2017 kkeithle at redhat.com
- GlusterFS 3.10.1 GA
* Fri Feb 24 2017 kkeithle at redhat.com
- GlusterFS 3.10.0 GA
* Wed Feb 22 2017 kkeithle at redhat.com
- GlusterFS 3.10.0 RC1
* Wed Feb 8 2017 kkeithle at redhat.com
- GlusterFS 3.10.0 RC0
* Wed Jan 18 2017 kkeithle at redhat.com
- GlusterFS 3.9.1 GA
* Wed Nov 16 2016 kkeithle at redhat.com
- GlusterFS 3.9.0 GA
* Thu Oct 20 2016 kkeithle at redhat.com
- GlusterFS 3.8.5 GA
* Mon Aug 22 2016 kkeithle at redhat.com
- GlusterFS 3.8.3 GA
* Wed Aug 10 2016 kkeithle at redhat.com
- GlusterFS 3.8.2 GA
* Mon Jul 11 2016 kkeithle at redhat.com
- GlusterFS 3.8.1 GA
* Thu Jun 16 2016 kkeithle at redhat.com
- GlusterFS 3.8.0 GA
* Mon Apr 18 2016 kkeithle at redhat.com
- GlusterFS 3.7.11 GA
* Mon Mar 21 2016 kkeithle at redhat.com
- GlusterFS 3.7.9 GA
* Mon Nov 9 2015 kkeithle at redhat.com
* Fri Feb 12 2016 kkeithle at redhat.com
- GlusterFS 3.7.8 GA
* Mon Nov 9 2015 kkeithle at redhat.com
- GlusterFS 3.7.6 GA
* Wed Oct 7 2015 kkeithle at redhat.com
- GlusterFS 3.7.5 GA
- CVE-2014-3619: add multifrag.diff [bnc#919879]
* Fri Feb 27 2015 jengelh@inai.de
- CVE-2014-3619: add multifrag.diff [bnc#919879]
* Mon Aug  4 2014 scorot@free.fr
- Update to new upstream release 3.5.2
  * NFS server crashes in _socket_read_vectored_request
  * Can't write to quota enable folder
  * nfs: reset command does not alter the result for nfs options
    earlier set
  * features/gfid-access: stat on .gfid virtual directory return
    EINVAL
  * creating symlinks generates errors on stripe volume
  * Self-heal errors with "afr crawl failed for child 0 with ret -1"
    while performing rolling upgrade.
  * [AFR] I/O fails when one of the replica nodes go down
  * Fix inode leaks in gfid-access xlator
  * NFS subdir authentication doesn't correctly handle
    multi-(homed,protocol,etc) network addresses
  * nfs-utils should be installed as dependency while installing
    glusterfs-server
  * Excessive logging in quotad.log of the kind 'null client'
  * client_t clienttable cliententries are never expanded when all
    entries are used
  * AFR : self-heal of few files not happening when a AWS EC2 Instance
    is back online after a restart
  * Dist-geo-rep : deletion of files on master, geo-rep fails to
    propagate to slaves.
  * Allow the usage of the wildcard character '*' to the options
    "nfs.rpc-auth-allow" and "nfs.rpc-auth-reject"
  * glfsheal: Improve the way in which we check the presence of
    replica volumes
  * Resource cleanup doesn't happen for clients on servers after
    disconnect
  * mounting a volume over NFS (TCP) with MOUNT over UDP fails
  * backport 'gluster volume status --xml' issues
  * Glustershd memory usage too high
* Tue Jul 29 2014 scorot@free.fr
- Update to new upstream release 3.5.1
  * A new volume option server.manage-gids has been added.
    This option should be used when users of a volume are in more
    than approximately 93 groups (Bug 1096425).
  * Duplicate Request Cache for NFS has now been disabled by
    default, this may reduce performance for certain workloads,
    but improves the overall stability and memory footprint for
    most users.
  * Others changes are mostly bug fixes.
- disable systemd pre an post scripts for old product and then fix
  build on SLE 11
* Mon May  5 2014 jengelh@inai.de
- Update to new upstream release 3.5.0
  * AFR_CLI_enhancements: Improved logging with more clarity and
  statistical information. It allows visibility into why a
  self-heal process was initiated and which files are affected, for
  example. Prior to this enhancement, clearly identifying
  split-brain issues from the logs was often difficult, and there
  was no facility to identify which files were affected by a split
  brain issue automatically. Remediating split brain without quorum
  will still require some manual effort, but with the tools
  provided, this will become much simpler.
  * Exposing Volume Capabilities: Provides client-side insight into
  whether a volume is using the BD translator and, if so, which
  capabilities are being utilized.
  * File Snapshot: Provides a mechanism for snapshotting individual
  files. The most prevalent use case for this feature will be to
  snapshot running VMs, allowing for point-in-time capture. This
  also allows a mechanism to revert VMs to a previous state
  directly from Gluster, without needing to use external tools.
  * GFID Access: A new method for accessing data directly by GFID.
  With this method, the data can be directly consumed in changelog
  translator, which is logging ‘gfid’ internally, very efficiently.
  * On-Wire Compression + Decompression: Use of this feature reduces
  the overall network overhead for Gluster operations from a
  client.
  * Prevent NFS restart on Volume change (Part 1): Previously, any
  volume change (volume option, volume start, volume stop, volume
  delete, brick add, etc.) would restart the NFS server, which led
  to service disruptions. This feature allow modifying certain
  NFS-based volume options without such interruptions occurring.
  Part 1 is anything not requiring a graph change.
  * Quota Scalability: Massively increase the amount of quota
  configurations from a few hundred to 65536 per volume.
  * readdir_ahead: Gluster now provides read-ahead support for
  directories to improve sequential directory read performance.
  * zerofill: Enhancement to allow zeroing out of VM disk images,
  which is useful in first time provisioning or for overwriting an
  existing disk.
  * Brick Failure Detection: Detecting failures on the filesystem
  that a brick uses makes it possible to handle errors that are
  caused from outside of the Gluster environment.
  * Disk encryption: Implement the previous work done in HekaFS into
  Gluster. This allows a volume (or per-tenant part of a volume) to
  be encrypted “at rest” on the server using keys only available on
  the client. [Note: Only content of regular files is encrypted.
  File names are not encrypted! Also, encryption does not work in
  NFS mounts.]
  * Geo-Replication Enhancement: Previously, the geo-replication
  process, gsyncd, was a single point of failure as it only ran on
  one node in the cluster. If the node running gsyncd failed, the
  entire geo-replication process was offline until the issue was
  addressed. In this latest incarnation, the improvement is
  extended even further by foregoing use of xattrs to identify
  change candidates and directly consuming from the volume
  changelog, which will improve performance twofold: one, by
  keeping a running list of only those files that may need to be
  synced; and two, the changelog is maintained in memory, which
  will allow near instant access to which data needs to be changed
  and where by the gsync daemon.
* Thu Feb 28 2013 jengelh@inai.de
- Update to new upstream release 3.4.0alpha (rpm: 3.4.0~qa9)
  * automake-1.13 support
- Enable AIO support
* Tue Nov 27 2012 jengelh@inai.de
- Use `glusterd -N` in glusterd.service to run in foreground
  as required
* Tue Nov 27 2012 cfarrell@suse.com
- license update: GPL-2.0 or LGPL-3.0+
* Fri Nov  9 2012 jengelh@inai.de
- Update to new upstream release 3.4.0qa2
  * No changelog provided by upstream
- Remove glusterfs-init.diff, merged upstream
- Provide systemd service file
* Wed Oct 31 2012 jengelh@inai.de
- Update to new upstream release 3.3.1
  * mount.glusterfs: Add support for {attribute,entry}-timeout options
  * cli: Proper xml output for "gluster peer status"
  * self-heald: Fix inode leak
  * storage/posix: implement native linux AIO support
* Mon Sep 24 2012 jengelh@inai.de
- Update to new upstream release 3.3.0
  * New: Unified File & Object access
  * New: Hadoop hooks - HDFS compatibility layer
  * New volume type: Repstr - replicated + striped (+ distributed)
  volumes
* Fri Dec  2 2011 coolo@suse.com
- add automake as buildrequire to avoid implicit dependency
* Wed Oct  5 2011 jengelh@medozas.de
- Initial package for build.opensuse.org
