Summary: The GNU core utilities: a set of tools commonly used in shell scripts
Name:    coreutils
Version: 5.97
Release: 13
License: GPL
Group:   System Environment/Base
Url:     http://www.gnu.org/software/coreutils/
BuildRequires: libselinux-devel >= 1.25.6-1
BuildRequires: libacl-devel
Requires: libselinux >= 1.25.6-1

Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
Source101:	DIR_COLORS
Source102:	DIR_COLORS.xterm
Source105:  colorls.sh
Source106:  colorls.csh
Source200:  su.pamd
Source201:  runuser.pamd
Source202:  su-l.pamd
Source203:  runuser-l.pamd

# From upstream
Patch1: coreutils-sort-compatibility.patch
Patch2: coreutils-rename.patch
Patch10: coreutils-newhashes.patch

# Our patches
Patch100: coreutils-chgrp.patch
Patch107: fileutils-4.1.10-timestyle.patch
Patch182: coreutils-acl.patch
Patch183: coreutils-df-cifs.patch

# sh-utils
Patch703: sh-utils-2.0.11-dateman.patch
Patch704: sh-utils-1.16-paths.patch
# RMS will never accept the PAM patch because it removes his historical
# rant about Twenex and the wheel group, so we'll continue to maintain
# it here indefinitely.
Patch706: coreutils-pam.patch
Patch713: coreutils-4.5.3-langinfo.patch
Patch715: coreutils-4.5.3-sysinfo.patch

# (sb) lin18nux/lsb compliance
Patch800: coreutils-i18n.patch

Patch900: coreutils-setsid.patch
Patch907: coreutils-5.2.1-runuser.patch
Patch908: coreutils-getgrouplist.patch
Patch912: coreutils-overflow.patch
Patch913: coreutils-afs.patch
Patch914: coreutils-autoconf.patch
Patch915: coreutils-split-pam.patch

#SELINUX Patch
Patch950: coreutils-selinux.patch

BuildRoot: %_tmppath/%{name}-root
BuildRequires:	gettext libtermcap-devel bison
%{?!nopam:BuildRequires: pam-devel}
BuildRequires:	texinfo >= 4.3
BuildRequires: autoconf >= 2.58, automake >= 1.8
Prereq:		/sbin/install-info
%{?!nopam:Requires: pam >= 0.66-12}
Prereq: grep, findutils

# Require a C library that doesn't put LC_TIME files in our way.
Conflicts: glibc < 2.2

Provides:	fileutils = %version, sh-utils = %version, stat, textutils = %version
Obsoletes:	fileutils sh-utils stat textutils

# readlink(1) moved here from tetex.
Conflicts:  tetex < 1.0.7-66

%description
These are the GNU core utilities.  This package is the combination of
the old GNU fileutils, sh-utils, and textutils packages.

%prep
%setup -q

# From upstream
%patch1 -p1 -b .sort-compatibility
%patch2 -p1 -b .rename
%patch10 -p1 -b .newhashes

# Our patches
%patch100 -p1 -b .chgrp
%patch107 -p1 -b .timestyle
%patch182 -p1 -b .acl
%patch183 -p1 -b .df-cifs

# sh-utils
%patch703 -p1 -b .dateman
%patch704 -p1 -b .paths
%patch706 -p1 -b .pam
%patch713 -p1 -b .langinfo
%patch715 -p1 -b .sysinfo

# li18nux/lsb
%patch800 -p1 -b .i18n

# Coreutils
%patch900 -p1 -b .setsid
%patch907 -p1 -b .runuser
%patch908 -p1 -b .getgrouplist
%patch912 -p1 -b .overflow
%patch913 -p1 -b .afs
%patch914 -p1 -b .autoconf
%patch915 -p1 -b .splitl

#SELinux
%patch950 -p1 -b .selinux

# Don't run basic-1 test, since it breaks when run in the background
# (bug #102033).
perl -pi -e 's/basic-1//g' tests/stty/Makefile*

chmod a+x tests/sort/sort-mb-tests

