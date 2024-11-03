#

API_CONTAINER := './ops/dev/api/Dockerfile'
API_COMPOSE := './ops/dev/api/compose.yml'

API_SERVICE := 'api'


# Set Up

config-env:
	cp .env.example ./ops/dev/api/.env
	cp .env.example ./api/minitwitter/.env

build:
    docker build --file {{API_CONTAINER}} --tag api:latest .

setup: config-env build


#

up:
    docker compose -f {{API_COMPOSE}} up -d --remove-orphans
    just logs

down:
    docker compose -f {{API_COMPOSE}} down

restart: down up

logs:
    docker compose -f {{API_COMPOSE}} logs --follow=true {{API_SERVICE}} psql celery

shell:
	docker compose -f {{API_COMPOSE}} exec {{API_SERVICE}} python manage.py shell

test:
    docker compose -f {{API_COMPOSE}} run --remove-orphans --rm {{API_SERVICE}} python manage.py test --noinput --exclude=slow

test-all:
    docker compose -f {{API_COMPOSE}} run --remove-orphans --rm {{API_SERVICE}} python manage.py test --noinput

test-path TEST:
    docker compose -f {{API_COMPOSE}} run --remove-orphans --rm {{API_SERVICE}} python manage.py test --noinput {{TEST}}

fmt:
    black api/
    ruff check api/ --fix

#

remove-volumes:
	docker compose -f {{API_COMPOSE}} down -v

migrate:
    docker compose -f {{API_COMPOSE}} run --remove-orphans --rm {{API_SERVICE}} python manage.py migrate

populate-users:
    docker compose -f {{API_COMPOSE}} run --remove-orphans --rm {{API_SERVICE}} python manage.py populate_1_users

populate-posts:
    docker compose -f {{API_COMPOSE}} run --remove-orphans --rm {{API_SERVICE}} python manage.py populate_2_posts

populate: remove-volumes migrate populate-users populate-posts restart
