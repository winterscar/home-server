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
    > docker run -it --rm -v /mnt/config:/data -v one-token.json:/one-token.json \
      --entrypoint=/bin/ash christophetd/duplicacy-autobackup
    > cd /data
    > duplicacy init home-server-backup one://backups/home-server
    > duplicacity list
    > duplicacity restore -r [DESIRED REVISION (usually latest)]
    ```
    > You will need to provide a one-token.json file. You can get one from [here](https://duplicacy.com/one_start).

4. Finally, run  the following to start all the services:
    ```bash
    docker run --rm \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -v /mnt/config:/config \
      docker/compose \
      -f /config/compose/docker-compose.yaml \
      --project-directory=/config \
      up -d
    ```

# Configuring services
The home server defines two kinds of services: `System Services` and `Application Services`

## System Services
This category of service runs as part of the `ROS` command. It is referenced from the `cloud-config.yml` file, which points to `rancher/index.yml`, which in turn looks under `/[letter]/[service-name].yml`. 

Making changes to system services is slightly more tricky than changing application services. 

0. `SSH` into the server
1. Delete the files in `/var/lib/rancher/cache`.
2. run `sudo ros s rm [service-name] && sudo ros s up [service-name]`

## Application Services
Application services are run by `docker-compose`. However, no `docker-compose.yaml` file is present in this repo. Instead, each service is defined in `docker-compose` compatible yaml in the `/compose` folder. Each service in it's own file, with the file name indicating both the service and container name. As such, you should refrain from defining a `container_name`.

Making changes to Application services is very straight forward. Simply edit, add or delete files to the `/compose` directory, and push. The home server will automatically pull changes to the master branch and apply them.

# Adding new services
[...]
Beware that there is an overly aggressive caching of yml files - so when you push a new yml file to your repo, you need to delete the files in `/var/lib/rancher/cache`.

# Making changes

docker run -ti --rm -v ${HOME}:/root -v $(pwd):/git alpine/git diff --name-only master origin/master