#!/bin/bash

ansible-playbook -i hosts pods.yml

ansible-playbook -i hosts add_server.yml

for i in `seq 0 20`
do
    ansible-playbook -i hosts experiment_add_server.yml
done

for i in `seq 0 20`
do
    ansible-playbook -i hosts experiment_remove_server.yml
done