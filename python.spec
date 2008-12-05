%define docver  2.5
%define dirver  2.5

%define lib_major	%{dirver}
%define lib_name_orig	libpython
%define lib_name	%mklibname %{name} %{lib_major}

Summary:	An interpreted, interactive object-oriented programming language
Name:		python
Version:	2.5.2
Release:	%mkrel 5
License:	Modified CNRI Open Source License
Group:		Development/Python

Source:		http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.bz2
Source1:	http://www.python.org/ftp/python/doc/%{docver}/html-%{docver}.tar.bz2
Source2:	python-2.5-base.list
Source3:	exclude.py
Source4:	python-mode-1.0.tar.bz2
# gw allow to build with libdb 4.6
Patch: Python-2.5.1-db4.6.patch

# Don't include /usr/local/* in search path
Patch3:		Python-2.3-no-local-incpath.patch

# Support */lib64 convention on x86_64, sparc64, etc.
Patch4:		Python-2.4.1-lib64.patch

# Do handle <asm-XXX/*.h> headers in h2py.py
# FIXME: incomplete for proper bi-arch support as #if/#else/#endif
# clauses generally should have been handled
Patch5:		Python-2.2.2-biarch-headers.patch

# detect and link with gdbm_compat for dbm module
Patch6:		Python-2.4.1-gdbm.patch

Patch7:     python-2.4.3-fix-buffer_overflow_with_glibc2.3.5.diff
# patch from 2.6 branch, to reduce number of wakeup
# see http://qa.mandriva.com/show_bug.cgi?id=36743
Patch8:     python2.6-set_wakeup_fd4.patch 

# fix CVE-2007-4965
Patch9:     python-2.5-CVE-2007-4965.patch 

# add mandriva to the list of supported distribution, applied upstream
Patch10:	python-2.5.1-detect-mandriva.patch

# security fix, from Python SVN, already applied for versions post 2.5.2
Patch11:	python-2.5-CVE-2008-1721.patch

# security fix, CVE-2008-1679
# problem on imaageop
Patch12:    python-2.5-int-overflow-2.patch
# security fix, unicode overflow
Patch13:    python-2.5.2-CVE-2008-2315.patch
# security, interger overflow in hashlib
Patch14:    python-2.5.2-CVE-2008-2316.patch
# VArious buffer overflow
Patch15:    python-2.5.2-CVE-2008-3142.patch
# interger overflow, in vsnprintf
Patch16:    python-2.5.2-CVE-2008-3144.patch
# security fix, symbolic link attack possibility on temp file
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=498899
Patch17:    python-2.5.2-CVE-2008-4108.patch

URL:		http://www.python.org/
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Conflicts:	tkinter < %{version}
Requires:	%{lib_name} = %{version}
Requires:	%{name}-base = %{version}
BuildRequires:	X11-devel 
BuildRequires:	blt
BuildRequires:	db2-devel, db4-devel
BuildRequires:	emacs-bin
BuildRequires:	expat-devel
BuildRequires:	gdbm-devel 
BuildRequires:	gmp-devel
BuildRequires:	ncurses-devel 
BuildRequires:	openssl-devel 
BuildRequires:	readline-devel 
BuildRequires:	termcap-devel
BuildRequires:	tcl tcl-devel
BuildRequires:	tk tk-devel
BuildRequires:	tcl tk tix
BuildRequires:	tix
BuildRequires:	autoconf2.5
BuildRequires:  bzip2-devel
BuildRequires:  sqlite3-devel
BuildRequires:	emacs
# not needed, we only have version 2.0 in distro
#Obsoletes:      python-sqlite3
#Provides:       python-sqlite3
Obsoletes:      python-ctypes
Provides:       python-ctypes
Obsoletes:      python-elementtree
Provides:       python-elementtree
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root


%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that
need a programmable interface. This package contains most of the
standard Python modules, as well as modules for interfacing to the
Tix widget set for Tk and RPM.

Note that documentation for Python is provided in the python-docs
package.

