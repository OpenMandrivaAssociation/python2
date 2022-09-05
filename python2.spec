# Patching guideline for python :
# - no big patch with invasive change not
#     approved by upstream ( ie not coming from upstream svn )
# - small bugfix must be sent to upstream and approved if they
#     change any interface
# - all patchs should be commented ( unless for security,
#     as they are usually easy to spot )

# This is for python >= 3.0 only
%define _python_bytecompile_build 0

%ifarch %{ix86}
%define _disable_lto 1
%endif

%bcond_with tests

%define docver 2.7.16
%define dirver %(echo %{version} |cut -d. -f1-2)

%define api %{dirver}
%define major 1
%define libname %mklibname python %{api} %{major}
%define devname %mklibname python2 -d

%ifarch %{ix86} x86_64 ppc
%bcond_without valgrind
%else
%bcond_with valgrind
%endif

# (tpg) pkgconfig(python) and python-devel is only provided by python3
%global __provides_exclude ^pkgconfig\\(python\\)|^python-devel$

Summary:	An interpreted, interactive object-oriented programming language
Name:		python2
Version:	2.7.18
Release:	3
License:	Modified CNRI Open Source License
Group:		Development/Python
Url:		http://www.python.org/
Source0:	http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
Source1:	http://www.python.org/ftp/python/doc/%{docver}/python-%{docver}-docs-html.tar.bz2
Source2:	bdist_rpm5.py
Source3:	python2.macros
Source100:	%{name}.rpmlintrc
Patch0:		python-2.7.14-module-linkage.patch
Patch1:		python-makeinstall.patch

# Support */lib64 convention on x86_64, sparc64, etc.
# similar patches reported upstream on http://bugs.python.org/issue1294959
Patch4:		python-2.7.4-lib64.patch

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
Patch16:	python-2.7.10-plural-fix.patch

# skip semaphore test, as it requires /dev/shm
Patch23:	python-2.7.1-skip-shm-test.patch

# add support for berkeley db <= 5.1
# sent upstream: http://bugs.python.org/issue11817
Patch24:	Python-2.7.4-berkeley-db-5.3.patch

# do not use uname -m to get the exact name on mips/arm
Patch25:	python-2.7.4-arch.patch

Patch26:	Python-2.7.4-berkeley-db-5.3-2.patch

Patch32:	python-2.5-cflags.patch

# configure erroneously adds invalid -OPT:Olimit=0 to cflags when using clang
Patch33:	python-2.7.11-clang_olimit.patch
# distutils erroneously uses -R when compiling with gcc if clang was used to build
# it should use the correct option for the building compiler not the compiler python was built with
Patch34:	python-2.7.11-rpath_opt.patch
# (tpg) Squashed patch from ClearLinux
Patch36:	python-2.7.14-clearlinux-opt.patch
Patch37:	python-2.7.14-modules-config.patch

BuildRequires:	blt
BuildRequires:	chrpath
BuildRequires:	tix
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	db18-devel
BuildRequires:	gdbm-devel
BuildRequires:	gmp-devel
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(libnsl)
BuildRequires:	python2-six
%if %{with valgrind}
BuildRequires:	valgrind-devel
%endif
# (2010/03/21, misc: interfere with test__all )
BuildConflicts:	python-pyxml
# backwards compatibility for unfixed packages
Provides:	python(abi) = %{api}
Obsoletes:	python < %{EVRD}
Provides:	python = %{EVRD}
Conflicts:	tkinter < %{EVRD}
Conflicts:	python-devel < 2.7-6
Conflicts:	python-pyxml
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

%package -n %{libname}
Summary:	Shared libraries for Python %{version}
Group:		System/Libraries
Obsoletes:	%{_lib}python2.7 < 2.7.5-4

%description -n %{libname}
This packages contains Python shared object library.  Python is an
interpreted, interactive, object-oriented programming language often
compared to Tcl, Perl, Scheme or Java.

%package -n %{devname}
Summary:	The libraries and header files needed for Python development
Group:		Development/Python
Requires:	%{name} = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	python2-pkg-resources
Obsoletes:	%{name}-devel < %{EVRD}
# (misc) needed to ease upgrade , see #47803
Obsoletes:	%{mklibname -d %{name} 2.5} < 2.7
Obsoletes:	%{mklibname -d %{name} 2.6} < 2.7
Obsoletes:	%{mklibname -d %{name} 2.7} < 2.7-4
Provides:	%{name}-devel = %{EVRD}
Provides:	python-devel = %{EVRD}

