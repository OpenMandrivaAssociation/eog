%define gi_major 3.0
%define girname %mklibname %{name}-gir %{gi_major}

%define url_ver	%(echo %{version}|cut -d. -f1,2)

Summary:	The Eye of GNOME image viewer
Name:		eog
Version:	3.4.1
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
Source0: 	http://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
URL:		http://www.gnome.org/projects/eog/

BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(exempi-2.0) >= 1.99.5
BuildRequires: pkgconfig(gdk-pixbuf-2.0) >= 2.4.0
BuildRequires: pkgconfig(gio-2.0) >= 2.31.0
BuildRequires: pkgconfig(gio-unix-2.0) >= 2.31.0
BuildRequires: pkgconfig(glib-2.0) >= 2.31.0
BuildRequires: pkgconfig(gnome-desktop-3.0) >= 2.91.2
BuildRequires: pkgconfig(gnome-icon-theme) >= 2.19.1
BuildRequires: pkgconfig(gsettings-desktop-schemas) >= 2.91.92
BuildRequires: pkgconfig(gthread-2.0) >= 2.31.0
BuildRequires: pkgconfig(gtk+-3.0) >= 2.90.4
BuildRequires: pkgconfig(gtk+-unix-print-3.0) >= 2.90.4
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(libexif) >= 0.6.14
BuildRequires: pkgconfig(libpeas-1.0) >= 0.7.4
BuildRequires: pkgconfig(libpeas-gtk-1.0) >= 0.7.4
BuildRequires: pkgconfig(librsvg-2.0) >= 2.26.0
BuildRequires: pkgconfig(libxml-2.0) >= 2.0
BuildRequires: pkgconfig(shared-mime-info) >= 0.20
BuildRequires: pkgconfig(x11)
BuildRequires: gnome-doc-utils
BuildRequires: jpeg-devel
BuildRequires: intltool >= 0.40.0
Requires:	librsvg
Requires:	gnome-icon-theme

BuildRequires:	desktop-file-utils

%description
This is the Eye of Gnome, an image viewer program. It is meant
to be a fast and functional image viewer as well as an image
cataloging program. It does proper handling of large images and
images with full opacity information, and can zoom and scroll
images quickly while keeping  memory usage constant.

%files -f %{name}.lang
%doc AUTHORS NEWS README
%{_datadir}/GConf/gsettings/eog.convert
%{_datadir}/glib-2.0/schemas/org.gnome.eog.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.eog.gschema.xml
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/eog
%{_datadir}/icons/hicolor/*/*/*
%dir %{_libdir}/eog
%dir %{_libdir}/eog/plugins
%{_libdir}/eog/plugins/fullscreen.plugin
%{_libdir}/eog/plugins/reload.plugin
%{_libdir}/eog/plugins/statusbar-date.plugin
%{_libdir}/eog/plugins/*.so*

#--------------------------------------------------------------------

%package -n %{girname}
Summary:        GObject Introspection interface description for %name
Group:          System/Libraries

%description -n %{girname}
GObject Introspection interface description for %name.

%files -n %{girname}
%{_libdir}/eog/girepository-1.0/Eog-%{gi_major}.typelib

#--------------------------------------------------------------------

%package devel
Group:		Development/C
Summary:	C headers needed to build EOG plugins

%description devel
This is the Eye of Gnome, an image viewer program. It is meant
to be a fast and functional image viewer as well as an image
cataloging program. It does proper handling of large images and
images with full opacity information, and can zoom and scroll
images quickly while keeping  memory usage constant.

Install this if you want to build EOG plugins.

%files devel
%doc %{_datadir}/gtk-doc/html/eog
%{_includedir}/eog-3.0
%{_libdir}/pkgconfig/eog.pc

#--------------------------------------------------------------------

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--enable-introspection=yes \
	--disable-schemas-compile \
	--disable-scrollkeeper
%make

%install
rm -rf %{buildroot}
%makeinstall_std

desktop-file-install --vendor="" \
	--add-category=Graphics \
	--add-category=2DGraphics \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

%find_lang %{name} --with-gnome

find %{buildroot} -name *.la -delete

