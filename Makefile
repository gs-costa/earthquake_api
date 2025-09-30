format:
	ruff check .
	ruff format --check .

database-up:
	docker compose up -d

database-down:
	docker compose down

migrate:
	poetry run alembic upgrade head

migrate-down:
	poetry run alembic downgrade -1

create-migration:
	poetry run alembic revision --autogenerate -m "$(MSG)"