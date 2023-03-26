ifneq ($(wildcard docker/.env.example),)
	ENV_FILE = .env.example
endif
ifneq ($(wildcard .env),)
	ifeq ($(COMPOSE_PROJECT_NAME),)
		include .env
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
	poetry run uvicorn run:app