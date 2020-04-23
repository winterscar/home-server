#!/usr/bin/env python3
import yaml
import os

class Loader(yaml.SafeLoader):
    def __init__(self, stream):
      self._root = os.path.split(stream.name)[0]
      self._file = os.path.basename(stream.name)
      super(Loader, self).__init__(stream)
    def services(self, node):
      data = {}
      ignore = [self._file, 'docker-compose.yaml']
      for service in os.listdir(self._root):
        if service.endswith('.yaml') and not (service in ignore):
          servicefile = os.path.join(self._root, service)
          servicename = os.path.splitext(service)[0]
          with open(servicefile, 'r') as s:
            data[servicename] = yaml.load(s, Loader)
            data[servicename]['container_name'] = servicename
      return data

Loader.add_constructor('!services', Loader.services)

with open('/config/compose/_compose.yaml', 'r') as c:
  compose = yaml.load(c, Loader)

with open('/config/compose/docker-compose.yaml', 'w') as outfile:
  yaml.dump(compose, outfile, default_flow_style=False)