build-web:
	cd amis-editor &&\
	npx yarn && \
	source ../.env.dev &&\
	export VITE_API_HOST=$$VITE_API_HOST &&\
	npx ts-clean-built --built &&\
	npx yarn build && cd ..

