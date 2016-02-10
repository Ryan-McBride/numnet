import sys
import random
import string
import os

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

def getReader():
    return random.choice([line.rstrip('\n') for line in open('lists/readers.txt')])

def getChime():
    return random.choice([line.rstrip('\n') for line in open('lists/chimes.txt')])

def composeCmd(commands):
    os.system(" && ".join(commands))

def createListFile(chime):
    f = open('.temp/list.txt', 'w')
    order = [
        "file '../sounds/" + chime + "'",
        "file 'numbers.mp3'",
        "file '../sounds/" + chime + "'",
        "file 'numbers.mp3'",
        "file '../sounds/" + chime + "'"
    ]
    for item in order:
        f.write("%s\n" % item)
    f.close()

def makeSound(numbers, reader, chime):
    createListFile(chime)
    composeCmd([
        "say -r 20 -v " + reader + " -o .temp/numbers.wav --data-format=LEF32@7500 " + numbers,
        "ffmpeg -y -v 0 -i .temp/numbers.wav .temp/numbers.mp3",
        "ffmpeg -y -v 0 -f concat -i .temp/list.txt -c copy .temp/catnums.mp3",
        "ffmpeg -y -v 0 -i .temp/catnums.mp3 -i sounds/longnoise.mp3 -filter_complex amerge output.mp3"
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

    if len(sys.argv) > 2:
        coded_message = cleanse(sys.argv[2])
    else:
        coded_message = randString(length)

    coded_nums = getNums(coded_message)

    makeSound(getDiff(message_nums, coded_nums), getReader(), getChime())
    rmTempDir()
    
    print coded_message
    print getDiff(message_nums, coded_nums)

mainSteps()
