.PHONY: help install dev-infra dev-api dev-web clean

help:
	@echo "SoulGravity Local Dev Commands"
	@echo "------------------------------"
	@echo "make install    - Install Python dependencies"
	@echo "make dev-infra  - Start Postgres, Redis, RabbitMQ (Docker)"
	@echo "make dev-api    - Start API Gateway locally (requires dev-infra)"
	@echo "make dev-web    - Start Web Console locally"
	@echo "make clean      - Stop Docker containers"

install:
	pip install -r requirements.txt

dev-infra:
	docker compose -f deploy/docker-compose.dev.yml up -d
	@echo "Infrastructure started. Waiting for DB..."
	@sleep 5

dev-api:
	export DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/soulgravity && \
	export REDIS_URL=redis://localhost:6379/0 && \
	export RABBITMQ_URL=amqp://user:password@localhost:5672// && \
	alembic upgrade head && \
	uvicorn apps.api_gateway.main:app --host 0.0.0.0 --port 8000 --reload

dev-web:
	cd web-console && npm install && npm run dev

clean:
	docker compose -f deploy/docker-compose.dev.yml down
