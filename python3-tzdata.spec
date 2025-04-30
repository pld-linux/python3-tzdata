# Conditional build:
%bcond_without	tests	# unit tests

%define		module	tzdata
Summary:	zic-compiled binaries for the IANA time zone database
Name:		python3-%{module}
Version:	2025.2
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
# if pypi:
#Source0Download: https://pypi.org/simple/tzdata/
Source0:	https://files.pythonhosted.org/packages/source/t/tzdata/%{module}-%{version}.tar.gz
# Source0-md5:	1e0a85189737abbc555fbcf139e989eb
URL:		https://pypi.org/project/tzdata/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.2
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-subtests
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Python package containing zic-compiled binaries for the IANA
time zone database. It is intended to be a fallback for systems that
do not have system time zone data installed (or don't have it
installed in a standard location), as a part of PEP 615.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif


%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS.md README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info
