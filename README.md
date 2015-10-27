# smsweb
Asynchronous SMS Gateway Web Service
## Requirements
 1. Centos 6
 2. mongoDB
 3. wavecom modem
## Instalation
 1. create user smsweb and to to group dialout
    ```sh
	# useradd smsweb
	# passwd smsweb
	# usermod -G dialout smsweb
	# grep 'dialout' /etc/group
	```
 2. Download and extract smsweb in home folder of smsweb
 3. edit config.py


## Reference
 1. https://www.centos.org/docs/5/html/5.1/Deployment_Guide/s2-users-add.html
 2. http://www.techotopia.com/index.php/Managing_CentOS_6_Users_and_Groups
 3. http://www.cyberciti.biz/faq/linux-list-all-members-of-a-group/
 4. http://docs.gunicorn.org/en/19.3/design.html
 5. http://docs.gunicorn.org/en/19.3/faq.html