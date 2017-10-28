Title: Setting up KVM guests for Open vSwitch
Date: 2014-05-20 11:10
Tags: KVM, OpenvSwitch
Slug: setting-up-kvm-guests-for-openvswitch
Status: published

### Introduction

[Open vSwitch](http://openvswitch.org/ "Open vSwitch") is a virtual switch
fully implemented in software (both user space as well as kernel space).
The official documents lists a number of switching feature supported by
OVS. The post will detail setting up KVM guest to use OVS for their
networking.

### Compiling, Installing and setting up OVS

Building ovs is same as any package in linux. You run configure and then
make and finally 'make install' will install the required components.
In this post the ovs version 1.9.3 is used and is installed in the path
/opt/ovs. Refer to the INSTALL documents for more information.
Note: Ensure gre module is loaded before inserting the ovs module.
'modprobe gre'
Note: ovs version 2.1.2 has problems in loading the kmod due to this
bug 'Bug\#746602: skb\_copy\_ubufs() not exported by the Debian Linux
kernel 3.2.57-3'.

    $ ./configure --prefix=$PWD/Output
                 --datarootdir=$PWD/Output_docs
                 --sysconfdir=/opt/deploy-ovs/etc
                 --sharedstatedir=/opt/deploy-ovs/com
                 --localstatedir=/opt/deploy-ovs/var
                 --with-linux=/lib/modules/`uname -r`/build

    $ make
    $ make install

The runtime configurations are stored in this setup in /opt/deploy-ovs.

    # ovs/bin/ovsdb-tool -v create
    /opt/deploy-ovs/etc/openvswitch/conf.db
    /opt/ovs/vswitch.ovsschema

    deb:/opt# ls -R deploy-ovs/etc
    deploy-ovs/etc:
    openvswitch

Start the configuration database.

    # ovs/sbin/ovsdb-server
    --remote=punix:/opt/deploy-ovs/var/run/openvswitch/db.sock
    --remote=db:Open_vSwitch,manager_options
    --private-key=db:SSL,private_key
    --certificate=db:SSL,certificate
    --bootstrap-ca-cert=db:SSL,ca_cert
    --pidfile
    --log-file
    2014-05-20T17:10:30Z|00001|vlog|INFO|opened log file /opt/deploy-ovs/var/log/op
    envswitch/ovsdb-server.log
    2014-05-20T17:10:30Z|00002|ovsdb_server|INFO|ovsdb-server (Open vSwitch) 1.9.3
    2014-05-20T17:10:40Z|00003|memory|INFO|2448 kB peak resident set size after 10.
    0 seconds
    2014-05-20T17:10:40Z|00004|memory|INFO|

Initialize db.

    deb:/opt# ovs/bin/ovs-vsctl --log-file --no-wait init

Start ovs daemon

    # ovs/sbin/ovs-vswitchd --pidfile --log-file
    2014-05-20T17:58:06Z|00001|vlog|INFO|opened log file /opt/deploy-ovs/var/log/op
    envswitch/ovs-vswitchd.log
    2014-05-20T17:58:06Z|00002|worker(worker)|INFO|worker process started
    2014-05-20T17:58:06Z|00002|reconnect|INFO|unix:/opt/deploy-ovs/var/run/openvswi
    tch/db.sock: connecting...
    2014-05-20T17:58:06Z|00003|reconnect|INFO|unix:/opt/deploy-ovs/var/run/openvswi
    tch/db.sock: connected
    2014-05-20T17:58:06Z|00004|bridge|INFO|ovs-vswitchd (Open vSwitch) 1.9.3

### OVS bridge setup

Create a bridge.

    deb:/opt# ovs/bin/ovs-vsctl --log-file add-br br0

    # ip addr
    1: lo:  mtu 16436 qdisc noqueue state UNKNOWN
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
        inet6 ::1/128 scope host
           valid_lft forever preferred_lft forever
    9: br0:  mtu 1500 qdisc noop state DOWN
        link/ether 9e:02:a8:45:81:40 brd ff:ff:ff:ff:ff:ff

### KVM guest setup

kvm guest networking setup is simple. No network definitions needs to be
provisioned in the host. The guest interface simply connects to the ovs bridge.
The xml for guest will include the interface definition as under:

```xml
<interface type='bridge'>
    <mac address='<MAC address>'/>
    <source bridge='<ovs bridge eg: br0>'/>
    <virtualport type='openvswitch'>
    <target dev='vnet0'/>
    <model type='virtio'/>
</interface>
```

Start the vmguest. Notice that the 'vnet0' is automatically added into
the ovs bridge br0.

     ovs-vsctl show
    55d241c9-1689-4535-b13b-556873e7089c
        Bridge "br0"
            Port "br0"
                Interface "br0"
                    type: internal
            Port "vnet0"
                Interface "vnet0"

### Connectivity setup

Now that the bridge is setup the interfaces needs to be assigned IP address
for connectivity. In this post static ip is allocated to the interfaces.
In the host.

    # ifconfig br0 10.0.0.1 netmask 255.255.255.0 up

In case of guests

    # ifconfig eth0 10.0.0.2 netmask 255.255.255.0 up

Now ping host to guest.

    # ping 10.0.0.2
    PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
    64 bytes from 10.0.0.2: icmp_req=1 ttl=64 time=0.722 ms
    64 bytes from 10.0.0.2: icmp_req=2 ttl=64 time=0.391 ms
    ^C
    --- 10.0.0.2 ping statistics ---
    2 packets transmitted, 2 received, 0% packet loss, time 999ms
    rtt min/avg/max/mdev = 0.391/0.556/0.722/0.167 ms

Guest and Host now communicate over ovs bridge.

### IP assignment with dnsmasq

[dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html "dnsmasq") is a
simple dns server that has an integrated dhcp and tftp server. dnsmasq
can be used to dynamically allocate IP address to vm guest.
In the example below we are reserving a range of IP address that will
be allocated to the vm guest as and when they request via dhclient
command.

    dnsmasq -R -h -p 0 -i br0 --dhcp-range=192.168.100.128,192.168.100.130 -d
    dnsmasq: started, version 2.71 DNS disabled
    dnsmasq: compile time options: IPv6 GNU-getopt no-DBus no-i18n no-IDN
    DHCP DHCPv6 no-Lua TFTP no-conntrack ipset auth no-DNSSEC
    dnsmasq-dhcp: DHCP, IP range 192.168.100.128 -- 192.168.100.130, lease time 1h
    dnsmasq-dhcp: DHCPDISCOVER(br0) 52:54:00:d7:2a:30
    dnsmasq-dhcp: DHCPOFFER(br0) 192.168.100.128 52:54:00:d7:2a:30
    dnsmasq-dhcp: DHCPREQUEST(br0) 192.168.100.128 52:54:00:d7:2a:30
    dnsmasq-dhcp: DHCPACK(br0) 192.168.100.128 52:54:00:d7:2a:30

In the example above the dnsmasq is started and will serve interface (-i
options) br0. DNS is not activated in the server and the ip range is specified
with the option --dhcp-range

### Alternate configuration for vm guest for using OVS

**Note: This did not work in Debian 7.5 (libvirt version 0.9.12.3)**

Alternatively the OVS definitions can be grouped inside a network
definition as under:

```xml
<network>
    <name>OVSNet</name>
    <forward mode='bridge'/>
    <bridge name='br0' />
    <virtualport type='openvswitch'/>
</network>
```

Guest VMs can then bind to this network. In the domain configuration of the
guest, the interface definition is changed as under:

```xml
<interface type='network'>
    <source network='OVSNet'/>
</interface>
```

References
----------

[Post](http://www.opencloudblog.com/?p=177 "kvm ovs") about ovs and kvm
integration.
