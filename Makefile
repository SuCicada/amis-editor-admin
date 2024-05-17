ifneq ("$(wildcard .env)","")
	include .env
	export
endif
#run:
#	serve demo-5.4.1 -p 58760
#dev:
#	serve demo-test -p 58760
build: clean
	#tsc
	vite build
	du -sh dist

#npx rimraf node_modules
clean:
	ts-clean-built --built
	# npx rimraf dist

dist_server:
	serve dist -p 58761

define copy_dist
	if [ -d "$(MAKE_SERVER_WEB_PATH)" ]; then \
		rimraf "$(MAKE_SERVER_WEB_PATH)" ; \
		mkdir -p "$(MAKE_SERVER_WEB_PATH)" ; \
		cp -r ./"$(patsubst %,%,$(1))"/* "$(MAKE_SERVER_WEB_PATH)" ; \
		echo "copy dist to $(MAKE_SERVER_WEB_PATH)" ; \
	fi
endef

copy_dist-dev:
	$(call copy_dist, dist)

copy_dist-prod:
	$(call copy_dist, dist-prod)

build-prod:
	#yarn run build:prod
	rimraf dist-prod
	vite build --mode production --outDir dist-prod
#	du -sh dist
	@make copy_dist-prod
