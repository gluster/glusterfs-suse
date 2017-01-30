
Summary:          Core Utilities for the Gluster Distributed File System
Name:             glusterfs-coreutils
Version:          0.2.0
Release:          1%{?dist}
License:          GPLv3
Group:            System Environment/Base
URL:              https://github.com/gluster/glusterfs-coreutils
Source0:          https://github.com/gluster/%{name}/archive/%{version}/%{name}-%{version}.tar.gz


Provides:         bundled(gnulib)

Requires:         glusterfs-api >= 3.8.6

BuildRequires:    glusterfs-api-devel >= 3.8.6
BuildRequires:    help2man >= 1.36
BuildRequires:    readline-devel

%description
gluster-coreutils provides a set of basic utilities such as cat, mkdir, ls,
stat, rm and tail that are implemented specifically using the GlusterFS API.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
%make_install

%files
%license COPYING
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Wed Jul 27 2016 Anoop C S <anoopcs@redhat.com> - 0.2.0-1
- Initial public release (#1360506)

* Fri Jun 03 2016 Anoop C S <anoopcs@redhat.com> - 0.0.1-0.1.git259f269
- Fixed unused variable build error

* Thu May 05 2016 Anoop C S <anoopcs@redhat.com> - 0.0.1-0.4.git60d57d8
- Fixed creation of links within upstream

* Fri Apr 29 2016 Anoop C S <anoopcs@redhat.com> - 0.0.1-0.3.gitf9a4a2e
- Initial package based on upstream spec file

