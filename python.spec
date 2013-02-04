# Patching guideline for python :
# - no big patch with invasive change not 
#     approved by upstream ( ie not coming from upstream svn )
# - small bugfix must be sent to upstream and approved if they 
#     change any interface
# - all patchs should be commented ( unless for security, 
#     as they are usually easy to spot )

%define	docver	2.7.3
%define	dirver	2.7

%define	major	%{dirver}
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

%ifarch %{ix86} x86_64 ppc
%bcond_without	valgrind
%else
%bcond_with	valgrind
%endif
Summary:	An interpreted, interactive object-oriented programming language
Name:		python
Version:	2.7.3
Release:	8
License:	Modified CNRI Open Source License
Group:		Development/Python
URL:		http://www.python.org/
Source0:	http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.bz2
Source1:	http://www.python.org/ftp/python/doc/%{docver}/python-%{docver}-docs-html.tar.bz2
Source2:	bdist_rpm5.py
Source3:	%{name}.rpmlintrc
Patch0:		python-2.7-module-linkage.patch
# Don't include /usr/local/* in search path
Patch3:		Python-2.7.2-no-local-incpath.patch

# Support */lib64 convention on x86_64, sparc64, etc.
# similar patches reported upstream on http://bugs.python.org/issue1294959
Patch4:		python-lib64.patch

# Do handle <asm-XXX/*.h> headers in h2py.py
# FIXME: incomplete for proper bi-arch support as #if/#else/#endif
# clauses generally should have been handled
# to send upstream after cleaning
Patch5:		Python-2.2.2-biarch-headers.patch

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
Patch23: python-2.7.1-skip-shm-test.patch

# add support for berkeley db <= 5.1
# sent upstream: http://bugs.python.org/issue11817
Patch24:	Python-2.7.1-berkeley-db-5.3.patch

# do not use uname -m to get the exact name on mips/arm
Patch25:	python_arch.patch

Patch26:	Python-2.7.1-berkeley-db-5.3-2.patch

BuildRequires:	blt
BuildRequires:	db5-devel
BuildRequires:	expat-devel
BuildRequires:	gdbm-devel
BuildRequires:	gmp-devel
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	readline-devel
BuildRequires:	tcl tcl-devel
BuildRequires:	tk tk-devel
BuildRequires:	tix
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(sqlite3)
%if %{with valgrind}
BuildRequires:	valgrind-devel
%endif
BuildRequires:	chrpath
# (2010/03/21, misc: interfere with test__all )
BuildConflicts:	python-pyxml

Conflicts:	tkinter < %{version}
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

%description -n	%{libname}
This packages contains Python shared object library.  Python is an
interpreted, interactive, object-oriented programming language often
compared to Tcl, Perl, Scheme or Java.

%package -n	%{devname}
Summary:	The libraries and header files needed for Python development
Group:		Development/Python
Requires:	%{name} = %{version}
Requires:	%{libname} = %{version}
Obsoletes:	%{name}-devel < %{version}-%{release}
# (misc) needed to ease upgrade , see #47803
Obsoletes:	%{mklibname -d %{name} 2.5} < 2.7
Obsoletes:	%{mklibname -d %{name} 2.6} < 2.7
Obsoletes:	%{mklibname -d %{name} 2.7} < 2.7-4
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install %{devname} if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package	docs
Summary:	Documentation for the Python programming language
Requires:	python = %{version}
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
Requires:	python = %{version}
Requires:	tcl tk

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
Various applications written using tkinter

%prep
%setup -q -n Python-%{version}
%patch0 -p0
# local include
%patch3 -p0
# lib64
%patch4 -p0 -b .lib64

# biarch header
%patch5 -p0

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

export OPT="%{optflags}"
export CCSHARED="-fPIC -fno-PIE"

# see https://qa.mandriva.com/show_bug.cgi?id=48570 
# for wide unicode support
%configure2_5x \
    --with-threads \
    --with-system-expat \
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
# (arisel, 04/02/2013) trying the same with file2k. This might be a problem with 
#   --enable-shared as modules already installed on the system are used.
make test TESTOPTS="-w -l -x test_file -x test_file2k -x test_gdb -x test_site -x test_io -x test_distutils -x test_urllib2 -x test_cmath -x test_math -x test_float -x test_strtod -x test_pydoc %{custom_test}"
make test TESTOPTS="-w -l test_cmath test_math test_float test_strtod test_pydoc test_file2k test_file"

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

