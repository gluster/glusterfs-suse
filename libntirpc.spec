
Name:		libntirpc
Version:	1.4.3
Release:	1%{?dev:%{dev}}%{?dist}
Summary:	New Transport Independent RPC Library
Group:		System/Libraries
License:	BSD-3-Clause
Url:		https://github.com/nfs-ganesha/ntirpc
Source0:	https://github.com/nfs-ganesha/ntirpc/archive/v%{version}/ntirpc-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	krb5-devel

%description
This package contains a new implementation of the original libtirpc, 
transport-independent RPC (TI-RPC) library for NFS-Ganesha. It has
the following features not found in libtirpc:
 1. Bi-directional operation
 2. Full-duplex operation on the TCP (vc) transport
 3. Thread-safe operating modes
 3.1 new locking primitives and lock callouts (interface change)
 3.2 stateless send/recv on the TCP transport (interface change)
 4. Flexible server integration support
 5. Event channels (remove static arrays of xprt handles, new EPOLL/KEVENT
    integration)

%package -n libntirpc1_4
Summary:	New Transport Independent RPC Library
Group:		System/Libraries
# libtirpc has /etc/netconfig, most machines probably have it anyway
# for NFS client
Requires:	libtirpc

%description -n libntirpc1_4
This package contains a new implementation of the original libtirpc, 
transport-independent RPC (TI-RPC) library for NFS-Ganesha. It has
the following features not found in libtirpc:
 1. Bi-directional operation
 2. Full-duplex operation on the TCP (vc) transport
 3. Thread-safe operating modes
 3.1 new locking primitives and lock callouts (interface change)
 3.2 stateless send/recv on the TCP transport (interface change)
 4. Flexible server integration support
 5. Event channels (remove static arrays of xprt handles, new EPOLL/KEVENT
    integration)

%package devel
Summary:	Development headers for %{name}
Requires:	%{name}%{?_isa} = %{version}
Group:		Development/Libraries/C and C++

%description devel
Development headers and auxiliary files for developing with %{name}.

%prep
%setup -q -n ntirpc-%{version}

%build
%cmake -DOVERRIDE_INSTALL_PREFIX=/usr -DTIRPC_EPOLL=1 -DUSE_GSS=ON "-GUnix Makefiles"

make %{?_smp_mflags}

%install
## make install is broken in various ways
## make install DESTDIR=%%{buildroot}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -p -m 0755 build/src/%{name}.so.%{version} %{buildroot}%{_libdir}/
ln -s %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so.1
ln -s %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so
mkdir -p %{buildroot}%{_includedir}/ntirpc
cp -a ntirpc %{buildroot}%{_includedir}/
install -p -m 644 build/libntirpc.pc %{buildroot}%{_libdir}/pkgconfig/
mkdir -p %{buildroot}%{_defaultlicensedir}/%{name}
install -c -m 0644 COPYING %{buildroot}%{_defaultlicensedir}/%{name}/

%post -n libntirpc1_4 -p /sbin/ldconfig

%postun -n libntirpc1_4 -p /sbin/ldconfig

%files -n libntirpc1_4
%{_libdir}/libntirpc.so.*
%doc NEWS README
%dir %{_defaultlicensedir}
%{_defaultlicensedir}/*

%files devel
%{_libdir}/libntirpc.so
%{_includedir}/ntirpc/
%{_libdir}/pkgconfig/libntirpc.pc

%changelog
* Tue Oct 25 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.3-1
- libntirpc 1.4.3 GA

* Tue Oct 25 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.2-1
- libntirpc 1.4.2 GA

* Tue Sep 20 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.1-1
- libntirpc 1.4.1 GA

* Mon Sep 19 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-1
- libntirpc 1.4.0 GA

* Tue Sep 6 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-0.4pre3
- libntirpc 1.4.0-pre3, without jemalloc

* Thu Aug 4 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-0.3pre3
- libntirpc 1.4.0-pre3

* Mon Feb 29 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-0.2pre2
- libntirpc 1.4.0-pre2

* Fri Feb 5 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-0.1pre1
- libntirpc 1.4.0-pre1, correct release

* Fri Feb 5 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-1pre1
- libntirpc 1.4.0-pre1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 9 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com>
- Requires: libtirpc for /etc/netconfig (most already have it)

* Mon Oct 26 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.3.1-1
- libntirpc 1.3.1 GA

* Fri Oct 9 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.3.0-3
- libntirpc 1.3.0 GA, w/ -DTIRPC_EPOLL=ON

* Wed Sep 9 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.3.0-2
- libntirpc 1.3.0 GA, w/ correct top-level CMakeList.txt

* Wed Sep 9 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.3.0-1
- libntirpc 1.3.0 GA

* Thu Jul 16 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.2.1-3
- RHEL 6 finally has new enough cmake
- use -isystem ... to ensure correct <rpc/rpc*.h> are used
- ensure -DTIRPC_EPOLL is defined for correct evchan functionality

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.2.1-1
- Initial commit
