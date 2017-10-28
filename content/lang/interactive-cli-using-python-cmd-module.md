Title: Interactive CLI using Python cmd module
Date: 2014-05-18 04:16
Tags: Python
Slug: interactive-cli-using-python-cmd-module
Status: published

### Introduction

The python inbuilt module cmd can be used to create interactive command line
interface applications.

The cmdloop function defined in cmd.Cmd class starts the main loop.
The user configurable 'prompt' is displayed where in the user types the
commands and its arguments. The prompt message can be customized as well as
the command introductory message. By default '?' or the command 'help'
displays the available commands. The help message as well as tab completion
of commands and it argument can be easily customized. Other key aspects of
cmd module based implementation is the support for nesting cli classes.
This feature can be used to implement multiple levels of cli.

A sample python code using this cmd module is listed below:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmd

class test_cli(cmd.Cmd):
    def __init__(self, intro="Demo of pyton cli",
        prompt="(tc)"):
        cmd.Cmd.__init__(self)
        self.intro=intro
        self.prompt=prompt
        self.doc_header="Test Cli (type help &lt;topic&gt;):"
    def emptyline(self):
        pass
    def do_end(self, args):
        return True
    def help_end(self, args):
        print("End session")
    do_EOF = do_end
    help_EOF = help_end
    def do_quit(self, args):
        return True
    def help_quit(self, args):
        print("Quit session")
    def precmd(self, line):
        newline=line.strip()
        is_cmt=newline.startswith('#')
        if is_cmt:
            return ('')
        return (line)
    def do_nested(self, args):
        n_cli=test_level2_cli()
        n_cli.cmdloop()
    def help_nested(self, args):
        print("Start nested cli session")

class test_level2_cli(test_cli):
    def __init__(self):
        test_cli.__init__(self,
        intro="level 2 cli", prompt="(l2)")
    def do_print(self, args):
        print (args)
    def help_print(self):
        print (" Print the passed arguments ")

if __name__=='__main__':
   t_cli=test_cli()
   t_cli.cmdloop()
```

The output from the script is:

    $ ./test_cli.py
    Demo of pyton cli
    (tc)end

The current cli session can be ended by 'end' command or by EOF ('CTRL D').
The command loop can be quit by 'quit' command.

    $ ./test_cli.py
    Demo of pyton cli
    (tc)quit

In the test_cli class the function do_emptyline is implemented.
The function simple ignores the line and returns true. As seen if the
user types 'enter' no action is performed. The default behavior is to quit
when plain enter is pressed.

    $ ./test_cli.py
    Demo of pyton cli
    (tc)
    (tc)

The command completion is by pressing 'TAB'. The running help can be accessed
by pressing '?' or the 'help' command.

    $ ./test_cli.py
    Demo of pyton cli
    (tc)
    EOF     end     help    nested  quit
    (tc)?

    Test Cli (type help ):
    =============================
    EOF  end  help  nested  quit

    (tc)nes
    nested

### Nested CLI

The second level of cl is invoked after typing the 'nested' command.
The only command implemented in the nested cli is the 'print' command.
The command simply prints the passed arguments.
Note that the 'end' command first exits the inner loop and then another
invocation exits the outer loop (in this case the final loop).

    (tc)nested
    level 2 cli
    (l2)?

    Test Cli (type help ):
    =============================
    EOF  end  help  nested  print  quit

    (l2)print hello world
    hello world
    (l2)end
    (tc)end

### References

Python3 command
([cmd](https://docs.python.org/2/library/cmd.html "Python3 command module documentation"))
module documentation.

Argument parsing:
Though not related to cli the references here point to command line
argument parsing.

1.  Python3
    [argparse](https://docs.python.org/3/howto/argparse.html "argparse") tutorial.
2.  Python
    [getopt](https://docs.python.org/3/library/getopt.html#module-getopt "getopt") module.
3.  C
    [getopt](http://www.gnu.org/software/libc/manual/html_node/Getopt.html "c getopt")
4.  GNU
    [readline](http://en.wikipedia.org/wiki/GNU_Readline "readline").
    Basis for auto completion.
5.  C
    [arg\_parse](http://nongnu.askapache.com/argpbook/step-by-step-into-argp.pdf "argp").
    Step by step illustration of argp in C
