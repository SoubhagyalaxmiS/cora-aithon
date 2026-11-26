.PHONY: install test prototype poster architecture images deck guide docs all

install:
	npm install
	pip install -r requirements.txt

test:
	npm test

prototype:
	python3 app/prototype/build.py

poster:
	python3 tools/poster/build.py

architecture:
	python3 tools/architecture/build.py

images: poster architecture
	python3 tools/export/make_images.py

deck: images
	node tools/deck/build.js

guide:
	python3 tools/jury-guide/build_pdf.py

docs: poster architecture images deck guide

all: prototype docs test
