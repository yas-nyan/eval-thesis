#!/bin/bash
for i in `seq 0 100`
do
    ansible-playbook -i hosts experiment_remove_server.yml
    sleep 1
done
