#!/usr/bin/env python3
import os
from pathlib import Path

containers = map(str.rstrip, os.popen("docker ps --format '{{.Names}}'").readlines())
with open('/config/changes.txt', 'r') as changes:
  rebuilds = {c.stem for r in changes if (c := Path(r)).parts[0] == 'compose'}
  reloads  = {c for r in changes if (c := Path(r).parts[0]) in containers}

  if rebuilds:
    os.popen(f'docker-compose -f /config/compose/docker-compose.yaml \
                              --project-directory=/config/compose \
                              up -d --remove-orphans')
  for container in reloads - rebuilds:
    os.popen(f'docker restart {container}')