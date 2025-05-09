dev: 
	uv run services/${service}/src/${service}/main.py

push:
	kind load docker-image ${service}:dev --name rwml-34fa

build:
	docker build -t ${service}:dev -f docker/${service}.Dockerfile .

deploy: build push
	kubectl delete -f deployment/dev/${service}/${service}.yaml --ignore-not-found=true
	kubectl apply -f deployment/dev/${service}/${service}.yaml

lint: 
	ruff check . --fix