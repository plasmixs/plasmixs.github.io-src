Title: KVM guest migration using libvirt
Date: 2014-07-02 05:07
Tags: KVM, libvirt, Python
Slug: kvm-guest-migration-using-libvirt
Status: published

Libvirt provides APIs that can be used to migrate VM guest running on
one host to another seamlessly.

Side Note:
virsh command 'migrate' can be used to perform live migration of vm
guests.

    $ virsh migrate

Libvirt [page](http://libvirt.org/migration.html "libvirt migration")
details about the various migration techniques.

Essentially there are two main libvirt python APIs for performing
migration:
migrate and migrateToURI.
migrate (part of the domain class) migrates the domain name to a new
host based on the connection object.

```python
dest_connection = libvirt.open(dest_uri)
new_dom = dom.migrate(dest_connection, flags, None, None, 0)
dest_connection.close()
```

migrateToURI on the other hand takes a destination uri and manages the
connection internally.

```python
new_dom = dom.migrateToURI(dest_uri, flags, None, 0)
```

After a successful migration the new VM is visible in the host. This can
be verified by virsh list command.

Note: The flags determine the type of migration and also determine the
state of the VM during and after the migration.
