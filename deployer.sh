docker-compose down
yes | docker container prune
yes | docker system prune -a
docker-compose build
docker-compose up