.PHONY: up down refactor logs shell-api shell-db clean

# Start all services
up:
	docker compose -f deploy/docker-compose.yml up -d --build

# Stop all services
down:
	docker compose -f deploy/docker-compose.yml down

# Run backend refactoring script
refactor:
	chmod +x scripts/refactor_backend.sh
	./scripts/refactor_backend.sh

# View logs (follow)
logs:
	docker compose -f deploy/docker-compose.yml logs -f

# Shell into API container
shell-api:
	docker compose -f deploy/docker-compose.yml exec api_gateway /bin/bash

# Database shell (psql)
shell-db:
	docker compose -f deploy/docker-compose.yml exec postgres psql -U user -d soulgravity

# Clean up docker artifacts
clean:
	docker compose -f deploy/docker-compose.yml down -v
