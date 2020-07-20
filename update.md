First run this:

```
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /mnt/config:/config \
  docker/compose \
  -f /config/compose/docker-compose.yaml \
  --project-directory=/config \
  pull
```

Then run this:

```
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /mnt/config:/config \
  docker/compose \
  -f /config/compose/docker-compose.yaml \
  --project-directory=/config \
  up -d --force-recreate
```