import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
import urllib.request
import json
import re
import os 
from datetime import date
from datetime import datetime
import time
import xlwt
import stanza
#import glob
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import operator



nlp = stanza.Pipeline(lang='fr', processors="tokenize,pos,lemma")

dico_nbw = {}



stop_words = stopwords.words('french')
stop_words += ['ce', 'souvent', 'depuis', 'Nous', 'cela', 'après', '(En', 'qu\'elle', 'coll', 'd\'en', 'enfin', 'voir', 'with', 'ISSN', 'Édition', 'Éditions', 'font', 's\'est', 'dès', 'ligne]', 'plutôt', 'd\'abord', 'd\'ailleurs', 'tel', 'celles', 'quant', 'URL', 'DOI', 'celui','tous', 'lors', 'celle', 'qu\'ils', 's\'agit','contraires', 'lequel', 'comme', "aussi", "ainsi", "tout", "The", 'cet', 'tant', 'Une', "mise", "bien", "notamment", "également", "sans", "c\'est", "très", "travers", 'n\'est', 'd\'autres', 'encore', 'permet', "fois", "peu", "mis", "qu\'il", 'entre','d\'une', 'd\'un', 'Les', 'dont', 'l\'on', 'vient', 'l\'un', 'Pas', 'celuici', 'années', 'année', 'd\'être', 'faire', "lequels", 'Lequel','qualificatif', 'apposition', 'au', 'adj', 'Cet', 'Cette', 'C\'est', 'Autant', 'Aussi', 'Autour', 'Ainsi','siècle', 'xxie', 'xixe', 'xxe', 'extension', 'ajectivement', 'plus', "application", "titre", "emporté", "commencé", "affaiblissement", "étendre", "appartenir", "appartient", "résulte", "procéder", "soumet", "métonymie", "assurer", "assure", "introduire", "manière", "afficher", "simple", "subsiste", "fait", "non", "oui", "subsister", "subsistent", "parfaite", "découlent", "découle", "découler", "parfait", "venir", "peut", "ce", "cette", "grande", "grand", 'certains', 'certain', 'certaine', 'certaines', 'connu', 'connue', 'connaître', 'conforme', 'dire', 'tcha', 'doit','être', 'xixe', 'désigner', 'désigne', 'désignant', 'façon', 'adj', 'loc', 'adv', 'deux', 'trois', 'quatre', 'siècle', 'extension', 'adjectivement', 'par', 'analogie', 'plus', 'selon', 'xvi', 'xviiie', 'xvie', 'xve', 'gran', 'xive', 'xviie', 'xive', 'xviii', 'xvii', 'xv', 'xiv', 'xiii', 'xii', 'aux', 'avec', 'ce', 'où', "lequel", 'lesquels', "duquel", 'ces', 'dans', 'de', 'des', 'du', 'elle', 'en', 'et', 'eux', 'il', 'ils', 'je', 'la', 'le', 'les', 'leur', 'lui', 'ma', 'mais', 'me', 'même', 'mes', 'moi', 'mon', 'ne', 'nos', 'notre', 'nous', 'on', 'par', 'pas', 'pour', 'qu', 'que', 'qui', 'sa', 'se', 'ses', 'son', 'sur', 'ta', 'te', 'tes', 'toi', 'ton', 'tu', 'un', 'une', 'vos', 'votre', 'vous', 'leurs']


nlp = stanza.Pipeline(lang='fr', processors="tokenize,pos,lemma")

dico_nbw = {}


list_term = open("liste_termes.txt", "w", encoding = "utf-8")

def toto_mots(dossier_fichiers) : 
    
    liste_mots_uniques = []

    for f in os.listdir(dossier_fichiers) : 
    
        m = open(dossier_fichiers+'/'+f, "r", encoding="utf-8")
        fichier=m.read()
        m.close()

        doc = nlp(fichier)
        for sent in doc.sentences:
            
            for word in sent.words:
                pos = word.upos
                
                if len(word.text) > 2 and len(word.text) < 30 and word.text not in liste_mots_uniques and word.text not in stop_words and "." not in word.text :
                    if pos == "NOUN" or pos == "ADJ" or pos == "PROPN" or pos == "X" :
                        liste_mots_uniques.append(word.text)
                else : 
                    pass 

                    

        # fichier = re.sub("’", "\'", fichier)
        # bagofwords = re.split(r" |\n", fichier)
        # for word in bagofwords : 
        #     res = re.sub(r",|\.|[0-9]+|!|\"|\(|\)|\(.?\)|\s|;|:|http.+|\-|\?", "", word)
        #     if len(res) > 2 and res not in stop_words : 
        #         clean_bagofwords.append(res)
        # big_list.extend(clean_bagofwords)
        # liste_mots_uniques = list(set(big_list))

        
        
        
        return liste_mots_uniques






