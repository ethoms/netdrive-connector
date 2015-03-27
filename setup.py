#!/usr/bin/env python

from distutils.core import setup

setup(
    name='netdrive-connector',
    version='1.1',
    description='GUI tool to setup mountable SFTP and WebDAV connections.',
    author='Euan Thoms',
    author_email='euan@potensol.com',
    url='http://www.potensol.com/projects/netdrive-connector',
    license='BSD License',
    platforms=['linux-*'],
    packages=['netdriveconnector'],
    package_dir={'netdriveconnector': 'netdriveconnector'},
    package_data={'netdriveconnector': ['*.ui']},
    data_files=[
        ('share/pixmaps',['data/netdrive-connector.png']),
        ('share/applications',['data/netdrive-connector.desktop']),
    ],
    scripts=['bin/netdrive-connector', 'bin/netdrive-connector_run-as-root', 'bin/add-sftp-connector', 'bin/add-webdav-connector', 'bin/remove-sftp-connector', 'bin/remove-webdav-connector'],
)
