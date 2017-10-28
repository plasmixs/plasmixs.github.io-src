Title: Vagrant and libvirt
Date: 2016-09-19
Tags: libvirt
Slug: vagrant
Status: draft

### Introduction

Vagrant is a tool that can help in
The post details running vagrant with the libvirt plugin.

#### Installation of Vagrant and the libvirt plugin

'''
$ vagrant plugin install vagrant-libvirt
Installing the 'vagrant-libvirt' plugin. This can take a few minutes...
'''

#### Importing a box image for the libvirt provider

The following command imports the Centos 7 box image.
The image can be obtained from the location:

'''
$ vagrant box add CentOS-7-x86_64-Vagrant-1609_01.LibVirt.box --name Centos7
==> box: Box file was not detected as metadata. Adding it directly...
==> box: Adding box 'Centos7' (v0) for provider:
    box: Unpacking necessary files from: file:///home/rameshd/Work/Disk_ISO/CentOS-7-x86_64-Vagrant-1609_01.LibVirt.box
==> box: Successfully added box 'Centos7' (v0) for 'libvirt'!
'''

### Running the imported box

'''
$ vagrant init Centos7; vagrant up --provider libvirt
A `Vagrantfile` has been placed in this directory. You are now
ready to `vagrant up` your first virtual environment! Please read
the comments in the Vagrantfile as well as documentation on
`vagrantup.com` for more information on using Vagrant.
Bringing machine 'default' up with 'libvirt' provider...
==> default: Uploading base box image as volume into libvirt storage...
==> default: Creating image (snapshot of base box volume).
==> default: Creating domain with the following settings...
==> default:  -- Name:              Disk_ISO_default
==> default:  -- Domain type:       kvm
==> default:  -- Cpus:              1
==> default:  -- Memory:            512M
==> default:  -- Management MAC:
==> default:  -- Loader:
==> default:  -- Base box:          Centos7
==> default:  -- Storage pool:      default
==> default:  -- Image:             /var/lib/libvirt/images/Disk_ISO_default.img (41G)
==> default:  -- Volume Cache:      default
==> default:  -- Kernel:
==> default:  -- Initrd:
==> default:  -- Graphics Type:     vnc
==> default:  -- Graphics Port:     5900
==> default:  -- Graphics IP:       127.0.0.1
==> default:  -- Graphics Password: Not defined
==> default:  -- Video Type:        cirrus
==> default:  -- Video VRAM:        9216
==> default:  -- Keymap:            en-us
==> default:  -- TPM Path:
==> default:  -- INPUT:             type=mouse, bus=ps2
==> default:  -- Command line :
==> default: Creating shared folders metadata...
==> default: Starting domain.
==> default: Waiting for domain to get an IP address...
==> default: Waiting for SSH to become available...
    default:
    default: Vagrant insecure key detected. Vagrant will automatically replace
    default: this with a newly generated keypair for better security.
    default:
    default: Inserting generated public key within guest...
    default: Removing insecure key from the guest if it's present...
    default: Key inserted! Disconnecting and reconnecting using new SSH key...
==> default: Configuring and enabling network interfaces...
==> default: Rsyncing folder: /home/r/Work/Disk_ISO/ => /vagrant
'''

SSH into the box

'''
$ vagrant ssh
[vagrant@localhost ~]$ ll
total 0
'''

Cleanup is via the vagrant destroy command

'''
$ vagrant destroy
==> default: Removing domain...
'''


### References

1.  Python3
    [packaging](http://www.diveintopython3.net/packaging.html "packaging") documentation.