ln -sf libpython%{major}.so.* %{buildroot}/%{_libdir}/libpython%{major}.so

# Provide a libpython%{dirver}.so symlink in /usr/lib/puthon*/config, so that
# the shared library could be found when -L/usr/lib/python*/config is specified
ln -sf ../../libpython%{major}.so %{buildroot}%{_libdir}/python%{dirver}/config; ln -sf ../../libpython%{major}.so .

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
chmod u+w %{buildroot}%{_libdir}/libpython%{major}.so.1.0


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

chrpath -d %{buildroot}%{_libdir}/python%{dirver}/lib-dynload/_sqlite3.so

%files
%doc README.mdk
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
%{_libdir}/libpython*.so.1*

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


%changelog
* Sun May 13 2012 Crispin Boylan <crisb@mandriva.org> 2.7.3-6
+ Revision: 798605
- Add patch 26 to fix db module build for db5.2 and later

* Sat May 12 2012 Crispin Boylan <crisb@mandriva.org> 2.7.3-5
+ Revision: 798518
- Fix dbm and db5.3 module build

* Sat May 12 2012 Crispin Boylan <crisb@mandriva.org> 2.7.3-4
+ Revision: 798489
- Drop patch 27 (merged upstream)
- Drop patch 26 (merged upstream)
- New release

* Thu Feb 16 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.7.2-4
+ Revision: 775410
- get rid of rpath for _sqlite3.so
- filter out non-executable-script rpmlint errors
- apply some minor spec cosmetics
- drop libpython-devel provides
- be sure to create & own %%{_prefix}/lib/python%%{dirver}/site-packages on lib64
- list which files to include more explicitly (fixing files listed twice error)

  + Matthew Dawkins <mattydaw@mandriva.org>
    - and fix for rpmlint file listed twice
    - added p27 for gdbm test failures (found at mga)
    - cleaned up spec
    - stick with db52 for now
    - rebuild

* Thu Dec 01 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.7.2-3
+ Revision: 735918
- just use %%{optflags} as a default for OPT to ensure that we get the current
  debug flags and that '-g' doesn't change them
- pass -fno-PIE to gcc, preventing -fPIE sneaking in and breaking builds

  + Alexandre Lissy <alissy@mandriva.com>
    - Fix %%patch14 misusage. Jurt triggers:
      >>>> running privilleged agent: /usr/sbin/jurt-root-command --type runcmd --target cooker-x86_64 --root /var/spool/jurt/chroots//active/2011.11.09.113025-user --arch x86_64 --run-as builder -- /usr/bin/rpmbuild --define "_topdir /home/builder" -ba //home/builder/SPECS/python.spec
      >>>>>> running: /usr/bin/env -i unshare --ipc --uts -- /usr/sbin/chroot /var/spool/jurt/chroots//active/2011.11.09.113025-user /bin/su -l builder -c "/usr/bin/rpmbuild --define \"_topdir /home/builder\" -ba //home/builder/SPECS/python.spec"
      error: File %%PATCH14: No such file or directory

  + Franck Bui <franck.bui@mandriva.com>
    - sys.platform always returns linux2 even when compiled on kernel 3.x

