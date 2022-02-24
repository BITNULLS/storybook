run:
	export FLASK_APP=edu_storybook/app.py
	export FLASK_ENV=development
	flask run
windows-run:
	$Env:FLASK_APP = "app.py"
	$Env:FLASK_ENV = "development"
	python -m flask run
setup:
	rm -r temp/
	mkdir temp/
	mkdir temp/file_upload/
	pip3 install -r requirements.txt
test:
	python -m unittest test_edu_storybook
server:
	if [ ! -d ../../instantclient* ]; then \
	sudo apt install unzip; \
	wget https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-basic-linux.x64-21.4.0.0.0dbru.zip; \
	unzip instantclient-basic-linux.x64-21.4.0.0.0dbru.zip; \
	rm instantclient-basic-linux.x64-21.4.0.0.0dbru.zip; \
	else echo Instant Client Already Present; \
	fi
