#Importation des modules permettant d'afficher un diagramme de gantt

import pandas as pd
import plotly.express as px



tab = [
    [1, 13, 6, 2],
    [10, 12, 18, 18],
    [17, 9, 13, 4],
    [12, 17, 2, 6],
    [11, 3, 5, 16]]

tab_normal= [[1,10,17,12,11],
[13,12,9,17,3],
[6,18,13,2,5],
[2,18,4,6,16]
]

#Fonction de l'heuristique GUPTA retourne C_max et retourne un dictionnaire contenant l'ordonnacement des taches, leur date de debut,et de fin
#La fonction prend en parametres un meme tableau disposé de 2 manieres differentes 
#dans le tableau 'tab_normal' chaque ligne represente une machine
#dans le tableau 'tab' chaque ligne represente une tache

def gupta(tab,tab_normal): 

    #Recuperation du nombre de taches et de machines
    nb_taches = len(tab)
    nb_machines = len(tab_normal)

    
    tab2= []  #creation du tableau tab2
    for t in tab :
        temp =[]
        for i in range(len(t)-1) :
            temp.append(t[i]+t[i+1]) #Pik + Pik+1
        tab2.append(temp)


    #Rajouter pour chque ligne le minimum de Pik + Pik+1
    for t in tab2 :
        t.append(min(t))

    #Trouver pour chaque ligne ei
    for i in range(len(tab)):
        if tab[i][0]<tab[i][-1]:
            tab2[i].append(1)
        else:
            tab2[i].append(-1)
    
    #Calculer et ajouter si
    for t in tab2 :
        t.append(t[-1]/t[-2])

    
    tache_si={}
    for i in range(len(tab2)) :
         tache_si[i+1]=tab2[i][-1]

    #Tri des taches selon l'ordre decroissant si
    tache_si = dict(sorted(tache_si.items(),key=lambda item: item[1],reverse=True))

    #Recuperer l'ordre des taches dans un tableau 'classement'
    classement = []
    for k in tache_si.keys() :
        classement.append(k)

    #Trier le tableau tab_normal selon l'ordre des taches
    temp =[]
    x=[]
    for i in range(nb_machines):
        for j in classement :
            x.append(tab_normal[i][j-1])
        temp.append(x)
        x=[]

    tab_normal=temp

    #Initialiser le dictionnaire 'machines' , et pour chaque machine assigner un dictionnaire de taches
    machines = {}
    for i in range(nb_machines):
        machines['M'+str(i+1)] = {}

    #Pour chaque tache assigner un dictionnaire contenant la date de debut , de fin, et le temps d'execution
    for i in range(nb_machines):
        for j in classement :
            machines['M'+str(i+1)]['T'+str(j)]={'début': 0, 'C':0,'fin':0}
    
    #Initialiser la liste affichage qui nous a servi lors de l'affichage des donnees dans un diagramme de gantt
    affichage = []
    #Initialiser la premier tache de la premiere machine
    temp = {'début':0 ,
     'C':tab[0][0],
     'fin' : tab[0][0]
    }
    machines['M1']['T1']=temp

    #J'ai considéré lors de l'affichage dans le diagramme que chaque nombre représente une année apres 2000
    #Par exemple : si une tache commence dans le tableau a 19, alors lors de la representation sur le diagramme elle commence a 2019
    affichage.append(dict(Tache= 'T1', Start= '2000-1-1' , End=str(2000+tab[0][0])+'-1-1', Machine='M1'))


    for i in range(nb_machines):
        for j in range(nb_taches) :
            if i==0 and j==0 :  #Eviter la premier valeur
                pass
            if i==0 : #Cas de la premier machine (Il n'y a pas de machines precedente)

                m = list(machines.items())[i][0] # Cle de la machine 
                #print(m)
                m_t=list(machines[m].items())[j][0] # Cle tache
                m_tp=list(machines[m].items())[j-1][0]  #Cle tache precedente sur la machine actuelle
                
                machines['M1'][m_t]['début']= machines['M1'][m_tp]['fin'] # Chaque tache commence lorsque la precedente prend fin
                machines['M1'][m_t]['C']=tab_normal[0][j]
                var = machines['M1'][m_t]['début']+machines['M1'][m_t]['C']
                machines['M1'][m_t]['fin']= var  #Fin = debut + temps d'execution

                #Ajouter les informations a la liste affichage
                affichage.append(dict(Tache= m_t , Start= str(2000+machines['M1'][m_t]['début'])+'-1-1' , End= str(2000+var)+'-1-1', Machine='M1'))
                #print(machines['M1'][m_t])
                pass
            else :
                m = list(machines.items())[i][0] # Cle de la machine
                m_t=list(machines[m].items())[j][0] # Cle de la tache
                #print(m)
                mp=list(machines.items())[i-1][0] # Cle de la machine precedente
                mp_t=list(machines[mp].items())[j][0] # Cle de la meme tache dans la machine precedente
                m_tp=list(machines[m].items())[j-1][0] # Cle de la tache precedente sur la meme machine
                
                machines[m][m_t]['début']=max(machines[mp][m_t]['fin'],machines[m][m_tp]['fin']) #Max(fin tache precedente sur la machine , Fin de la tache sur la machine precedente)
                machines[m][m_t]['C']=tab_normal[i][j]
                var = machines[m][m_t]['début']+machines[m][m_t]['C']
                machines[m][m_t]['fin']= var

                affichage.append(dict(Tache= m_t , Start= str(2000+machines[m][m_t]['début'])+'-1-1' , End= str(2000+var)+'-1-1', Machine=m))
    #Recuperer C_max            
    m = list(machines.items())[-1][0]
    m_t=list(machines[m].items())[-1][0]
    c_max= machines[m][m_t]['fin']

    #Mettre la liste 'affichage' comme parametre pour le dataframe
    df = pd.DataFrame(reversed(affichage))
    fig=px.timeline(df, x_start="Start", x_end="End", y="Machine", color="Tache")
    #Affichage du diagramme de gantt dans le navigateur
    fig.show()

    return machines , c_max

gupta(tab,tab_normal) # Tester l'algorithme sur les tables :tab et tab_normal
