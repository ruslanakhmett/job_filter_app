rebuild:
	docker-compose down -v
	docker-compose up -d --build

stop:
	docker-compose stop

run:
	docker-compose up -d

dbin:
	docker-compose exec db psql --username=django_user --dbname=django_db_docker

delete:
	docker container prune
	docker image prune
	docker volume prune