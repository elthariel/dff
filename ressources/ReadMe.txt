Digital Forensics Framework

1. Introduction
2. Installation
 2.1 Windows
 2.2 Linux
3. Usage
4. Support

1. Introduction

A fully integrated software dedicated to digital forensics, made from three
important objectives :

- Modularity, contrary to monolithic tools, the modularity proposes a tool which
  is based on a core and a host of modules. This modular conception presents two
  advantages : first it permits to improve rapidly the software, second , it
  permits to easily split the different task for developers.

- Scriptability, it is obvious that scriptability gives more flexibility for a
  tool. It enables automation and gives the possibility to extend features.

- Genericity, the project tends to be OS independent. We don't want to force
  people to install a specific Operating System in order to use our software.


2. Installation

2.1 Windows

Python and Python QT have to be installed first.
Web-page where Python should be downloaded :
http://www.python.org/download/releases/2.5.4/.
Web-page where Python QT should be downloaded :
http://www.riverbankcomputing.co.uk/software/pyqt/download

DFF is provided with a Nullsoft installer. User just have to launch it and
follow instructions to install DFF


2.2 Linux

Using distribution package :

RPM and DEB packages are provided on http://www.digital-forensic.org. Graphical
helper from window manager can be used when double clicking on the package.

DEB installation from terminal :
#> dpkg -i dff-<version>.deb

RPM installation from terminal 
#> rpm -i dff-<version>.rpm

Compiling from sources :

A GZipped tarball is also provided.
Cmake and latest version of swig are needed (http://www.swig.org, developer have
to compile and install the latest version himself).
In the top-source tree type :
$> cmake .
It creates make files.
To build type :
$> make
Install :
#> make install
Console Run :
$> dff.py
Graphical Run :
$> dff.py -g

3. Usage

DFF reads a disk dump (for example from GNU 'dd' utils). Two user interfaces are
provided ; graphical and console. Command-line console also sits in graphical as
well.

Graphical :
Click on the 'File' menu and select 'Add dump'.
Right-click on the dump, in the 'Files' tab, select 'Open with' and apply a
filesystem module ; select 'fs' and 'fat' for example.
Files appears in the 'Virtual File System' tab.
Many informations are provided under 'log' and 'info' tabs.


Console :
Opening a local folder :
dff / > local --path /home/user/dumps --parent /

--path is the directory to open
--parent is a virtual node, first specify the root one : /

Applying fat module on a dump :
dff / > fat dumps/test.fat.dd

Listing nodes :
dff / > ls

Completion is provided using the <Tab> key. User can obtain help using :
dff / > man <command>


4. Support

Online chat is on an IRC channel : #digital-forensic on irc.freenode.net
network.

Main website : http://www.digital-forensic.org .

3 mailing lists are provided :
- User discussions about DFF : dff@digital-forensic.org, registration and
  posting freely available.
 - Developers discussions about DFF : dff-devel@digital-forensic.org,
   registration and posting freely available.
 - News about DFF releases and event : dff-announce@digital-forensic.org,
   registration freely available, low level traffic.

Archives of this mailing lists : http://lists.digital-forensic.org

A project manager exists at http://tracker.digital-forensic.org , ideas and bug
submited by e-mail will be reported on it.

Documentation sits on http://wiki.digital-forensic.org.

