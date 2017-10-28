Title: KVM guest networking - DHCP
Date: 2014-05-20 11:05
Tags: KVM
Slug: kvm-guest-networking-dhcp
Status: published

The posts lists the required xml for managing guest ip address assignment
using dhcp.
A new network 'nwk0' is defined in kvm. The network has dhcp configurations
as under:

* ip address assignment start from 192.168.100.128 to 192.168.100.130.
* A MAC address is binded with the appropriate ip address.
* Internal bridge device is assigned an ip of 192.168.100.1. This allows guest
to host communications.

The XML for the network is defined as under:

```xml
<network>
  <name>nwk0</name>
  <bridge name='br00' stp='on' delay='0' />
  <mac address='52:54:00:89:B1:69'/>
  <ip address='192.168.100.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.100.128' end='192.168.100.130' />
      <host mac='52:54:00:d7:2a:30' name='doma0' ip='192.168.100.128'/>
    </dhcp>
  </ip>
</network>
```

The interface part of the domain XML for a guest machine, which connects to
this network is defined as under:

```xml
<interface type='network'>
  <mac address='52:54:00:d7:2a:30'/>
  <source network='nwk0'/>
  <model type='virtio'/>
</interface>
```

Now when the guest machine boots up it would be auto-assigned the ip
address '192.168.100.128'.
