Summary: The GNU core utilities: a set of tools commonly used in shell scripts
Name:    coreutils
Version: 4.5.3
Release: 19.0.1
License: GPL
Group:   System Environment/Base
Url:     ftp://alpha.gnu.org/gnu/coreutils/

Source0: ftp://prep.ai.mit.edu/pub/gnu/%name/%name-%version.tar.bz2
Source101:	DIR_COLORS
Source102:	DIR_COLORS.xterm
Source103:	readlink.c
Source104:	readlink.1
Source105:  colorls.sh
Source106:  colorls.csh
Source200:  su.pamd
Source201:  help2man

# textutils
Source501:	textutils-2.0-po-update.tar.bz2
Source510:	textutils-2.0-chinese-locales.tar.bz2

Patch0:		coreutils-4.5.2-lug.patch

# fileutils
Patch101: fileutils-4.0-spacedir.patch
Patch102: fileutils-4.0s-sparc.patch
Patch103: coreutils-4.5.2-trunc.patch
Patch105: coreutils-4.5.2-C.patch
Patch107: fileutils-4.1.10-timestyle.patch
Patch108: fileutils-4.1.5-afs.patch
Patch111: coreutils-4.5.2-dumbterm.patch
Patch112: fileutils-4.0u-glibc22.patch
Patch113: coreutils-4.5.2-nolibrt.patch
Patch114: fileutils-4.1-restorecolor.patch
Patch115: fileutils-4.1.1-FBoptions.patch
Patch1155: fileutils-4.1-force-option--override--interactive-option.patch
Patch116: fileutils-4.1-dircolors_c.patch
Patch117: fileutils-4.1-ls_c.patch
Patch118: fileutils-4.1-ls_h.patch
Patch152: fileutils-4.1.8-touch_errno.patch
Patch153: fileutils-4.1.10-utmp.patch
Patch180: coreutils-4.5.3-fr-fix.patch 
Patch181: coreutils-4.5.3-samefile.patch
Patch182: coreutils-4.5.3-acl.patch
Patch183: coreutils-4.5.3-aclcompile.patch
Patch184: coreutils-4.5.3-danglinglink.patch
Patch185: coreutils-4.5.3-errno.patch
Patch186: coreutils-4.5.3-LC_TIME.patch
Patch187: coreutils-4.5.3-prompt.patch
Patch188: coreutils-4.5.3-suidfail.patch
Patch189: coreutils-4.5.3-stoneage.patch
Patch190: coreutils-4.5.3-overwrite.patch

# textutils
Patch500: textutils-2.0.17-mem.patch
Patch502: textutils-2.0.21-man.patch

# sh-utils
Patch702: sh-utils-2.0-utmp.patch
Patch703: sh-utils-2.0.11-dateman.patch
Patch704: sh-utils-1.16-paths.patch
# RMS will never accept the PAM patch because it removes his historical
# rant about Twenex and the wheel group, so we'll continue to maintain
# it here indefinitely.
Patch706: coreutils-4.5.2-pam.patch
Patch710: sh-utils-2.0-rfc822.patch
Patch711: coreutils-4.5.3-hname.patch
Patch712: coreutils-4.5.3-chdir.patch
Patch713: coreutils-4.5.3-langinfo.patch
Patch714: coreutils-4.5.3-printf-ll.patch
Patch715: coreutils-4.5.3-sysinfo.patch
Patch716: coreutils-4.5.3-nogetline.patch
Patch717: coreutils-4.5.3-preserve.patch

# (sb) lin18nux/lsb compliance
Patch800: coreutils-4.5.3-i18n.patch

# Think the test suite failure is a bug..
Patch900: coreutils-4.5.3-test-bugs.patch
Patch901: coreutils-4.5.3-signal.patch
Patch902: coreutils-4.5.3-regex.patch
Patch903: coreutils-4.5.3-manpage.patch
Patch904: coreutils-lsw.patch


BuildRoot: %_tmppath/%{name}-root
BuildRequires:	gettext libtermcap-devel pam-devel texinfo 
Prereq:		/sbin/install-info
Requires:   pam >= 0.66-12
Prereq: grep, findutils

# Require a C library that doesn't put LC_TIME files in our way.
Conflicts: glibc < 2.2

Provides:	fileutils = %version, sh-utils = %version, stat, textutils = %version
Obsoletes:	fileutils sh-utils stat textutils

# readlink(1) moved here from tetex.
Conflicts:  tetex < 1.0.7-65

%description
These are the GNU core utilities.  This package is the combination of
the old GNU fileutils, sh-utils, and textutils packages.

%prep
%setup -q

%patch0 -p1
mv po/{lg,lug}.po

