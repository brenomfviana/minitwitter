#

API_CONTAINER := './ops/dev/api/Dockerfile'
API_COMPOSE := './ops/dev/api/compose.yml'

API_SERVICE := 'api'

#

up-api:
    docker compose -f {{API_COMPOSE}} up -d --remove-orphans
    just logs-api

down-api:
	docker compose -f {{API_COMPOSE}} down

logs-api:
	docker compose -f {{API_COMPOSE}} logs --follow=true {{API_SERVICE}}
