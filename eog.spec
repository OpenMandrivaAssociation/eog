Summary:	The Eye of GNOME image viewer
Name:     	eog
Version: 2.19.5
Release: %mkrel 1
License:	GPL
Group:		Graphical desktop/GNOME
Source: 	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
URL:		http://www.gnome.org/

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	libglade2.0-devel
BuildRequires:	libgnomeui2-devel >= 2.5.5
BuildRequires:	librsvg-devel >= 2.0.0
BuildRequires:	libgnomeprintui-devel >= 2.2
BuildRequires:	lcms-devel
BuildRequires:	scrollkeeper >= 0.3
BuildRequires:  libexif-devel
BuildRequires:  eel-devel
BuildRequires:  pygtk2.0-devel
BuildRequires:  gnome-doc-utils
BuildRequires:  perl-XML-Parser
BuildRequires:  desktop-file-utils
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

# Menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat >$RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%{name}): command="%{_bindir}/%{name}" needs="gnome" \
icon="image-viewer.png" section="Multimedia/Graphics" \
title="Eye of Gnome" longtitle="Eye of Gnome Image Viewer" \
startup_notify="true" xdg="true"
EOF
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Graphics" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


rm -rf %buildroot/var/lib/scrollkeeper

%clean
rm -rf $RPM_BUILD_ROOT


%post  
%{update_menus}
%update_scrollkeeper
%update_desktop_database
%post_install_gconf_schemas %name
%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas %name

%postun
%clean_scrollkeeper
%{clean_menus}
%clean_desktop_database
%clean_icon_cache hicolor

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS NEWS README
%{_sysconfdir}/gconf/schemas/*
%{_bindir}/*
%{_datadir}/applications/*
%_datadir/pixmaps/eog
%{_datadir}/eog
%_datadir/icons/hicolor/*/*/*
%dir %{_datadir}/omf/eog
%{_datadir}/omf/eog/*-C.omf
%{_menudir}/*

%files devel
%defattr(-, root, root)
%doc ChangeLog
%_includedir/eog-2.20
%_libdir/pkgconfig/eog.pc
