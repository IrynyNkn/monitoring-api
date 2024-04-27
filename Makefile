run-db:
	docker compose up -d redis influxdb postgres

make-migrations:
	docker compose run --rm --no-deps app alembic revision --autogenerate -m "New migration"

run: | run-db
	docker compose up -d flower
	docker compose up app celery_worker
