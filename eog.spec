%define gi_major 3.0
%define girname %mklibname %{name}-gir %{gi_major}

Summary:	The Eye of GNOME image viewer
Name:		eog
Version:	3.2.2
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/projects/eog/
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz

BuildRequires:	gnome-doc-utils
BuildRequires:	intltool >= 0.40.0
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(exempi-2.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0.2
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 2.91.2
BuildRequires:	pkgconfig(gsettings-desktop-schemas) >= 2.91.92
BuildRequires:	pkgconfig(libpeas-1.0) >= 0.7.4
BuildRequires:	pkgconfig(gnome-icon-theme)
BuildRequires:	pkgconfig(shared-mime-info)

Requires: librsvg
Requires: gnome-icon-theme
Requires: pygtk2.0
Requires: gnome-python-gnomevfs

%description
This is the Eye of Gnome, an image viewer program. It is meant
to be a fast and functional image viewer as well as an image
cataloging program. It does proper handling of large images and
images with full opacity information, and can zoom and scroll
images quickly while keeping  memory usage constant.

%package -n %{girname}
Summary: GObject Introspection interface description for %name
Group: System/Libraries

%description -n %{girname}
GObject Introspection interface description for %name.

%package devel
Group: Development/C
Summary: C headers needed to build EOG plugins

%description devel
The packages contains the development files for %{name}.


%prep
%setup -q

%build

%configure2_5x \
	--disable-static \
	--enable-introspection=yes \
	--disable-schemas-compile \
	--disable-scrollkeeper

%make


%install
rm -rf %{buildroot} %{name}.lang

%makeinstall_std
%{find_lang} %{name} --with-gnome

for omf in %{buildroot}%{_datadir}/omf/eog/eog-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/eog-// -e s/.omf//)) $(echo $omf|sed -e s!%{buildroot}!!)" >> %{name}.lang
done

# remove unpackaged files
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%preun
%preun_uninstall_gconf_schemas %{name}

%files -f %{name}.lang
%doc AUTHORS NEWS README
%{_sysconfdir}/gconf/schemas/*
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/eog
%{_datadir}/icons/hicolor/*/*/*
%dir %{_datadir}/omf/eog
%{_datadir}/omf/eog/*-C.omf
%dir %{_libdir}/eog
%dir %{_libdir}/eog/plugins
%{_libdir}/eog/plugins/fullscreen.eog-plugin
%{_libdir}/eog/plugins/reload.eog-plugin
%{_libdir}/eog/plugins/statusbar-date.eog-plugin
%{_libdir}/eog/plugins/*.so*

%files -n %{girname}
%{_libdir}/eog/girepository-1.0/Eog-%{gi_major}.typelib

%files devel
%doc ChangeLog
%{_includedir}/eog-3.0
%{_libdir}/pkgconfig/eog.pc
%{_datadir}/gtk-doc/html/eog

