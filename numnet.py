import sys
import random
import string
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('message', help='message to be encoded')
parser.add_argument('--pad', help='one-time pad. if not user, one will be generated')
parser.add_argument('--voice', help='specify an osx say voice')
parser.add_argument('--chime', help='specify a chime file')
parser.add_argument('--output', help="path to save output file. If not specified, file will be uploaded to vocaroo")
args = parser.parse_args()

def getNums(mess):
    message_code = ""
    for c in mess:
        if c != " ":
            message_code = message_code + str(ord(c.upper()) - 64) + " "
    return message_code

def cleanse(mess):
    return filter(lambda c: c.isalpha(), mess).upper()

def randString(length):
    return "".join(random.choice(string.ascii_uppercase) for _ in range(length))

def getDiff(mess, coded):
    key = []
    mess = mess.split()
    coded = coded.split()
    for index in range(len(mess)):
        num = int(mess[index]) - int(coded[index])
        if num < 0:
            num = num + 26
        key.append(str(num))
    return ". ".join(key)

def pickRandomFromFile(filePath):
    return random.choice([line.rstrip('\n') for line in open(filePath)])

def getReader():
    if(args.voice):
        return args.voice
    else:
        return pickRandomFromFile('readers.txt')

def getChime():
    os.system('ls sounds/chimes > .temp/chimes.txt')
    return pickRandomFromFile('.temp/chimes.txt')

def getNoise():
    os.system('ls sounds/noises > .temp/noises.txt')
    return pickRandomFromFile('.temp/noises.txt')

def composeCmd(commands):
    os.system(" && ".join(commands))

def createListFile(chime):
    if(args.chime):
        chimeFile = "'../" + args.chime + "'"
    else:
        chimeFile = "'../sounds/chimes/" + chime + "'"
    f = open('.temp/list.txt', 'w')
    order = [
        "file " + chimeFile,
        "file 'numbers.mp3'",
        "file " + chimeFile,
        "file 'numbers.mp3'",
        "file " + chimeFile,
    ]
    for item in order:
        f.write("%s\n" % item)
    f.close()

def makeSound(numbers, reader, chime, noise):
    if args.output:
        output = args.output
        upload = 'echo "file saved to ' + args.output + '"'
    else:
        output = '.temp/output.mp3'
        upload = 'curl --form \"upload_data=@.temp/output.mp3\" http://s0.vocaroo.com/media/upload.php'
    createListFile(chime)
    composeCmd([
        "say -r 60 -v " + reader + " -o .temp/numbers.wav --data-format=LEF32@7500 " + numbers,
        "ffmpeg -y -v 0 -i .temp/numbers.wav -af \"volume=1.7\" .temp/numbers.mp3",
        "ffmpeg -y -v 0 -f concat -safe 0 -i .temp/list.txt -c copy .temp/catnums.mp3",
        "ffmpeg -y -v 0 -i .temp/catnums.mp3 -i sounds/noises/" + noise + " -filter_complex amerge " + output,
        upload
    ])
    
def makeTempDir():
    os.system('mkdir .temp')

def rmTempDir():
    os.system('rm -rf .temp')

def mainSteps():
    makeTempDir()

    message = cleanse(sys.argv[1])
    message_nums = getNums(message)
    length = len(message)

    if args.pad:
        coded_message = cleanse(args.pad)
    else:
        coded_message = randString(length)

    coded_nums = getNums(coded_message)
    
    print coded_message
    print getDiff(message_nums, coded_nums)

    makeSound(getDiff(message_nums, coded_nums), getReader(), getChime(), getNoise())
    rmTempDir()

mainSteps()
