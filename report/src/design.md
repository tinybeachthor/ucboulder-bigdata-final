# Design decisions

<!-- toc -->

## Service architecture

The flow of data is as follows:
- `collect` job
- `queue`
- `process` worker
- `database` & `object storage`
- `web` server
- user through a website

Using the queue to decouple `collect` job and `process` workers allows
extra flexibility with scheduling the collect job and scaling the number
of workers as necessary.

All the processing is done asynchronously in the `process` worker and
the `web` server only returns data in a presentation format.

## Data stores

### PostgreSQL

This is a well tested production SQL database. We chose it for the ease
of deployment and good availability of documentation.

SQL database provides a very good access to indexed data, we use it to
retrieve the most recent articles by date.

### Object Storage

To store the generated audio files, we use an S3-like object storage.
Specifically Cloudflare R2, it has an integrated CDN and no fees for
egress traffic, making it a great economical choice to serve large
amount of large files to users.

## Deployment

Heroku provides a flexible easy to use environment with built-in system
metrics and auto scaling, as well as continuous delivery integration
with GitHub repositories.
