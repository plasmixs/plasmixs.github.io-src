Title: Simplifying OpenvSwitch setup with network namespaces
Date: 2016-08-13 3:55
Tags: OpenvSwitch, namespaces
Slug: network-namespaces-ovs
Status: published

[Namespaces](http://man7.org/linux/man-pages/man7/namespaces.7.html "namespace man page") in general have become extremly pervasive. They are fundamental to the container concepts and network namespaces form a very important part of the Openstack Neutron component.
They are also quite handy to setup quick test setups, especially when teamed with the openvswitch.

[ip netns](http://man7.org/linux/man-pages/man8/ip-netns.8.html "ip-netns man page") allows users to create persistent network namespaces. The post talks about creating two network namespaces and attaching them to an ovs bridge via the [veth](https://lwn.net/Articles/232688/ "veth commit diff") (Virtual ETHernet) interfaces. [ip link](http://linux-ip.net/html/tools-ip-link.html "ip link help") command lets you create the veth interfaces and also associate the veth interface to a namespace.

Start by adding a ovs bridge named br0.

```
$ sudo ovs-vsctl add-br br0
$ sudo ovs-vsctl show
4bdbff89-3663-42c3-a580-ad31ea3cf166
    Bridge "br0"
        Port "br0"
            Interface "br0"
                type: internal
```

Create two namespaces ns1 and ns2.

    $ sudo ip netns add ns1
    $ sudo ip netns add ns2

List the created namespaces.

    $ ip netns list
    ns2
    ns1

Create the veth pairs.

    $ sudo ip link add vns1 type veth peer name vpeerns1
    $ sudo ip link add vns2 type veth peer name vpeerns2

verify the interfaces with the ip link command

Add the peer interfaces to the corresponding namespaces.

    $ sudo ip link set vpeerns1 netns ns1
    $ sudo ip link set vpeerns2 netns ns2

Verify that that the interfaces are added to the namespace using ip command.

ex:

```
$ sudo ip netns exec ns1 ip link
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
18: vpeerns1@if19: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 8e:1a:37:c3:29:73 brd ff:ff:ff:ff:ff:ff link-netnsid 0
```

Bring up the interfaces.

    $ sudo ip link set vns1 up
    $ sudo ip link set vns2 up

Assign ip addresses to the interfaces in the namespaces.

    $ sudo ip netns exec ns1 ip addr add 1.1.1.1/24 dev vpeerns1
    $ sudo ip netns exec ns1 ip link set vpeerns1 up

Verify it using ip addr

```
$ sudo ip netns exec ns1 ip addr
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
18: vpeerns1@if19: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 8e:1a:37:c3:29:73 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 1.1.1.1/24 scope global vpeerns1
       valid_lft forever preferred_lft forever
```

Similarly assign ip for the other namespace as well.

    $ sudo ip netns exec ns2 ip addr add 1.1.1.2/24 dev vpeerns2
    $ sudo ip netns exec ns2 ip link set vpeerns2 up

Try pinging the other interface from one namespace. This will fail since the host will not forward packets from one namespace to other by default. IP forwarding can be enabled as follows in the host machine.

    $echo 1 > /proc/sys/net/ipv4/ip_forward

Now lets add the veth interfaces to OVS bridge

    $ sudo ovs-vsctl add-port br0 vns1
    $ sudo ovs-vsctl add-port br0 vns2

verify now

```
$ sudo ovs-vsctl show
4bdbff89-3663-42c3-a580-ad31ea3cf166
    Bridge "br0"
        Port "vns1"
            Interface "vns1"
        Port "br0"
            Interface "br0"
                type: internal
        Port "vns2"
            Interface "vns2"
```

By default the "NORMAL" actions flow is available in the bridge.

```
$ sudo ovs-ofctl dump-flows br0
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=13357.785s, table=0, n_packets=0, n_bytes=0, idle_age=13357, priority=0 actions=NORMAL
```

Now the ping works due to the above flow installed in the bridge.

```
$ sudo ip netns exec ns1 ping 1.1.1.2 -c 1
PING 1.1.1.2 (1.1.1.2) 56(84) bytes of data.
64 bytes from 1.1.1.2: icmp_seq=1 ttl=64 time=14.5 ms

--- 1.1.1.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 14.507/14.507/14.507/0.000 ms

$ sudo ovs-ofctl dump-flows br0
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=13641.380s, table=0, n_packets=6, n_bytes=364, idle_age=71, priority=0 actions=NORMAL
```

###Example with vlan match and OpenFlow actions###

Set VLAN 100 for one namespace and 200 for the other namespace.

    $ sudo ip netns exec ns1 ip link add link vpeerns1 name vpeerns1.100 type vlan id 100
    $ sudo ip netns exec ns2 ip link add link vpeerns2 name vpeerns2.200 type vlan id 200

Assign new IPs for the VLAN interfaces

    $ sudo ip netns exec ns1 ip addr add 2.2.2.1/24 dev vpeerns1.100
    $ sudo ip netns exec ns1 ip link set vpeerns1.100 up

    $ sudo ip netns exec ns2 ip addr add 2.2.2.2/24 dev vpeerns2.200
    $ sudo ip netns exec ns2 ip link set vpeerns2.200 up

Pinging now fails between the vlan interfaces, since we need to pop incoming vlan tag 100 and push a new vlan tag 200 to reach the other interface. Similarly the reverse flow also needs to be installed. The flows will be installed via the ovs-ofctl command. Alternativly the mod_vlan_vid can also be used in ovs to acheive the same.

```
$ sudo ip netns exec ns1 ping 2.2.2.2 -c 1
PING 2.2.2.2 (2.2.2.2) 56(84) bytes of data.

--- 2.2.2.2 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 0ms
```

First clear all the existing flows in ovs bridge.

    $ sudo ovs-ofctl del-flows br0

Add flow to match packets from ns1

    $ sudo ovs-ofctl -O openflow13 add-flow br0 "dl_vlan=100 actions=mod_vlan_vid:200,output:2"
    $ sudo ovs-ofctl -O openflow13 add-flow br0 "dl_vlan=200 actions=mod_vlan_vid=100,output:1"

Note: To find out the port numbers use dump-ports as under

    $ sudo ovs-ofctl dump-ports br0

Once the flows are installed the ping now passes through.

```
$ sudo ip netns exec ns2 ping 2.2.2.1 -c 1
PING 2.2.2.1 (2.2.2.1) 56(84) bytes of data.
64 bytes from 2.2.2.1: icmp_seq=1 ttl=64 time=5.85 ms

--- 2.2.2.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 5.855/5.855/5.855/0.000 ms
```
Flow dump is as follows

```
$ sudo ovs-ofctl dump-flows br0
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=1710.499s, table=0, n_packets=14, n_bytes=1068, idle_age=21, dl_vlan=200 actions=mod_vlan_vid:100,output:1
 cookie=0x0, duration=1687.621s, table=0, n_packets=24, n_bytes=1216, idle_age=21, dl_vlan=100 actions=mod_vlan_vid:200,output:2
```

####References:####
1. <https://blogs.igalia.com/dpino/2016/04/10/network-namespaces/>
+  <http://blog.scottlowe.org/2013/09/04/introducing-linux-network-namespaces/>
+  <https://lwn.net/Articles/580893/>
+  <http://www.opencloudblog.com/?p=66>
