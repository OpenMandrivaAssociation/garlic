%define name 	garlic
%define version 1.6
%define release %mkrel 1

Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Summary: 	Free molecular viewer and editor
License: 	GPL
Group: 		Sciences/Chemistry
Source0: 	%{name}-%{version}.tar.bz2
Source1: 	%{name}-%{version}-doc.tar.bz2
Source2:	%{name}.1.bz2
URL: 		http://garlic.mefos.hr/sources
BuildRequires: 	ImageMagick X11-devel

%description
Garlic is a full-featured molecular viewer and editor.  It is 
intended mainly for biological macromolecules (proteins and DNA) 
in PDB format.  It can also render high-quality images for 
presentations or publishing.

%prep
%setup -q -a 1
mv garlic-%version doc
perl -pi -e "s/^CCOPT.*/CCOPT = $RPM_OPT_FLAGS/" Makefile
rm -rf doc/mouse/.xvpics/
perl -pi -e 's/usr\/X11R6\/lib/usr\/X11R6\/%{_lib}/g' Makefile

%build
%make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install -m755 garlic $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/%{name}
install -m644 .garlicrc *.pdb $RPM_BUILD_ROOT/%{_libdir}/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
cp %SOURCE2 $RPM_BUILD_ROOT/%{_mandir}/man1

install -d $RPM_BUILD_ROOT{%{_miconsdir},%{_liconsdir}}
convert -size 16x16 %{name}.xpm $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
convert -size 32x32 %{name}.xpm $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -size 48x48 %{name}.xpm $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

# menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=garlic
Categories=Science;Chemistry;
Name=Garlic
Icon=%{name}
Comment=3D Molecule Viewer
EOF

%post 
%update_menus

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%doc README HISTORY BUGS *.script doc
%{_bindir}/*
%{_libdir}/%{name}
%{_mandir}/man1/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
