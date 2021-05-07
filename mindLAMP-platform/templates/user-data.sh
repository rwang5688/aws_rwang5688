#!/bin/bash
# install and start Apache
yum update -y
yum install -y httpd
cd /var/www/html
echo "<html><h1>Hello World from ${Ec2Instance01Name}.</h1></html>" > index.html
service httpd start
chkconfig httpd on
# install and start Docker Swarm
yum install -y docker
usermod -a -G docker ec2-user
hostnamectl set-hostname ${DomainName}
mkdir /etc/systemd/system/docker.service.d
printf "[Service]\nExecStart=\nExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H fd:// --containerd=/run/containerd/containerd.sock\n" | tee /etc/systemd/system/docker.service.d/override.conf
systemctl daemon-reload
service docker restart
docker swarm init
# install CloudWatch monitoring scripts
yum install -y perl-Switch perl-DateTime perl-Sys-Syslog perl-LWP-Protocol-https perl-Digest-SHA.x86_64
cd /home/ec2-user/
curl https://aws-cloudwatch.s3.amazonaws.com/downloads/CloudWatchMonitoringScripts-1.2.2.zip -O
unzip CloudWatchMonitoringScripts-1.2.2.zip
rm -rf CloudWatchMonitoringScripts-1.2.2.zip

#   Use the commands below to enable memory metrics monitoring in CloudWatch
#   /home/ec2-user/aws-scripts-mon/mon-put-instance-data.pl --mem-util --mem-used --mem-avail --verify --verbose
#   /home/ec2-user/aws-scripts-mon/mon-put-instance-data.pl --mem-util --mem-used --mem-avail
#   */1 * * * * root /home/ec2-user/aws-scripts-mon/mon-put-instance-data.pl --mem-util --mem-used --mem-avail


