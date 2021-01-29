install-test-requirements:
	pip3 install -r requirements.txt

clean:
	sudo docker rm -f webservice

build-image: 
	cd stub && docker build -t webserviceimg .

run-image: 
	cd stub && docker run -d --name webservice -p 80:80 webserviceimg

test:
	cd tests && pytest -v

prepare-and-test: 
	make clean
	make build-image
	make run-image
	make test