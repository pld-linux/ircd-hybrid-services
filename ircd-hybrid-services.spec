# TODO:
# - patch the config files for better use with PLD
# - make a trigger, that it won't work as expected
#   unless configured with irc daemon
# - test with other irc servers
#
%define		realname hybserv-bg
%define		shortname hybserv
Summary:	Services for ircd-hybrid
Summary(pl):	Us³ugi dla ircd-hybrid
Name:		ircd-hybrid-services
Version:	1.0
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/%{realname}/%{realname}-%{version}.tgz
# Source0-md5:	7b2bc42c11db685ac8152fd65faa597a
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-build.patch
URL:		http://hybserv-bg.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
Requires:	ircd-hybrid
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hybserv-bg is greatly enhanced version of the pupular hybserv IRC
services,designed to complement ircd-hybrid-7-bg; its most notable
features are HostServ, SeenServ, nickname change enforcement, dual
language help system.

%description -l pl
Hybserver-bg to wielce ulepszona wersja popularnych us³ug dla IRCa
hybserv, zaprojektowanego by dope³niæ ircd-hybrid-7-bg; jego godne
odnotowania cechy to HostServ, SeenServ, wymuszenie zmiany nicka,
dwujêzyczna pomoc.

%prep
%setup -q -n %{realname}
%patch0 -p1

%build
%configure2_13  \
	--prefix=%{_libdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT%{_libdir}/hybserv/tools \
	$RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT%{_sysconfdir}/hybserv \
	$RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT/etc/sysconfig

cd bin

install cleandb fixlevel servchk $RPM_BUILD_ROOT%{_libdir}/hybserv/tools
install encryptconf encryptdb mkpasswd $RPM_BUILD_ROOT%{_libdir}/hybserv/tools

install hybserv $RPM_BUILD_ROOT%{_sbindir}

for f in hybserv.conf logon.news motd.dcc motd.global settings.conf ; do
	install $f $RPM_BUILD_ROOT%{_libdir}/hybserv
	ln -s %{_libdir}/hybserv/$f $RPM_BUILD_ROOT%{_sysconfdir}/hybserv/$f
done

cd -

rm -rf `find help -type d -name *CVS*`
cp -r help $RPM_BUILD_ROOT%{_libdir}/hybserv

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/hybserv
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/hybserv

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING KNOWNBUGS README RELEASENOTES-1.8.0 TODO
%attr(660,root,root) %config(noreplace) %verify(not md5 mtime size) %{_libdir}/hybserv/hybserv.conf
%attr(660,root,root) %config(noreplace) %verify(not md5 mtime size) %{_libdir}/hybserv/logon.news
%attr(660,root,root) %config(noreplace) %verify(not md5 mtime size) %{_libdir}/hybserv/motd.dcc
%attr(660,root,root) %config(noreplace) %verify(not md5 mtime size) %{_libdir}/hybserv/motd.global
%attr(660,root,root) %config(noreplace) %verify(not md5 mtime size) %{_libdir}/hybserv/settings.conf
%attr(755,root,root) %{_libdir}/hybserv/tools/*
%{_libdir}/hybserv/help/*
%attr(754,root,root) %{_sbindir}/*
%{_sysconfdir}/hybserv/*
%attr(754,root,root) /etc/rc.d/init.d/%{shortname}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{shortname}
