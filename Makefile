########################################
########## debug and untils ############
########################################

#DOCKER_IMGURL = ghcr.io/zrthstr/libgen-seedtools:latest
DOCKER_IMGURL = ghcr.io/subdavis/libgen-seedtools:latest

pull:
	docker pull $(DOCKER_IMGURL)

run-without-compose: pull
	docker run -it $(DOCKER_IMGURL) -v lb:/opt/persistent

shell-enter-running-instance:
	docker exec -it $$(docker ps | grep libgen-seedtool | awk '{print $$1}' ) /bin/sh

shell-enter-new-instance-debug:
	docker run -it --entrypoint /bin/sh $(DOCKER_IMGURL)


#############################
########## compose ##########
#############################

### currently still needed for testing

#compose: pull
#	docker compose run libgen-seedtools

#compose-new: volumes-rm compose-rm compose

#compose-stop:
#	docker compose stop libgen-seedtools

#compose-rm: compose-stop
#	docker compose rm -vsf

#volumes-rm:
#	for e in $$(docker volume ls | grep 'libgen-seedtools' |awk '{print $$2}' ); do docker volume rm $$e ; done


############################
########### run ############
############################

up:
	docker compose up -d
	docker compose logs -f 

stop:
	docker compose stop libgen-seedtools