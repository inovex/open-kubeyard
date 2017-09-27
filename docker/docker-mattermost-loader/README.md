# Mattermost Loader

Within Mattermost so called outgoing webhooks can be defined. These webhooks send chat data to a defined address whenever a new message is occurring within the given channel. The mattermost-loader provides a interface to collect this data and writes it to a defined kafka topic as JSON. The mattermost-loader provides two interfaces for storing data:

* ```http://adress:8080/log``` logs the data in the same format as it is provided by the hook (without critical data like tokens)
* ```http://adress:8080/logasdump``` provides the data in the same format a mattermost dump would generate

The configuration of a webhook must be defined as follows:

* Content Type => application/json
* Trigger Words => must stay empty
* Callback URLs => the url to the mattermost loader e.g. http://12.34.56.78:8080/log

The mattermost-loader is realized as a fatjar which is capsuled in a docker container. See the **Dockerfile** for detailed information.
The fatjar has two arguments ```kafkatopic``` and ```kafkaconnect``` which specify where the data will be published to e.g.: ```--kafkatopic test --kafkaconnect kafka.kubeyard:9092```
