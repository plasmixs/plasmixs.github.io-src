Title: Python distutils
Date: 2014-05-19 01:30
Tags: Python
Slug: python-distutils
Status: published

### Introduction

Python distutils can be used to package python scripts along with its
dependent module scripts.
The directory show a python script test_script.py. There is also a
package under the directory 'package'. The package directory contains the
\_\_init\_\_.py and a module file 'test_pkg.py'. In addition to the project
files there are the distutils files 'setup.cfg' and 'test_setup.py'.

The contents of the directory are listed below:

    $ ls
    package  setup.cfg  test_script.py  test_setup.py

    $ ls package/
    __init__.py  test_pkg.py

The contents of the setup configuration file is listed below:

    $ cat setup.cfg
    [build]
    executable=/usr/bin/env python

    [install]
    install-base=/opt/test
    install-purelib=/opt/test
    install-platlib=/opt/test
    install-headers=/opt/test
    install-scripts=/opt/test
    install-data=/opt/test

The config file specifies that the python environment variable needs to
be altered to /usr/bin/env python in the script. This might be useful to
specify the python version available in the target machines.
The '[install]' section specifies where in the binaries and other
project related files are to be installed.

Contents of the setup file is listed below:

    $ cat test_setup.py

    from distutils.core import setup

    setup(name='distutils-test',
          version='1.0',
          author='test-author',
          author_email='test@autor.com',
          url='www.test-author.com',
          packages=['package'],
          scripts=['test_script.py']
          )

Output after running the test_setup.py. 'bdist' argument specifies
that a binary distribution needs to be generated.

    $ python3 test_setup.py bdist
    running bdist
    running bdist_dumb
    running build
    running build_py
    creating build
    creating build/lib
    creating build/lib/package
    copying package/__init__.py -> build/lib/package
    copying package/test_pkg.py -> build/lib/package
    running build_scripts
    creating build/scripts-3.2
    copying and adjusting test_script.py -> build/scripts-3.2
    changing mode of build/scripts-3.2/test_script.py from 644 to 755
    installing to build/bdist.linux-x86_64/dumb
    running install
    running install_lib
    creating build/bdist.linux-x86_64
    creating build/bdist.linux-x86_64/dumb
    creating build/bdist.linux-x86_64/dumb/opt
    creating build/bdist.linux-x86_64/dumb/opt/test
    creating build/bdist.linux-x86_64/dumb/opt/test/package
    copying build/lib/package/__init__.py -> build/bdist.linux-x86_64/dumb/opt/test/package
    copying build/lib/package/test_pkg.py -> build/bdist.linux-x86_64/dumb/opt/test/package
    byte-compiling build/bdist.linux-x86_64/dumb/opt/test/package/__init__.py to __init__.cpython-32.pyc
    byte-compiling build/bdist.linux-x86_64/dumb/opt/test/package/test_pkg.py to test_pkg.cpython-32.pyc
    running install_scripts
    copying build/scripts-3.2/test_script.py -> build/bdist.linux-x86_64/dumb/opt/test
    changing mode of build/bdist.linux-x86_64/dumb/opt/test/test_script.py to 755
    running install_egg_info
    Writing build/bdist.linux-x86_64/dumb/opt/test/distutils_test-1.0.egg-info
    creating /tmp/distutils/dist
    Creating tar archive
    removing 'build/bdist.linux-x86_64/dumb' (and everything under it)

After building the package a output tar file is generated in the
directory 'dist'.

    $ ls dist/
    distutils-test-1.0.linux-x86_64.tar.gz

The contents of the tar file are exactly the same as the source
directory.

    $ tar zxvf distutils-test-1.0.linux-x86_64.tar.gz
    ./
    ./opt/
    ./opt/test/
    ./opt/test/test_script.py
    ./opt/test/distutils_test-1.0.egg-info
    ./opt/test/package/
    ./opt/test/package/__init__.py
    ./opt/test/package/test_pkg.py
    ./opt/test/package/__pycache__/
    ./opt/test/package/__pycache__/__init__.cpython-32.pyc
    ./opt/test/package/__pycache__/test_pkg.cpython-32.pyc
    debian:/tmp/distutils/dist$ ls -R
    .:
    distutils-test-1.0.linux-x86_64.tar.gz  opt

    ./opt:
    test

    ./opt/test:
    distutils_test-1.0.egg-info  package  test_script.py

    ./opt/test/package:
    __init__.py  __pycache__  test_pkg.py

    ./opt/test/package/__pycache__:
    __init__.cpython-32.pyc  test_pkg.cpython-32.pyc

### References

1.  Python3
    [packaging](http://www.diveintopython3.net/packaging.html "packaging") documentation.
2.  Python3
    [distutils](https://docs.python.org/3.3/distutils/ "distutils")
    documentation
