import sys
import getopt
import time

import transform
import load



def main(argv):

    #default settings
    mboxPath = '~/Data/inovexNewsflash.mbox/mbox'
    kafkaConnect_list = ['localhost:9092']
    kafkaTopic = 'test'
    client_secret_file = './secret/client_secret.json'
    inputmode = "";
    outputmode = "";
    writefilepath = "./output/"
    scheduled = False;
    credentials_path = None

    try:
        opts, args = getopt.getopt(argv, "", ["help", "mboxpath=", "writefilepath=", "kafka=", "topic=", "secret=", "credentials=", "inputmode=", "outputmode=", "scheduled"])
    except getopt.GetoptError:
        print "newsflash-loader argument error check --help for more information"
        sys.exit(2)


    # find arguments
    for opt, arg in opts:

        if "--help" == opt:
            print "----newsflash loader help----"
            print "-----------------------------"
            print "required parameters:"
            print "--inputmode [mbox|gmail] \"the inputmode describes where the input should be taken from\""
            print "--outputmode [kafka|file] \"the outputmode describes where the output should be stored\""
            print "-----------------------------"
            print "optional parameters:"
            print "--mboxpath \"path to mbox if you want to load from mbox\""
            print "--writefilepath \"if you choose outputmethod file then this is the path to the folder you want to write in\""
            print "--kafka \"kafka host e.g. localhost:9092\""
            print "--topic \"kafka topic to wich this loader should produce\""
            print "--secret \"the path to the client secret json e.g. ~/secret.json\""
            print "--scheduled \"restartes the loading every minute\""
            print "--credentials \"set the path to the credentials file\""
            print "-----------------------------"
            print "generates the following json:"
            print(
            "{\"subject\": \"messagesubject\",\n\"formatted_timestamp\": \"datestring\",\n\"unix_timestamp\": datevalue,\n\"from\": \"sending account\",\n\"content\": \"content of newsflash\"}")
            exit()
        elif "--mboxpath" == opt:
            mboxPath = arg

        elif "--writefilepath" == opt:
            writefilepath = arg

        elif "--kafka" == opt:
            kafkaConnect_list = [arg]

        elif "--topic" == opt:
            kafkaTopic = arg

        elif "--secret" == opt:
            client_secret_file = arg

        elif "--inputmode" == opt:
            inputmode = arg

        elif "--outputmode" == opt:
            outputmode = arg

        elif "--scheduled" == opt:
            scheduled = True

        elif "--credentials" == opt:
            credentials_path = arg



    if inputmode not in ("mbox", "gmail", "debug"):
        print "newsflash-loader needs the argument --inputmode to be set to a valid value, check --help for more information"
        sys.exit(2)

    if outputmode not in ("kafka", "file", "none"):
        print "newsflash-loader needs the argument --outputmode to be set to valid value, check --help for more information"
        sys.exit(2)

    #WTF fucked up Hack
    #removing the options from the arguments bevore the import of extract so the args parser used there does not break the parsing here
    sys.argv = [sys.argv[0]]

    from extract import Extract

    print "starting newsflash loader"

    extractor = Extract()


    while True:

        print "starting extraction newsflashes"

        json_list = []
        if inputmode == "gmail":



            emails = extractor.fromGmail(client_secret_file, credentials_path)
            json_list = transform.gmailToJsonList(emails)

        elif inputmode == "mbox":
            #start data loading from mbox

            mBoxData = extractor.fromMbox(mboxPath)
            json_list = transform.mboxToJsonList(mBoxData)
        elif inputmode == "debug":
            json_list.append("Debug message newsflash loader")


        if outputmode == "kafka":
            load.loadToKafka(json_list, kafkaTopic, kafkaConnect_list)

        elif outputmode == "file":
            load.loadToFile(json_list, writefilepath)

        elif outputmode == "none":
            print json_list

        if not scheduled:
            break


        time.sleep(60)


if __name__ == "__main__":
    main(sys.argv[1:])