dev: 
	uv run services/${service}/src/${service}/main.py

push:
	kind load docker-image trades:dev --name rwml-34fa

build:
	docker build -t ${service}:dev -f docker/${service}.Dockerfile .

deploy: build push
	kubectl delete -f deployment/dev/trades/trades.yaml
	kubectl apply -f deployment/dev/trades/trades.yaml

lint: 
	ruff check . --fix