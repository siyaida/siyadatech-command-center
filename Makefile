# Siyadatech Ragaban — Makefile
.PHONY: help build up down logs migrate test lint deploy

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build all Docker images
	docker compose build

up: ## Start all services
	docker compose up -d

down: ## Stop all services
	docker compose down

logs: ## View logs from all services
	docker compose logs -f

migrate: ## Run database migrations
	docker compose exec api alembic upgrade head

migrate-make: ## Create new migration
	docker compose exec api alembic revision --autogenerate -m "$(NAME)"

test: ## Run backend tests
	cd backend && python -m pytest tests/ -v

lint: ## Run linters
	cd backend && flake8 app/ && black --check app/
	cd frontend && npx next lint

format: ## Format code
	cd backend && black app/
	cd frontend && npx prettier --write "**/*.{ts,tsx,js,jsx,json,css}"

shell: ## Open API container shell
	docker compose exec api bash

db-shell: ## Open PostgreSQL shell
	docker compose exec postgres psql -U ragaban -d ragaban

redis-cli: ## Open Redis CLI
	docker compose exec redis redis-cli

backup: ## Backup database
	docker compose exec postgres pg_dump -U ragaban -d ragaban > backup-$(shell date +%Y%m%d-%H%M%S).sql

deploy-stc: ## Deploy to STC Cloud
	./infra/stc-cloud/deploy.sh

deploy-vps: ## Deploy to VPS
	./deploy.sh

health: ## Check API health
	curl -s https://siyadatech.siyada-cybersecurity.com/health | jq .