# fileutils
%patch101 -p1 -b .space
%patch102 -p1 -b .sparc
%patch103 -p0 -b .trunc
%patch105 -p0 -b .Coption
%patch107 -p1 -b .timestyle
%patch108 -p1 -b .afs
%patch111 -p0 -b .dumbterm
%patch112 -p1 -b .glibc22
%patch113 -p1 -b .nolibrt
%patch114 -p1 -b .restore
%patch115 -p1 -b .FBopts
%patch1155 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch152 -p1
%patch153 -p1
%patch180 -p1 -b .frfix
%patch181 -p1 -b .samefile
%patch182 -p1 -b .acl
%patch183 -p1 -b .aclcompile
%patch184 -p1 -b .danglinglink
%patch185 -p1 -b .errno
%patch186 -p1 -b .LC_TIME
%patch187 -p1 -b .prompt
%patch188 -p1 -b .suidfail
%patch189 -p1 -b .stoneage
%patch190 -p1 -b .overwrite

# textutils
%patch500 -p1
# patch in new ALL_LINGUAS
%patch502 -p1

# sh-utils
%patch702 -p1 -b .utmp
%patch703 -p1 -b .dateman
%patch704 -p1 -b .paths
%patch706 -p1 -b .pam
%patch710 -p1 -b .rfc822
%patch711 -p1 -b .hname
%patch712 -p1 -b .chdir
%patch713 -p1 -b .langinfo
%patch714 -p1 -b .printf-ll
%patch715 -p1 -b .sysinfo
%patch716 -p1 -b .nogetline
%patch717 -p1 -b .preserve

# li18nux/lsb
%patch800 -p1 -b .i18n

# Coreutils
%patch900 -p1 -b .test-bugs
%patch901 -p1 -b .signal
%patch902 -p1 -b .regex
%patch903 -p1 -b .manpage
%patch904 -p1 -b .lsw

%build
%{expand:%%global optflags %{optflags} -D_GNU_SOURCE=1}
touch aclocal.m4 configure config.hin Makefile.in */Makefile.in */*/Makefile.in
cp %SOURCE201 man/help2man
chmod +x man/help2man
HELP2MAN=$(pwd)/man/help2man
export HELP2MAN
%configure --enable-largefile --enable-pam || :
make all CPPFLAGS="-DUSE_PAM" su_LDFLAGS="-lpam -lpam_misc"

gcc -o readlink $RPM_OPT_FLAGS %SOURCE103

unset LINGUAS || :
for i in AUTOMAKE ACLOCAL;do perl -pi -e "s%^$i = .*$%$i = /bin/true%g" Makefile.in;done
%configure
[[ -f ChangeLog && -f ChangeLog.bz2  ]] || bzip2 -9f ChangeLog

make

# Run the test suite.
make check || :

# XXX docs should say /var/run/[uw]tmp not /etc/[uw]tmp
perl -pi -e 's,/etc/utmp,/var/run/utmp,g;s,/etc/wtmp,/var/run/wtmp,g' doc/coreutils.texi


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# man pages are not installed with make install
make mandir=$RPM_BUILD_ROOT%{_mandir} install-man

# fix japanese catalog file
if [ -d $RPM_BUILD_ROOT/%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES ]; then
   mkdir -p $RPM_BUILD_ROOT/%{_datadir}/locale/ja/LC_MESSAGES
   mv $RPM_BUILD_ROOT/%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES/*mo \
		$RPM_BUILD_ROOT/%{_datadir}/locale/ja/LC_MESSAGES
   rm -rf $RPM_BUILD_ROOT/%{_datadir}/locale/ja_JP.EUC
fi

# let be compatible with old fileutils, sh-utils and textutils packages :
mkdir -p $RPM_BUILD_ROOT{/bin,%_bindir,%_sbindir,%_sysconfdir/pam.d}
for f in basename cat chgrp chmod chown cp cut date dd df echo env false link ln ls mkdir mknod mv nice pwd rm rmdir sleep sort stty sync touch true uname unlink
do
	mv $RPM_BUILD_ROOT/{%_bindir,bin}/$f 
done

# chroot was in /usr/sbin :
mv $RPM_BUILD_ROOT/{%_bindir,%_sbindir}/chroot
# {cat,sort,cut} were previously moved from bin to /usr/bin and linked into 
for i in env cut; do ln -sf ../../bin/$i $RPM_BUILD_ROOT/usr/bin; done

mkdir -p $RPM_BUILD_ROOT/etc/profile.d
install -c -m644 %SOURCE101 $RPM_BUILD_ROOT/etc/
install -c -m644 %SOURCE102 $RPM_BUILD_ROOT/etc/
install -c -m755 %SOURCE105 $RPM_BUILD_ROOT/etc/profile.d
install -c -m755 %SOURCE106 $RPM_BUILD_ROOT/etc/profile.d

# readlink
install readlink $RPM_BUILD_ROOT%{_bindir}
install -m644 %SOURCE104 $RPM_BUILD_ROOT%_mandir/man1

# su
install -m 4755 src/su $RPM_BUILD_ROOT/bin

# These come from util-linux and/or procps.
for i in hostname uptime ; do
	rm -f $RPM_BUILD_ROOT{%_bindir/$i,%_mandir/man1/${i}.1}
done

install -m 644 %SOURCE200 $RPM_BUILD_ROOT%_sysconfdir/pam.d/su

ln -sf test $RPM_BUILD_ROOT%_bindir/[

bzip2 -f9 old/*/C* || :

