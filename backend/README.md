Dependency:
1. Mongodb
2. mongoengine::MongoDB [ ODM - object doment mapper on PyMongo and Motor(async python Mongo Library]
3. APSchedular
4. python daemon - pydaemon
5. python schema - pyschema
6. python greenlet 
8. pyzmq framework
9. Config parser
10. 

Config file:
 config/* : ini file and default values
 batch/*  : [offline] APSchedular with system batchfiles and interative shell and batch processor using doit
 batch/systembatches/*: all 7 system batch detail implementations 
 models/*: mongoengine documents and schema files, Mongo constants 
 pubsub/*: interprocess observer pattern to communicate from offline processes to post-processings 
 daemon/*: [post-processing] pydaemon based post processing framework using thread executors
 integrtion/*: integration with CC processor and Bank ACH processor 
 
 