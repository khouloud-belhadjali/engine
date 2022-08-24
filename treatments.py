import os
import math 
import numpy as np
import os
def lecture_online(chemin_acces):
    t4 = [0, 0]
    list_strokes= [0, 0, 0, 0]
    detecteur1 = [0, 0, 0, 0]
    detecteur2 = [0, 0]
    ALL = [0, 0]
    tab = []
    res = []
    vecteur = []
    sum = 0
    with open(chemin_acces, 'r', encoding="utf8") as f:
        tline = f.readlines()
    for v in tline:
        if "<trace>" in v :
            tab.append(v)              #ici j'ai recupéré les strokes ,je les ai mis dans tab
    for i in range(0, len(tab)):
            ch = tab[i].split('e>')    #je vais parcourir chaque tracé un par un
            ch = ch[1]
            ch = ch.split('</')
            ch = ch[0]                 #ici j'ai recupéré ce qui est entre <trace> </trace>
            t = ch.split(",")           #t est une liste qui contient des lots de 4 valeurs
            for k in range(0, len(t)):
                t1 = t[k].split(' ')
                list_strokes = np.vstack([list_strokes, [float(t1[0]), float(t1[1]), float(t1[2]), float(t1[3])]])
               # sum = sum+float(t1[1])
            list_strokes = np.vstack([list_strokes, detecteur1])
    list_strokes = np.delete(list_strokes, (len(list_strokes)-1), axis=0)
    return list_strokes
#*************************************calcule max et min*******************************

def maxi(lettre,j):
    max=lettre[0][j]
    res =0
    for i in range(1, len(lettre)):
        if(lettre[i][j]>max): #car max des y =0
            max=lettre[i][j]
            res = i
    return lettre[res][j]
def min(lettre,j): #j est soit 0(x) soit1(y)
    min=lettre[0][j]
    res =0
    for i in range(1, len(lettre)):
        if(lettre[i][j] < min):
            min=lettre[i][j]
            res = i
    return lettre[res][j]
    
def moyenne(lettre):
    sum =0
    for i in range(0, len(lettre)):
        sum = sum +lettre[i][1]
    y_moyenne = sum /len(lettre)
    return y_moyenne

#************************************* is_a_dot *******************************

def is_a_dot(obj):

    diagonale = math.sqrt(pow((maxi(obj,0) - min(obj,0)),2)+pow((maxi(obj,1) - min(obj,1)),2))
    if(0.001<diagonale<7):
        return True
    else:
        return False
#************************************* detect_dots *******************************
#for i in range(0,lent(ref)):
    #calculer le moy
def position(obj):
    positions = np.where(~obj.any(axis=1))[0] #celui detect une ligne de zeos
    return positions
#print(positions) #les position de zero

positions= []
def detect_dots(obj):
    y_moyenne = moyenne(obj)
    list = []
    stroke =[0,0]
    positions = position(obj)
    for i in range(0, len(positions)):
        start = positions[i]+1
        if(not (i == len(positions)-1)):
            end = positions[i+1]
        else:
            end = len(obj)
        for j in range(start, end):
            t1 = obj
            stroke = np.vstack([stroke, [float(obj[j][0]), float(obj[j][1])]])
        stroke = np.delete(stroke, (0), axis=0)
        if(is_a_dot(stroke)):
            if(stroke[0][1]<y_moyenne and stroke[len(stroke)-1][1] < y_moyenne):
                list.append('+1')
            elif(stroke[0][1]>y_moyenne and stroke[len(stroke)-1][1] > y_moyenne):
                list.append('-1')
        else:
            list.append('0')
        stroke=[0,0]
      #  if(is_a_dot(stroke)):

    return list

