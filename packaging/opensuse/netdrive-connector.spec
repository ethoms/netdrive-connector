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


Name:           netdrive-connector
Version:        1.3.2
Release:        0
License:        BSD-2-Clause
Summary:        GUI tool to setup mountable SFTP and WebDAV connections on Linux/UNIX systems
Url:            http://github.com/ethoms/netdrive-connector/
Group:          Development/Languages/Python
Source:         netdrive-connector_%{version}.orig.tar.gz
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-qt4
Requires:       openssh
Requires:       openssh-askpass
Requires:       expect
Requires:       sshfs
Requires:       davfs2
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
/usr/bin/add-sftp-connector
/usr/bin/add-webdav-connector
/usr/bin/netdrive-connector
/usr/bin/netdrive-connector_automountd
/usr/bin/netdrive-connector_run-as-root
/usr/bin/remove-sftp-connector
/usr/bin/remove-webdav-connector
/usr/share/applications/netdrive-connector.desktop
/usr/share/pixmaps/netdrive-connector.png

%defattr(-,root,root,-)
%{python_sitelib}/*

%doc README.rst CHANGELOG LICENSE

%changelog CHANGELOG
