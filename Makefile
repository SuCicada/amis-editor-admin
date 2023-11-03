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

clean:
	ts-clean-built --built
	rm -rf dist

dist_server:
	serve dist -p 58761

dist_copy:
	rimraf $(MAKE_SERVER_WEB_HOST)
	mkdir -p $(MAKE_SERVER_WEB_HOST)
	cp -r dist/* $(MAKE_SERVER_WEB_HOST)
