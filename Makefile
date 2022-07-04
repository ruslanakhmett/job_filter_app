rebuild:
	docker-compose down -v
	docker-compose up -d --build

stop:
	docker-compose stop

run:
	docker-compose up -d
