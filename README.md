# hotels-api

# создание сети
docker network create myNetwork

# конетейнер для БД
docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcdkqptyoiqnae \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16
    
# контейнер для Redis
docker run --name booking_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:7-alpine

# контейнер для нашего приложения (Hotels-API)
docker run --name booking-back `
    -p 7777:8001 `
    --network=myNetwork `
    booking_image

# контейнер для celery
docker run --name booking_celery_worker `
    --network=myNetwork `
    booking_image `
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO

# контейнер для celery-beat
docker run --name booking_celery_beat `
    --network=myNetwork `
    booking_image `
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

# создание образа на основе Dockerfile
docker build -t booking_image .


# docker контейнер для nginx
docker run --name booking_nginx `
    --volume ./nginx.conf:/etc/nginx/nginx.conf `
    --network=myNetwork `
    --rm -p 80:80 nginx


# GitLab Runner

# docker котрейнер для gitlab-runner:
docker run -d --name gitlab-runner --restart always \
    -v /srv/gitlab-runner/config:/etx/gitlab-runner\
    -v /var/run/docker.sock:/var/run/docker.sock \
    gitlab/gitlab-runner:latest

# регистрация gitlab-runner:
docker run --rm -it -v /srv/gitlab-runner/config:/etc/gitlab-runner gitlab/gitlab-runner:latest register