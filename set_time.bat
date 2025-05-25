@echo off
:: Extract current hour in two-digit format
set hour=0%time:~0,2%
set hour=%hour:~-2%

:: Display the result
echo Current hour is: %hour%

docker buildx build --push --platform linux/amd64 -t ghcr.io/tushar-r-09/${service}:0.1.3-beta.$$(%date:~-4%%date:~3,2%%date:~0,2%%time:~0,2%%time:~3,2%%time:~6,2%) -f docker/${service}.Dockerfile .
