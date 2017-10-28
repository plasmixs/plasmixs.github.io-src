Title: vm guest management using libvirt and python
Date: 2014-04-04 11:53
Tags: KVM, libvirt, Python
Slug: vm-guest-management-using-libvirt-and-python
Status: published

The post is in continuation of the earlier posts. Links to the earlier
[post1](http://plasmixs.wordpress.com/2013/10/11/vm-guest-creation-using-libvirt-tools/ "vm guest creation using libvirt tools") and
[post2](http://plasmixs.wordpress.com/2013/10/09/simple-script-for-starting-a-kvm-guest-with-custom-kernel-and-fs/ "Simple script for starting a KVM guest with custom kernel and fs")

[libvirt](http://libvirt.org/ "libvirt link") offers library and tools to
manage virtual machines. Libvirt extensions for python language are available
as part of the python-libvirt package. The package allows us to use python to
create and manage virtual machines that are independent of the underlying
hypervisor.

### Required python and libvirt versions

libvirt does not work with python 3.x yet. The following versions were used
during this post. These were tested under Debian 7.

To install libvirt and the python extensions under debian use the
apt-get command as under:

    apt-get install libvirt python-libvirt

### Obtaining Help on libvirt

The API reference for libvirt can be obtained anytime using the python help
function as under:

```python
    >>> import libvirt
    >>> help (libvirt)
```

This will display the built in documentation for libvirt. The documentation
can be quit anytime by pressing the 'q' switch.

More detailed document can be obtained from this site:
[libvirt documentation](http://libvirt.org/docs.html)

### Connection establishment

The first step is to connect to the libvirt daemon using the python-libvirt
package. The API to connect is **open**. The API returns a connection handler
that refers to this new connection. The connection handler is passed as
reference to the common APIs.

```python
    >>> import libvirt
    >>> conn_handler = libvirt.open("")
    >>> conn_handler
    libvirt.virConnect instance at 0xb39320
```

To close the connection use the **close** API.

```python
    >>> conn_handler.close()
    0
```

### Domain management

#### Define vm guest

The domain can be defined using the **defineXML** API of libvirt.
The API takes a XML description as the input.

```python
    >>> f=open("/Work/Contents/a.xml")
    >>> xml=f.read()
    >>> xml
    "<domain type='kvm'>\n ... "
    >>> dom_ref=conn_handler.defineXML(xml)
```

The contents of a.xml is shown below.

```xml
<domain type='kvm'>
  <name>test-vm</name>
  <memory unit='KiB'>524288</memory>
  <currentMemory unit='KiB'>524288</currentMemory>
  <vcpu placement='static'>1</vcpu>
  <os>
    <type arch='x86_64' machine='pc-1.1'>hvm</type>
    <boot dev='cdrom'/>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <pae/>
  </features>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>destroy</on_reboot>
  <on_crash>destroy</on_crash>
  <devices>
    <emulator>/usr/bin/kvm</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='raw'/>
      <source file='/Work/Contents/hd.ext3'/>
      <target dev='hda' bus='ide'/>
    </disk>
    <disk type='file' device='cdrom'>
      <driver name='qemu' type='raw'/>
      <source file='/Work/Contents/cd.iso'/>
      <target dev='hdc' bus='ide'/>
      <readonly/>
    </disk>
  </devices>
</domain>
```

The created domain can be viewed using the **listDefineDomains** API.

```python
    >>> conn_handler.listDefinedDomains()
    ['test-vm']
```

Notice the above APIs use the connection handler reference. In order to get
details about domains we need to use the domain reference in the APIs.

To get the XML for the domain use the **XMLDesc** API.

```python
    >>> dom_ref.XMLDesc(0)
    "<domain type='kvm'>\n ... "
```

To further get details about the domain use the **info** API.

```python
    >>> dom_ref.info()
    [5, 524288L, 524288L, 1, 0L]
```

The fields correspond to the following details.

1. Shows the state
2.  Max memory for the domain
3.  Current memory of the domain
4.  Current VCPUs for the domain and
5.  The CPU time i.e the amount of time the domain is running.


#### Domain undefine

To undefine the domain use **undefine** API with the domain reference.

```python
    >>> conn_handler.listDefinedDomains()
    ['test-vm']
    >>> dom_ref.undefine()
    >>> conn_handler.listDefinedDomains()
    []
```

After undefine the list does not show the domain.

### Further references

[IBM developer works article on KVM scripting with
python](http://www.ibm.com/developerworks/linux/library/os-python-kvm-scripting1/index.html?ca=drs-)
