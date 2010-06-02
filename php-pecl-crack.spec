%define		_modname	crack
%define		_status		beta
Summary:	%{_modname} - checks if password is vulnerable to dictionary attacks
Summary(pl.UTF-8):	%{_modname} - sprawdzanie czy hasło jest podatne na ataki słownikowe
Name:		php-pecl-%{_modname}
Version:	0.4
Release:	2
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	7cfe9df99f546cf6bd55b535d71e3b1f
Patch0:		%{name}-m4_fixes.patch
URL:		http://pecl.php.net/package/crack/
BuildRequires:	cracklib-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Obsoletes:	php-crack
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides an interface to the cracklib (libcrack)
libraries that come standard on most Unix-like distributions. This
allows you to check passwords against dictionaries of words to ensure
some minimal level of password security.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Ten pakiet dostarcza interfejsu do bibliotek cracklib (libcrack),
dostarczanych z większością dystrybucji uniksopodobnych. Pozwala to na
porównanie haseł względem słowników celem zapewnienia minimalnego
poziomu bezpieczeństwa.

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
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,EXPERIMENTAL}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
