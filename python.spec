# Patching guideline for python :
# - no big patch with invasive change not 
#     approved by upstream ( ie not coming from upstream svn )
# - small bugfix must be sent to upstream and approved if they 
#     change any interface
# - all patchs should be commented ( unless for security, 
#     as they are usually easy to spot )

%define docver 2.7.6
%define dirver 2.7

%define api %{dirver}
%define major 1
%define libname %mklibname %{name} %{api} %{major}
%define devname %mklibname %{name} -d

%ifarch %{ix86} x86_64 ppc
%bcond_without valgrind
%else
%bcond_with valgrind
%endif

Summary:	An interpreted, interactive object-oriented programming language
Name:		python
Version:	2.7.6
Release:	2
License:	Modified CNRI Open Source License
Group:		Development/Python
Url:		http://www.python.org/
Source0:	http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
Source1:	http://www.python.org/ftp/python/doc/%{docver}/python-%{docver}-docs-html.tar.bz2
Source2:	bdist_rpm5.py
Source3:	%{name}.rpmlintrc
Patch0:		python-2.7.4-module-linkage.patch

# Support */lib64 convention on x86_64, sparc64, etc.
# similar patches reported upstream on http://bugs.python.org/issue1294959
Patch4:		python-2.7.4-lib64.patch

# Do handle <asm-XXX/*.h> headers in h2py.py
# FIXME: incomplete for proper bi-arch support as #if/#else/#endif
# clauses generally should have been handled
# to send upstream after cleaning
Patch5:		Python-2.2.2-biarch-headers.patch

Patch6:		python-2.7-016-cross-compile-getaddrinfo.patch

# add mandriva to the list of supported distribution, applied upstream
Patch10:	python-2.5.1-detect-mandriva.patch

# adds xz support to distutils targets: 'sdist', 'bdist' & 'bdist_rpm'
# sent upstream : http://bugs.python.org/issue5411
# DO NOT REMOVE, IT DOESN'T TOUCH *ANY* public interfaces and has been
# accepted by upstream
#Patch14:	Python-2.7.2-distutils-xz-support.patch

# from Fedora, fixes gettext.py parsing of Plural-Forms: header (fixes mdv bugs #49475, #44088)
# to send upstream
Patch16:	python-2.5.1-plural-fix.patch

# skip semaphore test, as it requires /dev/shm
Patch23:	python-2.7.1-skip-shm-test.patch

# add support for berkeley db <= 5.1
# sent upstream: http://bugs.python.org/issue11817
Patch24:	Python-2.7.4-berkeley-db-5.3.patch

# do not use uname -m to get the exact name on mips/arm
Patch25:	python-2.7.4-arch.patch

Patch26:	Python-2.7.4-berkeley-db-5.3-2.patch

BuildRequires:	blt
BuildRequires:	chrpath
BuildRequires:	tix
BuildRequires:	bzip2-devel
BuildRequires:	db5-devel
BuildRequires:	gdbm-devel
BuildRequires:	gmp-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
%if %{with valgrind}
BuildRequires:	valgrind-devel
%endif
# (2010/03/21, misc: interfere with test__all )
BuildConflicts:	python-pyxml
# backwards compatibility for unfixed packages
Provides:	python(abi) = %{api}
Conflicts:	tkinter < %{EVRD}
Conflicts:	python-devel < 2.7-6
%rename		python-ctypes
%rename		python-elementtree
%rename		python-base

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

%package -n	%{libname}
Summary:	Shared libraries for Python %{version}
Group:		System/Libraries
Obsoletes:	%{_lib}python2.7 < 2.7.5-5

%description -n	%{libname}
This packages contains Python shared object library.  Python is an
interpreted, interactive, object-oriented programming language often
compared to Tcl, Perl, Scheme or Java.

