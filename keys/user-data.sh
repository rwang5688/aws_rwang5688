#!/bin/bash
yum update -y
yum install httpd -y
cd /var/www/html
echo "Hello from Web Server 1 in us-east-2e N. Virginia" > index.html
echo "Hello from Web Server 2 in us-east-2f N. Virginia" > index.html
echo "Hello from Web Server 3 in ap-southeast-2a Sydney" > index.html
echo "Hello from Web Server 4 in eu-north-1a Stockholm" > index.html
service httpd start
chkconfig httpd on
sudo yum install -y perl-Switch perl-DateTime perl-Sys-Syslog perl-LWP-Protocol-https perl-Digest-SHA.x86_64
cd /home/ec2-user/
curl https://aws-cloudwatch.s3.amazonaws.com/downloads/CloudWatchMonitoringScripts-1.2.2.zip -O
unzip CloudWatchMonitoringScripts-1.2.2.zip
rm -rf CloudWatchMonitoringScripts-1.2.2.zip

#   Use the commands below for the lab.
#   /home/ec2-user/aws-scripts-mon/mon-put-instance-data.pl --mem-util --verify --verbose
#   /home/ec2-user/aws-scripts-mon/mon-put-instance-data.pl --mem-util --mem-used --mem-avail
#   */1 * * * * root /home/ec2-user/aws-scripts-mon/mon-put-instance-data.pl --mem-util --mem-used --mem-avail