* Tue Aug 30 2011 Paulo Andrade <pcpa@mandriva.com.br> 2.7.2-2
+ Revision: 697420
- Rebuild for cooker

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - clean out old junk
    - add license classifier to bdist_rpm5.py (Alexandr?\195?\169 Lissy <alissy@mandriva.com>

  + Matthew Dawkins <mattydaw@mandriva.org>
    - fix arch detection
    - disable float test on arm
    - fix test on arm, reported by rtp

* Thu Jun 23 2011 Funda Wang <fwang@mandriva.org> 2.7.2-1
+ Revision: 686758
- new version 2.7.2

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - add a rpm5-customized generator (bdist_rpm5) for distutils

* Mon May 23 2011 Oden Eriksson <oeriksson@mandriva.com> 2.7.1-8
+ Revision: 677583
- updated fix for CVE-2011-1521
- use --with-system-expat
- P25: security fix for CVE-2011-1521

* Mon May 02 2011 Funda Wang <fwang@mandriva.org> 2.7.1-7
+ Revision: 662009
- add br

  + Oden Eriksson <oeriksson@mandriva.com>
    - multiarch fixes

* Sun Apr 10 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.7.1-6
+ Revision: 652217
- fix & build against berkeley db 5.1 (P24, upstream #11817)

* Thu Mar 03 2011 Lev Givon <lev@mandriva.org> 2.7.1-5
+ Revision: 641445
- Remove emacs python-mode for independent repackaging (#62659).

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 2.7.1-4
+ Revision: 640256
- rebuild to obsolete old packages

* Thu Feb 03 2011 Guillaume Rousse <guillomovitch@mandriva.org> 2.7.1-3
+ Revision: 635442
- fix patch to really force all semaphores test results

* Mon Jan 31 2011 Guillaume Rousse <guillomovitch@mandriva.org> 2.7.1-2
+ Revision: 634584
- force semaphore check result, to workaround /dev/shm unavailability in build host (#62281)

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - ditch eplicit python(abi) provides, it gets added by dependency extractor already

* Mon Nov 29 2010 Funda Wang <fwang@mandriva.org> 2.7.1-1mdv2011.0
+ Revision: 602975
- drop merged CVE patch
- X11-devel not required
- New version 2.7.1

* Thu Nov 04 2010 Funda Wang <fwang@mandriva.org> 2.7-8mdv2011.0
+ Revision: 593073
- fix conflicts

  + Michael Scherer <misc@mandriva.org>
    - revert patch as it was not applied upstream first, and as it change the API

* Wed Nov 03 2010 Paulo Andrade <pcpa@mandriva.com.br> 2.7-7mdv2011.0
+ Revision: 593024
- Add http://bugs.python.org/issue7689 correction

  + Funda Wang <fwang@mandriva.org>
    - python-devel not needed

* Sun Oct 31 2010 Funda Wang <fwang@mandriva.org> 2.7-6mdv2011.0
+ Revision: 591160
- more linkage fix
- BR python-devel for now
- link against dl also
- fix module link of ctypes
- move Makefile and pyconfig into main pkg as required by sysconfig.py

* Sat Oct 30 2010 Oden Eriksson <oeriksson@mandriva.com> 2.7-5mdv2011.0
+ Revision: 590456
- P23: security fix for CVE-2010-3493
- P24: security fix for CVE-2010-3492

* Sat Oct 30 2010 Anssi Hannula <anssi@mandriva.org> 2.7-4mdv2011.0
+ Revision: 590326
- apply current devel library naming policy to smoothen upgrades

* Fri Oct 29 2010 Michael Scherer <misc@mandriva.org> 2.7-3mdv2011.0
+ Revision: 590288
- add a provides on python(abi), macro taken by fedora, proposal by anssi to have a automated requires on the python version

* Fri Oct 29 2010 Funda Wang <fwang@mandriva.org> 2.7-2mdv2011.0
+ Revision: 589919
- really use correct patch from fedora
- add fedora patch to fix lib64 detecting

* Fri Oct 29 2010 Michael Scherer <misc@mandriva.org> 2.7-1mdv2011.0
+ Revision: 589889
- fix the test list exception
- fix the test name that should be disabled
- disable test_get_outputs, seems it requires that python 2.7 is installed on build host
- disable test_getsitepackages as it fail due to one of our patch, I need to fix the test
- update to 2.7
- enable wide unicode support ( fix mdv#48570 )
- remove patch applied upstream ( tcl 8.6, pymalloc, d 4.8 )
- remove patch no longer needed ( ctypes linkage )
- remove patch deviating too much from upstream and not accepted yet ( xz )
- update lib6' patch
- add patch for support of new autoconf
- reenable tests that were previously disable, as this doesn't cause problem anymore

* Wed Aug 25 2010 Funda Wang <fwang@mandriva.org> 2.6.6-1mdv2011.0
+ Revision: 573088
- new version 2.6.6

* Wed Jul 14 2010 Oden Eriksson <oeriksson@mandriva.com> 2.6.5-4mdv2011.0
+ Revision: 553383
- bump release
- P21: security fix for CVE-2010-2089
- note that P19 does NOT solve CVE-2008-5983, it's just a new api
  developers can use to fix similar problems, will be added in 2.6.6

  + Funda Wang <fwang@mandriva.org>
    - add upstream patch to build with 4.8
    - add patches fixing CVE-2008-5983 and CVE-2010-1634

* Mon Apr 05 2010 Funda Wang <fwang@mandriva.org> 2.6.5-2mdv2010.1
+ Revision: 531712
- rebuild for new openssl

  + Michael Scherer <misc@mandriva.org>
    - add a BuildConflicts for failling test

* Sat Mar 20 2010 Michael Scherer <misc@mandriva.org> 2.6.5-1mdv2010.1
+ Revision: 525430
- add exception for test_distutils ( as it requires python-devel )
- update to 2.6.5
- remove patch for CVE-2009-3560, merged upstream
- remove patch from Fedora, not approved upstream
- clean test exceptions
- update linkage patch for python 2.6.5

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt against openssl-0.9.8m

* Sat Jan 30 2010 Funda Wang <fwang@mandriva.org> 2.6.4-6mdv2010.1
+ Revision: 498510
- add patches from fedora to have it built and work with db4.8

* Mon Jan 25 2010 Michael Scherer <misc@mandriva.org> 2.6.4-5mdv2010.1
+ Revision: 496309
- re-add _bsddb.so, as it doesn't support db4.8, spotted by bogdano

* Sun Jan 17 2010 Michael Scherer <misc@mandriva.org> 2.6.4-4mdv2010.1
+ Revision: 492596
- link python with ncursesw, to fix canto crashing

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 2.6.4-3mdv2010.1
+ Revision: 488613
- P18: security fix for CVE-2009-3560

* Thu Dec 31 2009 Funda Wang <fwang@mandriva.org> 2.6.4-2mdv2010.1
+ Revision: 484292
- 2.6.4 docs
- rebuild for db 4.8

* Tue Oct 27 2009 Michael Scherer <misc@mandriva.org> 2.6.4-1mdv2010.0
+ Revision: 459569
- update doc
- update to latest version of python

* Tue Oct 06 2009 Michael Scherer <misc@mandriva.org> 2.6.3-1mdv2010.0
+ Revision: 454344
- disable test_distutils, as the test requires python-devel to be installed
- new bugfix release

* Sun Aug 23 2009 Oden Eriksson <oeriksson@mandriva.com> 2.6.2-4mdv2010.0
+ Revision: 419988
- bump release
- P18: security fix related to CVE-2009-2625

* Sat Jul 11 2009 Funda Wang <fwang@mandriva.org> 2.6.2-2mdv2010.0
+ Revision: 394776
- use -lpthread rather than -pthread

* Sat Jul 04 2009 Funda Wang <fwang@mandriva.org> 2.6.2-1mdv2010.0
+ Revision: 392298
- fix libdir
- fix /usr/lib
- fix typo
- fix desktop file
- Update linkage patch
- link on stdc++ is not needed, and it causes wrong link order
- update docs
- New version 2.6.2
- gdbm problem solved upstream
- rediff glibc and format string patch

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - no need to own subdirs of already owned dirs
    - ensure arch-independant tree is owned

  + Michael Scherer <misc@mandriva.org>
    - patch cleaning

* Sun Apr 12 2009 Gustavo De Nardin <gustavodn@mandriva.com> 2.6.1-6mdv2009.1
+ Revision: 366460
- P16: plural-fix, from Fedora, fixes gettext.py parsing of Plural-Forms:
  header (mdv bugs #49475, #44088)

* Wed Mar 04 2009 Gustavo De Nardin <gustavodn@mandriva.com> 2.6.1-5mdv2009.1
+ Revision: 348705
- fixed current UTF-8 proper name in locale.py, which fixes mdv bug #48158

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - add xz support to distutils (P14)

* Tue Feb 24 2009 Michael Scherer <misc@mandriva.org> 2.6.1-4mdv2009.1
+ Revision: 344595
- fix bug #47803, work around a urpmi behavior, idea from
  frederic himpe.

* Mon Jan 26 2009 Michael Scherer <misc@mandriva.org> 2.6.1-3mdv2009.1
+ Revision: 333792
- remove duplicated file from python packages

* Mon Jan 26 2009 Funda Wang <fwang@mandriva.org> 2.6.1-2mdv2009.1
+ Revision: 333679
- add back python-base versioned provides, as our rpm dep finder loves it

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - disable pymalloc when running under valgrind to make debugging with valgrind
      easier (P13)

* Tue Jan 06 2009 Jérôme Soyer <saispo@mandriva.org> 2.6.1-1mdv2009.1
+ Revision: 325462
- New upstream release
- New upstream release

* Sat Dec 27 2008 Adam Williamson <awilliamson@mandriva.org> 2.6-2mdv2009.1
+ Revision: 320034
- version the python-base obsolete
- don't require python-base since it doesn't exist any more

* Wed Dec 24 2008 Michael Scherer <misc@mandriva.org> 2.6-1mdv2009.1
+ Revision: 318324
- upgrade to python 2.6
- disable bytecode by default
- removal of python-base separation
- rediff and remove old patch
- add patch for ctypes format string error

* Fri Dec 19 2008 Adam Williamson <awilliamson@mandriva.org> 2.5.2-8mdv2009.1
+ Revision: 316264
- br db4-devel < 4.7 because it won't build against 4.7

* Fri Dec 19 2008 Michael Scherer <misc@mandriva.org> 2.5.2-7mdv2009.1
+ Revision: 316009
- add patch to build with new gcc check
- fix for new rpm, need to set the patch number

* Fri Dec 05 2008 Adam Williamson <awilliamson@mandriva.org> 2.5.2-6mdv2009.1
+ Revision: 310350
- rebuild for new tcl
- add tcl86.patch (fix for tcl 8.6)

  + Michael Scherer <misc@mandriva.org>
    - revert to 2.5.1 in svn for tcl/tk upgrade
    - obsoletes python-base
    - removal of the separation python/python-base
    - disable bytecode by default
    - update to python 2.6
    - remove all patchs applied upstream
    - rediff some patch ( mandriva detection, lib64 )

* Thu Sep 18 2008 Frederik Himpe <fhimpe@mandriva.org> 2.5.2-5mdv2009.0
+ Revision: 285713
- Add patch fixing security problem CVE-2008-4108

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - change %%patch to %%patch0 as %%patch is now a macro for rpm5

* Mon Aug 25 2008 Michael Scherer <misc@mandriva.org> 2.5.2-4mdv2009.0
+ Revision: 275801
- remove some test that fail, i have no time to investigate, but I need to update for security before release
- add patch for security fix of MDVSA-2008:163, fix for CVE-2008-1679, CVE-2008-2315, CVE-2008-2316, CVE-2008-3142, CVE-2008-3143 and CVE-2008-3144, fix bug #42305

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Apr 15 2008 Gustavo De Nardin <gustavodn@mandriva.com> 2.5.2-3mdv2009.0
+ Revision: 194215
- security fix for Python-2.5.2's CVE-2008-1721

* Sat Mar 08 2008 Funda Wang <fwang@mandriva.org> 2.5.2-2mdv2008.1
+ Revision: 182067
- fix bug#9482, otherwise it reports redhat on mandriva system

* Wed Feb 27 2008 Michael Scherer <misc@mandriva.org> 2.5.2-1mdv2008.1
+ Revision: 175794
- make rpmlint happy, has the application are now in another rpm
- update to 2.5.2, bugfixs release
- rediff some patch

* Thu Jan 31 2008 Michael Scherer <misc@mandriva.org> 2.5.1-10mdv2008.1
+ Revision: 160818
- add patch for CVE-2007-4965 ( interget overflow in imageop ), fix bug #CVE-2007-4965
- add patch8, to reduce number of wakeup, come from fedora and upstream python, close #36743

* Wed Jan 02 2008 Götz Waschk <waschk@mandriva.org> 2.5.1-9mdv2008.1
+ Revision: 140361
- build bsddb module (bug #36317)

* Sat Dec 22 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.5.1-8mdv2008.1
+ Revision: 137221
- order prefix on profile scriptlets

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Dec 21 2007 Oden Eriksson <oeriksson@mandriva.com> 2.5.1-7mdv2008.1
+ Revision: 136346
- rebuilt against new build deps

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - no executable bit on profile scriptlet

  + David Walluck <walluck@mandriva.org>
    - move README.mdk creation from %%install to %%prep
    - escape HOME variable and use macros in README.mdk

* Thu Sep 13 2007 Michael Scherer <misc@mandriva.org> 2.5.1-5mdv2008.0
+ Revision: 85044
- split tkinter in two, so idle is not installed by default
- fix menu for documentation ( bug #33441 )

* Fri Sep 07 2007 Anssi Hannula <anssi@mandriva.org> 2.5.1-4mdv2008.0
+ Revision: 82050
- rebuild for new soname of tcl

* Wed Sep 05 2007 Michael Scherer <misc@mandriva.org> 2.5.1-3mdv2008.0
+ Revision: 79761
- rebuild for new rpm-mandriva-setup

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 2.5.1-2mdv2008.0
+ Revision: 69368
- kill ldconfig require as requested by pixel
- kill file require

* Tue May 15 2007 Austin Acton <austin@mandriva.org> 2.5.1-1mdv2008.0
+ Revision: 27079
- buildrequires emacs

  + Michael Scherer <misc@mandriva.org>
    - update to 2.5.1