%find_lang %name

# (sb) Deal with Installed (but unpackaged) file(s) found
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Remove these old glibc files on upgrade (bug #84090).
for file in $(find /usr/share/locale -type f -name LC_TIME); do
	[ -x /bin/rm ] && /bin/rm -f "$file"
done

# We must desinstall theses info files since they're merged in
# coreutils.info. else their postun'll be runned too last
# and install-info'll faill badly because of doubles
for file in sh-utils.info textutils.info fileutils.info; do
	if [ -f /usr/share/info/$file.bz2 ]; then
		/sbin/install-info /usr/share/info/$file.bz2 --dir=/usr/share/info/dir --remove &> /dev/null
	fi
done

%preun
if [ $1 = 0 ]; then
    [ -f %{_infodir}/%{name}.info.gz ] && \
      /sbin/install-info --delete %{_infodir}/%{name}.info.gz \
	%{_infodir}/dir || :
fi

%post
/bin/grep -v '(sh-utils)\|(fileutils)\|(textutils)' %{_infodir}/dir > \
  %{_infodir}/dir.rpmmodify || exit 0
    /bin/mv -f %{_infodir}/dir.rpmmodify %{_infodir}/dir
[ -f %{_infodir}/%{name}.info.gz ] && \
  /sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :

%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/DIR_COLORS*
%config(noreplace) %{_sysconfdir}/profile.d/*
%config(noreplace) /etc/pam.d/su
%doc ABOUT-NLS ChangeLog.bz2 NEWS README THANKS TODO old/*
/bin/*
%_bindir/*
%_infodir/coreutils*
%_mandir/man*/*
%_sbindir/chroot

%changelog
* Wed Oct 22 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-19.0.1
- Apply Paul Eggart's patches for 'ls -w'.

* Tue Feb 18 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-19
- Ship readlink(1) (bug #84200).

* Thu Feb 13 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-18
- Deal with glibc < 2.2 in %%pre scriplet (bug #84090).

* Wed Feb 12 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-16
- Require glibc >= 2.2 (bug #84090).

* Tue Feb 11 2003 Bill Nottingham <notting@redhat.com> 4.5.3-15
- fix group (#84095)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 4.5.3-14
- rebuilt

* Thu Jan 16 2003 Tim Waugh <twaugh@redhat.com>
- Fix rm(1) man page.

* Thu Jan 16 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-13
- Fix re_compile_pattern check.
- Fix su hang (bug #81653).

* Tue Jan 14 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-11
- Fix memory size calculation.

* Tue Dec 17 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-10
- Fix mv error message (bug #79809).

* Mon Dec 16 2002 Tim Powers <timp@redhat.com> 4.5.3-9
- added PreReq on grep

* Fri Dec 13 2002 Tim Waugh <twaugh@redhat.com>
- Fix cp --preserve with multiple arguments.

* Thu Dec 12 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-8
- Turn on colorls for screen (bug #78816).

* Mon Dec  9 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-7
- Fix mv (bug #79283).
- Add patch27 (nogetline).

* Sun Dec  1 2002 Tim Powers <timp@redhat.com> 4.5.3-6
- use the su.pamd from sh-utils since it works properly with multilib systems

* Fri Nov 29 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-5
- Fix test suite quoting problems.

* Fri Nov 29 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-4
- Fix scriplets.
- Fix i18n patch so it doesn't break uniq.
- Fix several other patches to either make the test suite pass or
  not run the relevant tests.
- Run 'make check'.
- Fix file list.

* Thu Nov 28 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-3
- Adapted for Red Hat Linux.
- Self-host for help2man.
- Don't ship readlink just yet (maybe later).
- Merge patches from fileutils and sh-utils (textutils ones are already
  merged it seems).
- Keep the binaries where the used to be (in particular, id and stat).

* Sun Nov 17 2002 Stew Benedict <sbenedict@mandrakesoft.com> 4.5.3-2mdk
- LI18NUX/LSB compliance (patch800)
- Installed (but unpackaged) file(s) - /usr/share/info/dir

* Thu Oct 31 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.3-1mdk
- new release
- rediff patch 180
- merge patch 150 into 180

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-6mdk
- move su back to /bin

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-5mdk
- patch 0 : lg locale is illegal and must be renamed lug (pablo)

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-4mdk
- fix conflict with procps

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-3mdk
- patch 105 : fix install -s

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-2mdk
- fix build
- don't chmode two times su
- build with large file support
- fix description
- various spec cleanups
- fix chroot installation
- fix missing /bin/env
- add old fileutils, sh-utils & textutils ChangeLogs

* Fri Oct 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-1mdk
- initial release (merge fileutils, sh-utils & textutils)
- obsoletes/provides: sh-utils/fileutils/textutils
- fileutils stuff go in 1xx range
- sh-utils stuff go in 7xx range
- textutils stuff go in 5xx range
- drop obsoletes patches 1, 2, 10 (somes files're gone but we didn't ship
  most of them)
- rediff patches 103, 105, 111, 113, 180, 706
- temporary disable patch 3 & 4
- fix fileutils url