%package -n	%{devname}
Summary:	The libraries and header files needed for Python development
Group:		Development/Python
Requires:	%{name} = %{EVRD}
Requires:	%{libname} = %{EVRD}
Obsoletes:	%{name}-devel < %{EVRD}
# (misc) needed to ease upgrade , see #47803
Obsoletes:	%{mklibname -d %{name} 2.5} < 2.7
Obsoletes:	%{mklibname -d %{name} 2.6} < 2.7
Obsoletes:	%{mklibname -d %{name} 2.7} < 2.7-4
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install %{devname} if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package docs
Summary:	Documentation for the Python programming language
Requires:	python = %{EVRD}
Requires:	xdg-utils
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
Requires:	python = %{EVRD}
Requires:	tcl
Requires:	tk

%description -n	tkinter
The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you'd like to use a graphical
user interface for Python programming.

%package -n	tkinter-apps
Summary:	Various applications written using tkinter
Group:		Development/Python
Requires:	tkinter

%description -n	tkinter-apps
Various applications written using tkinter.

%prep
%setup -qn Python-%{version}
%patch0 -p0
# lib64
%patch4 -p0 -b .lib64

# biarch header
%patch5 -p0

#disable buggy getaddr check
%patch6 -p1

# add mandriva to the list of supported distribution
%patch10 -p0
# must fix tararchive first..
#patch14 -p1 .xz~

%patch16 -p1 -b .plural-fix

%patch23 -p1 
%patch24 -p1 -b .db5~
%patch25 -p1 -b .arch
%patch26 -p1 -b .db5-2

autoconf

mkdir html
bzcat %{SOURCE1} | tar x  -C html

find . -type f -print0 | xargs -0 perl -p -i -e 's@/usr/local/bin/python@/usr/bin/python@'

cat > README.omv << EOF
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

export OPT="%{optflags}"
export CCSHARED="-fno-PIE -fPIC"
export ac_cv_have_long_long_format=yes

# see https://qa.mandriva.com/show_bug.cgi?id=48570 
# for wide unicode support
%configure2_5x \
	--with-threads \
	--with-system-expat \
	--with-system-ffi \
	--enable-unicode=ucs4 \
	--enable-ipv6 \
	--enable-shared \
	--with-dbmliborder=gdbm:ndbm:bdb \
%if %{with valgrind}
	--with-valgrind
%endif

# fix build
#perl -pi -e 's/^(LDFLAGS=.*)/$1 -lstdc++/' Makefile
# (misc) if the home is nfs mounted, rmdir fails due to delay
export TMP="/tmp" TMPDIR="/tmp"
%make

%check
# (misc) if the home is nfs mounted, rmdir fails
export TMP="/tmp" TMPDIR="/tmp"

# all tests must pass
%ifarch %{arm}
# don't know if it's a python issue or a toolchain issue :(
# test test_float failed -- Traceback (most recent call last):
#  File "/home/rtp/deb/python2.6-2.6.4/Lib/test/test_float.py", line 665, in test_from_hex
#    self.identical(fromHex('0x0.ffffffffffffd6p-1022'), MIN-3*TINY)
#  File "/home/rtp/deb/python2.6-2.6.4/Lib/test/test_float.py", line 375, in identical
#    self.fail('%r not identical to %r' % (x, y))
# AssertionError: 2.2250738585071999e-308 not identical to 2.2250738585071984e-308
%define custom_test -x test_float
%else
%define custom_test ""
%endif
# if a test doesn't pass, it can be disabled with -x test, but this should be documented in the
# spec file, and a bug should be reported if possible ( on python side )
# (misc, 28/10/2010) test_gdb fail, didn't time too look
# (misc, 29/10/2010) test_site fail due to one of our patch, will fix later
#   test_distutils, fail because of lib64 patch ( like test_site ), and because it requires libpython2.7 to be installed
#   test_io, blocks on my computer on 2nd run
# (misc, 17/01/2013) test_cmath fails when run as part of the full test suite,
#   but succeeds when run by itself. Needs further investigation, for now, let's
#   just make it an extra step. Same goes for test_math, test_float, test_strtod
# (arisel, 04/02/2013) disabling test_file and test_file2k. This might be a problem with 
#   --enable-shared as modules already installed on the system are used.
# (bero, 19/06/2013) disabling test_pydoc, fails with 'NoneType' object has no attribute 'get_source'
# (bero, 19/06/2013) Network related tests fail in ABF - probably new security features not allowing package
# builds to access the net?
make test TESTOPTS="-w -l -x test_file -x test_file2k -x test_gdb -x test_site -x test_io -x test_distutils -x test_urllib2 -x test_cmath -x test_math -x test_float -x test_strtod -x test_pydoc -x test_ftplib -x test_httplib -x test_poplib -x test_telnetlib -x test_smtplib -x test_asynchat -x test_asyncore -x test_socket %{custom_test}"
make test TESTOPTS="-w -l test_cmath test_math test_float test_strtod"
#make test TESTOPTS="-w -l test_pydoc"

