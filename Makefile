rebuild:
	docker-compose down -v
	docker-compose -f docker-compose.yml build
	docker-compose -f docker-compose.yml up -d

stop:
	docker-compose stop

run:
	docker-compose up -d

dbin:
	docker-compose exec db psql --username=django_user --dbname=django_db_docker

delete:
	docker container prune -f
	docker image prune -f 
	docker volume prune -f