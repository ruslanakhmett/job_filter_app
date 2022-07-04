rerun:
	docker-compose  down -v
	docker-compose up -d --build

stop:
	docker-compose  down -v