#************************************* delete_dots *******************************
def detect_strokes(obj,number): #number soit 0 pour dire j'extract tous les points, 1 pour extraire jute le premier et le dernier point de stroke
    nb = number
    detecteur1 = [0, 0, 0, 0]
    positions = position(obj)
    lettres_without_dots = [0, 0, 0, 0]
    stroke = [0, 0, 0, 0]
    for i in range(0, len(positions)):
        start = positions[i] + 1
        if (not (i == len(positions) - 1)):
            end = positions[i + 1]
        else:
            end = len(obj)
        for j in range(start, end):
            #t1 = obj[j]
            if(nb == 1):
                if(j == start or j == end-1 ):
                    stroke = np.vstack([stroke, [float(obj[j][0]), float(obj[j][1]), float(obj[j][2]), float(obj[j][3])]])
            elif(nb ==0):
                stroke = np.vstack([stroke, [float(obj[j][0]), float(obj[j][1]), float(obj[j][2]), float(obj[j][3])]])
        stroke = np.delete(stroke, (0), axis=0)
        if (not (is_a_dot(stroke)) ):
            lettres_without_dots = np.vstack([lettres_without_dots, stroke])
            if (nb == 0): #car quand j'extracte le premier et le dernier point de chaque stroke je veux pas un detecteur
                lettres_without_dots = np.vstack([lettres_without_dots, detecteur1])

        stroke = [0, 0, 0, 0]
    lettres_without_dots = np.delete(lettres_without_dots, (0), axis=0)
    if (nb == 0):
        lettres_without_dots = np.delete(lettres_without_dots, (len(lettres_without_dots) - 1), axis=0)

    return lettres_without_dots
#************************************* delete_dots *******************************

def clean_dots(obj):
    clean_letter = detect_strokes(obj,0)
    return clean_letter
#************************************* detect_penlift *******************************
def detect_penlift(obj):
    aux = [0,0,0,0]
    aux= np.vstack([aux,clean_dots(obj)])
    penlift = detect_strokes(aux,1)
    return penlift
#************************************* analyse_penlift *******************************
def analyse_penlift(ref,trace):
    detect_strokes = detect_penlift(trace)
    out = [0, 0, 0, 0]
    seuil = 5;
    out = [0, 0, 0, 0];
    success = [0, 0, 0, 0];  # if (nb_stroke_ref == nb_stroke_tracé)
    fail = [1, 1, 1, 1];
    if (len(detect_strokes)/2 > len(detect_penlift(ref))/2):
        for j in range(2, len(detect_strokes), 2):
            aux = detect_strokes[:][j - 1]
            if (j % 2) == 0:
               #if(aux[0] - seuil < detect_strokes[j][0] < aux[0] + seuil or aux[1] - seuil < detect_strokes[j][1] < aux[1] + seuil): # car impossible d'avoir 2 strokes qui ont des valeurs en x ou en y qui sont proche
                distance = math.sqrt(pow((detect_strokes[j][0] - detect_strokes[j-1][0]),2)+pow((detect_strokes[j][1] - detect_strokes[j-1][1]),2))
                if(distance<70):
                    aux = detect_strokes[:][j - 1]
                    out = np.vstack([out, aux])
    elif (len(detect_strokes)/2 < len(detect_penlift(ref))/2):
        out = np.vstack([out, [fail]])
    else:
        out = np.vstack([out, [success]])
    out = np.delete(out, (0), axis=0)
    return str(out)
#************************************* analyse_penlifts *******************************
def analyse_all_penlifts(trace):
    detecteur1 = [0, 0, 0, 0]
    positions = position(trace)
    all_strokes = [0, 0, 0, 0]
    stroke = [0, 0, 0, 0]
    for i in range(0, len(positions)):
        start = positions[i] + 1
        if (not (i == len(positions) - 1)):
            end = positions[i + 1]
        else:
            end = len(trace)
        for j in range(start, end):
            # t1 = obj[j]
                if (j == start or j == end - 1):
                    stroke = np.vstack([stroke, [float(trace[j][0]), float(trace[j][1]), float(trace[j][2]), float(trace[j][3])]])
    stroke = np.delete(stroke, (0), axis=0)
    tracets=stroke[1]
    for k in range(0,len(stroke)):
        if (k%2 !=0):
            all_strokes = np.vstack([all_strokes, stroke[k]])
    all_strokes = np.delete(all_strokes, (0), axis=0)
    return str(all_strokes)
#************************************* Underflow *******************************
def detect_underflow(trace):
    tracet = np.delete(trace, np.where(~trace.any(axis=1))[0], axis=0)
    overlines =[0, 0, 0, 0]
    points = [0, 0, 0, 0]
    nb =maxi(tracet,1)
    if(min(tracet,1)>100):
        for i in range(0,len(tracet)):
            if(min(tracet,1)<tracet[i][1] < min(tracet,1)+5):
                overlines = np.vstack([overlines,[tracet[i][0],tracet[i][1],tracet[i][2], tracet[i][3]]])
        overlines =np.delete(overlines, (0), axis=0)
        print("sous ligne")
        points = np.vstack([overlines[0], overlines[len(overlines) - 1], [overlines[0][0], 100, 0, 0],[overlines[len(overlines)-1][0], 100, 0, 0]])
        #return "lettre sous la ligne"
    elif(maxi(tracet,1)<95):
        for i in range(0,len(tracet)):
            if(maxi(tracet,1)-5<tracet[i][1] < maxi(tracet,1)):
                overlines = np.vstack([overlines,[tracet[i][0],tracet[i][1],tracet[i][2],tracet[i][3]]])
        overlines =np.delete(overlines, (0), axis=0)
        #print("sur ligne")
        points = np.vstack([overlines[0],overlines[len(overlines)-1],[overlines[0][0],100,0,0],[overlines[len(overlines)-1][0],100,0,0]])
    else:
        points = np.vstack([overlines])
    return str(points)
