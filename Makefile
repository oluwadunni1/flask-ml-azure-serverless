setup:
	python3 -m venv .venv
	# source .venv/bin/activate

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	#python -m pytest -vv --cov=webapp tests/*.py
	#python -m pytest --nbval notebooks/*.ipynb

lint:
	# This runs the linter on the Dockerfile (since you installed it)
	docker run --rm -i hadolint/hadolint < Dockerfile
	# This runs pylint on your app code (Updated path to webapp/)
	pylint --disable=R,C,W1203,W0702 webapp/app.py

# UPDATED: Consistent image name 'house-price-api'
docker-build:
	docker build -t house-price-api .

docker-run:
	docker run -p 5000:5000 house-price-api

docker-debug:
	# Run in background and attach shell
	docker run -d -p 5000:5000 --name house-price-debug house-price-api
	docker exec -it house-price-debug bash

docker-stop:
	# Helper to stop the debug container
	docker stop house-price-debug && docker rm house-price-debug

docker-clean:
	# Safer clean: removes dangling images and the specific app image
	# fails silently if image doesn't exist
	-docker rmi house-price-api
	docker system prune -f

all: install lint test