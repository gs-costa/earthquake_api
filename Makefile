format:
	ruff check .
	ruff format --check .

database-up:
	docker compose up -d postgres

database-down:
	docker compose down

database-migrate:
	poetry run alembic upgrade head

database-migrate-down:
	poetry run alembic downgrade -1

database-create-migration:
	poetry run alembic revision --autogenerate -m "$(MSG)"