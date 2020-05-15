
##-----------------------------------------------------------------------------
## All %%global definitions should be placed here and keep them sorted
##


##-----------------------------------------------------------------------------
## All package definitions should be placed here
##
Summary:          Gluster block storage utility
Name:             gluster-block
Version:          0.5
Release:          1%{?dist}
License:          GPL-2.0 or LGPL-3.0+
URL:              https://github.com/gluster/gluster-block
Source0:          https://github.com/gluster/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0001:        0001-configure.ac.patch

BuildRequires:    glusterfs-devel
BuildRequires:    pkgconfig(json-c)
BuildRequires:    help2man >= 1.36
BuildRequires:    libtirpc-devel
BuildRequires:    systemd
# tarball releases require running ./autogen.sh
BuildRequires:    automake, autoconf, libtool, git
Requires:         tcmu-runner >= 1.1.3
Requires:         targetcli >= 2.1.fb49
Requires:         rpcbind
Requires:         logrotate

%{?systemd_requires}

%description
gluster-block is a CLI utility, which aims at making gluster backed block
storage creation and maintenance as simple as possible.

%prep
%setup -q
%patch0001 -p1

%build
echo %{version} > VERSION
./autogen.sh
%configure
make V=1

%install
%make_install

mkdir -p %{buildroot}/%{_fillupdir}
mv %{buildroot}%{_sysconfdir}/sysconfig/gluster-blockd \
    %{buildroot}/%{_fillupdir}/sysconfig.gluster-blockd


%pre
%service_add_pre gluster-block-target.service
%service_add_pre gluster-blockd.service

%post
%service_add_post gluster-block-target.service
%service_add_post gluster-blockd.service

%preun
%service_del_preun gluster-block-target.service
%service_del_preun gluster-blockd.service

%postun
%service_del_postun gluster-block-target.service
%service_del_postun gluster-blockd.service

%files
%license COPYING-GPLV2 COPYING-LGPLV3
%doc README.md
%{_sbindir}/gluster-block
%{_sbindir}/gluster-blockd
%doc %{_mandir}/man8/gluster-block*.8*
%dir %{_localstatedir}/log/gluster-block
%{_unitdir}/gluster-blockd.service
%{_unitdir}/gluster-block-target.service
%dir /%{_fillupdir}
     /%{_fillupdir}/sysconfig.gluster-blockd
%config(noreplace) %{_sysconfdir}/logrotate.d/gluster-block
%dir %{_libexecdir}/gluster-block
     %{_libexecdir}/gluster-block/wait-for-bricks.sh
     %{_libexecdir}/gluster-block/upgrade_activities.sh
%dir %{_localstatedir}/lib/gluster-block
%config(noreplace) %{_localstatedir}/lib/gluster-block/gluster-block-caps.info

%changelog
* Thu May 14 2020 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 0.5-1

* Tue May 7 2019 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 0.4-1

* Tue Oct 17 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 0.3-1

* Wed Sep 13 2017 Niels de Vos <ndevos@redhat.com> - 0.2.1-2
- use pkgconfig for BuildRequires
- run setup in quiet mode
- run make_* macros instead of make commands in build/install section
- drop the INSTALL file from the documentation

* Fri Jun 30 2017 Niels de Vos <ndevos@redhat.com> - 0.2.1-1
- initial packaging, based on upstream .spec
- prevent ./autogen.sh'd need for git to determine the version
- added systemd macros in the scriptlets