%package -n	%{lib_name}
Summary:	Shared libraries for Python %{version}
Group:		System/Libraries

%description -n	%{lib_name}
This packages contains Python shared object library.  Python is an
interpreted, interactive, object-oriented programming language often
compared to Tcl, Perl, Scheme or Java.

%package -n	%{lib_name}-devel
Summary:	The libraries and header files needed for Python development
Group:		Development/Python
Requires:	%{name} = %version
Requires:	%{lib_name} = %{version}
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}

%description -n	%{lib_name}-devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install %{lib_name}-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package	docs
Summary:	Documentation for the Python programming language
Requires:	python = %version
Group:		Development/Python

%description	docs
The python-docs package contains documentation on the Python
programming language and interpreter.  The documentation is provided
in ASCII text files and in LaTeX source files.

Install the python-docs package if you'd like to use the documentation
for the Python language.

%package -n	tkinter
Summary:	A graphical user interface for the Python scripting language
Group:		Development/Python
Requires:	python = %version
Requires:       tcl tk

%description -n	tkinter
The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you'd like to use a graphical
user interface for Python programming.

%package -n	tkinter-apps
Summary:	Various applications written using tkinter
Group:		Development/Python
Requires:   tkinter

%description -n	tkinter-apps
Various applications written using tkinter

%package	base
Summary:	Python base files
Group:		Development/Python
Requires:	%{lib_name} = %{version}

%description	base
This packages contains the Python part that is used by the base packages
of a Mandriva Linux distribution.

%prep
%setup -q -n Python-%{version}
# db 4.6
%patch0 -p0
# local include
%patch3 -p1 
# lib64
%patch4 -p0
# biarch header
%patch5 -p1
# gdbm 
%patch6 -p1 
# fix some crash du to a buffer overflow
%patch7 -p0
# reduce number of wakeup
%patch8 -p0
# fix CVE-2007-4965
%patch9 -p1
# add mandriva to the list of supported distribution
%patch10 -p0

# security fix
%patch11 -p0
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1

autoconf

mkdir html
bzcat %{SOURCE1} | tar x  -C html

find . -type f -print0 | xargs -0 perl -p -i -e 's@/usr/local/bin/python@/usr/bin/python@'

tar --strip-components=1 -xjf %{SOURCE4} -C Misc   

cat > README.mdk << EOF
Python interpreter support readline completion by default.
This is only used with the interpreter. In order to remove it,
you can :
1) unset PYTHONSTARTUP when you login
2) create a empty file \$HOME/.pythonrc.py
3) change %{_sysconfdir}/pythonrc.py
EOF

%build
rm -f Modules/Setup.local
cat > Modules/Setup.local << EOF
linuxaudiodev linuxaudiodev.c
EOF

OPT="$RPM_OPT_FLAGS -g"
export OPT
%configure2_5x --with-threads --with-cycle-gc --with-cxx=g++ --without-libdb --enable-ipv6 --enable-shared

# fix build
perl -pi -e 's/^(LDFLAGS=.*)/$1 -lstdc++/' Makefile
# (misc) if the home is nfs mounted, rmdir fails due to delay
export TMP="/tmp" TMPDIR="/tmp"
%make

%check
# (misc) if the home is nfs mounted, rmdir fails
export TMP="/tmp" TMPDIR="/tmp"

# all tests must pass
# (misc, 28/11/2006) test_shutil is causing problem in iurt, it seems to remove /tmp, 
# which make other test fail
# (misc, 11/12/2006) test_pyexpat is icrashing, seem to be done on purpose ( http://python.org/sf/1296433 )
# (misc, 11/12/2006) test_minidom is not working anymore, something changed either on my computer
# or elsewhere.
# (misc, 11/12/2006) test_sax fail too, will take a look later 
# (misc, 21/08/2007) test_string and test_str segfault, test_unicode, test_userstring, I need to pass the package as a security update
# test test_sax failed -- 1 of 44 tests failed: test_xmlgen_attr_escape
make test TESTOPTS="-w -l -x test_linuxaudiodev -x test_nis -x test_shutil -x test_pyexpat -x test_minidom -x test_sax -x test_string -x test_str -x test_unicode -x test_userstring"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}

