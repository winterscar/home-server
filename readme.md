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
    > Note: The cloud config expects a certain hard-drive configuration on the bare metal. Ensure this matches the physical machine configuration before installing.
    > Also ensure your public SSH key is present in the cloud-config file or you will not be able to log in.

3. Your server will restart, installing Rancher OS to the disk. Once this has happened, ssh into the server and run the following commands to get started:

    ```bash
    > docker run -it --rm -v /config:/data -v one-token.json:/one-token.json \
      --entrypoint=/bin/ash christophetd/duplicacy-autobackup
    > duplicacy init home-server-backup one://backups/home-server
    > duplicacity list
    > duplicacity restore -r [DESIRED REVISION (usually latest)]
    ```
    > You will need to provide a one-token.json file. You can get one from [here](https://duplicacy.com/one_start).
