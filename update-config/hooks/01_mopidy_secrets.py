#!/usr/bin/env python3
import yaml
import os
import re

files = ["/config/mopidy/mat/mopidy.conf",
         "/config/mopidy/jessie/mopidy.conf",
         "/config/mopidy/guest/mopidy.conf"]

placeholder = re.compile(r"$\{(?P<path>.+?)\}")

with open("/config/mopidy/secrets.yaml", 'r') as stream:
  secrets = yaml.safe_load(stream)

for filepath in files:
  with open(filepath, 'r') as config:
    configdata = config.read()
  replacements = [m.group('path') for m in placeholder.finditer(configdata)]
  for replacement in replacements:
    value = secrets
    for segment in replacement.split('.'):
      value[segment]
    configdata.replace(r"${" + replacement + r"}", value)
  with open(filepath, 'w') as config:
    config.write(configdata)