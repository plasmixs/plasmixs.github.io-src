Title: Debugging with python logger module
Date: 2014-05-18 17:13
Tags: Python
Slug: debugging-with-python-logger-module
Status: published

### Introduction

The post details the usage of logging module in python.
The logging module can be very useful for debugging running
applications and to output interesting information about the running state.

The post directs the log messages to custom log file '/tmp/test.log'.
It also showcases the customization capabilities of the logging
module.
For example the format of logging messages can be customized as
required.

The level of individual messages can be controlled. The logging module
has the filtering capability to process messages only messages that are above a
specified severity level. In the example the logging level is set as debug'
level.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

if __name__=='__main__':

   # create logger instance
   logger = logging.getLogger('Test Log')
   logger.setLevel(logging.INFO)

   # create file handler
   fh = logging.FileHandler("/tmp/test.log")

   # set level to debug
   fh.setLevel(logging.DEBUG)

   # create formatter, this will set log message format
   formatter = logging.Formatter('%(asctime)s-%(levelname)s- %(message)s')

   # add formatter to logger
   fh.setFormatter(formatter)

   # add file handler to logger
   logger.addHandler(fh)

   logger.info('file logging started')
   logger.error('error message')
   logger.info('logging stopped')
```

The output from the script is:

    $ ./log.py
    $ cat /tmp/test.log
    2014-05-18 22:49:49,940-INFO- file logging started
    2014-05-18 22:49:49,941-ERROR- error message
    2014-05-18 22:49:49,941-INFO- logging stopped

### References

1.  Python3 logging
    [module](https://docs.python.org/3/library/logging.html#logging.Logger "logging module") documentation.
2.  Python logging
    [cookbook](https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook "logging cookbook")
3.  Python logging
    [howto](https://docs.python.org/3/howto/logging.html "logging howto")