%description -n %{devname}
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
Requires:	%{name} = %{EVRD}
Requires:	xdg-utils
Group:		Development/Python

%description docs
The python-docs package contains documentation on the Python
programming language and interpreter.  The documentation is provided
in ASCII text files and in LaTeX source files.

Install the python-docs package if you'd like to use the documentation
for the Python language.

%package -n tkinter2
Summary:	A graphical user interface for the Python 2.x scripting language
Group:		Development/Python
Requires:	%{name} = %{EVRD}
Requires:	tcl
Requires:	tk

%description -n tkinter2
The Tkinter (Tk interface) program is an graphical user interface for
the Python 2.x scripting language.

You should install the tkinter2 package if you'd like to use a graphical
user interface for Python 2.x programming.

%package -n tkinter2-apps
Summary:	Various applications written using tkinter 2.x
Group:		Development/Python
Requires:	tkinter2 = %{EVRD}

%description -n tkinter2-apps
Various applications written using tkinter 2.x.

%package test
Summary:	The self-test suite for the main python2 package
Group:		Development/Python
Requires:	%{name} = %{EVRD}

%description test
The self-test suite for the Python interpreter.
This is only useful to test Python itself.

%prep
%setup -qn Python-%{version}
%patch0 -p1
%patch1 -p1

# lib64
%patch4 -p1 -b .lib64

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
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch36 -p1
%patch37 -p1 -b .0037~

%if "%_lib" != "lib"
sed -i -e 's,^LIB=.*,LIB=%_lib,' Makefile.pre.in
%endif

mkdir html
tar xf %{SOURCE1} -C html
find html -type d |xargs chmod 755
find html -type f |xargs chmod 644

# Ensure that we're using the system copy of various libraries, rather than
# copies shipped by upstream in the tarball:
#   Remove embedded copy of expat:
rm -r Modules/expat || exit 1

#   Remove embedded copy of libffi:
for SUBDIR in darwin libffi libffi_arm_wince libffi_msvc libffi_osx ; do
  rm -r Modules/_ctypes/$SUBDIR || exit 1 ;
done

#   Remove embedded copy of zlib:
rm -r Modules/zlib || exit 1

find . -type f -print0 | xargs -0 sed -i -e 's@/usr/local/bin/python@/usr/bin/python2@'

# Scripts used internally must be run with python 2.x
sed -i -e 's,env python,python2,g' Parser/asdl_c.py

autoreconf -fi

%build
%define _disable_ld_no_undefined 1
rm -f Modules/Setup.local
cat > Modules/Setup.local << EOF
linuxaudiodev linuxaudiodev.c
EOF

export OPT="%{optflags} -D_GNU_SOURCE -fPIC -fwrapv"
export CCSHARED="-fno-PIE -fPIC"
export CPPFLAGS="$(pkg-config --libs-only-l libffi)"
export LINKCC=%{__cc}
export CC=%{__cc}
export ac_cv_have_long_long_format=yes

# see https://qa.mandriva.com/show_bug.cgi?id=48570
# for wide unicode support
%configure \
	--with-threads \
	--with-system-expat \
	--with-system-ffi \
	--enable-unicode=ucs4 \
	--enable-ipv6 \
	--enable-shared \
	--with-pymalloc \
	--without-cxx-main \
	--with-signal-module \
	--with-computed-gotos \
%ifnarch %{ix86}
	--enable-optimizations \
%else
	--disable-optimizations \
%endif
%ifnarch %{ix86}
	--with-lto \
%endif
	--with-dbmliborder=gdbm:ndbm:bdb \
%if %{with valgrind}
	--with-valgrind
%endif

# fix build
#perl -pi -e 's/^(LDFLAGS=.*)/$1 -lstdc++/' Makefile
# (misc) if the home is nfs mounted, rmdir fails due to delay
export TMP="/tmp" TMPDIR="/tmp"
%make_build

%if %{with tests}
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
# (tpg, 26/05/2014) disable hash and sqlite tests, because it may affect ABF build
make test TESTOPTS="-w -l -x test_file -x test_file2k -x test_gdb -x test_site -x test_io -x test_distutils -x test_urllib2 -x test_cmath -x test_math -x test_float -x test_strtod -x test_pydoc -x test_ftplib -x test_httplib -x test_poplib -x test_telnetlib -x test_smtplib -x test_asynchat -x test_asyncore -x test_socket -x test_sqlite -x test_hash %{custom_test}"
#make test TESTOPTS="-w -l test_cmath test_math test_float test_strtod"
#make test TESTOPTS="-w -l test_pydoc"
%endif

