Title: vm guest creation using libvirt tools
Date: 2013-10-11 11:14
Tags: KVM, libvirt
Slug: vm-guest-creation-using-libvirt-tools
Status: published

In the earlier post the creation of vm guest from the command line
(using kvm or qemu command) was discussed. [Link to earlier
post.](http://plasmixs.wordpress.com/2013/10/09/simple-script-for-starting-a-kvm-guest-with-custom-kernel-and-fs/ "Simple script for starting a KVM guest with custom kernel and fs")
The current post is about creating and managing vm guests using the
virt-installer and virsh commands. The commands are based on libvirt
library.

### Creation of a virtual machine

The creation of a new vm can be done using the command virt-install.
The commands are part of the virt-manager package in Debian. To install the
package in debian use the following command.

    #apt-get install virt-manager

In the example below a new vm is created using the virt-install command.
The vm uses the specified file system and kernel images. The command
creates the vm and starts it instantly.

    $ virt-install --name=x86vm
                  --ram=512 --vcpus=2,maxvcpus=2 --cpu host
                  --import
                 --boot kernel=$PWD/bzImage,kernel_args="vga=0 root=/dev/hda"
                  --disk=./virtcluster-x86vm.ext3
                  --network=user,model=virtio,mac=RANDOM
                  --graphics sdl

    Starting install...
    Creating domain...                                       |    0 B     00:00
    Domain creation completed. You can restart your domain by running:
      virsh --connect qemu:///session start x86vm

The vm can now be managed with the virsh. To list the vm created use the
list option in virsh command.

    $ virsh list --all
     Id    Name                           State
    ----------------------------------------------------
     1     x86vm                          running

### XML definitions

The xml definition of the vm can be obtained during the vm creation
(virt-install). It can also be obtained while it is running using virsh
command.

The --print-xml option in the virt-install command prints the xml
definition for the vm.

    $ virt-install --name=x86vm
           --ram=512
          --boot kernel=/tmp/bzImage,kernel_args="vga=0 root=/dev/hda"
          --disk=/tmp/x86vm.ext3 --network=user,model=virtio
          --graphics sdl
          --dry-run --print-xml

    ...xml contents...

The xml from virsh command can be obtained by the dumpxml option to
virsh.

    $ virsh dumpxml x86vm

    ...xml contents ..

Note: Once the vm gets defined in, the recommended way to modify the xml
is via virsh edit command.

### Destroy and Undefine

The vm can be destroyed and the name (ID and UUID) freed using the virsh
destroy followed by virsh undefine commands

    $virsh destroy x86vm
    Domain x86vm destroyed

    $virsh undefine x86vm
    Domain x86vm has been undefined

### Virtual image builder

virt-install creates a vm machine.
virt-builder (part of the guestfs tools) is used to build virtual
images from pre-configured distro templates.
More information on the following pages:

1.  <http://libguestfs.org/>
2.  <http://rwmj.wordpress.com/>
3.  <http://kashyapc.com/2014/01/27/virt-builder-to-trivially-create-various-linux-distribution-guest-images/>

### References

1.  <http://linux.die.net/man/1/virt-installation>
2.  <http://acidborg.wordpress.com/2010/02/19/how-to-manage-kvm-virtual-machines-using-virsh/>