build: stop
	docker-compose up --build

start: stop
	docker-compose up

stop:
	docker-compose down --remove-orphans