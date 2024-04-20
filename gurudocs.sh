case $1 in
  start)
    docker compose -f ./docker-compose.yml --env-file=frontend/.env up -d
    ;;
  stop)
    docker compose -f ./docker-compose.yml --env-file=frontend/.env down
    ;;
esac