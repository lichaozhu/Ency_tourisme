import re
import os
import json
import numpy
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



stop_words = stopwords.words('french')
stop_words += ['ce', 'souvent', 'depuis', 'Nous', 'cela', 'après', '(En', 'qu\'elle', 'coll', 'd\'en', 'enfin', 'voir', 'with', 'ISSN', 'Édition', 'Éditions', 'font', 's\'est', 'dès', 'ligne]', 'plutôt', 'd\'abord', 'd\'ailleurs', 'tel', 'celles', 'quant', 'URL', 'DOI', 'celui','tous', 'lors', 'celle', 'qu\'ils', 's\'agit','contraires', 'lequel', 'comme', "aussi", "ainsi", "tout", "The", 'cet', 'tant', 'Une', "mise", "bien", "notamment", "également", "sans", "c\'est", "très", "travers", 'n\'est', 'd\'autres', 'encore', 'permet', "fois", "peu", "mis", "qu\'il", 'entre','d\'une', 'd\'un', 'Les', 'dont', 'l\'on', 'vient', 'l\'un', 'Pas', 'celuici', 'années', 'année', 'd\'être', 'faire', "lequels", 'Lequel','qualificatif', 'apposition', 'au', 'adj', 'Cet', 'Cette', 'C\'est', 'Autant', 'Aussi', 'Autour', 'Ainsi','siècle', 'xxie', 'xixe', 'xxe', 'extension', 'ajectivement', 'plus', "application", "titre", "emporté", "commencé", "affaiblissement", "étendre", "appartenir", "appartient", "résulte", "procéder", "soumet", "métonymie", "assurer", "assure", "introduire", "manière", "afficher", "simple", "subsiste", "fait", "non", "oui", "subsister", "subsistent", "parfaite", "découlent", "découle", "découler", "parfait", "venir", "peut", "ce", "cette", "grande", "grand", 'certains', 'certain', 'certaine', 'certaines', 'connu', 'connue', 'connaître', 'conforme', 'dire', 'tcha', 'doit','être', 'xixe', 'désigner', 'désigne', 'désignant', 'façon', 'adj', 'loc', 'adv', 'deux', 'trois', 'quatre', 'siècle', 'extension', 'adjectivement', 'par', 'analogie', 'plus', 'selon', 'xvi', 'xviiie', 'xvie', 'xve', 'gran', 'xive', 'xviie', 'xive', 'xviii', 'xvii', 'xv', 'xiv', 'xiii', 'xii', 'aux', 'avec', 'ce', 'où', "lequel", 'lesquels', "duquel", 'ces', 'dans', 'de', 'des', 'du', 'elle', 'en', 'et', 'eux', 'il', 'ils', 'je', 'la', 'le', 'les', 'leur', 'lui', 'ma', 'mais', 'me', 'même', 'mes', 'moi', 'mon', 'ne', 'nos', 'notre', 'nous', 'on', 'par', 'pas', 'pour', 'qu', 'que', 'qui', 'sa', 'se', 'ses', 'son', 'sur', 'ta', 'te', 'tes', 'toi', 'ton', 'tu', 'un', 'une', 'vos', 'votre', 'vous', 'leurs']


nlp = stanza.Pipeline(lang='fr', processors="tokenize,pos,lemma")

dico_nbw = {}

###


###
def fichiers_assembles(nom_dossier):
    noms = sorted(os.listdir(nom_dossier))
    t = date.today().strftime("%m_%d_%Y")
    now = datetime.now()
    dt = now.strftime("%H:%M")
    tm = time.time() * 1000 
    log_name = str(t)+"_traitement"
    wb = xlwt.Workbook()
    ws = wb.add_sheet(log_name)
    ws.write(0, 0, "Nom de fichier")
    ws.write(0, 1, "Heure de l'extraction")
    for nom in noms :
        ws.write(noms.index(nom)+1,0,nom)
        ws.write(noms.index(nom)+1,1,dt+":"+str(tm))
    
    wb.save("./fichiers_controle/"+log_name+'.xls')

    data_textes = {"Textes traités" : noms}


    #ajouter la vérification de doublons pour les nouveaux fichiers ajoutés 



    #sortie en json des noms des fichiers
    with open("./fichiers_controle/textes_traites.json", "w+", encoding="utf-8") as file : 
        json.dump(data_textes, file)
    return noms



#print(fichiers_assembles('./textes_txt'))



def toto_mots(dossier_fichiers) : 
    clean_bagofwords = []
    big_list = []
    for f in os.listdir(dossier_fichiers) : 
    
        m = open(dossier_fichiers+'/'+f, "r", encoding="utf-8")
        fichier=m.read()
        fichier = re.sub("’", "\'", fichier)
        bagofwords = re.split(r" |\n", fichier)
        for word in bagofwords : 
            res = re.sub(r",|\.|[0-9]+|!|\"|\(|\)|\(.?\)|\s|;|:|http.+", "", word)
            if len(res) > 2 and res not in stop_words : 
                clean_bagofwords.append(res)
        big_list.extend(clean_bagofwords)
        liste_mots_uniques = list(set(big_list))


        
        return liste_mots_uniques


