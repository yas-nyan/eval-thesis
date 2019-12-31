#!/bin/bash
while true;
do
cat << EOS
$(date +'%s.%3N'),$(gobgp global rib -a ipv6 summary | grep Destination | awk '{print $2}')$(jool_siit eamt display --csv --no-headers | wc -l)
EOS
sleep 0.2s
done