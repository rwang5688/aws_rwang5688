#!/bin/bash
openssl version
aws s3 ls
aws s3 cp s3://wangrob-kms-lab-us-east-1 /home/ec2-user --recursive
ls
openssl rand -out PlaintextKeyMaterial.bin 32
ls
openssl rsautl -encrypt \
                -in PlaintextKeyMaterial.bin \
                -oaep \
                -inkey wrappingKey_7a3548f7-db96-4f95-96aa-7f8c93155e8e_04062420 \
                -keyform DER \
                -pubin \
                -out EncryptedKeyMaterial.bin
aws s3 cp /home/ec2-user s3://wangrob-kms-lab-us-east-1 --recursive