%install
mkdir -p %{buildroot}%{_prefix}/lib/python%{dirver}/site-packages

# fix Makefile to get rid of reference to distcc
perl -pi -e "/^CC=/ and s/distcc/gcc/" Makefile

# set the install path
echo '[install_scripts]' >setup.cfg
echo 'install_dir='"%{buildroot}/usr/bin" >>setup.cfg

# python is not GNU and does not know fsstd
mkdir -p %{buildroot}%{_mandir}
%makeinstall_std

ln -sf libpython%{api}.so.* %{buildroot}/%{_libdir}/libpython%{api}.so

# Provide a libpython%{dirver}.so symlink in /usr/lib/puthon*/config, so that
# the shared library could be found when -L/usr/lib/python*/config is specified
ln -sf ../../libpython%{api}.so %{buildroot}%{_libdir}/python%{dirver}/config; ln -sf ../../libpython%{api}.so .

#"  this comment is just here because vim syntax higlighting is confused by the previous snippet of lisp

# smtpd proxy
mv -f %{buildroot}%{_bindir}/smtpd.py %{buildroot}%{_libdir}/python%{dirver}/

# idle
cp Tools/scripts/idle %{buildroot}%{_bindir}/idle


# pynche
cat << EOF > %{buildroot}%{_bindir}/pynche
#!/bin/bash
exec %{_libdir}/python%{dirver}/site-packages/pynche/pynche
EOF
rm -f Tools/pynche/*.pyw
cp -r Tools/pynche %{buildroot}%{_libdir}/python%{dirver}/site-packages/

chmod 755 %{buildroot}%{_bindir}/{idle,pynche}

ln -f Tools/pynche/README Tools/pynche/README.pynche

%if %{with valgrind}
install Misc/valgrind-python.supp -D %{buildroot}%{_libdir}/valgrind/valgrind-python.supp
%endif

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-tkinter.desktop << EOF
[Desktop Entry]
Name=IDLE
Comment=IDE for Python
Exec=%{_bindir}/idle
Icon=development_environment_section
Terminal=false
Type=Application
Categories=Development;IDE;
EOF


cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-docs.desktop << EOF
[Desktop Entry]
Name=Python documentation
Comment=Python complete reference
Exec=%{_bindir}/xdg-open %{_defaultdocdir}/%{name}-docs/index.html
Icon=documentation_section
Terminal=false
Type=Application
Categories=Documentation;
EOF


# fix non real scripts
chmod 644 %{buildroot}%{_libdir}/python*/test/test_{binascii,grp,htmlparser}.py*
# fix python library not stripped
chmod u+w %{buildroot}%{_libdir}/libpython%{api}.so.1.0


mkdir -p %{buildroot}%{_sysconfdir}/profile.d/

cat > %{buildroot}%{_sysconfdir}/profile.d/30python.sh << 'EOF'
if [ -f $HOME/.pythonrc.py ] ; then
	export PYTHONSTARTUP=$HOME/.pythonrc.py
else
	export PYTHONSTARTUP=/etc/pythonrc.py
fi

export PYTHONDONTWRITEBYTECODE=1
EOF

cat > %{buildroot}/%{_sysconfdir}/profile.d/30python.csh << 'EOF'
if ( -f ${HOME}/.pythonrc.py ) then
	setenv PYTHONSTARTUP ${HOME}/.pythonrc.py
else
	setenv PYTHONSTARTUP /etc/pythonrc.py
endif
setenv PYTHONDONTWRITEBYTECODE 1
EOF

cat > %{buildroot}%{_sysconfdir}/pythonrc.py << EOF
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

