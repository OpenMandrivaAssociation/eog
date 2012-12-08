%define gi_major 3.0
%define girname %mklibname %{name}-gir %{gi_major}

Summary:	The Eye of GNOME image viewer
Name:		eog
Version:	3.6.2
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/projects/eog/
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/3.6/%{name}-%{version}.tar.xz

BuildRequires:	desktop-file-utils
BuildRequires:	intltool >= 0.40.0 itstool
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(exempi-2.0)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gnome-icon-theme)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libpeas-gtk-1.0)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(shared-mime-info)
BuildRequires:	pkgconfig(x11)
Requires:	librsvg
Requires:	gnome-icon-theme

%description
This is the Eye of Gnome, an image viewer program. It is meant
to be a fast and functional image viewer as well as an image
cataloging program. It does proper handling of large images and
images with full opacity information, and can zoom and scroll
images quickly while keeping  memory usage constant.

%package -n %{girname}
Summary:	GObject Introspection interface description for %name
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %name.

%package devel
Group:		Development/C
Summary:	C headers needed to build EOG plugins
Requires:	%{girname} = %{version}-%{release}

%description devel
This is the Eye of Gnome, an image viewer program. It is meant
to be a fast and functional image viewer as well as an image
cataloging program. It does proper handling of large images and
images with full opacity information, and can zoom and scroll
images quickly while keeping  memory usage constant.

Install this if you want to build EOG plugins.

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
%makeinstall_std

desktop-file-install --vendor="" \
	--add-category=Graphics \
	--add-category=2DGraphics \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

%find_lang %{name} --with-gnome

find %{buildroot} -name *.la -delete

%files -f %{name}.lang
%doc AUTHORS NEWS README
%{_bindir}/*
%dir %{_libdir}/eog
%dir %{_libdir}/eog/plugins
%{_libdir}/eog/plugins/fullscreen.plugin
%{_libdir}/eog/plugins/reload.plugin
%{_libdir}/eog/plugins/statusbar-date.plugin
%{_libdir}/eog/plugins/*.so*
%{_datadir}/GConf/gsettings/eog.convert
%{_datadir}/glib-2.0/schemas/org.gnome.eog.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.eog.gschema.xml
%{_datadir}/applications/*
%{_datadir}/eog
%{_datadir}/icons/hicolor/*/*/*

%files -n %{girname}
%{_libdir}/eog/girepository-1.0/Eog-%{gi_major}.typelib

%files devel
%doc %{_datadir}/gtk-doc/html/eog
%{_includedir}/eog-3.0
%{_libdir}/pkgconfig/eog.pc