%install
mkdir -p %{buildroot}%{_prefix}/lib/python%{dirver}/site-packages

# fix Makefile to get rid of reference to distcc
perl -pi -e "/^CC=/ and s/distcc/gcc/" Makefile

# set the install path
echo '[install_scripts]' >setup.cfg
echo 'install_dir='"%{buildroot}/usr/bin" >>setup.cfg

# python is not GNU and does not know fsstd
mkdir -p %{buildroot}%{_mandir}
%make_install

# Currently, _multiprocessing and future_builtins get renamed to *_failed.so
# because of what seems to be a false negative running a test ("No module named
# itertools" when doing a test import -- but itertools exists after make install)
# Let's just "fix" it the quick and dirty way...
cd %{buildroot}%{_libdir}/python%{dirver}/lib-dynload
for i in *_failed.so; do
	[ -e "$i" ] || continue
	mv ${i} ${i/_failed/}
done
cd -

ln -sf libpython%{api}.so.* %{buildroot}/%{_libdir}/libpython%{api}.so

# Provide a libpython%{dirver}.so symlink in /usr/lib/puthon*/config, so that
# the shared library could be found when -L/usr/lib/python*/config is specified
ln -sf ../../libpython%{api}.so %{buildroot}%{_libdir}/python%{dirver}/config; ln -sf ../../libpython%{api}.so .

#"  this comment is just here because vim syntax higlighting is confused by the previous snippet of lisp

# smtpd proxy
mv -f %{buildroot}%{_bindir}/smtpd.py %{buildroot}%{_libdir}/python%{dirver}/

# pynche
cat << EOF > %{buildroot}%{_bindir}/pynche2
#!/bin/bash
exec %{_libdir}/python%{dirver}/site-packages/pynche/pynche
EOF
rm -f Tools/pynche/*.pyw
cp -r Tools/pynche %{buildroot}%{_libdir}/python%{dirver}/site-packages/

chmod 755 %{buildroot}%{_bindir}/pynche2

ln -f Tools/pynche/README Tools/pynche/README.pynche

%if %{with valgrind}
install Misc/valgrind-python.supp -D %{buildroot}%{_libdir}/valgrind/valgrind-python.supp
%endif

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/openmandriva-tkinter2.desktop << EOF
[Desktop Entry]
Name=IDLE
Name[ru]=IDLE
Comment=IDE for Python
Comment[ru]=IDE для Python
Exec=%{_bindir}/idle2
Icon=development_environment_section
Terminal=false
Type=Application
Categories=Development;IDE;
EOF


cat > %{buildroot}%{_datadir}/applications/openmandriva-%{name}-docs.desktop << EOF
[Desktop Entry]
Name=Python documentation
Name[ru]=Документация Python
Comment=Python complete reference
Comment[ru]=Полная документация Python
Exec=%{_bindir}/xdg-open %{_defaultdocdir}/%{name}-docs/index.html
Icon=documentation_section
Terminal=false
Type=Application
Categories=Documentation;
EOF


# fix python library not stripped
chmod u+w %{buildroot}%{_libdir}/libpython%{api}.so.1.0

%if %{mdvver} <= 3000000
%multiarch_includes %{buildroot}/usr/include/python*/pyconfig.h
%endif

mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d
install -m644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/rpm/macros.d/

install -m644 %{SOURCE2} -D %{buildroot}%{_libdir}/python%{dirver}/distutils/command/bdist_rpm5.py

#chrpath -d %{buildroot}%{_libdir}/python%{dirver}/lib-dynload/_sqlite3.so

# Don't conflict with bits now provided by Python 3.x
# We don't strictly have to remove lib2to3, but I don't think it's
# used anywhere outside the 2to3 tool (which is provided by
# python 3.x)
rm -rf \
	%{buildroot}%{_bindir}/python \
	%{buildroot}%{_bindir}/python-config \
	%{buildroot}%{_bindir}/2to3 \
	%{buildroot}%{_libdir}/python%{dirver}/lib2to3

mv %{buildroot}%{_bindir}/pydoc %{buildroot}%{_bindir}/pydoc2
mv %{buildroot}%{_bindir}/idle %{buildroot}%{_bindir}/idle2

