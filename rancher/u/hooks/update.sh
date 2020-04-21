#!/bin/bash

cd /config
git pull && docker restart $(docker ps -q)