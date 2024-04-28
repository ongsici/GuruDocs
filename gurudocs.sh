case $1 in
  start)
    docker compose -f ./docker-compose.yml --env-file=frontend/.env up 
    ;;
  stop)
    docker compose -f ./docker-compose.yml --env-file=frontend/.env down
    ;;
esac