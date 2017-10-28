Title: RAW sockets programming in C
Date: 2014-10-11 16:20
Tags: C, sockets
Slug: raw-sockets-programming-in-c
Status: published

### Introduction

RAW sockets can be used to fetch packets with all layer headers intact.
The code below illustrates an example where packets are read from one
interface (eth0) and transmitted to another interface (eth1).

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <sys/socket.h>
#include <net/if.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <arpa/inet.h>

static int s = -1;
static int s1 = -1;

void onexit(int signum)
{
    (void)signum;
    printf("Exiting");
    close(s);
    close(s1);
}

int main()
{
    char buf[1600];
    ssize_t recv_size = -1;
    ssize_t send_size = -1;

    int i = 0;

    struct sockaddr_ll socket_address, socket_address1;

    s = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    s1 = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));

    if ((s == -1) || (s1 == -1))
    {
        perror("Socket creation failed");
        exit (0);
    }

    signal(SIGINT, onexit);

    memset(&socket_address, 0, sizeof (socket_address));
    socket_address.sll_family = PF_PACKET;
    socket_address.sll_ifindex = if_nametoindex("eth0");
    socket_address.sll_protocol = htons(ETH_P_ALL);

    i = bind(s, (struct sockaddr*)&socket_address,
    sizeof(socket_address));
    if (i == -1)
    {
        perror("Bind");
        exit (0);
    }

    memset(&socket_address1, 0, sizeof (socket_address1));
    socket_address1.sll_family = PF_PACKET;
    socket_address1.sll_ifindex = if_nametoindex("eth1");
    socket_address1.sll_protocol = htons(ETH_P_ALL);

    i = bind(s1, (struct sockaddr*)&socket_address1,
    sizeof(socket_address1));
    if (i == -1)
    {
        perror("Bind");
        exit (0);
    }

    while (1)
    {
        memset(&buf, 0, sizeof(buf));

        recv_size = recv(s, &buf, sizeof(buf), 0);
        if (recv_size == -1)
        {
            perror("Socket receive");
            exit (0);
        }

        printf("\n");
        for(i=0; i &lt; recv_size; i++)
        {
            printf("%02x ", buf[i]);
        }

        send_size = send(s1, &buf, recv_size, 0);
        if (send_size == -1)
        {
            perror("Socket send");
            exit (0);
        }
    }

    return 0;
}
```

The socket call creates a raw socket (SOCK_RAW specifies this).
Note: SOCK_PACKET is now obsolete.
Once the socket is created it is bounded to an interface using 'bind'.
Other possible ways to bind to an interface is via the setsockopt.
Examples of setsockopt:

```c
char *opt;
opt = "eth0";
setsockopt(sd, SOL_SOCKET, SO_BINDTODEVICE, opt, 4);
```

Note: There are suggestions to also use struct ifreq instead of the char *opt.

```c
struct ifreq ifr;
memset(&ifr, 0, sizeof(ifr));
snprintf(ifr.ifr_name, sizeof(ifr.ifr_name), "eth1");
setsockopt(sd, SOL_SOCKET, SO_BINDTODEVICE, (void *)&ifr,
sizeof(ifr));
```

Once the sockets are binded we can use 'send' and 'recv' calls for sending and
receiving packets respectively.

Some Raw sockets references:

1.  [Raw sockets in
    C](http://www.binarytides.com/raw-sockets-c-code-linux/ "Raw Sockets in C")
2.  [Raw Sockets C
    Examples](http://www.pdbuchan.com/rawsock/rawsock.html "Raw sockets C Examples")