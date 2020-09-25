
Summary:          Core Utilities for the Gluster Distributed File System
Name:             glusterfs-coreutils
Version:          0.3.1
Release:          1%{?dist}
License:          GPLv3
URL:              https://github.com/gluster/glusterfs-coreutils
# The source for this package was created from upstream source using the
# following command:
#       make dist
Source0:          https://github.com/gluster/glusterfs-coreutils/archive/v%{version}/%{name}-v%{version}.tar.gz
Source1:          gnulib-9c70545.tar.gz
Patch0001:        0001-bootstrap.sh.patch

Provides:         bundled(gnulib)

Requires:         glusterfs-api >= 3.8.6

BuildRequires:    gcc make
BuildRequires:    glusterfs-devel >= 3.8.6
BuildRequires:    help2man >= 1.36
BuildRequires:    readline-devel
BuildRequires:    autoconf automake libtool

%description
gluster-coreutils provides a set of basic utilities such as cat, mkdir, ls,
stat, rm and tail that are implemented specifically using the GlusterFS API.

%prep
%setup -q -n %{name}-%{version}%{?prereltag}
tar xpf %{SOURCE1}
%patch0001 -p1

%build
sed -i 's|m4_esyscmd.*|0.3.1,|' configure.ac
./autogen.sh && %configure
make

%install
%make_install

%files
%license COPYING
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 11 2019 Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 0.3.1-3
- rebuild with glusterfs-7

* Thu Aug 1 2019 Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 0.3.1-2
- restore i686

* Thu Aug 1 2019 Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 0.3.1-1
- glusterfs-coreutils 0.3.1 GA

* Thu Aug 1 2019 Anoop C S <anoopcs@redhat.com> - 0.3.0-7
- Adapt to ftruncate api changes

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 20 2019 Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 0.3.0-5
- rebuild for f31/rawhide

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.0-4
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 6 2018 Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 0.3.0-1
- glusterfs-coreutils 0.3.0 GA

* Tue Mar 20 2018 Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 0.2.0-7
- uninitialized variables

* Mon Feb 19 2018 Kaleb S. KEITHLEY <kkeithle [at] redhat.com> - 0.2.0-6
- gcc in BuildRoot

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jul 27 2016 Anoop C S <anoopcs@redhat.com> - 0.2.0-1
- Initial public release (#1360506)

* Fri Jun 03 2016 Anoop C S <anoopcs@redhat.com> - 0.0.1-0.1.git259f269
- Fixed unused variable build error

* Thu May 05 2016 Anoop C S <anoopcs@redhat.com> - 0.0.1-0.4.git60d57d8
- Fixed creation of links within upstream

* Fri Apr 29 2016 Anoop C S <anoopcs@redhat.com> - 0.0.1-0.3.gitf9a4a2e
- Initial package based on upstream spec file

