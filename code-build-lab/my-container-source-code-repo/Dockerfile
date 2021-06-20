# Base image: replace 12.04 with 18.04
FROM ubuntu:18.04

# Install dependencies: replace apt-get with apt
RUN apt update -y
RUN apt install -y apache2

# Install apache and write hello world message
RUN echo "<html><h1>Hello World from my Docker container!!! (Date: 2021-06-20, Version: 1)</h1></html>" > /var/www/html/index.html

# Configure apache
RUN a2enmod rewrite
RUN chown -R www-data:www-data /var/www
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_RUN_DIR /var/run/apache2
ENV APACHE_PID_FILE $APACHE_RUN_DIR/apache2.pid
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_LOG_DIR /var/log/apache2

# Make sure directories exist
RUN mkdir -p $APACHE_RUN_DIR $APACHE_LOCK_DIR $APACHE_LOG_DIR

EXPOSE 80

CMD ["/usr/sbin/apache2", "-D",  "FOREGROUND"]

