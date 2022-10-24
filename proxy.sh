#!/bin/bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod rewrite
sudo /etc/init.d/apache2 restart