%build
%ifarch s390 s390x
# Build at -O1 for the moment (bug #196369).
export CFLAGS="$RPM_OPT_FLAGS -fPIC -O1"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpic"
%endif
%{expand:%%global optflags %{optflags} -D_GNU_SOURCE=1}
touch aclocal.m4 configure config.hin Makefile.in */Makefile.in */*/Makefile.in
aclocal -I m4
autoconf --force
automake --copy --add-missing
%configure --enable-largefile --with-afs %{?!nopam:--enable-pam} \
	--enable-selinux \
	DEFAULT_POSIX2_VERSION=200112 alternative=199209 || :
make all %{?_smp_mflags} \
	%{?!nopam:CPPFLAGS="-DUSE_PAM"} \
	su_LDFLAGS="-pie %{?!nopam:-lpam -lpam_misc}"

[[ -f ChangeLog && -f ChangeLog.bz2  ]] || bzip2 -9f ChangeLog

# Run the test suite.
make check

# XXX docs should say /var/run/[uw]tmp not /etc/[uw]tmp
perl -pi -e 's,/etc/utmp,/var/run/utmp,g;s,/etc/wtmp,/var/run/wtmp,g' doc/coreutils.texi

pushd po
make pl.gmo
popd

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
mkdir -p $RPM_BUILD_ROOT{/bin,%_bindir,%_sbindir,/sbin}
%{?!nopam:mkdir -p $RPM_BUILD_ROOT%_sysconfdir/pam.d}
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

# su
install -m 4755 src/su $RPM_BUILD_ROOT/bin
install -m 755 src/runuser $RPM_BUILD_ROOT/sbin

# These come from util-linux and/or procps.
for i in hostname uptime kill ; do
	rm -f $RPM_BUILD_ROOT{%_bindir/$i,%_mandir/man1/$i.1}
done

%{?!nopam:install -m 644 %SOURCE200 $RPM_BUILD_ROOT%_sysconfdir/pam.d/su}
%{?!nopam:install -m 644 %SOURCE202 $RPM_BUILD_ROOT%_sysconfdir/pam.d/su-l}
%{?!nopam:install -m 644 %SOURCE201 $RPM_BUILD_ROOT%_sysconfdir/pam.d/runuser}
%{?!nopam:install -m 644 %SOURCE203 $RPM_BUILD_ROOT%_sysconfdir/pam.d/runuser-l}

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
%dir %{_datadir}/locale/*/LC_TIME
%config(noreplace) %{_sysconfdir}/DIR_COLORS*
%config(noreplace) %{_sysconfdir}/profile.d/*
%{?!nopam:%config(noreplace) /etc/pam.d/su}
%{?!nopam:%config(noreplace) /etc/pam.d/su-l}
%{?!nopam:%config(noreplace) /etc/pam.d/runuser}
%{?!nopam:%config(noreplace) /etc/pam.d/runuser-l}
%doc ABOUT-NLS ChangeLog.bz2 NEWS README THANKS TODO old/*
/bin/basename
/bin/cat
/bin/chgrp
/bin/chmod
/bin/chown
/bin/cp
/bin/cut
/bin/date
/bin/dd
/bin/df
/bin/echo
/bin/env
/bin/false
/bin/link
/bin/ln
/bin/ls
/bin/mkdir
/bin/mknod
/bin/mv
/bin/nice
/bin/pwd
/bin/rm
/bin/rmdir
/bin/sleep
/bin/sort
/bin/stty
%attr(4755,root,root) /bin/su
/bin/sync
/bin/touch
/bin/true
/bin/uname
/bin/unlink
%_bindir/*
%_infodir/coreutils*
%_mandir/man*/*
%_sbindir/chroot
/sbin/runuser

