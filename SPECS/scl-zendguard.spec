%define debug_package %{nil}

# Package namespaces
%global ns_name ea
%global ns_dir /opt/cpanel
%global _scl_prefix %ns_dir

%scl_package %scl

# This makes the ea-php<ver>-build macro stuff work
%scl_package_override

# The different PHP versions are actually supported by different
# versions of the loader, so we'll have different versions and source
# files depending on our PHP.
%if "%{php_version}" == "5.6"
%global zend_source  zend-loader-php5.6-linux-x86_64.tar.gz
%global zend_srcdir  zend-loader-php5.6-linux-x86_64
%global zend_sodir   ./
%global use_zend_opcache 1
%endif
%if "%{php_version}" == "5.5"
%global zend_source  zend-loader-php5.5-linux-x86_64.tar.gz
%global zend_srcdir  zend-loader-php5.5-linux-x86_64
%global zend_sodir   ./
%global use_zend_opcache 1
%endif
%if "%{php_version}" == "5.4"
%global zend_source  ZendGuardLoader-70429-PHP-5.4-linux-glibc23-x86_64.tar.gz
%global zend_srcdir  ZendGuardLoader-70429-PHP-5.4-linux-glibc23-x86_64
%global zend_sodir   php-5.4.x/
%global use_zend_opcache 0
%endif

Name:    %{?scl_prefix}php-zendguard
Vendor:  Zend Technologies, Ltd.
Summary: Loader for Zend Guard-encoded PHP files
Version: 3.3
Release: 1%{?dist}
License: Redistributable
Group:   Development/Languages
URL:     http://www.zend.com/en/products/guard/downloads

# We've defined the source archive above, since it is dependent on PHP
# version.
Source:  %{zend_source}

BuildRequires: scl-utils-build
BuildRequires: %{?scl_prefix}scldevel
BuildRequires: %{?scl_prefix}build
BuildRequires: %{?scl_prefix}php-devel
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%if %{use_zend_opcache}
Conflicts:     %{?scl_prefix}php-opcache
%endif

# Don't provide extensions as shared library resources
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}

%description
The Zend Guard Loader enables use of Zend-encoded PHP files running
under PHP %{php_version}.

%prep
%setup -q -n %{zend_srcdir}

%build
# Nothing to do here, since it's a binary distribution.

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

# The module(s)
install -d -m 755 $RPM_BUILD_ROOT%{php_extdir}
install -m 755 %{zend_sodir}ZendGuardLoader.so $RPM_BUILD_ROOT%{php_extdir}
%if %{use_zend_opcache}
install -m 755 %{zend_sodir}opcache.so $RPM_BUILD_ROOT%{php_extdir}
%endif

# The ini snippet
install -d -m 755 $RPM_BUILD_ROOT%{php_inidir}
cat > $RPM_BUILD_ROOT%{php_inidir}/zendguard.ini <<EOF
; Enable Zend Guard Loader extension module
zend_extension="%{php_extdir}/ZendGuardLoader.so"
EOF
%if %{use_zend_opcache}
echo 'zend_extension="%{php_extdir}/opcache.so"' >> $RPM_BUILD_ROOT%{php_inidir}/zendguard.ini
%endif

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.txt
%config(noreplace) %{php_inidir}/zendguard.ini
%{php_extdir}/ZendGuardLoader.so
%if %{use_zend_opcache}
%{php_extdir}/opcache.so
%endif

%changelog
* Mon Jul 20 2015 Trinity Quirk <trinity.quirk@cpanel.net> - 3.3-1
- Initial creation
