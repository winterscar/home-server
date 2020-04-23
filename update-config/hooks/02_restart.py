#!/usr/bin/env python3
import os

with open('/config/changes.txt', 'r') as changes:
  # Get running containers
  containers = []
  for container in os.popen("docker ps --format '{{.Names}}'").readlines():
    containers.append(container.rstrip())
  
  for file in changes:
    path = file.rstrip()
    if path.split('/')[0] == "compose":
      service = os.path.splitext(os.path.basename(path))[0]
      os.popen(f'docker-compose -f /config/compose/docker-compose.yaml \
       up -d --remove-orphans {service}')
    elif path.split('/')[0] in containers:
      os.popen(f'docker restart {path.split('/')[0]}')