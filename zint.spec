%define name	zint
%define version 2.4.3
%define rel	1

%define major	2.4
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}
%define qlibname	%mklibname q%{name} %{major}
%define qdevname	%mklibname -d q%{name}

Name:		%{name}
Version:	%{version}
Release:	%mkrel %{rel}
Summary:	Barcode generator
License:	GPLv3+
URL:		http://www.zint.org.uk
Source:		http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Group:		Graphics

# patch to disable creation of rpaths
Patch0:		%{name}-rpath.patch

BuildRequires:	cmake
BuildRequires:	libpng-devel
BuildRequires:	zlib-devel
BuildRequires:	qt4-devel
BuildRequires:	desktop-file-utils

%description
Zint is a C library for encoding data in several barcode variants. The
bundled command-line utility provides a simple interface to the library.
Features of the library:
- Over 50 symbologies including all ISO/IEC standards, like QR codes.
- Unicode translation for symbologies which support Latin-1 and 
  Kanji character sets.
- Full GS1 support including data verification and automated insertion of 
  FNC1 characters.
- Support for encoding binary data including NULL (ASCII 0) characters.
- Health Industry Barcode (HIBC) encoding capabilities.
- Output in PNG, EPS and SVG formats with user adjustable sizes and colors.
- Verification stage for SBN, ISBN and ISBN-13 data.

%package -n %{libname}
Summary:	C library for encoding data in several barcode variants
Group:		System/Libraries

%description -n %{libname}
Zint is a C library for encoding data in several barcode variants.

Features of the library:
- Over 50 symbologies including all ISO/IEC standards, like QR codes.
- Unicode translation for symbologies which support Latin-1 and
  Kanji character sets.
- Full GS1 support including data verification and automated insertion of
  FNC1 characters.
- Support for encoding binary data including NULL (ASCII 0) characters.
- Health Industry Barcode (HIBC) encoding capabilities.
- Output in PNG, EPS and SVG formats with user adjustable sizes and colors.
- Verification stage for SBN, ISBN and ISBN-13 data.

%package -n %{devname}
Summary:	Library and header files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{devname}
C library and header files needed to develop applications that use 
the Zint library. The API documentation can be found on the project website:
http://www.zint.org.uk/zintSite/Manual.aspx

%package qt
Summary:	Zint Barcode Studio
Group:		Graphics

%description qt
Zint Barcode Studio is a Qt-based GUI which allows desktop users to generate 
barcodes which can then be embedded in documents or HTML pages.

%package -n %{qlibname}
Summary:	libQZint shared libraries
Group:		System/Libraries

%description -n %{qlibname}
libQZint shared libraries.

%package -n %{qdevname}
Summary:	Library and header files for %{name}-qt
Group:		Development/C
Requires:	%{qlibname} = %{version}-%{release}
Provides:	q%{name}-devel = %{version}-%{release}
Provides:	libq%{name}-devel = %{version}-%{release}

%description -n %{qdevname}
C library and header files needed to develop applications that use libQZint.

%prep
%setup -q
%patch0 -p1

# remove BSD-licensed file required for Windows only (just to ensure that this package is plain GPLv3+)
rm -f backend/ms_stdint.h

# remove bundled getopt sources (we use the corresponding Fedora package instead)
rm -f frontend/getopt*.*

%build
%cmake
%make VERBOSE=1

%install
rm -rf %{buildroot}
%makeinstall_std -C build

#we don't need this(?)
rm -rf %{buildroot}%{_datadir}/cmake

#icon
install -D -p -m 644 %{name}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

#.desktop file
install -D -p -m 644 %{name}-qt.desktop %{buildroot}%{_datadir}/applications/%{name}-qt.desktop

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc readme
%{_bindir}/%{name}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libzint.so.%{major}*

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_libdir}/libzint.so

%files qt
%defattr(-,root,root)
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{name}-qt.desktop
%{_datadir}/pixmaps/%{name}.png

%files -n %{qlibname}
%defattr(-,root,root)
%{_libdir}/libQZint.so.%{major}*

%files -n %{qdevname}
%defattr(-,root,root)
%{_includedir}/qzint.h
%{_libdir}/libQZint.so
