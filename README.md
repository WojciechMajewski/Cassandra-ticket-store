# Cassandra ticket store
 
### Steps needed to run the application:

1. Navigate to the root folder of this repository using LINUX
2. Make sure the docker is running
3. Run these three containers:

>docker run --name cass1 -p 9042:9042 -e CASSANDRA_CLUSTER_NAME=OpenerCluster -e HEAP_NEWSIZE=1M -e MAX_HEAP_SIZE=1024M -d cassandra:latest

>docker run --name cass2 -e CASSANDRA_SEEDS="$(docker inspect --format='{{.NetworkSettings.IPAddress}}' cass1)" -e CASSANDRA_CLUSTER_NAME=OpenerCluster -e HEAP_NEWSIZE=1M -e MAX_HEAP_SIZE=1024M -d cassandra:latest

>docker run --name cass3 -e CASSANDRA_SEEDS="$(docker inspect --format='{{.NetworkSettings.IPAddress}}' cass1)" -e CASSANDRA_CLUSTER_NAME=OpenerCluster -e HEAP_NEWSIZE=1M -e MAX_HEAP_SIZE=1024M -d cassandra:latest

4. Run main.py
5. The app should be working

### If You enconter an error such as:

>cassandra.cluster.NoHostAvailable: ('Unable to connect to any servers', {'172.17.0.2:9042': ConnectionRefusedError(111, "Tried connecting to [('172.17.0.2', 9042)]. Last error: Connection refused")})

then be patient, after 30 seconds try running main.py again.
Sometimes docker containers encounter errors, You can check if everything is working by using:

>docker inspect --format='{{.NetworkSettings.IPAddress}}' cass1

>docker inspect --format='{{.NetworkSettings.IPAddress}}' cass2

>docker inspect --format='{{.NetworkSettings.IPAddress}}' cass3

which should output addresses:

>172.17.0.2

>172.17.0.3

>172.17.0.4

respectively.

### When You are done with our app, we suggest running:

>docker stop cass1

>docker stop cass2

>docker stop cass3

And in case of errors, try:

>docker rm cass1

>docker rm cass2

>docker rm cass3

after which go back to step 1 above.

### Stress tests
To run the stress tests using cassandra-stress, the containers must be running, and .yaml files from this repository must be created in the docker container cass1. After that running one of the commands included in a .txt file in this repository the specific stress test will be performed and saved as a .html graph.
