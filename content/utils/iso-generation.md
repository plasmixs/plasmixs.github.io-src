Title: ISO generation
Date: 2014-05-18 18:03
Tags: Python
Slug: iso-generation
Status: published

### Introduction

The genisoimage utility can be used to create iso out a directory tree.
The post shows usage of genisoimage in a python script to generate a iso image
of a directory.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

def make_iso(iso_dir, iso_name):
    '''-J is for Joliet format, -f is for follow symbolic links
    -r is for rockridge extensions. Needed to preserve permissions'''

    cmd=["genisoimage", "-J", "-r", "-f", "-debug", "-v", "-o",
    "{0}".format(iso_name),
    "{0}".format(iso_dir)]

    try:
	out=subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
    	   errstr="Cmd: {0} returned {1}\\n".format(e.cmd, e.returncode)
	   if e.output != None:
       	       errstr=errstr+"Output {0}\n".format(e.output)
   	   raise execCmdError(errstr)
    return (out)

if __name__=='__main__':
    make_iso('/tmp/iso_dir', 'test.iso')
```

The directory '/tmp/iso_dir' contains a directory tree that will be converted
to iso image.

The output from the script is:

    $ ls -R iso_dir/
    iso_dir/:
    test_dir  test_file.txt

    iso_dir/test_dir:
    testfile.txt

    $ ./iso.py
    Warning: -follow-links does not always work correctly; be careful.
    I: -input-charset not specified, using utf-8 (detected in locale settings)
    genisoimage 1.1.11 (Linux)
    graft_dir: ' : ', node: '/tmp/iso_dir', (scan)
    Scanning /tmp/iso_dir
    Scanning /tmp/iso_dir/test_dir
    scan done
    Writing:   Initial Padblock                        Start Block 0
    Done with: Initial Padblock                        Block(s)    16
    Writing:   Primary Volume Descriptor               Start Block 16
    Done with: Primary Volume Descriptor               Block(s)    1
    Writing:   Joliet Volume Descriptor                Start Block 17
    Done with: Joliet Volume Descriptor                Block(s)    1
    Writing:   End Volume Descriptor                   Start Block 18
    Done with: End Volume Descriptor                   Block(s)    1
    Writing:   Version block                           Start Block 19
    Done with: Version block                           Block(s)    1
    Writing:   Path table                              Start Block 20
    Done with: Path table                              Block(s)    4
    Writing:   Joliet path table                       Start Block 24
    Done with: Joliet path table                       Block(s)    4
    Writing:   Directory tree                          Start Block 28
    Done with: Directory tree                          Block(s)    2
    Writing:   Joliet directory tree                   Start Block 30
    Done with: Joliet directory tree                   Block(s)    2
    Writing:   Directory tree cleanup                  Start Block 32
    Done with: Directory tree cleanup                  Block(s)    0
    Writing:   Extension record                        Start Block 32
    Done with: Extension record                        Block(s)    1
    Writing:   The File(s)                             Start Block 33
    Total translation table size: 0
    Total rockridge attributes bytes: 552
    Total directory bytes: 2542
    Path table size(bytes): 26
    Done with: The File(s)                             Block(s)    0
    Writing:   Ending Padblock                         Start Block 33
    Done with: Ending Padblock                         Block(s)    150
    Max brk space used 0
    183 extents written (0 MB)
    rameshd@deb:/tmp$ ll
    drwxr-xr-x 3 rameshd rameshd   4096 May 18 23:17 iso_dir
    -rwxr-xr-x 1 rameshd rameshd    746 May 18 23:19 iso.py
    -rw-r--r-- 1 rameshd rameshd 374784 May 18 23:19 test.iso

The contents of the iso can be viewed by by temporarily mounting the iso into
a directory.

    $ mkdir a

    # mount test.iso a
    mount: block device /tmp/test.iso is write-protected, mounting read-only

    # ls -R a
    a:
    test_dir  test_file.txt

    a/test_dir:
    testfile.txt

### References

Python3
[subprocess](https://docs.python.org/3/library/subprocess.html "python subprocess")
module documentation.