%changelog
* Tue Oct 17 2006 Tim Waugh <twaugh@redhat.com> 5.97-13
- Own LC_TIME locale directories (bug #210751).

* Wed Oct  4 2006 Tim Waugh <twaugh@redhat.com> 5.97-12
- Fixed 'cp -Z' when destination exists, again (bug #189967).

* Thu Sep 28 2006 Tim Waugh <twaugh@redhat.com> 5.97-11
- Back-ported rename patch (bug #205744).

* Tue Sep 12 2006 Tim Waugh <twaugh@redhat.com> 5.97-10
- Ignore 'cifs' filesystems for 'df -l' (bug #183703).
- Include -g/-G in runuser man page (part of bug #199344).
- Corrected runuser man page (bug #200620).

* Thu Aug 24 2006 Tim Waugh <twaugh@redhat.com> 5.97-9
- Fixed warnings in pam, i18n, sysinfo, selinux and acl patches (bug #203166).

* Wed Aug 23 2006 Tim Waugh <twaugh@redhat.com> 5.97-8
- Don't chdir until after PAM bits in su (bug #197659).

* Tue Aug 15 2006 Tim Waugh <twaugh@redhat.com> 5.97-7
- Fixed 'sort -b' multibyte problem (bug #199986).

* Fri Jul 21 2006 Tim Waugh <twaugh@redhat.com> 5.97-6
- Added runuser '-g' and '-G' options (bug #199344).
- Added su '--session-command' option (bug #199066).

* Tue Jul 18 2006 Tomas Mraz <tmraz@redhat.com> 5.97-5
- 'include' su and runuser scripts in su-l and runuser-l scripts

* Thu Jul 13 2006 David Howells <dhowells@redhat.com> 5.97-4
- split the PAM scripts for "su -l"/"runuser -l" from that of normal "su" and
  "runuser" (#198639)
- add keyinit instructions to PAM scripts

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.97-3.1
- rebuild

* Tue Jul 11 2006 Tomas Mraz <tmraz@redhat.com> 5.97-3
- allow root to su to expired user (#152420)

* Thu Jun 29 2006 Tim Waugh <twaugh@redhat.com> 5.97-2
- Allow 'sort +1 -2' (patch from upstream).

* Sun Jun 25 2006 Tim Waugh <twaugh@redhat.com> 5.97-1
- 5.97.  No longer need tempname or tee patches, or pl translation.

* Sun Jun 25 2006 Tim Waugh <twaugh@redhat.com> 5.96-4
- Include new hashes (bug #196369).  Patch from upstream.
- Build at -O1 on s390 for the moment (bug #196369).

* Fri Jun  9 2006 Tim Waugh <twaugh@redhat.com>
- Fix large file support for temporary files.

* Mon Jun  5 2006 Tim Waugh <twaugh@redhat.com> 5.96-3
- Fixed Polish translation.

* Mon May 22 2006 Tim Waugh <twaugh@redhat.com> 5.96-2
- 5.96.  No longer need proc patch.

* Fri May 19 2006 Tim Waugh <twaugh@redhat.com>
- Fixed pr properly in multibyte locales (bug #192381).

* Tue May 16 2006 Tim Waugh <twaugh@redhat.com> 5.95-3
- Upstream patch to fix cp -p when proc is not mounted (bug #190601).
- BuildRequires libacl-devel.

* Mon May 15 2006 Tim Waugh <twaugh@redhat.com>
- Fixed pr in multibyte locales (bug #189663).

* Mon May 15 2006 Tim Waugh <twaugh@redhat.com> 5.95-2
- 5.95.

* Wed Apr 26 2006 Tim Waugh <twaugh@redhat.com> 5.94-4
- Avoid redeclared 'tee' function.
- Fix 'cp -Z' when the destination exists (bug #189967).

* Thu Apr 20 2006 Tim Waugh <twaugh@redhat.com> 5.94-3
- Make 'ls -Z' output more consistent with other output formats.

* Fri Mar 24 2006 Tim Waugh <twaugh@redhat.com> 5.94-2
- 5.94.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.93-7.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.93-7.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Tim Waugh <twaugh@redhat.com>
- Fixed chcon(1) bug reporting address (bug #178523).

* Thu Jan  5 2006 Tim Waugh <twaugh@redhat.com> 5.93-7
- Don't suppress chown/chgrp errors in install(1) (bug #176708).

* Mon Jan  2 2006 Dan Walsh <dwalsh@redhat.com> 5.93-6
- Remove pam_selinux.so from su.pamd, not needed for targeted and Strict/MLS 
  will have to newrole before using.

* Fri Dec 23 2005 Tim Waugh <twaugh@redhat.com> 5.93-5
- Fix "sort -n" (bug #176468).

* Fri Dec 16 2005 Tim Waugh <twaugh@redhat.com>
- Explicitly set default POSIX2 version during configure stage.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Tim Waugh <twaugh@redhat.com>
- Parametrize SELinux (bug #174067).
- Fix runuser.pamd (bug #173807).

* Thu Nov 25 2005 Tim Waugh <twaugh@redhat.com> 5.93-4
- Rebuild to pick up new glibc *at functions.
- Apply runuser PAM patch from bug #173807.  Ship runuser PAM file.

* Tue Nov 14 2005 Dan Walsh <dwalsh@redhat.com> 5.93-3
- Remove multiple from su.pamd

* Mon Nov 14 2005 Tim Waugh <twaugh@redhat.com> 5.93-2
- Call setsid() in su under some circumstances (bug #173008).
- Prevent runuser operating when setuid (bug #173113).

* Tue Nov  8 2005 Tim Waugh <twaugh@redhat.com> 5.93-1
- 5.93.
- No longer need alt-md5sum-binary, dircolors, mkdir, mkdir2 or tac patches.

* Fri Oct 28 2005 Tim Waugh <twaugh@redhat.com> 5.92-1
- Finished porting i18n patch to sort.c.
- Fixed for sort-mb-tests (avoid +n syntax).

* Fri Oct 28 2005 Tim Waugh <twaugh@redhat.com> 5.92-0.2
- Fix chgrp basic test.
- Include md5sum patch from ALT.

* Mon Oct 24 2005 Tim Waugh <twaugh@redhat.com> 5.92-0.1
- 5.92.
- No longer need afs, dircolors, utmp, gcc4, brokentest, dateseconds,
  chown, rmaccess, copy, stale-utmp, no-sign-extend, fchown patches.
- Updated acl, dateman, pam, langinfo, i18n, getgrouplist, selinux patches.
- Dropped printf-ll, allow_old_options, jday, zh_CN patches.
- NOTE: i18n patch not ported for sort(1) yet.

* Fri Sep 30 2005 Tomas Mraz <tmraz@redhat.com> - 5.2.1-56
- use include instead of pam_stack in pam config

* Fri Sep 9 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-55
- Reverse change to use raw functions

* Thu Sep  8 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-54
- Explicit setuid bit for /bin/su in file manifest (bug #167745).

* Tue Sep 6 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-53
- Allow id to run even when SELinux security context can not be run
- Change chcon to use raw functions.

* Thu Jun 28 2005 Tim Waugh <twaugh@redhat.com>
- Corrected comments in DIR_COLORS.xterm (bug #161711).

* Wed Jun 22 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-52
- Fixed stale-utmp patch so that 'who -r' and 'who -b' work
  again (bug #161264).

* Fri Jun 17 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-51
- Use upstream hostid fix.

* Thu Jun 16 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-50
- Don't display the sign-extended part of the host id (bug #160078).

* Tue May 31 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-49
- Eliminate bogus "can not preserve context" message when moving files.

* Wed May 25 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-48
- Prevent buffer overflow in who(1) (bug #158405).

* Fri May 20 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-47
- Better error checking in the pam patch (bug #158189).

* Mon May 16 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-46
- Fix SELinux patch to better handle MLS integration

* Mon May 16 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-45
- Applied Russell Coker's selinux changes (bug #157856).

* Fri Apr  8 2005 Tim Waugh <twaugh@redhat.com>
- Fixed pam patch from Steve Grubb (bug #154946).
- Use better upstream patch for "stale utmp".

* Tue Mar 29 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-44
- Added "stale utmp" patch from upstream.

* Thu Mar 24 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-43
- Removed patch that adds -C option to install(1).

* Wed Mar 14 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-42
- Fixed pam patch.
- Fixed broken configure test.
- Fixed build with GCC 4 (bug #151045).

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-41
- Jakub Jelinek's sort -t multibyte fixes (bug #147567).

* Sat Feb  5 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-40
- Undo last change (bug #145266).

* Fri Feb  4 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-38
- Special case for ia32e in uname (bug #145266).

* Thu Jan 13 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-37
- Fixed zh_CN translation (bug #144845).  Patch from Mitrophan Chin.

* Mon Dec 28 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-36
- Fix to only setdefaultfilecon if not overridden by command line

* Mon Dec 27 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-35
- Change install to restorecon if it can

* Wed Dec 15 2004 Tim Waugh <twaugh@redhat.com>
- Fixed small bug in i18n patch.

* Mon Dec  6 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-34
- Don't set fs uid until after pam_open_session (bug #77791).

* Thu Nov 25 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-33
- Fixed colorls.csh (bug #139988).  Patch from Miloslav Trmac.

* Mon Nov  8 2004 Tim Waugh <twaugh@redhat.com>
- Updated URL (bug #138279).

* Mon Oct 25 2004 Steve Grubb <sgrubb@redhat.com> 5.2.1-32
- Handle the return code of function calls in runcon.

* Mon Oct 18 2004 Tim Waugh <twaugh@redhat.com>
- Prevent compiler warning in coreutils-i18n.patch (bug #136090).

* Tue Oct  5 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-31
- getgrouplist() patch from Ulrich Drepper.
- The selinux patch should be applied last.

* Mon Oct  4 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-30
- Mv runuser to /sbin

* Mon Oct  4 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-28
- Fix runuser man page.

* Mon Oct  4 2004 Tim Waugh <twaugh@redhat.com>
- Fixed build.

* Fri Sep 24 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-26
- Add runuser as similar to su, but only runable by root

* Fri Sep 24 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-25
- chown(1) patch from Ulrich Drepper.

* Tue Sep 14 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-24
- SELinux patch fix: don't display '(null)' if getfilecon() fails
  (bug #131196).

* Fri Aug 20 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-23
- Fixed colorls.csh quoting (bug #102412).
- Fixed another join LSB test failure (bug #121153).

* Mon Aug 16 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-22
- Fixed sort -t LSB test failure (bug #121154).
- Fixed join LSB test failure (bug #121153).

* Wed Aug 11 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-21
- Apply upstream patch to fix 'cp -a' onto multiply-linked files (bug #128874).
- SELinux patch fix: don't error out if lgetfilecon() returns ENODATA.

* Tue Aug 10 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-20
- Added 'konsole' TERM to DIR_COLORS (bug #129544).

* Wed Aug  4 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-19
- Added 'gnome' TERM to DIR_COLORS (bug #129112).
- Worked around a bash bug #129128.
- Fixed an i18n patch bug in cut (bug #129114).

* Tue Aug  3 2004 Tim Waugh <twaugh@redhat.com>
- Fixed colorls.{sh,csh} so that the l. and ll aliases are always defined
  (bug #128948).

* Tue Jul 13 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-18
- Fixed field extraction in sort (bug #127694).

* Fri Jun 25 2004 Tim Waugh <twaugh@redhat.com>
- Added 'TERM screen.linux' to DIR_COLORS (bug #78816).

* Wed Jun 23 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-17
- Move pam-xauth to after pam-selinux

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-15
- Fix ls -Z (bug #125447).

* Fri Jun  4 2004 Tim Waugh <twaugh@redhat.com>
- Build requires bison (bug #125290).

* Fri Jun  4 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-14
- Fix selinux patch causing problems with ls --format=... (bug #125238).

* Thu Jun 3 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-13
- Change su to use pam_selinux open and pam_selinux close

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-12
- Don't call access() on symlinks about to be removed (bug #124699).

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-11
- Fix ja translation (bug #124862).

* Tue May 18 2004 Jeremy Katz <katzj@redhat.com> 5.2.1-10
- rebuild

* Mon May 17 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-9
- Mention pam in the info for su (bug #122592).
- Remove wheel group rant again (bug #122886).
- Change default behaviour for chgrp/chown (bug #123263).  Patch from
  upstream.

* Mon May 17 2004 Thomas Woerner <twoerner@redhat.com> 5.2.1-8
- compiling su PIE

* Wed May 12 2004 Tim Waugh <twaugh@redhat.com>
- Build requires new versions of autoconf and automake (bug #123098).

* Tue May  4 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-7
- Fix join -t (bug #122435).

* Tue Apr 20 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-6
- Fix 'ls -Z' displaying users/groups if stat() failed (bug #121292).

* Fri Apr 9 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-5
- Add ls -LZ fix
- Fix chcon to handle "."

* Wed Mar 17 2004 Tim Waugh <twaugh@redhat.com>
- Apply upstream fix for non-zero seconds for --date="10:00 +0100".

* Tue Mar 16 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-3
- If preserve fails, report as warning unless user requires preserve

* Tue Mar 16 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-2
- Make mv default to preserve on context

* Sat Mar 13 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-1
- 5.2.1.

* Fri Mar 12 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-9
- Add '-Z' to 'ls --help' output (bug #118108).

* Fri Mar  5 2004 Tim Waugh <twaugh@redhat.com>
- Fix deref-args test case for rebuilding under SELinux (bug #117556).

* Wed Feb 25 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-8
- kill(1) offloaded to util-linux altogether.

* Tue Feb 24 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-7
- Ship the real '[', not a symlink.

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-6
- Apply Paul Eggert's chown patch (bug #116536).
- Merged chdir patch into pam patch where it belongs.

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-5
- Fixed i18n patch bug causing sort -M not to work (bug #116575).

* Sat Feb 21 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-4
- Reinstate kill binary, just not its man page (bug #116463).

* Sat Feb 21 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-3
- Updated ls-stat patch.

* Fri Feb 20 2004 Dan Walsh <dwalsh@redhat.com> 5.2.0-2
- fix chcon to ignore . and .. directories for recursing

* Fri Feb 20 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-1
- Patch ls so that failed stat() is handled gracefully (Ulrich Drepper).
- 5.2.0.

* Thu Feb 19 2004 Tim Waugh <twaugh@redhat.com>
- More AFS patch tidying.

* Wed Feb 18 2004 Dan Walsh <dwalsh@redhat.com> 5.1.3-0.2
- fix chcon to handle -h qualifier properly, eliminate potential crash 

* Wed Feb 18 2004 Tim Waugh <twaugh@redhat.com>
- Stop 'sort -g' leaking memory (i18n patch bug #115620).
- Don't ship kill, since util-linux already does.
- Tidy AFS patch.

* Mon Feb 16 2004 Tim Waugh <twaugh@redhat.com> 5.1.3-0.1
- 5.1.3.
- Patches ported forward or removed.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 5.0-40
- rebuilt

* Tue Jan  20 2004 Dan Walsh <dwalsh@redhat.com> 5.0-39
- Change /etc/pam.d/su to remove preservuser and add multiple

* Tue Jan  20 2004 Dan Walsh <dwalsh@redhat.com> 5.0-38
- Change is_selinux_enabled to is_selinux_enabled > 0

* Tue Jan  20 2004 Dan Walsh <dwalsh@redhat.com> 5.0-37
- Add pam_selinux to pam file to allow switching of roles within selinux

* Fri Jan 16 2004 Tim Waugh <twaugh@redhat.com>
- The textutils-2.0.17-mem.patch is no longer needed.

* Thu Jan 15 2004 Tim Waugh <twaugh@redhat.com> 5.0-36
- Fixed autoconf test causing builds to fail.

* Tue Dec  9 2003 Dan Walsh <dwalsh@redhat.com> 5.0-35
- Fix copying to non xattr files

* Thu Dec  4 2003 Tim Waugh <twaugh@redhat.com> 5.0-34.sel
- Fix column widths problems in ls.

* Tue Dec  2 2003 Tim Waugh <twaugh@redhat.com> 5.0-33.sel
- Speed up md5sum by disabling speed-up asm.

* Wed Nov 19 2003 Dan Walsh <dwalsh@redhat.com> 5.0-32.sel
- Try again

* Wed Nov 19 2003 Dan Walsh <dwalsh@redhat.com> 5.0-31.sel
- Fix move on non SELinux kernels

* Fri Nov 14 2003 Tim Waugh <twaugh@redhat.com> 5.0-30.sel
- Fixed useless acl dependencies (bug #106141).

* Fri Oct 24 2003 Dan Walsh <dwalsh@redhat.com> 5.0-29.sel
- Fix id -Z

* Tue Oct 21 2003 Dan Walsh <dwalsh@redhat.com> 5.0-28.sel
- Turn on SELinux
- Fix chcon error handling

* Wed Oct 15 2003 Dan Walsh <dwalsh@redhat.com> 5.0-28
- Turn off SELinux

* Mon Oct 13 2003 Dan Walsh <dwalsh@redhat.com> 5.0-27.sel
- Turn on SELinux

* Mon Oct 13 2003 Dan Walsh <dwalsh@redhat.com> 5.0-27
- Turn off SELinux

* Mon Oct 13 2003 Dan Walsh <dwalsh@redhat.com> 5.0-26.sel
- Turn on SELinux

* Sun Oct 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling without pam support

* Fri Oct 10 2003 Tim Waugh <twaugh@redhat.com> 5.0-23
- Make split(1) handle large files (bug #106700).

* Thu Oct  9 2003 Dan Walsh <dwalsh@redhat.com> 5.0-22
- Turn off SELinux

* Wed Oct  8 2003 Dan Walsh <dwalsh@redhat.com> 5.0-21.sel
- Cleanup SELinux patch

* Fri Oct  3 2003 Tim Waugh <twaugh@redhat.com> 5.0-20
- Restrict ACL support to only those programs needing it (bug #106141).
- Fix default PATH for LSB (bug #102567).

* Thu Sep 11 2003 Dan Walsh <dwalsh@redhat.com> 5.0-19
- Turn off SELinux

* Wed Sep 10 2003 Dan Walsh <dwalsh@redhat.com> 5.0-18.sel
- Turn on SELinux

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 5.0-17
- Turn off SELinux

* Tue Sep 2 2003 Dan Walsh <dwalsh@redhat.com> 5.0-16.sel
- Only call getfilecon if the user requested it.
- build with selinux

* Wed Aug 20 2003 Tim Waugh <twaugh@redhat.com> 5.0-14
- Documentation fix (bug #102697).

* Tue Aug 12 2003 Tim Waugh <twaugh@redhat.com> 5.0-13
- Made su use pam again (oops).
- Fixed another i18n bug causing sort --month-sort to fail.
- Don't run dubious stty test, since it fails when backgrounded
  (bug #102033).
- Re-enable make check.

* Fri Aug  8 2003 Tim Waugh <twaugh@redhat.com> 5.0-12
- Don't run 'make check' for this build (build environment problem).
- Another uninitialized variable in i18n (from bug #98683).

* Wed Aug 6 2003 Dan Walsh <dwalsh@redhat.com> 5.0-11
- Internationalize runcon
- Update latest chcon from NSA

* Wed Jul 30 2003 Tim Waugh <twaugh@redhat.com>
- Re-enable make check.

* Wed Jul 30 2003 Tim Waugh <twaugh@redhat.com> 5.0-9
- Don't run 'make check' for this build (build environment problem).

* Mon Jul 28 2003 Tim Waugh <twaugh@redhat.com> 5.0-8
- Actually use the ACL patch (bug #100519).

* Wed Jul 18 2003 Dan Walsh <dwalsh@redhat.com> 5.0-7
- Convert to SELinux

* Mon Jun  9 2003 Tim Waugh <twaugh@redhat.com>
- Removed samefile patch.  Now the test suite passes.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 28 2003 Tim Waugh <twaugh@redhat.com> 5.0-5
- Both kon and kterm support colours (bug #83701).
- Fix 'ls -l' alignment in zh_CN locale (bug #88346).

* Mon May 12 2003 Tim Waugh <twaugh@redhat.com> 5.0-4
- Prevent file descriptor leakage in du (bug #90563).
- Build requires recent texinfo (bug #90439).

* Wed Apr 30 2003 Tim Waugh <twaugh@redhat.com> 5.0-3
- Allow obsolete options unless POSIXLY_CORRECT is set.

* Sat Apr 12 2003 Tim Waugh <twaugh@redhat.com>
- Fold bug was introduced by i18n patch; fixed there instead.

* Fri Apr 11 2003 Matt Wilson <msw@redhat.com> 5.0-2
- fix segfault in fold (#88683)

* Sat Apr  5 2003 Tim Waugh <twaugh@redhat.com> 5.0-1
- 5.0.

* Mon Mar 24 2003 Tim Waugh <twaugh@redhat.com>
- Use _smp_mflags.

* Mon Mar 24 2003 Tim Waugh <twaugh@redhat.com> 4.5.11-2
- Remove overwrite patch.
- No longer seem to need nolibrt, errno patches.

* Thu Mar 20 2003 Tim Waugh <twaugh@redhat.com>
- No longer seem to need danglinglink, prompt, lug, touch_errno patches.

* Thu Mar 20 2003 Tim Waugh <twaugh@redhat.com> 4.5.11-1
- 4.5.11.
- Use packaged readlink.

* Wed Mar 19 2003 Tim Waugh <twaugh@redhat.com> 4.5.10-1
- 4.5.10.
- Update lug, touch_errno, acl, utmp, printf-ll, i18n, test-bugs patches.
- Drop fr_fix, LC_TIME, preserve, regex patches.

* Wed Mar 12 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-21
- Fixed another i18n patch bug (bug #82032).

* Tue Mar 11 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-20
- Fix sort(1) efficiency in multibyte encoding (bug #82032).

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