def frequence_fichier(dossier_fichiers, liste_mots_uniques) : 
    
    pattern_json  = {}
    dico_fichier_freq = {}
    dico_new = {}
    dico_mot_annee = {}
    mega_list = []
    q_dic = {}
    n_dic = {}
    s_dic = {}
    liste_freq = []
    fichier_list = []
    max_list = []
    for f in sorted(os.listdir(dossier_fichiers)) : 
    
        dico_mots_par_fichier = dict.fromkeys(liste_mots_uniques, 0)
        m = open(dossier_fichiers+'/'+f, "r", encoding="utf-8")
        fichier=m.read()
        fichier = re.sub("’", "\'", fichier)
        bagofwords = re.split(r" |\n", fichier)
        for word in bagofwords : 

            if word in dico_mots_par_fichier.keys() :    
                dico_mots_par_fichier[word]+=1
        
        for k, v in dico_mots_par_fichier.items():
            affi = k + '\t' + str(v)+'\t'+f+'\n'
            l = open("freq_fichier.txt", "a+")
            l.write(affi)

    return dico_mots_par_fichier

                
        #sorted(dico_mots_par_fichier.items(), key=lambda t: t[0], reverse=True)
        #sorted([(value,key) for (key,value) in dico_mots_par_fichier.items()])

        #dico_trie = sorted(dico_mots_par_fichier.items(), reverse=True, key=operator.itemgetter(1))


        
def frequence_graphe(dossier_fichiers, dico_mots_par_fichier) : 

    n_dic={}
    s_dic = {}
    mega_list = []

    for f in sorted(os.listdir(dossier_fichiers)) : 

        

        for mot, freq in dico_mots_par_fichier.items():
            
            #print(mot, freq)
            n_dic[f] = freq
            s_dic[mot] = n_dic
            

            if s_dic not in mega_list :
                    
                mega_list.append(s_dic)

                
                         
            else : 
                pass


        #print (mega_list)
    
    


    str_json = json.dumps(mega_list, indent=4)

    
        
    jfile = open("mega2.json", "w")

    json.dump(str_json, jfile, indent=6)

        
        #jjforprint = json.dump(dico_fichier_freq, open('freq_df.json', "w"), indent=4, sort_keys=True)

    #df.to_csv("freq_mots_chaque_document.csv", "w+")  
    #with open("freq_mots_chaque_document.csv", mode = "w+") as writer :
    #    df.to_csv(writer) 
        
    return str_json



def graphe_json(str_json) : 
    data = json.loads(str_json)
    for i in data : 
        
        for mot, reste in i.items() : 
            
            years = reste.keys()
            freq = reste.values()
            df = pd.DataFrame({"Année" : years, "Fréquence" : freq})
            df.plot(kind="bar", x = "Année", y="Fréquence", color = "blue")

            df.to_csv ('./freq/freq_%s_par_annee.csv'%mot, index = False, header=True)
            
            plt.savefig("./visu/%s.png"%mot)


    







# def graphe_freq(dossier_fichiers, dico_fichier_freq) : 

#     freqs = []
#     years = []
    
#     for mot, year_freq in dico_fichier_freq.items() : 
         
#             try:
#                 for year, freq in year_freq.items() :
#                     if int(freq) > 0 :
#                         years.append(year.split("_")[:1])
#                         names.append(freq)
        




freq_f = frequence_fichier("./textes_txt", toto_mots("./textes_txt"))
freq_g = frequence_graphe("./textes_txt", freq_f)

#graphe_json(freq_g) 


list_term.close()
#structure : machin : {2010_2 : 6}
#dico_fichier_freq[mot]=dict({f : freq})

# first we'll do it the default way, with gaps on weekends
# fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4))

# for mot, year_freq in freq_f.items() : 
#     for year, freq in year_freq.items():
#         if int(freq) > 0 : ""
#             ax1.plot(year, freq, 'o-')
#             ax1.set_title("%s"%mot)

#             fig.autofmt_xdate()
#             plt.savefig('%s'%mot+"_"+'%s'%year.split("_")[:2]+'.png')



# years = list(freq_f.keys())


# for v in freq_f.values() : 
#     for 

#     list_f.append(v[1]) 
#     plt.plot(years, list_f, label="%s"%v[0])
#     plt.ylim(1,100)
#     plt.ylabel ('freq')
#     plt.xlabel ('year')
#     plt.savefig('%s'%v[0]+'.png')

    





