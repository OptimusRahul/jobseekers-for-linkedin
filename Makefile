.PHONY: install run test clean dev help migrate-up migrate-down migrate-create migrate-history

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using uv
	uv sync

dev: ## Install with dev dependencies
	uv sync --dev

run: ## Run the FastAPI server
	uv run uvicorn src.main:app --reload

test: ## Run API tests
	uv run python test_api.py

clean: ## Remove cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete

update: ## Update dependencies
	uv lock --upgrade
	uv sync

list: ## List installed packages
	uv pip list

tree: ## Show dependency tree
	uv pip tree

# Database migrations
migrate-up: ## Run database migrations
	uv run alembic upgrade head

migrate-down: ## Rollback last migration
	uv run alembic downgrade -1

migrate-create: ## Create a new migration (use: make migrate-create MSG="description")
	uv run alembic revision --autogenerate -m "$(MSG)"

migrate-history: ## Show migration history
	uv run alembic history --verbose

migrate-current: ## Show current migration version
	uv run alembic current

lint: ## Check code quality (placeholder)
	@echo "Linting not configured yet"

format: ## Format code (placeholder)
	@echo "Formatting not configured yet"
