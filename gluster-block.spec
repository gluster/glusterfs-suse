Summary:          Gluster block storage utility
Name:             gluster-block
Version:          0.2.1
Release:          2%{?dist}
License:          GPL-2.0 or LGPL-3.0+
URL:              https://github.com/gluster/gluster-block
Source0:          https://github.com/gluster/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

# posted for review upstream: https://review.gluster.org/17657
Patch0:           0001-build-do-not-require-git-to-find-the-version.patch

BuildRequires:    pkgconfig(glusterfs-api)
BuildRequires:    pkgconfig(json-c)
BuildRequires:    help2man >= 1.36
%{?systemd_requires}
BuildRequires:    systemd
# tarball releases require running ./autogen.sh
BuildRequires:    automake, autoconf, libtool, git

Requires:         tcmu-runner >= 1.0.4
Requires:         targetcli >= 2.1.fb43
Requires:         rpcbind

%description
gluster-block is a CLI utility, which aims at making gluster backed block
storage creation and maintenance as simple as possible.

%prep
%setup -q
%patch0 -p1 -b.VERSION

%build
echo %{version} > VERSION
./autogen.sh
%configure
make

%install
%make_install
%if 0%{?_unitdir:1}
mkdir -p "%buildroot/%_unitdir"
rm -Rf "%buildroot/%_initddir"
ln -s service "%buildroot/%_sbindir/rcgluster-blockd"
%else
ln -s "%_initddir/gluster-blockd" "%buildroot/%_sbindir/rcgluster-blockd"
%endif

%pre
%service_add_pre gluster-blockd.service

%post
%service_add_post gluster-blockd.service

%preun
%service_del_preun gluster-blockd.service

%postun
%service_del_postun gluster-blockd.service

%files
%defattr(-,root,root)
%license COPYING-GPLV2 COPYING-LGPLV3
%doc README.md
%{_sbindir}/gluster-block
%{_sbindir}/gluster-blockd
%{_sbindir}/rcgluster-blockd
%{_mandir}/man8/gluster-block*.8*
%{_unitdir}/gluster-blockd.service
%exclude %{_sysconfdir}/sysconfig/gluster-blockd

%changelog
* Wed Sep 13 2017 Niels de Vos <ndevos@redhat.com> - 0.2.1-2
- use pkgconfig for BuildRequires
- run setup in quiet mode
- run make_* macros instead of make commands in build/install section
- drop the INSTALL file from the documentation

* Fri Jun 30 2017 Niels de Vos <ndevos@redhat.com> - 0.2.1-1
- initial packaging, based on upstream .spec
- prevent ./autogen.sh'd need for git to determine the version
- added systemd macros in the scriptlets
