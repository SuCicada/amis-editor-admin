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
