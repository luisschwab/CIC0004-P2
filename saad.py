import os
import csv

CODE  = 0
NAME  = 1
CLASS = 2
SEMESTER  = 3
PROFESSOR = 4
TIME = 5
OFFERS = 6
OCCUPIED = 7
PLACE = 8

mempool = []
saved = []


def Input():
    global command, argument
    command, *argument = input().split(maxsplit=1)

def leia():
    for i in argument:
        if i in saved:
            pass
        else:
            try:
                with open(i, 'r') as file:
                    next(file)
                    reader = csv.reader(file)
                    current = {}
                    for row in reader:
                        current['code'] = row[CODE]
                        current['name'] = row[NAME]
                        current['class'] = row[CLASS]
                        current['semester'] = row[SEMESTER]
                        current['professor'] = row[PROFESSOR]
                        current['time'] = row[TIME]
                        current['offers'] = row[OFFERS]
                        current['occupied'] = row[OCCUPIED]
                        current['place'] = row[PLACE]

                        mempool.append(current)
                        current = {}
                    saved.append(i) 
            except:
                print(f"\nerror opening {os.path.abspath(i)}\n")

def carga():
    teach = []
    profName = " ".join(argument)
    for i in range(len(mempool)):
        x = mempool[i]
        for value in x.values():
            if profName in value:
                teach.append(mempool[i])
    teach = sorted(teach, key = lambda x: (x['name'], x['class']))

    if (not teach):
        print(f"No hay {profName}...")
    else:
        subjects, classes = [], []
        prev = teach[0]
        for p in teach:
            if(p['code'] == prev['code']):
                classes.append(p)
            else:
                subjects.append(classes)
                classes = []
                
                classes.append(p)
            prev = p
        subjects.append(classes)

        ctc, num = 0, 0
        print(profName + ":")
        for k in subjects:
            print(" * " + k[0]['name'] + " (" + k[0]['code'] + "):")
            for l in k:
                removeFromName = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyz ()"
                workload = l['professor']
                for char in removeFromName:
                    workload = workload.replace(char, "")
                if(int(l['occupied']) >= 6):
                    num += int(l['occupied'])
                    ctc += int(workload)
                
                print("     Turma " + l['class'] + ": " + workload + "h (" + l['occupied'] + " alunos)")
        print(f"[Carga total considerada: {ctc}h ({ctc/num:.2f}h/aluno)]")

def matriculas():
    noDuplicates = []
    current = []
    notFound = []

    classCODES = argument[0].split(" ")
    for classCode in classCODES:
        found = False
        for row in mempool:
            if row['code'] == classCode:
                current.append(row)
                found = True

        if(not found):
            notFound.append(classCode)
        
        current = sorted(current, key = lambda x: (x['name'], x['class']))

        for i in current:
            for j in current:
                if(i==j):
                    break
                if(i['name'] == j['name'] and i['class'] == j['class']):
                    current.remove(i)

        if(found):
            noDuplicates.append(current)
        current = []

    output = []
    for i in noDuplicates:
        sum = 0
        current = {}
        for j in i:
            sum += int(j['occupied'])
        current['code'] = j['code']
        current['name'] = j['name']
        current['sum'] = sum

        output.append(current)    

    output = sorted(output, key = lambda x: x['sum'], reverse = True)
    notFound = sorted(notFound)
    
    for i in output:
        print(f"{i['sum']} matriculados em {i['name']} ({i['code']})")
    for j in notFound:
        print(f"No hay {j}...")


if __name__ == "__main__":

    Input()
    while(1):
        if(command == 'FIM'):
            quit()
        elif(command == 'leia'):
            leia()
        elif(command == 'carga'):
            carga()
        elif(command == 'matriculas'):
            matriculas()
        else:
            print("Comando inválido.")
        Input()