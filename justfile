#

API_CONTAINER := './ops/dev/api/Dockerfile'
API_COMPOSE := './ops/dev/api/compose.yml'

API_SERVICE := 'api'


#

build:
    docker build --file {{API_CONTAINER}} --tag api:latest .

up:
    docker compose -f {{API_COMPOSE}} up -d --remove-orphans
    just logs

down:
    docker compose -f {{API_COMPOSE}} down

restart: down up

logs:
    docker compose -f {{API_COMPOSE}} logs --follow=true {{API_SERVICE}} psql

remove-volumes:
	docker compose -f {{API_COMPOSE}} down -v

test-all:
    docker compose -f {{API_COMPOSE}} run --remove-orphans --rm {{API_SERVICE}} python manage.py test --noinput

test TEST:
    docker compose -f {{API_COMPOSE}} run --remove-orphans --rm {{API_SERVICE}} python manage.py test --noinput {{TEST}}

fmt:
    black api/
    ruff check api/ --fix
