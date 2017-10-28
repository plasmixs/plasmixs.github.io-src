Title: Building RPM packages with precompiled binaries
Date: 2013-10-05 18:09
Tags: RPM
Slug: building-rpm-packages-with-pre-compiled-binaries
Status: published

Most of the [tutorials][1] on building rpm packages start from
compiling packages. This may not always be the case. There are occasions
where it would be required to distribute rpm packages of already
compiled binaries or libraries or any other blobs.

This is very much possible and simple using rpmbuild. Please note this
is not an RPM tutorial. This is just a guide for building rpm packages
out of precompiled binary packages and libraries.

### Required software Installations:

This is tested in opensuse 12.3 and in Debian 6.

The command line utility
[rpmbuild](http://www.rpm.org/max-rpm-snapshot/rpmbuild.8.html "rpmbuild") is
used for the building rpm mpackages. The rpmbuild installation steps for
opensuse and Debian are listed below.

    opensuse:
    # zypper in rpmbuild

    Debian:
    # apt-get install rpm

### Macros file:

The next step is to define the ~/.rpmmacro file. The file contains the
macro definitions.

    %_topdir /tmp/rpm
    %_tmppath %{_topdir}
    %_dbpath %{_topdir}/rpmdb
    %_builddir ./
    %_rpmdir ./bld/rpm
    %_sourcedir %{_topdir}
    %_specdir %{_topdir}
    %_srcrpmdir %{_topdir}
    %_buildrootdir %{_topdir}/rpmbuild
    %buildroot %{_buildrootdir}/%{name}-%{version}-%{release}

    #binary packages path
    %_bindir /usr/local/bin

    #binary paths that will be the installation path for the file.
    %_bin %{buildroot}%{_bindir}

    #macros to delete and create paths.
    %rm_br rm -rf %{buildroot}
    %mk_path mkdir -p %{_bin}

    #file perm, owner, group, dir perm
    %_bin_perm %defattr(0755,root,root,0644)

The macros defined influence the rpm package creation environment. The
top-level directory is set as /tmp/rpm in this macros file (_topdir).
Under this directory the rpmdb directory and the rpmbuild directories
are created. Packaging happens in the rpmbuild directory (This directory
is the sysroot emulation of the target). The rpms are generated under
the CWD/bld/rpm.
The rpm directory in /tmp is as

    > ls -R /tmp/rpm/
    /tmp/rpm/:
    rpmbuild  rpmdb  rpm-tmp.fkPD8J  rpm-tmp.KvIP93  rpm-tmp.yifKPY

    /tmp/rpm/rpmbuild:
    HelloWorld-1.0-1

    /tmp/rpm/rpmbuild/HelloWorld-1.0-1:
    usr

    /tmp/rpm/rpmbuild/HelloWorld-1.0-1/usr:
    local

    /tmp/rpm/rpmbuild/HelloWorld-1.0-1/usr/local:
    bin

    /tmp/rpm/rpmbuild/HelloWorld-1.0-1/usr/local/bin:
    helloworld

    /tmp/rpm/rpmdb:
    Basenames     Group       Obsoletename  Requirename  Triggername
    Conflictname  Installtid  Packages      Sha1header
    Dirnames      Name        Providename   Sigmd5

### The Spec file:

The rpm spec file then describes the package details and also contains
the list of files that are available in the rpm package. A sample rpm
spec file for packaging helloworld binary is given below for reference.

    #
    #Hello world sample rpm spec file.
    #
    Name: HelloWorld
    Version: 1.0
    Release: 1
    Summary: Hello World binary
    License: license.txt

    %description
    More detailed description of the hello world binary

    %install
    %rm_br
    %mk_path
    cp ./helloworld %{_bin}

    %clean
    %rm_br

    %files
    %_bin_perm
    %{_bindir}/helloworld

In the above spec file a binary "helloworld" is packaged. It is pushed
to the directory /usr/local/bin, indicated by the %install section.
%file contains the list of files that will be part of the rpm package.
The spec file also specifies the %clean which specifies that the
/tmp/rpm directory needs to be deleted once the packaging is done.

### Running the rpmbuild

The rpm package is created by invoking the command:

    > rpmbuild -bb rpm.spec

The output should look something this.

    > rpmbuild -bb rpm.spec
    Executing(%install): /bin/sh -e /tmp/rpm/rpm-tmp.aFLlMO
    + umask 022
    + cd ./
    + rm -rf /tmp/rpm/rpmbuild/HelloWorld-1.0-1
    + mkdir -p /tmp/rpm/rpmbuild/HelloWorld-1.0-1/usr/local/bin
    + cp ./helloworld /tmp/rpm/rpmbuild/HelloWorld-1.0-1/usr/local/bin
    + /usr/lib/rpm/brp-compress
    + /usr/lib/rpm/brp-suse
    Processing files: HelloWorld-1.0-1.i586
    Provides: HelloWorld = 1.0-1 HelloWorld(x86-32) = 1.0-1
    Requires(rpmlib): rpmlib(CompressedFileNames) <= 3.0.4-1 rpmlib(PayloadFilesHavePrefix) <= 4.0-1
    Requires: libc.so.6 libc.so.6(GLIBC_2.0)
    Checking for unpackaged file(s): /usr/lib/rpm/check-files /tmp/rpm/rpmbuild/HelloWorld-1.0-1
    Wrote: ./bld/rpm/i586/HelloWorld-1.0-1.i586.rpm
    Executing(%clean): /bin/sh -e /tmp/rpm/rpm-tmp.oFhfmT
    + umask 022
    + cd ./
    + rm -rf /tmp/rpm/rpmbuild/HelloWorld-1.0-1
    + rm -rf filelists

As specified in the rpm.spec file the rpm is created in the CWD/bld/rpm
directory.

    > ls -R ./bld/
    ./bld/:
    rpm

    ./bld/rpm:
    i586

    ./bld/rpm/i586:
    HelloWorld-1.0-1.i586.rpm

The rpm can be installed using the ***rpm -i*** command.

### Debugging:

The ***rpmbuild --showrc*** command can be used to dump the macros and values
defined in rpmrc and the macro files. This is very useful for debugging
the packaging environment.

See ***man rpmbuild*** or ***rpm --help*** for further details.

### RPM spec tricks

-   Suppress automatic dependency generation.

    ```AutoRreq: no```

-   Ignore unlisted files so that they will not cause a build fail

    ```%define _unpackaged_files_terminate_build 0```

-   Ignore auto dependency for python

    ```%global __requires_exclude ^/usr/bin/python$```

-   Multiple rpm from a single rpm.spec file.
    Achieved by having multiple sections in the rpm.spec file.

    ```%package -n new-section```

-   post section in rpm.spec file's first argument decides whether a install,
    erase or upgrade operation is performed for the rpm file.

    ```
    %post
    if [ "$1" = "1" ]; then
        #Install
    elif [ "$1" = "2" ]; then
        #Upgrade
    fi
    ```



[1]: RPM links

1. <http://fedoraproject.org/wiki/How_to_create_an_RPM_package>
* <http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/index.html>
* <https://www.gurulabs.com/goodies/guru-guides/>
* <http://www.rpm.org/max-rpm/>