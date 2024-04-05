#!/usr/bin/env bash
awslocal s3 mb s3://objects

echo "Hello S3" > /tmp/hello.txt
awslocal s3 cp /tmp/hello.txt s3://objects/hello.txt
