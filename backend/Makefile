run:
	export FLASK_APP=server.py
	export FLASK_ENV=development
	flask run 
setup:
	rm -r temp/
	mkdir temp/
	mkdir temp/file_upload/
	pip3 install -r requirements.txt
server:
	if [ ! -d ../../instantclient* ]; then \
	sudo apt install unzip; \
	wget https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-basic-linux.x64-21.4.0.0.0dbru.zip; \
	unzip instantclient-basic-linux.x64-21.4.0.0.0dbru.zip; \
	rm instantclient-basic-linux.x64-21.4.0.0.0dbru.zip; \
	else echo Instant Client Already Present; \
	fi