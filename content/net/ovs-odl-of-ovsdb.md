Title: OpenDaylight and OpenvSwitch interation via OVSDB and OpenFlow
Date: 2016-08-15 3:30
Tags: OpenvSwitch, SDN controller
Slug: ovs-odl-of-ovsdb
Status: published

[OpenDaylight](https://www.opendaylight.org/) a JAVA based SDN controller exposes multiple south bound interfaces for talking to network elements. [OpenFlow](https://www.opennetworking.org/sdn-resources/openflow) is a ONF standardised control protocol. [OVSDB](https://tools.ietf.org/html/rfc7047) defined as an IETF RFC form the management part of the [OpenvSwitch](http://openvswitch.org/).

>Note:
>install the following features in karaf:
>odl-ovsdb-southbound-impl-rest and odl-openflowplugin-flow-services-rest

##OVSDB configuration##

ODL can connect to the [ovsdb-server](http://openvswitch.org/support/dist-docs/ovsdb-server.1.txt) running in the ovs host either in an active mode or in passive mode.

>Note
>The following arguments to ovsdb-server are important.

```
--remote=punix:/usr/local/var/run/openvswitch/db.sock \
--remote=db:Open_vSwitch,Open_vSwitch,manager_options \
--private-key=db:Open_vSwitch,SSL,private_key \
--certificate=db:Open_vSwitch,SSL,certificate \
--bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert
```

The second "--remote" specifies that the configuration for a remote ovsdb conection can be set using the ovs-vsctl set-manager sub command. If its missing it can be added as under

    $sudo ovs-appctl -t ovsdb-server ovsdb-server/add-remote db:Open_vSwitch,Open_vSwitch,manager_options

In active mode the ODL controller connects to the OVS instance of ovsdb-server.
Configure OVS to listen on a passive connection

    $ovs-vsctl set-manager ptcp:6640

Configure ODL to connect to ovs.

    $ curl -X PUT -H "Content-Type: application/json" -H "Application/json" -d@connect.json -u admin:admin http://<controller ip>.20:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2Fhost1

contents of the connect.json file is as under:

```
{
  "node": [
  {
    "node-id": "ovsdb://host1",
    "connection-info":
    {
      "ovsdb:remote-ip": "192.168.100.10",
      "ovsdb:remote-port": 6640
    }
  }
  ]
}
```

The GET verb lists the connected node in the above curl command.

In the passive mode, OVS connects to an ODL instance (6640 is the IANA registered port for ovsdb). This is set as follows:

    $sudo ovs-vsctl set-manager tcp:<controller ip>:6640

In both cases verify the connection status with the ovs-vsctl command

```
$ sudo ovs-vsctl show4bdbff89-3663-42c3-a580-ad31ea3cf166
    Manager "tcp:192.168.100.20:6640"
        is_connected: true

or

$ sudo ovs-vsctl show
4bdbff89-3663-42c3-a580-ad31ea3cf166
    Manager "ptcp:6640"
        is_connected: true
```

Using OVSDB the bridge, port and controller configurations can be set in OVS.
The configurations will be sent to the controller using the NorthBound RESTCONF APIs.

Create a bridge br0 using restconf.

    $ curl -X PUT -H "Content-Type: application/json" -H "Application/json" -d@br.json -u admin:admin http://<controller ip>:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2Fhost1%2Fbridge%2Fbr0

contents of br.json is as under:

```
{
  "network-topology:node": [
  {
    "node-id": "ovsdb://host1/bridge/br0",
    "ovsdb:bridge-name": "br0",
    "ovsdb:managed-by": "/network-topology:network-topology/network-topology:topology[network-topology:topology-id='ovsdb:1']/network-topology:node[network-topology:node-id='ovsdb://host1']"
  }
  ]
}
```

Addition of a vxlan ports to bridge via restconf

    $ curl -X PUT -H "Content-Type: application/json" -H "Application/json" -d@port.json -u admin:admin http://<controller ip>:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2Fhost1%2Fbridge%2Fbr0/termination-point/vxlan0/

contents of port.json is:

```
{
  "network-topology:termination-point": [
    {
      "tp-id": "vxlan0",
      "ovsdb:options": [
        {
          "ovsdb:option": "remote_ip",
          "ovsdb:value" : "flow"
        },
        {
          "ovsdb:option": "key",
          "ovsdb:value" : "flow"
        }
      ],
      "ovsdb:name": "vxlan0",
      "ovsdb:interface-type": "ovsdb:interface-type-vxlan",
      "ovsdb:ofport_request": 1
    }
  ]
}
```

verify in ovs:

```
$ sudo ovs-vsctl show
    Manager "ptcp:6640"
        is_connected: true
    Bridge "br0"
        Controller "tcp:192.168.100.20:6653"
            is_connected: true
        fail_mode: secure
        Port "vxlan0"
            Interface "vxlan0"
                type: vxlan
                options: {key=flow, remote_ip=flow}
        Port "br0"
            Interface "br0"
                type: internal
```

Adding a simple port via restconf is same. The port.json now contains

```
{
  "network-topology:termination-point": [
    {
      "tp-id": "vns2",
      "ovsdb:name": "vns2",
      "ovsdb:ofport_request": 3
    }
  ]
}
```

Connect bridge to controller via restconf

    $ curl -X PUT -H "Content-Type: application/json" -H "Application/json" -d@controller.json -u admin:admin http://<controller ip>:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2Fhost1%2Fbridge%2Fbr0

contents of controller.json is as under:

```
{
  "network-topology:node": [
  {
    "node-id": "ovsdb://host1/bridge/br0",
    "ovsdb:bridge-name": "br0",
    "ovsdb:fail-mode": "ovsdb-fail-mode-secure",
    "ovsdb:protocol-entry": [
      {
        "protocol": "ovsdb:ovsdb-bridge-protocol-openflow-13"
      }
    ],
    "ovsdb:bridge-other-configs": [
      {
        "bridge-other-config-key": "datapath-id",
        "bridge-other-config-value": "0000000000000001"
      }
    ],
    "ovsdb:controller-entry": [
      {
        "target": "tcp:<controller ip>:6653"
      }
    ]
  }
  ]
}
```

##OpenFlow configuration##

Flow addition via ODL can be done either via the config store (and eventually RPC) or by directly invoking the RPC (bypassing the config store). The former has the advantage that the flows are persisted. The [page](https://wiki.opendaylight.org/view/OpenDaylight_OpenFlow_Plugin:User_Guide/Flow_Configuration) details the advantages and disadvantages of both methods.

Installing a default flow to redirect non-matching packets to controller.

    $ curl -X PUT -H "Content-Type: application/xml" -H "Application/xml" -d@flow.xml -u admin:admin http://<controller ip>:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/1

The contents of the flow.xml is as under:

```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<flow xmlns="urn:opendaylight:flow:inventory">
  <priority>10</priority>
  <flow-name>default-catch-all</flow-name>
  <match>
    <ethernet-match>
      <ethernet-type>
        <type>2048</type>
      </ethernet-type>
    </ethernet-match>
  </match>
  <id>1</id>
  <table_id>0</table_id>
  <instructions>
    <instruction>
      <order>0</order>
      <apply-actions>
        <action>
          <order>0</order>
          <output-action>
            <output-node-connector>CONTROLLER</output-node-connector>
            <max-length>60</max-length>
          </output-action>
        </action>
      </apply-actions>
    </instruction>
  </instructions>
</flow>
```

Verify this flow in ovs.

```
$ sudo ovs-ofctl dump-flows br0 -OOpenFlow13
OFPST_FLOW reply (OF1.3) (xid=0x2):
 cookie=0x0, duration=11.976s, table=0, n_packets=0, n_bytes=0, priority=10,ip actions=CONTROLLER:60
```

Example of flow additions for the vlan based topology described in this [article](http://plasmixs.github.io/network-namespaces-ovs.html)

    $ curl -X POST -H "Content-Type: application/xml" -H "Application/xml" -d@flow.xml -u admin:admin http://<controller ip>:8181/restconf/operations/sal-flow:add-flow
    $ curl -X POST -H "Content-Type: application/xml" -H "Application/xml" -d@flow1.xml -u admin:admin http://<controller ip>:8181/restconf/operations/sal-flow:add-flow

contents of flow.xml and flow1.xml are as under:

```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<input xmlns="urn:opendaylight:flow:service">
  <barrier>false</barrier>
  <node xmlns:inv="urn:opendaylight:inventory">/inv:nodes/inv:node[inv:id="openflow:1"]</node>

  <cookie>55</cookie>
  <hard-timeout>0</hard-timeout>
  <idle-timeout>0</idle-timeout>
  <installHw>false</installHw>

  <match>
    <vlan-match>
      <vlan-id>
	      <vlan-id>100</vlan-id>
	      <vlan-id-present>true</vlan-id-present>
      </vlan-id>
      <vlan-pcp>0</vlan-pcp>
    </vlan-match>
  </match>

  <instructions>

    <instruction>
      <order>0</order>

      <apply-actions>
	      <action>
	        <order>0</order>
	        <pop-vlan-action/>
	      </action>
      </apply-actions>

    </instruction>

    <instruction>
      <order>1</order>

      <write-metadata>
        <metadata>200</metadata>
        <metadata-mask>0xff</metadata-mask>
      </write-metadata>
    </instruction>

    <instruction>
      <order>2</order>
      <go-to-table>
	      <table_id>1</table_id>
      </go-to-table>
    </instruction>

  </instructions>

  <priority>20</priority>
  <strict>false</strict>
  <table_id>0</table_id>
</input>
```

and

```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<input xmlns="urn:opendaylight:flow:service">
  <barrier>false</barrier>
  <node xmlns:inv="urn:opendaylight:inventory">/inv:nodes/inv:node[inv:id="openflow:1"]</node>

  <cookie>55</cookie>
  <hard-timeout>0</hard-timeout>
  <idle-timeout>0</idle-timeout>
  <installHw>false</installHw>
  
  <match>
    <metadata>
      <metadata>200</metadata>
      <metadata-mask>0xFF</metadata-mask>
    </metadata>
  </match>
  
  <instructions>
    
    <instruction>
      <order>0</order>
      
      <apply-actions>
        <action>
          <order>1</order>
          <push-vlan-action>
            <ethernet-type>0x8100</ethernet-type>
          </push-vlan-action>
        </action>

        <action>
          <order>2</order>
          <set-field>
            <vlan-match>
              <vlan-id>
                <vlan-id>200</vlan-id>
                <vlan-id-present>true</vlan-id-present>
              </vlan-id>
            </vlan-match>
          </set-field>
        </action>

        <action>
          <order>3</order>
          <output-action>
            <output-node-connector>3</output-node-connector>
          </output-action>
        </action>
      </apply-actions>

    </instruction>

  </instructions>
  
  <priority>20</priority>
  <strict>false</strict>
  <table_id>1</table_id>
</input>

```

The reverse flows can also be added by reversing the VLAN id in the match and action fields.
Verify the flows from ovs.

```
$ sudo ovs-ofctl dump-flows br0 -OOpenFlow13
OFPST_FLOW reply (OF1.3) (xid=0x2):
 cookie=0x37, duration=531.922s, table=0, n_packets=2, n_bytes=148, priority=20,dl_vlan=100,dl_vlan_pcp=0 actions=pop_vlan,write_metadata:0xc8/0xff,goto_table:1
 cookie=0x37, duration=114.503s, table=0, n_packets=2, n_bytes=148, priority=20,dl_vlan=200,dl_vlan_pcp=0 actions=pop_vlan,write_metadata:0x64/0xff,goto_table:1
 cookie=0x0, duration=2017.154s, table=0, n_packets=0, n_bytes=0, priority=10,ip actions=CONTROLLER:60
 cookie=0x37, duration=385.238s, table=1, n_packets=2, n_bytes=148, priority=20,metadata=0xc8/0xff actions=push_vlan:0x8100,set_field:4296->vlan_vid,output:3
 cookie=0x37, duration=109.592s, table=1, n_packets=2, n_bytes=148, priority=20,metadata=0x64/0xff actions=push_vlan:0x8100,set_field:4196->vlan_vid,output:2
```

Verify the connectivity by pinging

```
$ sudo ip netns exec ns2 ping 2.2.2.1 -c 1
PING 2.2.2.1 (2.2.2.1) 56(84) bytes of data.
64 bytes from 2.2.2.1: icmp_seq=1 ttl=64 time=1.51 ms

--- 2.2.2.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 1.514/1.514/1.514/0.000 ms
```

####References:####
1. <https://wiki.opendaylight.org/view/OpenDaylight_OpenFlow_Plugin:Main>
2. <http://docs.opendaylight.org/en/stable-boron/user-guide/openflow-plugin-project-user-guide.html>
3. <http://docs.opendaylight.org/en/stable-boron/user-guide/ovsdb-netvirt.html>
