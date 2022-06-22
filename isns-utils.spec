%define libname %mklibname isns
%define devname %mklibname -d isns

Name:           isns-utils
Version:        0.101
Release:        2
Summary:        The iSNS daemon and utility programs

License:        LGPLv2+
URL:            https://github.com/open-iscsi/open-isns
Source0:        https://github.com/open-iscsi/open-isns/archive/v%{version}.tar.gz#/open-isns-%{version}.tar.gz
Source1:        https://src.fedoraproject.org/rpms/isns-utils/raw/rawhide/f/isnsd.service

BuildRequires:  gcc
BuildRequires:  pkgconfig(openssl) automake pkgconfig systemd
BuildRequires:	pkgconfig(libsystemd)
BuildRequires: make
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
The iSNS package contains the daemon and tools to setup a iSNS server,
and iSNS client tools. The Internet Storage Name Service (iSNS) protocol
allows automated discovery, management and configuration of iSCSI and
Fibre Channel devices (using iFCP gateways) on a TCP/IP network.

%package -n %{libname}
Summary: Shared library files for iSNS

%description -n %{libname}
Shared library files for iSNS

%package -n %{devname}
Summary: Development files for iSNS
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files for iSNS

%prep
%autosetup -p1 -n open-isns-%{version}

%build
%configure --enable-shared --disable-static
%make_build

%install
%make_install
make install_hdrs DESTDIR=%{buildroot}
make install_lib DESTDIR=%{buildroot}
chmod 755 %{buildroot}%{_sbindir}/isns*
chmod 755 %{buildroot}%{_libdir}/libisns.so.0
rm -rf %{buildroot}%{_prefix}/lib/systemd
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/isnsd.service

%post
%systemd_post isnsd.service

%postun
%systemd_postun isnsd.service

%preun
%systemd_preun isnsd.service

%files
%doc COPYING README
%{_sbindir}/isnsd
%{_sbindir}/isnsadm
%{_sbindir}/isnsdd
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_unitdir}/isnsd.service
%dir %{_sysconfdir}/isns
%dir %{_var}/lib/isns
%config(noreplace) %{_sysconfdir}/isns/*

%files -n %{libname}
%{_libdir}/libisns.so.0

%files -n %{devname}
%{_includedir}/libisns
%{_libdir}/libisns.so