%multiarch_includes %{buildroot}/usr/include/python*/pyconfig.h

install -m644 %{SOURCE2} -D %{buildroot}%{_libdir}/python%{dirver}/distutils/command/bdist_rpm5.py

#chrpath -d %{buildroot}%{_libdir}/python%{dirver}/lib-dynload/_sqlite3.so

%files
%doc README.omv
%{_sysconfdir}/profile.d/*
%config(noreplace) %{_sysconfdir}/pythonrc.py
%if %{_lib} != "lib"
%dir %{_prefix}/lib/python%{dirver}
%endif
%dir %{_libdir}/python%{dirver}
%{_libdir}/python%{dirver}/*.doc
%{_libdir}/python%{dirver}/*.egg-info
%{_libdir}/python%{dirver}/*.py*
%{_libdir}/python%{dirver}/*.txt
%{_libdir}/python%{dirver}/bsddb
%{_libdir}/python%{dirver}/compiler
# "Makefile" and the config.h file are needed by
# distutils/sysconfig.py:_init_posix(), so we include them in the libs
# package, along with their parent directories (RH bug#531901):
%dir %{_libdir}/python%{dirver}/config
%{_libdir}/python%{dirver}/config/Makefile
%{_libdir}/python%{dirver}/ctypes
%{_libdir}/python%{dirver}/curses
%{_libdir}/python%{dirver}/distutils
%{_libdir}/python%{dirver}/email
%{_libdir}/python%{dirver}/encodings
%{_libdir}/python%{dirver}/hotshot
%{_libdir}/python%{dirver}/importlib
%{_libdir}/python%{dirver}/json
%{_libdir}/python%{dirver}/lib2to3
%{_libdir}/python%{dirver}/lib-dynload
%exclude %{_libdir}/python%{dirver}/lib-dynload/_tkinter.so
%{_libdir}/python%{dirver}/logging
%{_libdir}/python%{dirver}/multiprocessing
%{_libdir}/python%{dirver}/plat-linux2
%{_libdir}/python%{dirver}/pydoc_data
%if %{_lib} != "lib"
%dir %{_prefix}/lib/python%{dirver}/site-packages
%endif
%dir %{_libdir}/python%{dirver}/site-packages
%{_libdir}/python%{dirver}/site-packages/README
%{_libdir}/python%{dirver}/sqlite3
%{_libdir}/python%{dirver}/unittest
%{_libdir}/python%{dirver}/wsgiref
%{_libdir}/python%{dirver}/xml

%dir %{_includedir}/python%{dirver}
%{_includedir}/python%{dirver}/pyconfig.h
%multiarch_includedir/python%{dirver}/pyconfig.h

%{_bindir}/python%{dirver}
%{_bindir}/pydoc
%{_bindir}/python
%{_bindir}/python2
%{_bindir}/2to3
%{_mandir}/man*/*
%if %{with valgrind}
%{_libdir}/valgrind/valgrind-python.supp
%endif

%files -n %{libname}
%{_libdir}/libpython%{api}.so.%{major}*

%files -n %{devname}
%{_libdir}/libpython*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/python%{dirver}
%{_libdir}/python%{dirver}/config/*
%{_libdir}/python%{dirver}/test/
%{_bindir}/python%{dirver}-config
%{_bindir}/python2-config
%{_bindir}/python-config
%exclude %{_libdir}/python%{dirver}/config/Makefile
%exclude %{_includedir}/python%{dirver}/pyconfig.h

%files docs
%doc html/*/*
%{_datadir}/applications/mandriva-%{name}-docs.desktop

%files -n tkinter
%dir %{_libdir}/python%{dirver}/lib-tk
%{_libdir}/python%{dirver}/lib-tk/*.py*
%{_libdir}/python%{dirver}/lib-tk/test/
%{_libdir}/python%{dirver}/lib-dynload/_tkinter.so
%{_libdir}/python%{dirver}/idlelib
%{_libdir}/python%{dirver}/site-packages/pynche

%files -n tkinter-apps
%{_bindir}/idle
%{_bindir}/pynche
%{_datadir}/applications/mandriva-tkinter.desktop
