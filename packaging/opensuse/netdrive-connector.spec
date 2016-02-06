#
# spec file for package python-netdrive-connector
#
# Copyright (c) 2016 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/


Name:           python-netdrive-connector
Version:        1.2
Release:        0
License:        
Summary:        GUI tool to setup mountable SFTP and WebDAV connections on Linux/UNIX systems
Url:            http://github.com/ethoms/netdrive-connector/
Group:          Development/Languages/Python
Source:         https://pypi.python.org/packages/source/n/netdrive-connector/netdrive-connector-%{version}.tar.gz
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if 0%{?suse_version} && 0%{?suse_version} <= 1110
%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%else
BuildArch:      noarch
%endif

%description
netdrive-connector is a simple PyQt4 wrapper for the existing and standardized
way to get SFTP and WebDAV shared folders (remote filesystems) mounted into your
local filesystem. Usually a folder inside your home folder. With the optional
addition of auto-mounting at desktop login and passwordless login.

It makes it quick and easy to get one of these shared folders up and running
without having to know how to set them up manually.

%prep
%setup -q -n netdrive-connector-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog