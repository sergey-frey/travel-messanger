ifneq ($(wildcard docker/.env.example),)
	ENV_FILE = .env.example
endif
ifneq ($(wildcard .env.example),)
	ifeq ($(COMPOSE_PROJECT_NAME),)
		include .env.example
	endif
endif
ifneq ($(wildcard docker/.env),)
	ENV_FILE = .env
endif
ifneq ($(wildcard .env),)
	ifeq ($(COMPOSE_PROJECT_NAME),)
		include .env
	endif
endif

export

.PHONY: install
install: ## Installations
	poetry env use python3
	poetry install
	poetry run pre-commit install

.PHONY: run-backend
run-backend: ## Run backend
	poetry run uvicorn run:app --reload

.PHONY: migrate-init
migrate-init: ## Initial migrations
	poetry run alembic init migrations

.PHONY: migrate-create
migrate-create: ## Create a new revision file
	poetry run alembic revision --autogenerate -m "nevers"

.PHONY: migrate-up
migrate-up: ## Upgrade to a later version
	poetry run alembic upgrade head

.PHONY: migrate-down
migrate-down: ## Revert to a previous version
	poetry run alembic downgrade $(revision)

.PHONY: compose-build
compose-build: ## Build or rebuild services
	docker-compose -f docker/docker-compose.yml --env-file docker/$(ENV_FILE) build

.PHONY: compose-up
compose-up: ## Create and start containers
	docker-compose -f docker/docker-compose.yml --env-file docker/$(ENV_FILE) up -d