def frequence_fichier(dossier_fichiers, liste_mots_uniques) : 
    
    pattern_json  = {}
    dico_fichier_freq = {}
    liste_freq = []
    for f in sorted(os.listdir(dossier_fichiers)) : 
        dico_mots_par_fichier = dict.fromkeys(liste_mots_uniques, 0)
        m = open(dossier_fichiers+'/'+f, "r", encoding="utf-8")
        fichier=m.read()
        fichier = re.sub("’", "\'", fichier)
        
        bagofwords = re.split(r" |\n", fichier)
        for word in bagofwords : 
            res = re.sub(r",|\.|[0-9]+|!|\"|\(|\)|\(.?\)|\s|\-| |;|:|http.+", "", word)
            if res in dico_mots_par_fichier.keys() and res not in stop_words and len(res)>2 :    
                dico_mots_par_fichier[res]+=1 
        #sorted(dico_mots_par_fichier.items(), key=lambda t: t[0], reverse=True)
        #sorted([(value,key) for (key,value) in dico_mots_par_fichier.items()])

        dico_trie = sorted(dico_mots_par_fichier.items(), reverse=True, key=operator.itemgetter(1))

        for item in dico_mots_par_fichier.items():
            liste_freq.append(item)
        
        #dico_fichier_freq[f]=liste_freq
        dico_fichier_freq[f]=liste_freq
        
        
        print (dico_fichier_freq)
        
        jjforprint = json.dump(dico_fichier_freq, open('freq_df.json', "w"), indent=4, sort_keys=True)

        
    #df = pd.DataFrame(pattern_json.values(),index = pattern_json.keys())
    #df.to_csv("freq_mots_chaque_document.csv", "w+")  
    #with open("freq_mots_chaque_document.csv", mode = "w+") as writer :
    	#df.to_csv(writer) 
        
        
    return liste_freq


def frequence_dossier(dossier_fichiers, liste_mots_uniques) : 
    dico_mots_par_fichier = dict.fromkeys(liste_mots_uniques, 0)
    pattern_json  = {}
    for f in sorted(os.listdir(dossier_fichiers)) : 
        
        m = open(dossier_fichiers+'/'+f, "r", encoding="utf-8")
        fichier=m.read()
        fichier = re.sub("’", "\'", fichier)
        bagofwords = re.split(r" |\n", fichier)
        for word in bagofwords : 
            res = re.sub(r",|\.|[0-9]+|!|\"|\(|\)|\(.?\)|\s|\-| |;|:|", "", word)
            if res in dico_mots_par_fichier.keys() and res not in stop_words and len(res)>2 :    
                dico_mots_par_fichier[res]+=1 

    df = pd.DataFrame(dico_mots_par_fichier.values(), index = dico_mots_par_fichier.keys(),columns = ['Fréquence dans tous les documents'])        
    df1 = df.sort_values(by=['Fréquence dans tous les documents'], ascending=False)
   
    with open("freq_mots_tous_les_documents.csv", mode = "w+") as writer :
    	df1.to_csv(writer)  
    return






def extract_thematique(dossier_fichiers) : 
    fichier_theme  = {}
    mots_grand = []
    for f in sorted(os.listdir(dossier_fichiers)) : 
        #dico_mots_par_fichier = dict.fromkeys(liste_mots_uniques, 0)
        m = open(dossier_fichiers+'/'+f, "r", encoding="utf-8")
        lines = m.readlines()[:20]
        theme = lines[5:8]
        mots = " ".join(theme)
        
        mots_clefs = []
        #print (mots)
        doc = nlp(mots)

        for sent in doc.sentences:
            
            for word in sent.words:
                pos = word.pos
                
                if len(word.text) > 5 and word.text not in mots_clefs :
                    if "NOUN" == pos or "ADJ" == pos  : 

                        try : 
                            
                            mots_clefs.append(word.text.lower())
                            
                        except : 
                            pass

                fichier_theme[f] = mots_clefs
                mots_grand.extend(mots_clefs)
                

    print (set(mots_grand))



#extract_thematique("./textes_txt")            


        #print(dico_mots_par_fichier)
        #df = pd.DataFrame(data = dico_mots_par_fichier, index = list(sorted(os.listdir(dossier_fichiers))))
        #with pd.ExcelWriter('tf_fichier.xlsx') as writer:
        #    df.to_excel(writer)
        
        #return dico_mots_par_fichier
        #return pattern_json
