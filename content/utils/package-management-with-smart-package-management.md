Title: Package management with Smart package management
Date: 2014-04-05 17:26
Tags: RPM, smartpm
Slug: package-management-with-smart-package-management
Status: published

The [Smart package manager](http://labix.org/smart "Smart PM Site") is the
currently supported package manager in
[Yocto](https://www.yoctoproject.org/ "Yocto Project Site"). The post shows
how to install and manage rpm packages in the target using smartpm.

### Brief about the steps

1.  Create a RPM repository. This will index the rpms.
2.  Start a webserver that will serve the rpms and the index file.
3.  Configure smart in the target to pick up these rpms
4.  Finally install the rpms

### Creating a RPM repository

Create a new directory for the repository. The directory contains two
sub directories for the main rpm and for updated rpm.

    $ ls repo/
    main update

The main directory is populated with two rpms.

    $ ls repo/main/
    test_bin-1.0-1.i586.rpm utLib-1.0-1.i586.rpm

The repository is created using the utility **createrepo**

    $ createrepo -v .
    1/2 - test_bin-1.0-1.i586.rpm
    2/2 - utLib-1.0-1.i586.rpm
    Saving Primary metadata
    Saving file lists metadata
    Saving other metadata

    $ ls repo/main/
    repodata test_bin-1.0-1.i586.rpm utLib-1.0-1.i586.rpm

    $ ls repo/main/repodata/
    filelists.xml.gz other.xml.gz primary.xml.gz repomd.xml

The repository is now ready to host the rpms in the main directory.

### Serving the repository using a simple webserver

The python built in webserver can be used for the purpose.

    $ python -m SimpleHTTPServer
    Serving HTTP on 0.0.0.0 port 8000 ...

This starts the web server and all files under the directory will now be
served. Here in this example the http server is started in the repo
directory and hence the main as well as the update folder contents are
served automatically by this webserver.

### Smart configuration

The first step is to add the Smart channel. A channel is the way smart
knows about external repositories. A channel is added using the
**--add** option to the smart channel command. **smart update** command
retrieves the repository index and obtains the list of available rpm
packages.

    # smart channel --add main type=rpm-md baseurl=http://192.168.100.1:8000/main

    Alias: main
    Type: rpm-md
    Base URL: http://192.168.100.1:8000/main

    Include this channel? (y/N): y

    root@x86vm:/# smart update
    Loading cache...
    Updating cache...               ######################################## [100%]

    Fetching information for 'main'...

    -> http://192.168.100.1:8000/main/repodata/repomd.xml

    repomd.xml                      ######################################## [ 50%]
    -> http://192.168.100.1:8000/main/repodata/primary.xml.gz

    primary.xml.gz                  ######################################## [ 75%]
    -> http://192.168.100.1:8000/main/repodata/filelists.xml.gz

    filelists.xml.gz                ######################################## [100%]

    Updating cache...               ######################################## [100%]

    Channels have 2 new packages:
        test_bin-1.0-1@i586
        utLib-1.0-1@i586

    Saving cache...

The http server output is shown below:

    $ python -m SimpleHTTPServer
    Serving HTTP on 0.0.0.0 port 8000 ...
    192.168.100.128 - - [06/Apr/2014 18:34:20] "GET /main/repodata/repomd.xml HTTP/1.0" 200 -
    192.168.100.128 - - [06/Apr/2014 18:34:20] "GET /main/repodata/primary.xml.gz HTTP/1.0" 200 -
    192.168.100.128 - - [06/Apr/2014 18:34:20] "GET /main/repodata/filelists.xml.gz HTTP/1.0" 200 -

Notice that the index files are transferred as **smart update** is run.

### Smart install packages

To install a package use the **smart install** command.

    # smart install test_bin
    Loading cache...
    Updating cache...               ######################################## [100%]

    Computing transaction...

    Installing packages (1):
      test_bin-1.0-1@i586

    33.6kB of package files are needed. 116.1kB will be used.

    Confirm changes? (Y/n): y

    Fetching packages...

    -> http://192.168.100.1:8000/main/test_bin-1.0-1.i586.rpm

    test_bin-1.0-1.i586.rpm         ######################################## [100%]


    Committing transaction...
    Preparing...                    ######################################## [  0%]
       1:Installing test_bin        ######################################## [100%]

The http server out for the same is as follows:

    192.168.100.128 - - [06/Apr/2014 18:41:51] "GET /main/test_bin-1.0-1.i586.rpm HTTP/1.0" 200 -

smart packages details can be obtained from **smart info** command

    # smart info test_bin
    Loading cache...
    Updating cache...               ######################################## [100%]

    Name: test_bin
    Version: 1.0-1@i586
    Priority: 0
    Source: test_bin-1.0-1
    Group: Unspecified
    License: license.txt
    Installed Size: 116.1kB
    Reference URLs:
    Flags: new
    Channels: main
    Summary: Test binaries
    Description:
     Test Binaries

smart pm can be used for package update as well as remove operations.
