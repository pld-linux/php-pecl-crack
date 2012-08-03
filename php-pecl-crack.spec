# TODO
# - use system cracklib
%define		modname	crack
%define		status		beta
Summary:	%{modname} - checks if password is vulnerable to dictionary attacks
Summary(pl.UTF-8):	%{modname} - sprawdzanie czy hasło jest podatne na ataki słownikowe
Name:		php-pecl-%{modname}
Version:	0.4
Release:	5
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	7cfe9df99f546cf6bd55b535d71e3b1f
Patch0:		%{name}-m4_fixes.patch
Patch1:		fix-pecl-bug-5765.patch
URL:		http://pecl.php.net/package/crack/
#BuildRequires:	cracklib-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Obsoletes:	php-crack
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-pear-%{modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides an interface to the cracklib (libcrack)
libraries that come standard on most Unix-like distributions. This
allows you to check passwords against dictionaries of words to ensure
some minimal level of password security.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Ten pakiet dostarcza interfejsu do bibliotek cracklib (libcrack),
dostarczanych z większością dystrybucji uniksopodobnych. Pozwala to na
porównanie haseł względem słowników celem zapewnienia minimalnego
poziomu bezpieczeństwa.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .
%patch0 -p1
%patch1 -p1

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%doc CREDITS EXPERIMENTAL
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
