#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	Fast hash functions for strings
Name:		cityhash
Version:	1.0.3
Release:	1
License:	MIT
Group:		Libraries
URL:		http://code.google.com/p/cityhash
Source0:	http://cityhash.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	4d1a1102e696e699613c93ca8aeddd00
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CityHash provides hash functions for strings. The functions mix the
input bits thoroughly but are not suitable for cryptography.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q

%build
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_libdir}/libcityhash.so.*.*.*
%ghost %{_libdir}/libcityhash.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/city.h
%{_libdir}/libcityhash.so
%{_libdir}/libcityhash.la

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcityhash.a
%endif
