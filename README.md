# UdaConnect
## Overview
### Background
Conferences and conventions are hotspots for making connections.
Professionals in attendance often share the same interests and can make valuable business and personal connections with one another.
At the same time, these events draw a large crowd and it's often hard to make these connections in the midst of all of these events' excitement and energy.
To help attendees make connections, this project is for building the infrastructure for a service that can inform attendees if they have attended the same booths and presentations at an event.

### Goal
This POC is built with the core functionality of ingesting location and identifying individuals who have shared a close geographic proximity.

The main task is to enhance the POC application into a [MVP](https://en.wikipedia.org/wiki/Minimum_viable_product) to handle the large volume of location data that will be ingested.

I will refactor this application into a microservice architecture using message passing techniques that I have learned in this Udacity Cloud Native Architeture Nanodegree course.

### Technologies used in this project
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - API webserver
* [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
* [PostgreSQL](https://www.postgresql.org/) - Relational database
* [PostGIS](https://postgis.net/) - Spatial plug-in for PostgreSQL enabling geographic queries]
* [Vagrant](https://www.vagrantup.com/) - Tool for managing virtual deployed environments
* [VirtualBox](https://www.virtualbox.org/) - Hypervisor allowing to run multiple operating systems
* [K3s](https://k3s.io/) - Lightweight distribution of K8s to easily develop against a local cluster

## Running the app

### Prerequisites
To be able to run this project below tools need to be installed
1. [Install Docker](https://docs.docker.com/get-docker/)
2. [Set up `kubectl`](https://rancher.com/docs/rancher/v2.x/en/cluster-admin/cluster-access/kubectl/)
3. [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads) with at least version 6.0
4. [Install Vagrant](https://www.vagrantup.com/docs/installation) with at least version 2.0

### Environment Setup
To run the application, K8s cluster running locally is required and to interface with it via `kubectl`. Vagrant is used with VirtualBox to run K3s.

#### Initialize K3s
In this project's root, run `vagrant up`. 
```bash
$ vagrant up
```
The command will take a while and will leverage VirtualBox to load an [OpenSuse](https://www.opensuse.org/) OS and automatically install [K3s](https://k3s.io/). When taking a break from development, run `vagrant suspend` to conserve some ouf our system's resources and `vagrant resume` when we want to bring the resources back up. Some useful vagrant commands can be found in [this cheatsheet](https://gist.github.com/wpscholar/a49594e2e2b918f4d0c4).

#### Set up `kubectl`
After `vagrant up` is done, you will SSH into the Vagrant environment and retrieve the Kubernetes config file used by `kubectl`. We want to copy the contents of this file into our local environment so that `kubectl` knows how to communicate with the K3s cluster.
```bash
$ vagrant ssh
```
You will now be connected inside of the virtual OS. Run `sudo cat /etc/rancher/k3s/k3s.yaml` to print out the contents of the file. You should see output similar to the one that I've shown below. Note that the output below is just for your reference: every configuration is unique and you should _NOT_ copy the output I have below.

Copy the contents from the output issued from your own command into your clipboard -- we will be pasting it somewhere soon!
```bash
$ sudo cat /etc/rancher/k3s/k3s.yaml

apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJWekNCL3FBREFnRUNBZ0VBTUFvR0NDcUdTTTQ5QkFNQ01DTXhJVEFmQmdOVkJBTU1HR3N6Y3kxelpYSjIKWlhJdFkyRkFNVFU1T1RrNE9EYzFNekFlRncweU1EQTVNVE13T1RFNU1UTmFGdzB6TURBNU1URXdPVEU1TVROYQpNQ014SVRBZkJnTlZCQU1NR0dzemN5MXpaWEoyWlhJdFkyRkFNVFU1T1RrNE9EYzFNekJaTUJNR0J5cUdTTTQ5CkFnRUdDQ3FHU000OUF3RUhBMElBQk9rc2IvV1FEVVVXczJacUlJWlF4alN2MHFseE9rZXdvRWdBMGtSN2gzZHEKUzFhRjN3L3pnZ0FNNEZNOU1jbFBSMW1sNXZINUVsZUFOV0VTQWRZUnhJeWpJekFoTUE0R0ExVWREd0VCL3dRRQpBd0lDcERBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUFvR0NDcUdTTTQ5QkFNQ0EwZ0FNRVVDSVFERjczbWZ4YXBwCmZNS2RnMTF1dCswd3BXcWQvMk5pWE9HL0RvZUo0SnpOYlFJZ1JPcnlvRXMrMnFKUkZ5WC8xQmIydnoyZXpwOHkKZ1dKMkxNYUxrMGJzNXcwPQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://127.0.0.1:6443
  name: default
contexts:
- context:
    cluster: default
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    password: 485084ed2cc05d84494d5893160836c9
    username: admin
```
Type `exit` to exit the virtual OS and you will find yourself back in your computer's session. Create the file (or replace if it already exists) `~/.kube/config` and paste the contents of the `k3s.yaml` output here.

Afterwards, you can test that `kubectl` works by running a command like `kubectl describe services`. It should not return any errors.

### Steps
Simply run the following command to have everything up and running

`kubectl apply -f deployment/`
This run all kubernetes object defines in the **deployment** folder. The following is setup using above command:

1. Environment variables for the pods: `db-configmap.yaml`
2. Secrets for the pods: `db-secret.yaml`
3. Postgres database running PostGIS: `postgres.yaml`
4. Service and deployment for persons API: `persons-api.yaml`
4. Service and deployment for connection API: `connection-api.yaml`
5. Service and deployment for the web app:`udaconnect-app.yaml`
6. Service and deployment for the Kafka and Zookeeper:`kafka.yaml`
7. `sh scripts/run_db_command.sh <POD_NAME>` - Seed the database against the `postgres` pod. (`kubectl get pods` will give the `POD_NAME`)

Note: The first time you run this project, you will need to seed the database with dummy data. Use the command `sh scripts/run_db_command.sh <POD_NAME>` against the `postgres` pod. (`kubectl get pods` will give you the `POD_NAME`). Subsequent runs of `kubectl apply` for making changes to deployments or services shouldn't require you to seed the database again!

### Verifying it Works
Once the project is up and running, you should be able to see 3 deployments and 3 services in Kubernetes:
`kubectl get pods` and `kubectl get services` - should both return `udaconnect-app`, `udaconnect-api`, and `postgres`


These pages should also load on your web browser:
* `http://localhost:30002/` - Persons OpenAPI Documentation
* `http://localhost:300003/` - Person connection OpenAPI Documentation
* `http://localhost:30002/api/` - Base path for Persons API
* `http://localhost:30003/api/` - Base path for Connection API
* `http://localhost:30000/` - Frontend ReactJS Application


## Docker Images
[Frontend app](https://hub.docker.com/repository/docker/pasciano007/front), [Persons API](https://hub.docker.com/repository/docker/pasciano007/persons), [Person connections API](https://hub.docker.com/repository/docker/pasciano007/connection-api) custom images used to run this project.

## Configs and Secrets
In `deployment/db-secret.yaml`, the secret variable is `d293aW1zb3NlY3VyZQ==`. The value is simply encoded and not encrypted -- this is ***not*** secure! Anyone can decode it to see what it is.
```bash
# Decodes the value into plaintext
echo "d293aW1zb3NlY3VyZQ==" | base64 -d

# Encodes the value to base64 encoding. K8s expects your secrets passed in with base64
echo "hotdogsfordinner" | base64
```
This is okay for development against an exclusively local environment and we want to keep the setup simple so that you can focus on the project tasks. However, in practice we should not commit our code with secret values into our repository. A CI/CD pipeline can help prevent that.

## PostgreSQL Database
The database uses a plug-in named PostGIS that supports geographic queries. It introduces `GEOMETRY` types and functions that we leverage to calculate distance between `ST_POINT`'s which represent latitude and longitude.

_You may find it helpful to be able to connect to the database_. In general, most of the database complexity is abstracted from you. The Docker container in the starter should be configured with PostGIS. Seed scripts are provided to set up the database table and some rows.

### Software
To manually connect to the database, you will need software compatible with PostgreSQL.
* CLI users will find [psql](http://postgresguide.com/utilities/psql.html) to be the industry standard.
* GUI users will find [pgAdmin](https://www.pgadmin.org/) to be a popular open-source solution.

## Architecture Diagrams
This [Lucidchart](https://www.lucidchart.com/pages/) diagram shows services and relation between them
<img src="https://live.staticflickr.com/65535/50566541207_c647f8e3d3_c.jpg" width="200">


## Swagger documentation
Persons rest microservice api can be found at [this link](https://app.swaggerhub.com/apis/pascalito007/persons/1.0.0)


