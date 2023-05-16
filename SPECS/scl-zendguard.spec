%global extension_type php
%global upstream_name zendguard

%{?scl:%global _scl_prefix /opt/cpanel}
%{?scl:%scl_package %{extension_type}-%{upstream_name}}
%{?scl:BuildRequires: scl-utils-build}
%{?scl:Requires: %scl_runtime}
%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package_override}

# must redefine this in the spec file because OBS doesn't know how
# to handle macros in BuildRequires statements
%{?scl:%global scl_prefix %{scl}-}

# OBS builds the 32-bit targets as arch 'i586', but 32-bit archive is
# named 'i386'.  Other archives are named as the actual architecture.
%if "%{_arch}" == "i586"
%global archive_arch i386
%else
%global archive_arch %{_arch}
%endif

# The different PHP versions are actually supported by different
# versions of the loader, so we'll have different versions and source
# files depending on our PHP.
%if "%{php_version}" == "5.6"
%global zend_source  zend-loader-php5.6-linux-%{archive_arch}.tar.gz
%global zend_srcdir  zend-loader-php5.6-linux-%{archive_arch}
%global zend_sodir   ./
%global use_zend_opcache 1
%endif
%if "%{php_version}" == "5.5"
%global zend_source  zend-loader-php5.5-linux-%{archive_arch}.tar.gz
%global zend_srcdir  zend-loader-php5.5-linux-%{archive_arch}
%global zend_sodir   ./
%global use_zend_opcache 1
%endif
%if "%{php_version}" == "5.4"
%global zend_source  ZendGuardLoader-70429-PHP-5.4-linux-glibc23-%{archive_arch}.tar.gz
%global zend_srcdir  ZendGuardLoader-70429-PHP-5.4-linux-glibc23-%{archive_arch}
%global zend_sodir   php-5.4.x/
%global use_zend_opcache 0
%endif

Name:    %{?scl_prefix}%{extension_type}-%{upstream_name}
Vendor:  cPanel, Inc.
Summary: Loader for Zend Guard-encoded PHP files
Version: 3.3
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4596 for more details
%define release_prefix 10
Release: %{release_prefix}%{?dist}.cpanel
License: Redistributable
Group:   Development/Languages
URL:     http://www.zend.com/en/products/guard/downloads
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# We've defined the source archive above, since it is dependent on PHP
# version.
Source:  %{zend_source}

%{?scl:BuildRequires: %{?scl_prefix}scldevel}
%{?scl:BuildRequires: %{?scl_prefix}build}
BuildRequires: %{?scl_prefix}php-devel
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
Requires:      %{?scl_prefix}php-cli
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
* Wed May 10 2023 Brian Mendoza <brian.mendoza@cpanel.net> - 3.3-10
- ZC-10936: Clean up Makefile and remove debug-package-nil

* Tue Dec 28 2021 Dan Muey <dan@cpanel.net> - 3.3-9
- ZC-9589: Update DISABLE_BUILD to match OBS

* Tue Feb 18 2020 Tim Mullin <tim@cpanel.net> - 3.3-8
- EA-8865: Add php-cli as a dependency

* Wed Feb 01 2017 Dan Muey <dan@cpanel.net> - 3.3-7
- EA-5028 via EA-5900: reinstate opcache conflict
- (the obsoletes is problematic and there is a
-   proper way to address the problem it was intended to solve)

* Fri Dec 16 2016 Cory McIntire <cory@cpanel.net> - 3.3-6
- Updated Vendor field in the SPEC file

* Wed Jun 29 2016 David Nielson <david.nielson@cpanel.net> - 3.3-5
- SWAT-28: Obsolete opcache instead of conflicting with it

* Mon Jun 20 2016 Dan Muey <dan@cpanel.net> - 3.3-4
- EA-4383: Update Release value to OBS-proof versioning

* Mon Jul 20 2015 Trinity Quirk <trinity.quirk@cpanel.net> - 3.3-1
- Initial creation
