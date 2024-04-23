# Ansible vCenter content library to AWS S3 Migrator

This repository contains an Ansible playbook that automates the process of downloading items from a vCenter content library and subsequently uploading them to an AWS S3 bucket.

## Features

* Retrieves items from a specified vCenter content library.
* Downloads each item from the library to the local system.
* Uploads the downloaded items to a specified AWS S3 bucket.
* Updates the Content Library .json using a Python script.
* Cleanup

## Pre-requisites

* Ansible 2.9+
* AWS CLI installed and configured (Or part of the runtime environment)
* Hashicorp Vault with vCenter credentials
* Python 3.x
* Enough disk space for downloads


## Configuration

AWX Template accepts following parameters and default values:

* content_library_name: "Customer Content Library"
* s3_bucket_name: "s3-customercontentlibrary"
* s3_bucket_folder: "Content-Library"

* content_library_name: Name of the content library on targeted vCenter
* s3_bucket_name: Targeted S3 bucket where the files will be synced
* s3_bucket_folder: Name of folder in s3_bucket_name where the content library will be synced to.

Playbook also expect vcenter and AWS credentials (Provided from AWX credentials store)

Does not require privilege escalation.

## Usage

Note!: Primary use is to run in AWX with all the environment variables provided by AWS and runtime environment containing all the needed modules.