%files
%{_sysconfdir}/rpm/macros.d/*.macros
%if "%{_lib}" != "lib"
%dir %{_prefix}/lib/python%{dirver}
%endif
%dir %{_libdir}/python%{dirver}
%{_libdir}/python%{dirver}/*.doc
%{_libdir}/python%{dirver}/*.egg-info
%{_libdir}/python%{dirver}/*.py*
%{_libdir}/python%{dirver}/*.txt
%{_libdir}/python%{dirver}/bsddb
%exclude %{_libdir}/python%{dirver}/bsddb/test
%{_libdir}/python%{dirver}/compiler
# "Makefile" and the config.h file are needed by
# distutils/sysconfig.py:_init_posix(), so we include them in the libs
# package, along with their parent directories (RH bug#531901):
%dir %{_libdir}/python%{dirver}/config
%{_libdir}/python%{dirver}/config/Makefile
%{_libdir}/python%{dirver}/ctypes
%exclude %{_libdir}/python%{dirver}/ctypes/test
%{_libdir}/python%{dirver}/curses
%{_libdir}/python%{dirver}/distutils
%exclude %{_libdir}/python%{dirver}/distutils/tests
%{_libdir}/python%{dirver}/email
%exclude %{_libdir}/python%{dirver}/email/test
%{_libdir}/python%{dirver}/encodings
# FIXME why does this get built only in abf???
%optional %{_libdir}/python%{dirver}/ensurepip
%{_libdir}/python%{dirver}/hotshot
%{_libdir}/python%{dirver}/importlib
%{_libdir}/python%{dirver}/json
%exclude %{_libdir}/python%{dirver}/json/tests
%{_libdir}/python%{dirver}/lib-dynload
%exclude %{_libdir}/python%{dirver}/lib-dynload/_tkinter.so
%exclude %{_libdir}/python%{dirver}/lib-dynload/_ctypes_test.so
%exclude %{_libdir}/python%{dirver}/lib-dynload/_testcapimodule.so
%{_libdir}/python%{dirver}/logging
%{_libdir}/python%{dirver}/multiprocessing
%{_libdir}/python%{dirver}/plat-linux2
%{_libdir}/python%{dirver}/pydoc_data
%if "%{_lib}" != "lib"
%dir %{_prefix}/lib/python%{dirver}/site-packages
%endif
%dir %{_libdir}/python%{dirver}/site-packages
%{_libdir}/python%{dirver}/site-packages/README
%{_libdir}/python%{dirver}/sqlite3
%exclude %{_libdir}/python%{dirver}/sqlite3/test
%{_libdir}/python%{dirver}/unittest
%exclude %{_libdir}/python%{dirver}/unittest/test
%{_libdir}/python%{dirver}/wsgiref
%{_libdir}/python%{dirver}/xml

%dir %{_includedir}/python%{dirver}
%{_includedir}/python%{dirver}/pyconfig.h
%if %{mdvver} <= 3000000
%multiarch_includedir/python%{dirver}/pyconfig.h
%endif

%{_bindir}/python%{dirver}
%{_bindir}/pydoc2
%{_bindir}/python2
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
%{_bindir}/python%{dirver}-config
%{_bindir}/python2-config
%exclude %{_libdir}/python%{dirver}/config/Makefile
%exclude %{_includedir}/python%{dirver}/pyconfig.h

%files docs
%doc html/*/*
%{_datadir}/applications/openmandriva-%{name}-docs.desktop

%files -n tkinter2
%dir %{_libdir}/python%{dirver}/lib-tk
%{_libdir}/python%{dirver}/lib-tk/*.py*
%{_libdir}/python%{dirver}/lib-dynload/_tkinter.so
%{_libdir}/python%{dirver}/idlelib
%{_libdir}/python%{dirver}/site-packages/pynche

%files -n tkinter2-apps
%{_bindir}/idle2
%{_bindir}/pynche2
%{_datadir}/applications/openmandriva-tkinter2.desktop

%files test
%{_libdir}/python%{dirver}/bsddb/test
%{_libdir}/python%{dirver}/ctypes/test
%{_libdir}/python%{dirver}/distutils/tests
%{_libdir}/python%{dirver}/email/test
%{_libdir}/python%{dirver}/json/tests
%{_libdir}/python%{dirver}/sqlite3/test
%{_libdir}/python%{dirver}/unittest/test
%{_libdir}/python%{dirver}/test/
%{_libdir}/python%{dirver}/lib-tk/test/
%{_libdir}/python%{dirver}/lib-dynload/_ctypes_test.so
%{_libdir}/python%{dirver}/lib-dynload/_testcapimodule.so
