WinterScar Home Server
======================

# Quick start guide
The following steps will get you up and running on a new machine, or allow you to recover from a failure. 
## Configure server
Starting from a blank slate, the following steps will bring you back up to a fully functional home-server.

1. Follow the instructions [here](https://rancher.com/docs/os/v1.x/en/installation/workstation/boot-from-iso/)
   to boot to the `Rancher OS iso`.
2. Once you're logged in, run the following to install and configure Rancher OS.
    ```bash
    > sudo ros install \
      -c  https://raw.githubusercontent.com/winterscar/home-server/master/rancher/cloud-config.yml \
      -d /dev/sda
    ```
    > Note: You can the cloud-config expects disks labled filesN to contain media, and will mount them as such. If you have a different disk configuration, update the cloud config or lable your disks. 
    > Also ensure your public SSH key is present in the cloud-config file or you will not be able to log in.

3. Your server will restart, installing Rancher OS to the disk. Once this has happened, ssh into the server and run the following commands to get started:

    ```bash
    > docker run -it --rm -v /mnt/config:/data \
      -v $(pwd)/one-token.json:/one-token.json \
      -e DUPLICACY_ONE_TOKEN=/one-token.json\
      --entrypoint=/bin/ash christophetd/duplicacy-autobackup
    > cd /data
    > duplicacy init home-server-backup one://backups/home-server
    > duplicacy list
    > duplicacy restore -r [DESIRED REVISION (usually latest)]
    > logout
    > sudo chown -R rancher /mnt/*
    ```
    > You will need to provide a one-token.json file. You can get one from [here](https://duplicacy.com/one_start).

4. Finally, run  the following to start all the services:
    ```bash
    > docker run --rm \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -v /mnt/config:/config \
      docker/compose \
      -f /config/compose/docker-compose.yaml \
      --project-directory=/config \
      up -d --force-recreate
    ```

# Configuring services
The home server defines two kinds of services: `System Services` and `Application Services`.
System services are typically things that don't serve the user, but serve the system. For example, `mergerfs` is only consumed by the system itself. 
Application services are the 'front-end' so to speak (even if, like mosquitto, they dont actually have a front-end). They offer direct value to the user.

## System Services
System Services are not changed, added to, or removed often. As such they are not managed as part of the build pipeline, even if their configuration _is_. 

System Services are defined in  the `rancher` directory. Each service is listed in `index.yml`, and it's associated `docker-compose-esque` configuration under `rancher/<first-letter>/<service-name>`. 

To make changes to system services, commit the updated configuration to this repository, then `ssh` into the host machine and run
```bash
> recreate <service>
```

You can read more about system services [here](https://rancher.com/docs/os/v1.x/en/system-services/custom-system-services/).

## Application Services
Application services are run by `docker-compose`. However, no `docker-compose.yaml` file is present in this repo. Instead, each service is defined in `docker-compose` compatible yaml in the `/compose` folder. Each service in it's own file, with the file name indicating both the service and container name. As such, you should refrain from defining a `container_name` in the yaml.

Making changes to Application services is very straight forward. Simply edit, add or delete files to the `/compose` directory, and push. The home server will automatically pull changes to the master branch and apply them.

## Build Pipeline
One of the system-services defined on the home server is `update-config`. Its job is to watch the git repository (via a GitHub webhook) and then update the running containers to match the configuration.

The pipeline consists of a set of steps, triggered by a `push` to the master branch.

Each step of the pipeline is defined as an executable file under `update-config/hooks`, and the files are run in alphabetical order (technically, whatever order `sorted(<list>)` in python returns). Each executable is called with the GitHub payload as it's first and only argument. 

### 00_pull.sh
> Pulls this repository from github.
Because we're pulling first, it is possible to _override the subsequent pipeline steps_. However, note that only the step contents can be changed in this way. If you rename, add, or remove scripts, you will need to restart the container before they are executed.
```bash
> docker restart update-config
```

### 01_secrets.py
In order to facilitate the management of secrets, you can put them in the secrets.yaml file directly on the server according to the following pattern:

```yaml
path/to/file/with/secrets.txt:
  secret_key: secret_value
  another_secret: another_value
```
Then, in the file `path/to/file/with/secrets.txt`, simply replace any sensitive data with `${secret_key}` and the secret will be injected into the file

### 02_compose.py
> Turns the various `compose/*.yaml` files into a single `docker-compose.yaml` file. 

Additionally, this script adds some augmentations to each service, such as defining a `TZ` variable. This is a useful place to make changes that affect all or many of the system services, rather than having to modify each .yaml file.

If you need to add anything that is _not_ as service to the compose file, you can add it to _compose.yaml, which forms the basis of the final file.

### 03_restart.py
> Ensures containers that were edited are recreated or restarted on the home-server.

This script uses the changes data passed in from the webhook to ascertain which files have been changed. If any of the the `compose/*.yaml` files have, we can simply run `docker-compose up` and let comose do the work of figuring out _what_ needs to be recreated. 

If _configuration data_ has changed, the service probably needs to be restarted. The script will avoid restarting containers that have just been recreated, and also does not restart the `update-config` container, as that would be suicide.

# Services
This section details all the running services, including their function, useful links, and caveates.

## Mopidy
Mopidy streams the audio output into the Snapserver's fifo with a filesink as audio output in mopidy.conf:
```
[audio]
#output = autoaudiosink
output = audioresample ! audioconvert ! audio/x-raw,rate=48000,channels=2,format=S16LE ! wavenc ! filesink location=/tmp/snapcast/snapwhatever
```
Please make sure that the snapfifo file is not created by Mopidy, as Mopidy will create a regular file /tmp/snapfifo instead of a fifo. This will cause Snapcast to play from the beginning if you pause Mopidy.
Solution is to create the fifo manually with mkfifo /tmp/snapfifo or to start the Snapserver before Mopdy is started.

```
sudo mkfifo mopidy/snapcast/snapguest
```

## Linuxserver.io Services
All the following services are provided by `lsio`, and as such share very similar configurations.
+ [Grocy](https://hub.docker.com/r/linuxserver/grocy/) -
  ERP for your fridge. I use Grocy to manage reciepies and what's in my pantry.
+ [NZBHydra](https://hub.docker.com/r/linuxserver/nzbhydra2/) -
  Consolidates all NZB search services into a single API.
+ [Ombi](https://hub.docker.com/r/linuxserver/ombi/) -
  Allows users to request additional films / series to be added to Plex.
+ [Plex](https://hub.docker.com/r/linuxserver/plex/) -
  A self hosted media server, letting me watch my movies and series anywhere in the world.
+ [Radarr](https://hub.docker.com/r/linuxserver/radarr/) -
  Monitors a list of _wanted_ movies, and downloads them from Usenet when abvailable.
+ [SabNZBD](https://hub.docker.com/r/linuxserver/sabnzbd/) -
  Usenet download manager. Recieves files from Sonarr, Radarr and downloads them.
+ [Sonarr](https://hub.docker.com/r/linuxserver/sonarr/) -
  Monitors a list of _wanted_ series, and downloads new episodes from Usenet when abvailable.
+ [Tautulli](https://hub.docker.com/r/linuxserver/Tautulli/) -
  Plex stats. Montors usage data from plex so I can see who is watching what.
+ [Unifi](https://hub.docker.com/r/linuxserver/Unifi/) -
  Management interface for my home-network router and access points, made by Ubiquiti.

All these services share the following configuration:
### User
```yaml
environment:
  - PGID=${GROUP_ID}
  - PUID=${USER_ID}
```
This provides the s6 service inside the container with the `User` and `Group` it should run the application as. Providing these details ensures that files bind-mounted (via `-v` / `volume:`) are owned by `USER_ID`, not `root`. 

### Configuration
```yaml
volumes:
  - ${CONFIG}/radarr:/config
```
_bind-mounting_ volumes means that data written to those directories within the container persists across container recreation. All `lsio` services store their configuration data under `/config`.

## Home Assistant
[Home Assistant](home-assistant.io) is the central part of my Home Automation stack. It integrates connections from thousands of devices and services and makes them available from one place.

Home assistant is the only container that does not support changing user-role, and as such, the data it writes to the host is owned by `root`.

## Zigbee2mqtt
The drivers for the CC2531 Zigbee device are not included in rancher by default. Therefore, in 
the cloud-config file, we set `kernel-modules: true`. 
If this is not sufficient, you can run `rmmod cdc_acm && modprobe cdc_acm`

UDEV Rules in the cloud-config will mount the CC2531 as `/dev/usbZigbee`, which is then mounted into
the container.