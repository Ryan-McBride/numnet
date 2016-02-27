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

def pickRandomFromFile(filePath):
    return random.choice([line.rstrip('\n') for line in open(filePath)])

def getReader():
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
    f = open('.temp/list.txt', 'w')
    order = [
        "file '../sounds/chimes/" + chime + "'",
        "file 'numbers.mp3'",
        "file '../sounds/chimes/" + chime + "'",
        "file 'numbers.mp3'",
        "file '../sounds/chimes/" + chime + "'"
    ]
    for item in order:
        f.write("%s\n" % item)
    f.close()

def makeSound(numbers, reader, chime, noise):
    createListFile(chime)
    composeCmd([
        "say -r 60 -v " + reader + " -o .temp/numbers.wav --data-format=LEF32@7500 " + numbers,
        "ffmpeg -y -v 0 -i .temp/numbers.wav -af \"volume=1.7\" .temp/numbers.mp3",
        "ffmpeg -y -v 0 -f concat -i .temp/list.txt -c copy .temp/catnums.mp3",
        "ffmpeg -y -v 0 -i .temp/catnums.mp3 -i sounds/noises/" + noise + " -filter_complex amerge .temp/output.mp3",
        "curl --form \"upload_data=@.temp/output.mp3\" http://s0.vocaroo.com/media/upload.php"
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
    
    print coded_message
    print getDiff(message_nums, coded_nums)

    makeSound(getDiff(message_nums, coded_nums), getReader(), getChime(), getNoise())
    rmTempDir()

mainSteps()
