
# BRの作り方
## 基本
- vlan:exp1に所属
- ipv4: 202.0.73.51 - 80/24
- ipv6: RAに頼る

## アドレス割当
- br[1-30].sfc.wide.ad.jp
を予約．
- 202.0.73.51 - 81/24

## FRR
- area1のOSPFv2/v3に参加
    - Redistribute はNull0に向けたstatic routeを書く
```
Hello, this is FRRouting (version 6.0.3).
Copyright 1996-2005 Kunihiro Ishiguro, et al.

br01# show running-config
Building configuration...

Current configuration:
!
frr version 6.0.3
frr defaults traditional
hostname cloud-img-host2
log syslog informational
hostname br01
service integrated-vtysh-config
!
debug ospf6 neighbor
!
ip route 202.0.73.128/25 Null0
ipv6 route 64:ff9b:5322:601::/96 Null0
!
interface ens192
 ip ospf area 1.1.1.1
!
router ospf
 ospf router-id 202.0.73.30
 redistribute static
 area 1.1.1.1 range 202.0.73.0/25
!
router ospf6
 ospf6 router-id 202.0.73.30
 redistribute static
 area 1.1.1.1 range 2001:200:0:8831::/64
 interface ens192 area 1.1.1.1
!
line vty
!
end


```

## vcenter
テンプレート作成
Datastoreのパスはこちら
```
[datastore1 (hvs08)] br_init/build/br22.iso
```

# RRの作り方

## アドレス割当
- rr[1-4].sfc.wide.ad.jpを予約


# serverの作り方
60台Dockerで作る．
## アドレス割当
- 完全にRAに頼る.
    - translation prefixは一度A1SW1を経由して，hopさせる．
- Router-idは
    202.0.73.129 - 202.0.73.240


## Docker IPv6化
http://docs.docker.jp/engine/userguide/networking/default_network/ipv6.html

https://blog.komeho.info/2018/06/18/2110/

- proxy NDの有効
sudo vi /etc/sysctl.conf
```
net.ipv6.conf.ens192.proxy_ndp=1
```

- cat /etc/ndppd.conf
```
proxy ens192 {
  rule 2001:200:0:8831:1::/80 {
    static
  }
}
```

- service化
```
root@pod1:~# cat /lib/systemd/system/docker.service | grep ExecStart
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock --ipv6 --fixed-cidr-v6="2001:200:0:8831:1::/80"
```


- FRR導入
64のprefixをWIDEに流したら猛烈にバグったので，仕方なしにAnsibleでFRRを導入する
```
root@pod1:~# vtysh

Hello, this is FRRouting (version 7.2).
Copyright 1996-2005 Kunihiro Ishiguro, et al.

pod1# show running-config
Building configuration...

Current configuration:
!
frr version 7.2
frr defaults traditional
hostname pod1
log file /var/log/frr/frr.log informational
log syslog warnings
service integrated-vtysh-config
!
router ospf6
 ospf6 router-id 202.0.73.5
 area 1.1.1.1 range 2001:200:0:8831::/64
 interface ens192 area 1.1.1.1
!
line vty
!
end

```



# おまけ
- 1ライナーで時計とjoolの数を測定するヤツ

```
watch -n 0.5 'echo date:$(date +'%s.%N') ; bash -c "echo lines:$(jool_siit eamt display --csv --no-headers | wc -l)"'

```

ワンライナーでBGPの経路数とjoolの数を調べるヤツ
```bash
#!/bin/bash
cat << EOS
date: $(date +'%s.%3N')
jool: $(jool_siit eamt display --csv --no-headers | wc -l)
gobgpd: $(gobgp global rib -a ipv6 summary | grep Destination | awk '{print $2}')
EOS
```

CSV版
```
#!/bin/bash
cat << EOS
$(date +'%s.%3N'),$(gobgp global rib -a ipv6 summary | grep Destination | awk '{print $2}')$(jool_siit eamt display --csv --no-headers | wc -l)
EOS

```