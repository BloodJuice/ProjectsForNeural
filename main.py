import os, shutil, re
from operator import itemgetter

def search():
    for adress, dirs, files in os.walk("E:\Нейронки\\r4"):
        for file in files:
            if file.endswith('.txt'):
                yield os.path.join(adress, file)

def read_from_pathtxt(path):
    with open(path, 'r') as r:
        for line in r:
            return line

# Сортировка файлов, в которых задаваемые параметры числовые. Параметры типо True, False пропускаем мимо.
def transformTextForNumberInCountValue(number1, number2, hub):
    for i in range(len(hub)):
        hub[i] = re.findall(r'\w+|[-+]?(?:\d+(?:\.\d*)?|\.\d+)', hub[i])
    for i in range(len(hub)):
        # print("TRANSFORM:\t", hub[i])
        hub[i][number2] = float(hub[i][number2])
        if hub[i][number1] != 'True' and hub[i][number1] != 'False':
            if hub[i][number1] != 'caption_base_best' and hub[i][number1] != 'caption_huge_best':
                hub[i][number1] = float(hub[i][number1])
    return hub

def parserFirst(nameFile, group, folder):
    hubSlave, hubMain = [], []
    counter = 1
    for i in search():
        # print(str(i))
        # lineSplit = i.split("\\")
        lineSplit = re.findall(r'\w+|[-+]?(?:\d+(?:\.\d*)?|\.\d+)', str(i))
        # print(lineSplit)
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
            print("HERE")
            hubSlave = transformTextForNumberInCountValue(number1=1, number2=3, hub=hubSlave)
            hubSlave = sorted(hubSlave, key=itemgetter(3))

            for i in range(counter - 1):
                hubMain.append(hubSlave[i])
            hubSlave.clear()
            counter = 1
    # for i in range(len(hubMain)):
    #     print("Main\t", hubMain[i])


    # Сортировка строк по значению параметров
    hubMain = sorted(hubMain, key=itemgetter(1))

    # Снова превращаю числа в строки
    for i in range(len(hubMain)):
        hubMain[i][3] = str(hubMain[i][3])
        if hubMain[i][1] != 'True' and hubMain[i][1] != 'False':
            if hubMain[i][1] != 'caption_base_best' and hubMain[i][1] != 'caption_huge_best':
                hubMain[i][1] = str(hubMain[i][1])

    # for i in range(60):
    #     print(hubMain[i])

    with open('E:\Нейронки\Parser\\files\\' + nameFile + '.txt', 'w') as file:
        for i in range(len(hubMain)):
            file.write(' '.join(hubMain[i]) + '\n')

def searcherParams():
    param, groupNew = [], 'beam'
    for i in search():
        lineSplit = re.findall(r'\w+', i)
        if lineSplit[3] != groupNew:
            param.append(groupNew)
            groupNew = lineSplit[3]
            if groupNew == 'unnormalized':
                param.append(groupNew)
    return param

def main():
    params = searcherParams()
    for j in range(len(params)):
        parserFirst(nameFile=params[j], group=3, folder=4)




if __name__ == '__main__':
    main()