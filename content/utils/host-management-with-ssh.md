Title: Host management with SSH
Date: 2014-05-20 08:35
Tags: ssh
Slug: host-management-with-ssh
Status: published

### Introduction

The post details setting up password less authentication using keys for
ssh access.
This enables a fully automated mechanism to execute tasks remotely in
hosts and also to transfer files easily between hosts.

The first step is to generate host keys, that would enable
authentication between the hosts. In this setup no pass phrase is given
which allows us to ssh into a host without user intervention.
Note 1: This is not secure.
Note 2: As an alternative
[ssh-agent](http://en.wikipedia.org/wiki/Ssh-agent "ssh-agent") can be
used. The drawback with ssh-agent is that every time the node reboots user
intervention is required to re-enter the password.

ssh key generation is done using the command ssh-keygen.

    $ssh-keygen -P "" -f keys/temp_host
    Generating public/private rsa key pair.
    Your identification has been saved in keys/temp_host.
    Your public key has been saved in keys/temp_host.pub.
    The key fingerprint is:
    33:33:b8:33:2a:98:a0:50:8a:4e:96:9a:ec:fe:17:f8 rameshd@deb
    The key's randomart image is:
    +--[ RSA 2048]----+
    |                 |
    |                 |
    |                 |
    |  .    .         |
    |.o. . . S        |
    |=+ . . . =       |
    |X+  . =          |
    |*o.  E o         |
    |oo.oo            |
    +-----------------+
    $ ls keys/
    temp_host  temp_host.pub

This places both the public as well as the private keys in the specified
directory.

Note: As an alternative
[ssh-copy-id](http://linux.die.net/man/1/ssh-copy-id "ssh copy id") can
be used to transfer keys.

The posts does not use ssh-copy-id because we would like to capture the
remote host's key in our specified known_host file rather than the
common ~/.ssh/known_hosts.

Establish a ssh connection with the remote host.
This will ask for password. Nothing useful needs to be done here except
that the hosts key is added in the known_hosts file.
Note 1: StrictHostKeyChecking is set as 'no'.
Note 2: Here the command 'hostname' is executed in the remote host.
This terminates the ssh link after the command is executed.
Any command can be placed here.

    $ ssh -o UserKnownHostsFile=/tmp/ssh/known_hosts
         -o StrictHostKeyChecking=no
         -i /tmp/ssh/keys/temp_host.pub
          root@192.168.100.128 hostname

    x86vm

The remote host's key is now available in the known_host file.

    $ cat known_hosts
    |1|rr84r4T6Ckf7C48LMHV1eP1k3Xk=|EOJg2q ......

The next step is to create a ssh configuration file. Maintaining a
separate config file and known_hosts (default is in ~/.ssh directory)
allows us to maintain separate config files for different groups of
remote nodes.
In this example the config file is maintained in the current
directory.
The contents of the config file are listed below. Look up to the man
pages of ssh_config for more details.

    $ cat ssh_config
    Host 192.168.100.128
      User root
      IdentityFile /tmp/ssh/keys/temp_host.pub
      UserKnownHostsFile /tmp/ssh/known_hosts

Thats it. Now that SSH is setup we can now execute commands remotely
using the ssh.

    $ ssh -F ssh_config 192.168.100.128 'ls /'
    bin
    boot
    dev
    ...

File transfer operations can be performed using scp

    $ scp -F ssh_config test 192.168.100.128:/tmp
    test                                          100%    0     0.0KB/s   00:00
    $ ssh -F ssh_config 192.168.100.128 'ls /tmp'
    test

Additionally a remote host entry can be removed from the known_hosts
using the ssh-keygen command.

    $ ssh-keygen -R 192.168.100.128 -f known_hosts
    known_hosts updated.
    Original contents retained as known_hosts.old

This would be useful when the host key changes, which may be due to the
node failure or due to security policies.
