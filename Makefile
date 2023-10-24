#run:
#	serve demo-5.4.1 -p 58760
#dev:
#	serve demo-test -p 58760
build: clean
	#tsc
	vite build

clean:
	ts-clean-built --built

dist_server:
	serve dist -p 58760
