function git () {
    (docker run -ti --rm -v ${HOME}:/root -v $(pwd):/git alpine/git "$@")
}

function ros () {
   (sudo ros "$@")
}

function restart () {
   sudo system-docker restart console
}

function recreate () {
    sudo rm /var/lib/rancher/cache/*
    docker stop "$@"
    ros s rm -f "$@"
    ros s up "$@"
}

function dps () {
    FORMAT='table {{.Names}}\t{{.Status}}'
    while getopts ":p" opt; do
      case $opt in
        p) FORMAT+='\t{{.Ports}}'
        ;;
      esac
    done
    docker ps --format "$FORMAT"
}

source /mnt/config/.env