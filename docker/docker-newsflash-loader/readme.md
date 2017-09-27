# Newsflash loader

The newsflash loader is able to read emails from either a mbox file or via the gmail api. The program is started via the main.py in the project or in the docker container under /loader/main.py which is also the default entry point. The loader collects the email data and converts it into a json. The json data can be written to a file or to kafka. For all options checkout the --help argument as in:

* docker run --rm newsflash-image --help
* python main.py --help


The authentication with gmail is (by now) happening through a secret.json file.
