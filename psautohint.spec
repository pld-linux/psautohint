#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	PSAutoHint - standalone version of AFDKO's autohinter
Summary(pl.UTF-8):	PSAutoHint - samodzielna wersja autohintera z AFDKO
Name:		psautohint
Version:	2.4.0
Release:	4
License:	Apache v2.0
Group:		Applications/Publishing
#Source0Download: https://github.com/adobe-type-tools/psautohint/releases
Source0:	https://github.com/adobe-type-tools/psautohint/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f626eb26eb635903b1f32f6c1dcf77e5
URL:		https://github.com/adobe-type-tools/psautohint
BuildRequires:	python3 >= 1:3.7
BuildRequires:	python3-setuptools >= 1:36.4
BuildRequires:	python3-setuptools_scm >= 2.1
%if %{with tests}
# fonttools[ufo]
BuildRequires:	python3-fonttools >= 4.29.0
BuildRequires:	python3-fs >= 2.2.0
BuildRequires:	python3-lxml >= 4.7.1
BuildRequires:	python3-pytest >= 5.3.0
BuildRequires:	python3-pytest-randomly >= 1.2.3
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
Requires:	python3 >= 1:3.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PSAutoHint - standalone version of AFDKO's autohinter.

%description -l pl.UTF-8
PSAutoHint - samodzielna wersja autohintera z AFDKO.

%prep
%setup -q

# disable pytest-xdist
%{__sed} -i '/-n auto/d' pytest.ini

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__python3} -m pytest -v -r a tests/unittests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING NEWS.md README.md
%attr(755,root,root) %{_bindir}/psautohint
%attr(755,root,root) %{_bindir}/psstemhist
%dir %{py3_sitedir}/psautohint
%attr(755,root,root) %{py3_sitedir}/psautohint/_psautohint.cpython-*.so
%{py3_sitedir}/psautohint/*.py
%{py3_sitedir}/psautohint/__pycache__
%{py3_sitedir}/psautohint-%{version}-py*.egg-info
