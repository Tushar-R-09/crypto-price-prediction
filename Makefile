####################################################################################
##Development
####################################################################################

dev: 
	uv run services/${service}/src/${service}/main.py

push-for-dev:
	kind load docker-image ${service}:dev --name rwml-34fa

build-for-dev:
	docker build -t ${service}:dev -f docker/${service}.Dockerfile .

deploy-for-dev: build-for-dev push-for-dev
	kubectl delete -f deployment/dev/${service}/${service}.yaml --ignore-not-found=true
	kubectl apply -f deployment/dev/${service}/${service}.yaml

run: build-for-dev
	docker run -it ${service}:dev

####################################################################################
##Production
####################################################################################
TAG := $(shell powershell -Command "Get-Date -Format 'yyyyMMddHHmmss'")

build-and-push-for-prod:
	@echo "Building image with tag..."
	@echo Using tag: ${TAG}
	@docker buildx build --push --platform linux/amd64 -t ghcr.io/tushar-r-09/${service}:0.1.3-beta.${TAG} -f docker/${service}.Dockerfile .


deploy-for-prod:
	kubectl delete -f deployment/prod/${service}/${service}.yaml --ignore-not-found=true
	kubectl apply -f deployment/prod/${service}/${service}.yaml


lint: 
	ruff check . --fix