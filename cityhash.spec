#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_with	sse42		# SSE 4.2 instructions

Summary:	Fast hash functions for strings
Summary(pl.UTF-8):	Szybka funkcja haszująca dla łańcuchów znaków
Name:		cityhash
Version:	1.1.1
%define	gitref	f5dc54147fcce12cefd16548c8e760d68ac04226
%define	snap	20220720
%define	rel	1
Release:	0.%{snap}.%{rel}
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/google/cityhash
Source0:	https://github.com/google/cityhash/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	8d094c144754e39445b67c18d9d51826
URL:		https://github.com/google/cityhash
BuildRequires:	libstdc++-devel
%if %{with sse42}
Requires:	cpuinfo(sse4_2)
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CityHash provides hash functions for strings. The functions mix the
input bits thoroughly but are not suitable for cryptography.

%description -l pl.UTF-8
Biblioteka CityHash udostępnia funkcje haszujące dla łańcuchów znaków.
Funkcje mieszają gruntownie bity wejścia, ale nie nadają się do
kryptografii.

%package devel
Summary:	Development files for CityHash library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki CityHash
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
This package contains header file for developing applications that
use CityHash library.

%description devel -l pl.UTF-8
Ten pakiet zawiera plik nagłówkowy do tworzenia aplikacji
wykorzystujących bibliotekę CityHash.

%package static
Summary:	Static CityHash library
Summary(pl.UTF-8):	Statyczna biblioteka CityHash
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static CityHash library.

%description static -l pl.UTF-8
Statyczna biblioteka CityHash.

%prep
%setup -q -n %{name}-%{gitref}

%build
%configure \
	%{?with_sse42:--enable-sse4.2} \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcityhash.la

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README
%{_libdir}/libcityhash.so.*.*.*
%ghost %{_libdir}/libcityhash.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcityhash.so
%{_includedir}/city.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcityhash.a
%endif
