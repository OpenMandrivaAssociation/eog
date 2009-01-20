Summary:	The Eye of GNOME image viewer
Name:     	eog
Version: 2.25.5
Release: %mkrel 1
License:	GPLv2+
Group:		Graphical desktop/GNOME
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
URL:		http://www.gnome.org/projects/eog/

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	libgnomeui2-devel >= 2.5.5
BuildRequires:	librsvg-devel >= 2.0.0
BuildRequires:	lcms-devel
BuildRequires:	scrollkeeper >= 0.3
BuildRequires:  libexif-devel
BuildRequires:  exempi-devel
BuildRequires:  pygtk2.0-devel
BuildRequires:  gnome-python-devel
BuildRequires:  gnome-doc-utils
BuildRequires:  gtk-doc
BuildRequires:  intltool >= 0.40.0
Requires(post): scrollkeeper >= 0.3 desktop-file-utils
Requires(postun): scrollkeeper >= 0.3 desktop-file-utils
Requires: librsvg
Requires: gnome-icon-theme
Requires: pygtk2.0 gnome-python-gnomevfs

%description
This is the Eye of Gnome, an image viewer program. It is meant
to be a fast and functional image viewer as well as an image
cataloging program. It does proper handling of large images and
images with full opacity information, and can zoom and scroll
images quickly while keeping  memory usage constant.

%package devel
Group: Development/C
Summary: C headers needed to build EOG plugins

%description devel
This is the Eye of Gnome, an image viewer program. It is meant
to be a fast and functional image viewer as well as an image
cataloging program. It does proper handling of large images and
images with full opacity information, and can zoom and scroll
images quickly while keeping  memory usage constant.

Install this if you want to build EOG plugins.


%prep
%setup -q

%build

%configure2_5x

%make


%install
rm -rf $RPM_BUILD_ROOT %name.lang

# needed otherwise gconf database installation will fail
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

%{find_lang} %{name} --with-gnome

for omf in %buildroot%_datadir/omf/eog/eog-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/eog-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done


rm -rf %buildroot%_libdir/eog/plugins/*a \
   %buildroot/var/lib/scrollkeeper

%clean
rm -rf $RPM_BUILD_ROOT


%if %mdkversion < 200900
%post  
%{update_menus}
%update_scrollkeeper
%update_desktop_database
%post_install_gconf_schemas %name
%update_icon_cache hicolor
%endif

%preun
%preun_uninstall_gconf_schemas %name

%if %mdkversion < 200900
%postun
%clean_scrollkeeper
%{clean_menus}
%clean_desktop_database
%clean_icon_cache hicolor
%endif

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS NEWS README
%{_sysconfdir}/gconf/schemas/*
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/eog
%_datadir/icons/hicolor/*/*/*
%dir %{_datadir}/omf/eog
%{_datadir}/omf/eog/*-C.omf
%dir %_libdir/eog
%dir %_libdir/eog/plugins
%_libdir/eog/plugins/fullscreen.eog-plugin
%_libdir/eog/plugins/reload.eog-plugin
%_libdir/eog/plugins/statusbar-date.eog-plugin
%_libdir/eog/plugins/*.so*

%files devel
%defattr(-, root, root)
%doc ChangeLog
%_includedir/eog-2.20
%_libdir/pkgconfig/eog.pc
%_datadir/gtk-doc/html/eog
