run:
	export FLASK_APP=edu_storybook/app.py
	export FLASK_ENV=development
	flask run
windows-run:
	$Env:FLASK_APP = "app.py"
	$Env:FLASK_ENV = "development"
	python3 -m flask run
setup:
	pip3 install -r requirements.txt
test:
	cd test_edu_storybook/
	python3 -m unittest \
	test_edu_storybook.test_edu_storybook \
	test_edu_storybook.test_api \
	test_edu_storybook.test_core \
	test_edu_storybook.test_ssg
server:
	if [ ! -d ../../instantclient* ]; then \
	sudo apt install unzip; \
	wget https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-basic-linux.x64-21.4.0.0.0dbru.zip; \
	unzip instantclient-basic-linux.x64-21.4.0.0.0dbru.zip; \
	rm instantclient-basic-linux.x64-21.4.0.0.0dbru.zip; \
	else echo Instant Client Already Present; \
	fi
