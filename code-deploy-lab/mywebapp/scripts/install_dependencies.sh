#!/bin/bash
yum install -y httpd
# force remove existing index.html
rm -f /var/www/html/index.html

