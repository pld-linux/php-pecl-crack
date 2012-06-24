%define		_modname	crack
%define		_status		beta
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
Summary:	%{_modname} - checks if password is vulnerable to dictionary attacks
Summary(pl):	%{_modname} - sprawdzanie czy has�o jest podatne na ataki s�ownikowe
Name:		php-pecl-%{_modname}
Version:	0.3
Release:	4
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	43a3dc3e4f2d16bf1e30ccea0d384183
Patch0:		%{name}-m4_fixes.patch
URL:		http://pecl.php.net/package/crack/
BuildRequires:	cracklib-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.322
%{?requires_php_extension}
Obsoletes:	php-crack
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides an interface to the cracklib (libcrack)
libraries that come standard on most unix-like distributions. This
allows you to check passwords against dictionaries of words to ensure
some minimal level of password security.

In PECL status of this extension is: %{_status}.

%description -l pl
Ten pakiet dostarcza interfejsu do bibliotek cracklib (libcrack),
dostarczanych z wi�kszo�ci� dystrybucji uniksopodobnych. Pozwala to na
por�wnanie hase� wzgl�dem s�ownik�w celem zapewnienia minimalnego
poziomu bezpiecze�stwa.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
%patch0 -p0

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,EXPERIMENTAL}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
