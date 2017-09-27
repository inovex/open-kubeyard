# docker-tranquility

Docker image of the [Druid](http://druid.io/) client [tranquility](https://github.com/druid-io/tranquility)

## Usage
The entrypoint of this image is `tranquility`, with `server -configFile /etc/tranquility/server.json` as the default command. Mount your config dir to `/etc/tranquility` and adjust the default command to your needs.
