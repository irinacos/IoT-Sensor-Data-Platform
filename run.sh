#!/bin/bash

export SCD_DVP=/var/lib/docker/volumes

# Adresa IP (default localhost) a nodului manager
IP_ADDRESS="127.0.0.1"

# Crearea imaginii pentru adaptor
docker build -t adapter_image:latest ./adapter

# Initializare Docker Swarm (daca nu este deja initializat)
if ! docker info | grep -q "Swarm: active"; then
    docker swarm init --advertise-addr $IP_ADDRESS --listen-addr $IP_ADDRESS:2377
fi

docker stack deploy -c stack.yml scd3