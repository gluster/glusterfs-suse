##-----------------------------------------------------------------------------
## All %%global definitions should be placed here and keep them sorted
##


##-----------------------------------------------------------------------------
## All package definitions should be placed here
##
Summary:          Gluster block storage utility
Name:             gluster-block
Version:          0.4
Release:          1%{?dist}
License:          GPL-2.0 or LGPL-3.0+
URL:              https://github.com/gluster/gluster-block
Source0:          https://github.com/gluster/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:           gluster-block-0.4-logrotate.patch

BuildRequires:    pkgconfig(glusterfs-api)
BuildRequires:    pkgconfig(json-c)
BuildRequires:    help2man >= 1.36

BuildRequires:    systemd
# tarball releases require running ./autogen.sh
BuildRequires:    automake, autoconf, libtool, git
Requires:         tcmu-runner >= 1.1.3
Requires:         targetcli >= 2.1.fb49
Requires:         rpcbind

%{?systemd_requires}

%description
gluster-block is a CLI utility, which aims at making gluster backed block
storage creation and maintenance as simple as possible.

%prep
%setup -q
%patch0 -p1

%build
echo %{version} > VERSION
./autogen.sh
%configure
%make_build

%install
%make_install

touch %{buildroot}%{_sharedstatedir}/gluster-block/gb_upgrade.status

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
%{_unitdir}/gluster-blockd.service
%{_unitdir}/gluster-block-target.service
%config(noreplace) %{_sysconfdir}/sysconfig/gluster-blockd
%config(noreplace) %{_sysconfdir}/logrotate.d/gluster-block
%{_libexecdir}/gluster-block
%dir %{_localstatedir}/log/gluster-block
%dir %{_sharedstatedir}/gluster-block
%ghost %{_sharedstatedir}/gluster-block/gb_upgrade.status
%config(noreplace) %{_sharedstatedir}/gluster-block/gluster-block-caps.info

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