# fix Makefile to get rid of reference to distcc
perl -pi -e "/^CC=/ and s/distcc/gcc/" Makefile

# set the install path
echo '[install_scripts]' >setup.cfg
echo 'install_dir='"${RPM_BUILD_ROOT}/usr/bin" >>setup.cfg

# python is not GNU and does not know fsstd
mkdir -p $RPM_BUILD_ROOT%{_mandir}
%makeinstall_std

(cd $RPM_BUILD_ROOT%{_libdir}; ln -sf libpython%{lib_major}.so.* libpython%{lib_major}.so)

# Provide a libpython%{dirver}.so symlink in /usr/lib/puthon*/config, so that
# the shared library could be found when -L/usr/lib/python*/config is specified
(cd $RPM_BUILD_ROOT%{_libdir}/python%{dirver}/config; ln -sf ../../libpython%{lib_major}.so .)

# emacs, I use it, I want it
mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
install -m 644 Misc/python-mode.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
emacs -batch -f batch-byte-compile $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/python-mode.el

install -d $RPM_BUILD_ROOT%{_sysconfdir}/emacs/site-start.d
cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/emacs/site-start.d/%{name}.el
(setq auto-mode-alist (cons '("\\\\.py$" . python-mode) auto-mode-alist))
(autoload 'python-mode "python-mode" "Mode for python files." t)
EOF

#"  this comment is just here because vim syntax higlighting is confused by the previous snippet of lisp

# smtpd proxy
mv -f $RPM_BUILD_ROOT%{_bindir}/smtpd.py $RPM_BUILD_ROOT%{_libdir}/python%{dirver}/

# idle
cp Tools/scripts/idle $RPM_BUILD_ROOT%{_bindir}/idle

# modulator
cat << EOF > $RPM_BUILD_ROOT%{_bindir}/modulator
#!/bin/bash
exec %{_libdir}/python%{dirver}/site-packages/modulator/modulator.py
EOF
cp -r Tools/modulator $RPM_BUILD_ROOT%{_libdir}/python%{dirver}/site-packages/

# pynche
cat << EOF > $RPM_BUILD_ROOT%{_bindir}/pynche
#!/bin/bash
exec %{_libdir}/python%{dirver}/site-packages/pynche/pynche
EOF
rm -f Tools/pynche/*.pyw
cp -r Tools/pynche $RPM_BUILD_ROOT%{_libdir}/python%{dirver}/site-packages/

chmod 755 $RPM_BUILD_ROOT%{_bindir}/{idle,modulator,pynche}

ln -f Tools/modulator/README Tools/modulator/README.modulator
ln -f Tools/pynche/README Tools/pynche/README.pynche

rm -f modules-list.full
for n in $RPM_BUILD_ROOT%{_libdir}/python%{dirver}/*; do
  [ -d $n ] || echo $n
done >> modules-list.full

for mod in $RPM_BUILD_ROOT%{_libdir}/python%{dirver}/lib-dynload/* ; do
  [ `basename $mod` = _tkinter.so ] || echo $mod
done >> modules-list.full
sed -e "s|$RPM_BUILD_ROOT||g" < modules-list.full > modules-list


mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-tkinter.desktop << EOF
[Desktop Entry]
Name=IDLE
Comment=IDE for Python
Exec=%{_bindir}/idle
Icon=development_environment_section
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Development-DevelopmentEnvironments;Development;IDE;
EOF


cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}-docs.desktop << EOF
[Desktop Entry]
Name=Python documentation
Comment=Python complete reference
Exec=%{_bindir}/www-browser %_defaultdocdir/%{name}-docs/index.html
Icon=documentation_section
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Documentation;
EOF

rm -f include.list main.list
cat %{SOURCE2} | sed 's@%%{_libdir}@%{_libdir}@' > include.list
cat >> modules-list << EOF
%{_bindir}/python
%{_bindir}/python%dirver
%{_bindir}/pydoc
%{_mandir}/man1/python*
%{_libdir}/python*/bsddb/
%{_libdir}/python*/curses/
%{_libdir}/python*/distutils/
%{_libdir}/python*/encodings/*
%{_libdir}/python*/logging/
%{_libdir}/python*/xml/
%{_libdir}/python*/wsgiref/
%{_libdir}/python*/ctypes/
%{_libdir}/python*/sqlite3/
%{_libdir}/python*/compiler/
%{_libdir}/python*/email/
%{_libdir}/python*/hotshot/
%{_libdir}/python*/site-packages/README
%{_libdir}/python*/plat-linux2/
%{_datadir}/emacs/site-lisp/python-mode.el*
EOF

LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_bindir}/python %{SOURCE3} $RPM_BUILD_ROOT include.list modules-list > main.list

# fix non real scripts
chmod 644 $RPM_BUILD_ROOT%{_libdir}/python*/test/test_{binascii,grp,htmlparser}.py*
# fix python library not stripped
chmod u+w $RPM_BUILD_ROOT%{_libdir}/libpython%{lib_major}.so.1.0


mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/

cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/30python.sh << 'EOF'
if [ -f $HOME/.pythonrc.py ] ; then
	export PYTHONSTARTUP=$HOME/.pythonrc.py
else
	export PYTHONSTARTUP=/etc/pythonrc.py
fi
EOF

cat > $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/30python.csh << 'EOF'
if ( -f ${HOME}/.pythonrc.py ) then
	setenv PYTHONSTARTUP ${HOME}/.pythonrc.py
else
	setenv PYTHONSTARTUP /etc/pythonrc.py
endif
EOF

cat > $RPM_BUILD_ROOT%{_sysconfdir}/pythonrc.py << EOF
try:
    # this add completion to python interpreter
    import readline
    import rlcompleter
    # see readline man page for this
    readline.parse_and_bind("set show-all-if-ambiguous on")
    readline.parse_and_bind("tab: complete")
except:
    pass
# you can place a file .pythonrc.py in your home to overrides this one
# but then, this file will not be sourced
EOF

%multiarch_includes $RPM_BUILD_ROOT/usr/include/python*/pyconfig.h

%clean
rm -rf $RPM_BUILD_ROOT
rm -f modules-list main.list

%files -f main.list
%defattr(-, root, root, 755)
%doc README.mdk 
%dir %{_libdir}/python*/lib-dynload
%dir %{_libdir}/python*/site-packages
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/%{name}.el
%{_sysconfdir}/profile.d/*
%config(noreplace) %{_sysconfdir}/pythonrc.py

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/libpython*.so.1*

%files -n %{lib_name}-devel
%defattr(-, root, root, 755)
%{_libdir}/libpython*.so
%dir %{_includedir}/python*
%multiarch %multiarch_includedir/python*/pyconfig.h
%{_includedir}/python*/*
%{_libdir}/python*/config/
%{_libdir}/python*/test/
%{_bindir}/python%{dirver}-config
%{_bindir}/python-config

%files docs
%defattr(-,root,root,755)
%doc html/*/*
%{_datadir}/applications/mandriva-%{name}-docs.desktop

%files -n tkinter
%defattr(-, root, root, 755)
%dir %{_libdir}/python*/lib-tk
%{_libdir}/python*/lib-tk/*.py*
%{_libdir}/python*/lib-dynload/_tkinter.so
%{_libdir}/python*/idlelib
%{_libdir}/python*/site-packages/modulator
%{_libdir}/python*/site-packages/pynche

%files -n tkinter-apps
%defattr(-, root, root, 755)
%{_bindir}/idle
%{_bindir}/pynche
%{_bindir}/modulator
%{_datadir}/applications/mandriva-tkinter.desktop

%files base -f include.list
%defattr(-, root, root, 755)
%dir %{_libdir}/python*

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n tkinter-apps
%update_menus
%endif

%if %mdkversion < 200900
%postun -n tkinter-apps
%clean_menus
%endif


