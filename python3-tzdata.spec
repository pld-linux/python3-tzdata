#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module	tzdata
Summary:	zic-compiled binaries for the IANA time zone database
Summary(pl.UTF-8):	Binaria skompilowane zic dla bazy danych stref czasowych IANA
Name:		python3-%{module}
Version:	2025.2
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/tzdata/
Source0:	https://files.pythonhosted.org/packages/source/t/tzdata/%{module}-%{version}.tar.gz
# Source0-md5:	1e0a85189737abbc555fbcf139e989eb
URL:		https://pypi.org/project/tzdata/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools >= 1:40.8.0
BuildRequires:	python3-wheel
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-subtests >= 0.14
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-sphinx_bootstrap_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Python package containing zic-compiled binaries for the IANA
time zone database. It is intended to be a fallback for systems that
do not have system time zone data installed (or don't have it
installed in a standard location), as a part of PEP 615.

%description -l pl.UTF-8
Pakiet Pythona zawierający skompilowane zic binaria bazy danych stref
czasowych IANA. Ma służyć jako fallback dla systemów bez systemowej
bazy danych stref czasowych zainstalowanej w standardowym miejscu,
jako część PEP 615.

%package apidocs
Summary:	API documentation for Python tzdata module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona tzdata
Group:		Documentation

%description apidocs
API documentation for Python tzdata module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona tzdata.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_subtests.plugin \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
# LICENSE is just summary, not actual Apache-2.0 text
%doc LICENSE NEWS.md README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
