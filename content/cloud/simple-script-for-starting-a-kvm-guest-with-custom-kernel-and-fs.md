Title: Simple script for starting a KVM guest with custom kernel and fs
Date: 2013-10-09 19:52
Tags: KVM, Shell
Slug: simple-script-for-starting-a-kvm-guest-with-custom-kernel-and-fs
Status: published

The script can be used to start a kvm guest with a specific kernel and file
system images. It also enables one user network link between the host and
the guest.

To install kvm in debian issue

    $apt-get install kvm

Copy the contents to a file and run it as a script.
This script is tested in debian 7.1

```bash
#!/bin/sh

#Assumption is that all the kernel and the file system image are under this
#directory.
IMAGE_PATH=$PWD/Images/

#Specify the kernel image
KERNEL="-kernel $IMAGE_PATH/bzImage"

#File system image. Example is specified with an ext3 raw harddisk image.
FS="-hda $IMAGE_PATH/virtcluster-x86vm.ext3"

APPEND_CMD="vga=0 root=/dev/hda"

#Enable the full virtulization of KVM. Needs hardware support.
#check grep "vmx" /proc/cpuinfo.
FULL_KVM="-enable-kvm"

#link details. The network (user level) between host and the guest.
#Using the virtio pci device. We can also use e1000 or rtl devices.
#check kvm -device? for device support.
LNK_NET_MODEL="virtio-net-pci"

#Macaddress of the interface.
LNK0_MAC_ADDR="00:16:3e:00:00:00"

# The ID is just a reference for the device.
LNK0_ID=net0

#net 0 details
NET0_DEVICE="-device $LNK_NET_MODEL,netdev=$LNK0_ID,mac=$LNK0_MAC_ADDR"
NET0="-netdev user,id=$LNK0_ID $NET0_DEVICE"

#Old obselete method.
#NET0="-net nic,model=$LNK_NET_MODEL,vlan=1,macaddr=$LNK0_MAC_ADDR"

#Machine name to be displayed on the top of the qemu window.
MACHINE_NAME="-name x86vm"

#Set smp option two cores.
SMP_OPTION=-smp 2

#Start the kvm (qemu-kvm).
#Incase kvm is not use qemu instead of kvm.
kvm $KERNEL $FS --append "$APPEND_CMD"\
    $NET0 $NET1\
    $FULL_KVM $SMP_OPTION\
    $MACHINE_NAME
```

A new SDL window opens that shows qemu/kvm booting the image.

### Reference links

1.  <http://www.linux-kvm.org/page/Networking>
2.  <http://pic.dhe.ibm.com/infocenter/lnxinfo/v3r0m0/index.jsp?topic=%2Fliaat%2Fliaatbptap.htm>
3.  <https://wiki.debian.org/KVM>