#************************************* Overflow *******************************
def detect_overflow(trace,expected):
    traces = clean_dots(trace)
    tracet = np.delete(traces, np.where(~traces.any(axis=1))[0], axis=0)
    overlines =[0, 0]
    points = [0, 0]
    nb =maxi(tracet,1)
    if(min(tracet,1)<50 and expected != "alif" and expected != "kef" and expected != "lem" and expected != "tad" and expected != "dha"):
        for i in range(0,len(tracet)):
            if(min(tracet,1)<tracet[i][1] < 50):
                overlines = np.vstack([overlines,[tracet[i][0],tracet[i][1]]])
        overlines =np.delete(overlines, (0), axis=0)
        maximum_over=overlines[0][0]
        minimum_over=overlines[0][0]
        max_over=0
        min_over=0
        for j in range(1,len(overlines)):
          if (overlines[j][0]>maximum_over):
            max_over =j
            maximum_over=overlines[j][0]
          if(overlines[j][0]<minimum_over):
            min_over=j
            minimum_over=overlines[j][0]
        points = np.vstack([overlines[max_over], overlines[min_over]])
    else:
        points = np.vstack([overlines])
    return str(points)
#************************************* Direction *******************************
def detect_reverse_direction(trace,expected):
    res = 1
    aux = [0, 0, 0, 0]
    aux = np.vstack([aux, clean_dots(trace)])
    stroke = [0, 0,0,0]
    positions = position(aux)
    for i in range(0, len(positions)):
        start = positions[i] + 1
        if (not (i == len(positions) - 1)):
            end = positions[i + 1]
        else:
            end = len(aux)
        for j in range(start, end):
            stroke = np.vstack([stroke, [float(aux[j][0]), float(aux[j][1]),float(aux[j][2]),float(aux[j][3])]])
        stroke = np.delete(stroke, (0), axis=0)
        if(expected != "ha" and expected != "kha" and expected != "jim"  and expected != "haa"):
          if (((abs(stroke[0][1]-stroke[len(stroke)-1][1]) < abs(stroke[0][0]-stroke[len(stroke)-1][0])) and stroke[0][0] <stroke[len(stroke)-1][0]) or ((abs(stroke[0][1]-stroke[len(stroke)-1][1]) > abs(stroke[0][0]-stroke[len(stroke)-1][0])) and stroke[0][1] >stroke[len(stroke)-1][1])):
              #fault_direction_stroke=np.vstack([fault_direction_stroke,stroke])
              #print("fault direction")
              res = 0
        else:
          if ((abs(stroke[0][1]-stroke[len(stroke)-1][1]) < abs(stroke[0][0]-stroke[len(stroke)-1][0])) and stroke[0][0] >stroke[len(stroke)-1][0]):
            res = 0
        stroke =[0, 0, 0, 0]
    return str(res)
#************************************* Order *******************************
def detect_invalid_order(ref, trace, expected):
    references = detect_penlift(ref)
    traces = detect_penlift(trace)
    resultat = 1
    aux = [0, 0, 0, 0]
    aux = np.vstack([aux, clean_dots(trace)])
    positions = position(aux)
    lettres_without_dots = [0, 0, 0, 0]
    longueur1 = 0
    longueur2 = 0
    nb = 0
    stroke = [0, 0, 0, 0]

    if (expected == "dha" or expected == "tad"):
        if (len(references) / 2 != len(traces) / 2):
            resultat = 0
        if (len(references) / 2 == len(traces) / 2):
          if((abs(traces[0][0]-traces[1][0])<abs(traces[0][1]-traces[1][1])) and (abs(traces[2][0]-traces[3][0])>abs(traces[2][1]-traces[3][1]))):
            resultat = 0
    return str(resultat)
#************************************* Form *******************************
