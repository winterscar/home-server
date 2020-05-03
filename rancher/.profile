source /mnt/config/.env

alias ros="sudo ros"
alias restart="sudo system-docker restart console"
alias sdocker="sudo system-docker"
alias runin="docker exec -it"

backup () {
  local OPTIND OPTARG opt
  while getopts ':nrh' opt; do
    case "$opt" in
      n) sdocker exec backup /app/duplicacy-autobackup.sh backup;;
      r) sdocker exec -it backup /bin/ash;;
      h) echo "n: Backup now, r: Start restore process"; return;;
    esac
  done
  sudo chown -R "${USER_ID}" "${CONFIG}"
}

git () {
  (docker run -ti --rm -v ${HOME}:/root -v $(pwd):/git alpine/git "$@")
}

recreate () {
  sudo rm /var/lib/rancher/cache/*
  ros s up --force-recreate "$@"
}

dps () {
  local OPTIND OPTARG opt f c;
  f='table {{.Names}}\t{{.Status}}'
  c='docker'
  while getopts ':psh' opt; do
    case "$opt" in
      p) f+='\t{{.Ports}}';;
      s) c="sdocker";;
      h) echo "p: Ports, s: system-docker"; return;;
    esac
  done
  eval "$c ps --format '$f'"
}