#!/usr/bin/env python3
import os
from pathlib import Path
from subprocess import check_call, check_output

# docker commands
d_ps = ['docker', 'ps', '--format', '{{.Names}}']
d_compose = ['docker-compose', '-f',  '/config/compose/docker-compose.yaml',
                              '--project-directory=/config/compose'
                              'up', '-d', '--remove-orphans']
d_restart = ['docker', 'restart']

containers = {c for c in check_output(d_ps, text=True).split('\n')}
with open('/config/changes.txt', 'r') as f:
  changes = [line.strip() for line in f]
  rebuilds = {c.stem for r in changes if (c := Path(r)).parts[0] == 'compose'}
  reloads  = {c for r in changes if (c := Path(r).parts[0]) in containers}

  if rebuilds:
    check_call(d_compose)
  for container in reloads - rebuilds:
    check_call(d_restart + container)