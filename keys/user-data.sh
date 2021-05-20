#!/bin/bash
# install Apache
yum update -y
yum install -y httpd
cd /var/www/html
#   pick one of these four lines
echo "<html><h1>Hello from Web Server 1 in us-east-1e N. Virginia</h1></html>" > index.html
echo "<html><h1>Hello from Web Server 2 in us-east-1f N. Virginia</h1></html>" > index.html
echo "<html><h1>Hello from Web Server 3 in ap-southeast-2a Sydney</h1></html>" > index.html
echo "<html><h1>Hello from Web Server 4 in eu-north-1a Stockholm</h1></html>" > index.html
# start Apache
service httpd start
chkconfig httpd on
# install CloudWatch monitoring scripts
sudo yum install -y perl-Switch perl-DateTime perl-Sys-Syslog perl-LWP-Protocol-https perl-Digest-SHA.x86_64
cd /home/ec2-user/
curl https://aws-cloudwatch.s3.amazonaws.com/downloads/CloudWatchMonitoringScripts-1.2.2.zip -O
unzip CloudWatchMonitoringScripts-1.2.2.zip
rm -rf CloudWatchMonitoringScripts-1.2.2.zip

#   Use the commands below to enable memory metrics monitoring in CloudWatch
#   /home/ec2-user/aws-scripts-mon/mon-put-instance-data.pl --mem-util --verify --verbose
#   /home/ec2-user/aws-scripts-mon/mon-put-instance-data.pl --mem-util --mem-used --mem-avail
#   Add the following line to the end of /etc/crontab
#   */1 * * * * root /home/ec2-user/aws-scripts-mon/mon-put-instance-data.pl --mem-util --mem-used --mem-avail


