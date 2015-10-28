# smsweb
Asynchronous SMS Gateway Web Service

## Pre Requirements
 1. Centos 6 or later
 2. [Install MongoDB]
 3. wavecom modem
 4. Webserver(Apache, Nginx, etc...) with CGI enable or wsgi
 For apache webserver edit /etc/httpd/conf/httpd.conf
  
 ```sh
 <Directory "/var/www/html">
 	Options Indexes FollowSymLinks ExecCGI
    AddHandler cgi-script py
    AllowOverride None
    Order allow,deny
    Allow from all
 </Directory>
 ```

## Instalation
 1. add user apache and to to group dialout
    
    ```sh
	# usermod -G dialout apache
	# grep 'dialout' /etc/group
	```
 2. Download and extract smsweb in webserver folder(/var/www/html) with CGI enable
 3. edit config.py with your own configuration hardware and then execute :
 
 ```sh
 # chown -R 755 /var/www/html
 # chown -R apache:apache /var/www/html/
 ```
 6. access your IP with browser
 
## API Access
 1. sending sms
 
 ```sh
 http://localhost/s.py 
 with POST method, parameter :
 rcpt = number,number ex. 081312000300,08997788921,0879989892383
 msg = this is a message
 ```
 2. Outbox sms
 
 ```sh
 http://localhost/outbox.py
 ```
 3. Sentitems sms
 
 ```sh
 http://localhost/sentitems.py
 ```
 4. Errornumber log
 
 ```sh
 http://localhost/errors.py
 ```
 



## Reference
 1. https://www.centos.org/docs/5/html/5.1/Deployment_Guide/s2-users-add.html
 2. http://www.techotopia.com/index.php/Managing_CentOS_6_Users_and_Groups
 3. http://www.cyberciti.biz/faq/linux-list-all-members-of-a-group/
 4. http://docs.gunicorn.org/en/19.3/design.html
 5. http://docs.gunicorn.org/en/19.3/faq.html
 
[Install MongoDB]:http://andres.jaimes.net/870/setup-mongo-on-centos-6/