%define		_modname	crack
%define		_status		stable

Summary:	%{_modname} - checks if password is vulnerable to dictionary attacks
Summary(pl):	%{_modname} - sprawdzanie czy has³o jest podatne na ataki s³ownikowe
Name:		php-pecl-%{_modname}
Version:	0.1
Release:	1
License:	Artistic
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	2c0dc4d436904838cc6aba41a3ca7dea
URL:		http://pecl.php.net/package/crack/
BuildRequires:	libtool
BuildRequires:	php-devel >= 3:5.0.0
Requires:	php-common >= 3:5.0.0
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
This package provides an interface to the cracklib (libcrack)
libraries that come standard on most unix-like distributions. This
allows you to check passwords against dictionaries of words to ensure
some minimal level of password security.

In PECL status of this extension is: %{_status}.

%description -l pl
Ten pakiet dostarcza interfejsu do bibliotek cracklib (libcrack),
dostarczanych z wiêkszo¶ci± dystrybucji uniksowo-podobnych. Pozwala to
na porównanie hase³ wzglêdem s³owników celem zapewnienia minimalnego
poziomu bezpieczeñstwa.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php-cgi.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php-cgi.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,EXPERIMENTAL}
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
