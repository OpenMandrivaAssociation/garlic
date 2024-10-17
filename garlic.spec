Summary:	Free molecular viewer and editor
Name:		garlic
Version:	1.6
Release:	8
License:	GPLv2+
Group:		Sciences/Chemistry
Url:		https://garlic.mefos.hr/sources
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-%{version}-doc.tar.bz2
Source2:	%{name}.1.bz2
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(x11)

%description
Garlic is a full-featured molecular viewer and editor. It is intended mainly
for biological macromolecules (proteins and DNA) in PDB format. It can also
render high-quality images for presentations or publishing.

%files
%doc README HISTORY BUGS *.script doc
%{_bindir}/*
%{_libdir}/%{name}
%{_mandir}/man1/*
%{_datadir}/applications/%{name}.desktop
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png

#----------------------------------------------------------------------------

%prep
%setup -q -a 1
mv garlic-%{version} doc
perl -pi -e "s/^CCOPT.*/CCOPT = %{optflags}/" Makefile
rm -rf doc/mouse/.xvpics/
perl -pi -e 's/usr\/X11R6\/lib/usr\/X11R6\/%{_lib}/g' Makefile

%build
%make

%install
mkdir -p %{buildroot}%{_bindir}
install -m755 garlic %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/%{name}
install -m644 .garlicrc *.pdb %{buildroot}%{_libdir}/%{name}
mkdir -p %{buildroot}%{_mandir}/man1
cp %SOURCE2 %{buildroot}%{_mandir}/man1

install -d %{buildroot}{%{_miconsdir},%{_liconsdir}}
convert -size 16x16 %{name}.xpm %{buildroot}%{_liconsdir}/%{name}.png
convert -size 32x32 %{name}.xpm %{buildroot}%{_iconsdir}/%{name}.png
convert -size 48x48 %{name}.xpm %{buildroot}%{_miconsdir}/%{name}.png

# menu
mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %{buildroot}%{_datadir}/applications/%{name}.desktop
[Desktop Entry]
Type=Application
Exec=garlic
Categories=Science;Chemistry;
Name=Garlic
Icon=%{name}
Comment=3D Molecule Viewer
EOF

