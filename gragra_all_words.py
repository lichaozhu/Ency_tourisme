import re
import pandas as pd
import json
def ouvre_fichier(chemin) : 
    
    file = open(chemin, "r", encoding='utf-8')
    contenu = file.readlines()
    file.close()
    return contenu 

def fichier_liste(contenu) : 
	liste3 = []
	biglist = []
	i = 0	
	while i < len(contenu) :
		cc = contenu[i]
		cc = cc.rstrip()
		cc_split = cc.split("\t")
		#cc_split += cc_split
		
		biglist.append(cc_split)
		i+=1
		

	

	return biglist






# for i in h : 
# 	print (i)


def liste_json(biglist) :
	liste_verif = []
	une_liste = []
	n = 0
	
	while n < len(biglist) - 1 : 
		sous_liste = biglist[n]
		mot = sous_liste[0]
		freq = int(sous_liste[1])
		annee = sous_liste[2]
		model = {mot : {annee : freq}}
		#if int(freq) > 0 : 
		if mot not in liste_verif : 

			une_liste.append(model)
			liste_verif.append(mot)
			
			with open('./all_words/%s.json'%mot, 'w+') as fp:
				json.dump(model, fp, indent=4)
			#with open('./doc_json/liste2_dics.json', 'w+') as fp:
			#	json.dump(une_liste, fp, indent=4)
			
			

		else : 
			m= 0
			while m < len(une_liste) - 1 : 
				momo = une_liste[m]
				if mot in momo.keys() : 
					dics = momo[mot]
					dics[annee] = freq
					

					
					with open('./all_words/%s.json'%mot, 'w+') as fp:
						json.dump(dics, fp, indent=4)
				m+=1
				

				
		n+=1
		
		

	return 





b = ouvre_fichier("freq_fichier.txt")
h = fichier_liste(b)
l = liste_json(h)




			#with open('./doc_json/%s.json'%mot, 'w+') as fp:
			#	son.dump(list2, fp, indent=4)
        
      




    


# df = pd.DataFrame({"Année" : year, "Fréquence" : freq})
# df.plot(kind="bar", x = "Année", y="Fréquence", color = "blue")

# df.to_csv ('./freq/freq_%s_par_annee.csv'%mot, index = False, header=True)

# plt.savefig("./visu/%s.png"%mot)