import os, shutil, re
from operator import itemgetter

def search(nameWay):
    for adress, dirs, files in os.walk(nameWay):
        for file in files:
            if file.endswith('.txt'):
                yield os.path.join(adress, file)

def read_from_pathtxt(path):
    with open(path, 'r') as r:
        for line in r:
            return line

def readFileForAnalysys(path):
    cloud = []
    with open(path, 'r') as r:
        for line in r:
            cloud.append(line)
    return cloud

# Сортировка файлов, в которых задаваемые параметры числовые. Параметры типо True, False пропускаем мимо.
def transformTextForNumberInCountValue(number1, number2, hub):
    for i in range(len(hub)):
        hub[i] = re.findall(r'\w+|[-+]?(?:\d+(?:\.\d*)?|\.\d+)', hub[i])
    for i in range(len(hub)):
        hub[i][number2] = float(hub[i][number2])
        if hub[i][number1] != 'True' and hub[i][number1] != 'False':
            if hub[i][number1] != 'caption_base_best' and hub[i][number1] != 'caption_huge_best':
                hub[i][number1] = float(hub[i][number1])
    return hub

def parserFirst(nameWay, nameFile, group, folder):
    hubSlave, hubMain = [], []
    counter = 1
    for i in search(nameWay):
        lineSplit = re.findall(r'\w+|[-+]?(?:\d+(?:\.\d*)?|\.\d+)', str(i))
        try:
            saver = abs(int(float(lineSplit[6])))
        except Exception:
            try:
                saver = abs(int(float(lineSplit[7])))
            except Exception:
                saver = abs(int(float(lineSplit[8])))

        if lineSplit[group] == nameFile:
            hubSlave.append("FILE_FOLDER:\t" + lineSplit[folder] + " PIC: " + str(saver) + "\t" + read_from_pathtxt(i) + "\n")
            counter += 1
        if counter == 60:
            hubSlave = transformTextForNumberInCountValue(number1=1, number2=3, hub=hubSlave)
            hubSlave = sorted(hubSlave, key=itemgetter(3))

            for i in range(counter - 1):
                hubMain.append(hubSlave[i])
            hubSlave.clear()
            counter = 1

    # Сортировка строк по значению параметров
    hubMain = sorted(hubMain, key=itemgetter(1))

    # Снова превращаю числа в строки
    for i in range(len(hubMain)):
        hubMain[i][3] = str(hubMain[i][3])
        if hubMain[i][1] != 'True' and hubMain[i][1] != 'False':
            if hubMain[i][1] != 'caption_base_best' and hubMain[i][1] != 'caption_huge_best':
                hubMain[i][1] = str(hubMain[i][1])

    with open('E:\Нейронки\Parser\\files\\' + nameFile + '.txt', 'w') as file:
        for i in range(len(hubMain)):
            file.write(' '.join(hubMain[i]) + '\n')
    return 0

def searcherParams(nameWay, positionGroup):
    param, groupNew = [], 'beam'
    for i in search(nameWay):
        lineSplit = re.findall(r'\w+', i)
        if lineSplit[positionGroup] != groupNew:
            param.append(groupNew)
            groupNew = lineSplit[positionGroup]
            if groupNew == 'unnormalized':
                param.append(groupNew)
    return param

def similarStrings(nameWay, nameLine):
    cloud = []
    for i in search(nameWay):
        for fileReadLine in readFileForAnalysys(i):
            try:
                if (re.search(nameLine, fileReadLine)).group() == nameLine:
                    cloud.append('true')
            except Exception:
                cloud.append('false')
        print(cloud)
        cloud.clear()
def main():
    params = searcherParams(nameWay="E:\Нейронки\\r4", positionGroup=3)
    for j in range(len(params)):
        parserFirst(nameWay="E:\Нейронки\\r4", nameFile=params[j], group=3, folder=4)
    # way = "E:\Нейронки\Parser\\files"
    # params = searcherParams(nameWay=way, positionGroup=4)
    # similarStrings(nameWay=way, nameLine='man')


if __name__ == '__main__':
    main()