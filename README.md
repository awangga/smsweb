# smsweb
Asynchronous SMS Gateway Web Service.

Made it for your notification and account verification Apps

## Built in with smsweb
 1. serial python lib
 2. pymongo python lib
 3. messaging python lib
 4. bson python lib
 5. gunicorn python lib

## Pre Requirements
 1. Centos 6 or later
 2. [Install MongoDB]
 3. Wavecom modem
 4. Install Apache Webserver with CGI enable or wsgi (a2enmod cgi)
 5. Rename config-sample.py to config.py edit with your configuration server

 ```sh
 # yum install httpd
 ``` 
 edit /etc/httpd/conf/httpd.conf
  
 ```sh
 <Directory "/var/www/html">
 	Options Indexes FollowSymLinks ExecCGI
    AddHandler cgi-script py
    AllowOverride None
    Order allow,deny
    Allow from all
 </Directory>
 ```
 on apache2 edit /etc/apache2/conf-available/serve-cgi-bin.conf

 ```
 <IfModule mod_alias.c>
	<IfModule mod_cgi.c>
		Define ENABLE_USR_LIB_CGI_BIN
	</IfModule>

	<IfModule mod_cgid.c>
		Define ENABLE_USR_LIB_CGI_BIN
	</IfModule>

	<IfDefine ENABLE_USR_LIB_CGI_BIN>
		ScriptAlias / /var/www/html/
		<Directory "/var/www/html">
			AllowOverride None
			Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
			AddHandler cgi-script py
			Require all granted
		</Directory>
	</IfDefine>
 </IfModule>

 ```


## Instalation
 1. add user apache and to to group dialout
    
    ```sh
	# usermod -G dialout apache
	# grep 'dialout' /etc/group
	```
 2. Download and extract smsweb in webserver folder(/var/www/html) with CGI enable
 3. edit config.py with your own configuration hardware and 
 4. Change owner as apache and mode 755 of smsweb by execute :
 
 ```sh
 # chown -R 755 /var/www/html
 # chown -R apache:apache /var/www/html/
 ```
 5. Change access mode for main.pid to 777
 ```sh
 # chown 777 main.pid
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
 



## User Manual
 1. Indonesia Manual Book
 
[Install MongoDB]:http://andres.jaimes.net/870/setup-mongo-on-centos-6/
[Indonesia Manual Book]:https://awangga.gitbooks.io/sms-web-service-untuk-pemula/content/chapter1.html
