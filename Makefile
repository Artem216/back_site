debug:
	docker compose -f docker/docker-compose.yaml up db --build -d
	python3 main.py

deploy:
	docker compose -f docker/docker-compose.yaml up --build -d