def contexte(dossier_fichiers, liste_mots, fenetre):
    #recherche d'occurrences
    pattern_json  = {}
    for f in sorted(os.listdir(dossier_fichiers)) :
        m = open(dossier_fichiers+'/'+f, "r", encoding="utf-8")
        extrait_texte =m.read()


        for mot in liste_mots : 
        
            occs = re.finditer(mot, extrait_texte, re.MULTILINE)
            if occs : 
    #récupération des positions de début et de fin des occurrences
                positions = [occ.span() for occ in occs]
    #mise en place de la fenêtre du concordancier
                centre = pd.DataFrame([extrait_texte[i:j] for (i,j) in positions])
                cotexte_g = pd.DataFrame([extrait_texte[i-fenetre : i-1] for (i,j) in positions])
                cotexte_d = pd.DataFrame([extrait_texte[j+1 : j+fenetre] for (i,j) in positions])
        
                concord = pd.concat([cotexte_g, centre, cotexte_d], axis=1)
                with open("./concord_fichier/%s_sociales.csv"%f, mode = "a") as writer :
                     concord.to_csv(writer)
                     
                
            else : 
                pass

            
def ex_ref(dossier_fichiers):
    for f in sorted(os.listdir(dossier_fichiers)) : 
        #dico_mots_par_fichier = dict.fromkeys(liste_mots_uniques, 0)
        m = open(dossier_fichiers+'/'+f, "r", encoding="utf-8")
        lines = m.readlines()[:80]
        for line in lines : 
            if re.search(r'Référence électronique',line):
                ll = lines[lines.index(line)+1].rstrip()
                

                return ll


def ex_page(dossier_fichiers):
    for f in sorted(os.listdir(dossier_fichiers)) : 
        #dico_mots_par_fichier = dict.fromkeys(liste_mots_uniques, 0)
        m = open(dossier_fichiers+'/'+f, "r", encoding="utf-8")
        lines = m.readlines()[:80]
        for line in lines : 
            b = re.search(r'Pagination',line)
            if b : 
                page = re.split(r'\:', line)[1].rstrip()
                print(page)
                return page


def auteur(dossier_fichiers):
    dic_auteur = {}
    for f in sorted(os.listdir(dossier_fichiers)) : 
        #dico_mots_par_fichier = dict.fromkeys(liste_mots_uniques, 0)
        m = open(dossier_fichiers+'/'+f, "r", encoding="utf-8")
        lines = m.readlines()[:10]
        for line in lines : 
            b = re.findall(r'[A-ZÉÈÀÇÎÙÂ][a-z]{2,} ?[A-ZÉÈÀÇÎÙÂ][a-z]{2,}',line)
            c = re.search(r'Tourisme|touristique', line, re.IGNORECASE)
            if len(b) > 1 and not c: 

                aut = ", ".join(b)
                dic_auteur[f] = aut
    return dic_auteur

def ref(dossier_fichiers):
    dic_ref = {}
    liste_vide = []
    for f in sorted(os.listdir(dossier_fichiers)) : 
        #dico_mots_par_fichier = dict.fromkeys(liste_mots_uniques, 0)
        m = open(dossier_fichiers+'/'+f, "r", encoding="utf-8")
        lines = m.readlines()[:35]
        for line in lines : 
            b = re.search(r'référence',line, re.IGNORECASE)
            ind = lines.index(line)
            newlines = "".join(lines[ind+1:])
            
            
            c = re.search(r'(.+?)\n\n', newlines)
            if c : 
                cc = c.group(1)
                if cc not in liste_vide : 
                    liste_vide.append(cc)
                    print(cc)
                    dic_ref[f] = "".join(liste_vide)
                else : 
                    pass
                       
    
    return dic_ref




# data = {"Titre de revue" : lines[0].rstrip(), 
#         "numéro" : re.split(r"\|", re.sub(" ", "", lines[1]))[0],
#         "année de publication" : re.split(r"\|", re.sub(" ", "", lines[1].rstrip()))[1],
#         "thématique" : lines[3].rstrip(),
#         "auteur" : auteur(fichier),
#         "Référence" : ex_ref(fichier)+", pp. "+ex_page(fichier) + "."
             


#         }

frequence_fichier("./textes_txt", toto_mots("./textes_txt"))









# output : concordancier 

#liste_test = ["déréalisation", "temporalité", "recensement", "revisite", "chambre", "civilisation", "postmoderne", "langage", "extérieur", "authentique", "élaboration", "hôtel", "spectacle", "motivations", "voyageur", "décor", "sécurité", "chemin", "contemporain", "identitaire", "dispositifs", "support", "gamme", "modernité", "transformations", "perception", "caustique", "subvertie", "condition", "apports"]




#liste_test = ["sociale", "sociales"]
#contexte("./textes_txt", liste_test, 100)



#print(extract_thematique("./textes_txt"))

#frequence_fichier("./textes_txt", toto_mots("./textes_txt"))
#frequence_dossier("./textes_txt", toto_mots("./textes_txt"))

















