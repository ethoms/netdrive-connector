# netdrive-connector
Utility to setup mountable SFTP and WebDAV connections.

## Introduction
netdrive-connector is a simple PyQt4 wrapper for the existing and standardized
way to get SFTP and WeDAV shared folders mounted into your filesystem. Usually
a folder inside your home folder. With the optional addition of auto-mounting 
at login and passwordless login.

It makes it quick and easy to get one of these shared folders up and running 
without having to know how to them up manually.

## Screenshots
![netdrive-connect main window](/screenshots/netdrive-connector1.png?raw=true "netdrive-connector Main Window")


## Pros
- Simple and effective
- Uses robust existing technologies (sshfs, davfs2)
- No unnecessary config files or metadata
- Saves learning how to set up these remote filesystems manually

## Cons
- Possiblity inhibits learning of underlying techologies

## Current Limitations
- The unmount at logout is KDE centric (uses ~/.kde/shutdown)
- No UI localization support (English only)
- Only available for Linux
- Makes some assumptions about the system configuration

## Usage Notes
Any regular user accounts that intend to mount a connection may need additional
unix groups ( fuse, sshfs, davfs2). This varies depending on the distribution.

## Packaging Notes
### WARNING:
> The webdav connection script 'add-webdav-connector' will turn setuid bit on 
/usr/bin/mount.davfs*

Subject to the distro and it's fuse, davfs2, sshfs a user may need adding to 
additional groups (fuse, davfs/davfs2 etc.)
In Slackware, only the davfs2 group is required.

An ssh-askpass program should be installed and configured to work with sshfs.

At some point in the operation of adding/removing connections, a temporary 
script is placed in /tmp and given execute permission. After use it is deleted. 
A regular user will need permissions to do this.

### Dependencies:
- python v2.7 or above (not python 3)
- PyQt4 v4.8 or above (python-qt4 on debian based distros)
- An ssh-askpass variant. Tested with x11-ssh-askpass.
- expect(version 5.x or above should be OK)
- fuse
- sshfs (sshfs-fuse) v2.4 or above recommended
- davfs2 v1.4.6 or above recommended
- openssh-client
- awk, grep, ls, cut, chown, cat, chmod, sed, uname

### Dep Notes:
Either davfs2 or sshfs are not required if that connection type is unused.
