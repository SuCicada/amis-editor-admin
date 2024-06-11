build-web:
	cd amis-editor &&\
	npm install && \
	source ../.env.dev &&\
	export VITE_API_HOST=$$VITE_API_HOST &&\
	npx ts-clean-built --built &&\
	npx npm run build && cd ..

start:
	python server.py
