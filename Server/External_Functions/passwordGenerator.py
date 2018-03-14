import random

def passwordGenerator(pass_length):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    upperalphabet = alphabet.upper()
    tempPassList = []

    for i in range(pass_length//3):
        tempPassList.append(alphabet[random.randrange(len(alphabet))])
        tempPassList.append(upperalphabet[random.randrange(len(upperalphabet))])
        tempPassList.append(str(random.randrange(10)))

    for j in range(pass_length-len(tempPassList)):
        tempPassList.append(alphabet[random.randrange(len(alphabet))])

    random.shuffle(tempPassList)
    pwstring = "".join(tempPassList)
    return pwstring



