
#NOMS DELS CAMPS DE L'EXCEL:
# ACOMPANYANT   USUARI	 DATA	 DESCRIPCIO	  SERVEI




import pandas as pd
import os
import time
from time import gmtime, strftime
import plantillaLatex
import subprocess
import tkinter as tk


df = pd.read_excel("../Formulari actes (treball als barris) (Responses) bo.xlsx")


#FUNCIO AUXILIAR PER OBTENIR ELS VALORS D'UNA COLUMNA PERO SENSE LES REPETICIONS DELS MATEIXOS
def obtenir_llista_ocurrencia_unica(series_pandas):
	ll = []
	for i in range(len(series_pandas)):
		if not series_pandas.iloc[i] in ll: #L'ERROR ESTÀ AQUI, NO PERMET ACCEDIR AMB INDEX ALS ELEMENTS DE SERIES_PANDAS SI POSO data_final = "10/05/2021". En canvi, si poso "31/05/2021" aleshores sí.
			ll += [series_pandas.iloc[i]]
	return ll

def crea_directori(nom_directori):
	try:
		os.mkdir(nom_directori)
	except FileExistsError:
		return True

def borra_columnes(dframe, ll_cols_a_esborrar):
	for col in ll_cols_a_esborrar:
		try:
			del dframe[col] #NOMES CAL FER-HO SI ENCARA HI HA LA COLUMNA BORRA
		except KeyError:
			print("Columna "+col+" no hi és. No s'ha esborrat.")


def arregla_nom(nomComplet):
	"""PRE: ANDRES ANDREO ORTEGA. POST: Andres Andreo Ortega"""
	ll_nomComplet = nomComplet.strip().split()
	for i in range(len(ll_nomComplet)):
		ll_nomComplet[i] = ll_nomComplet[i][0].upper() + ll_nomComplet[i][1:].lower()
	return " ".join(ll_nomComplet)


def posa_data_en_text(str_data):
	"""PRE: 02/10/2021, POST: Balaguer, 10 d'Octubre de 2021."""
	data = str_data.split("/")
	dd, mm, aaaa = data[0], data[1], data[2]
	dic_mesos = {1:"de gener",
				 2:"de febrer", 
				 3:"de març", 
				 4:"d'abril", 
				 5:"de maig", 
				 6:"de juny",
				 7:"de juliol",
				 8:"d'agost",
				 9:"de setembre",
				 10:"d'octubre",
				 11:"de novembre",
				 12:"de desembre"
				}
	return "Balaguer, "+str(int(dd))+" "+dic_mesos[int(mm)]+" de "+aaaa+"."


def crea_LaTeX(df_usuari, str_usuari, di, df): 
	"""Amb aquesta funcio creo un document LaTeX per l'usuari del df_usuari, que compilarem després per obtenir el PDF"""
	nom_arxiu_LaTeX = "_"+str_usuari+".tex"
	with open(nom_arxiu_LaTeX, "w", encoding='utf-8') as f:
		
		data = strftime("%d/%m/%Y %H:%M:%S", gmtime()).split()[0] #adaptat de stackoverflow https://stackoverflow.com/questions/415511/how-to-get-the-current-time-in-python
		
		#ESCRIVIM L'INICI DEL FITXER LATEX
		inici = plantillaLatex.inici.format(str_usuari, di, df, arregla_nom(str_usuari), di, df, posa_data_en_text(data))
		f.write(inici)
		
		#ESCRIVIM EL COS O BODY DE LA TAULA LATEX AMB ELS USUARIS DINS
		for data, acompanyant, descripcio in zip(df_usuari["DATA"], df_usuari["ACOMPANYANT"], df_usuari["DESCRIPCIO"]):
			taula_long_variable = plantillaLatex.taula_long_variable.format(data,acompanyant,descripcio)
			f.write(taula_long_variable)
		
		#TANQUEM AMB EL FINAL ESTÀNDARDS DEL FITXER LATEX
		final = plantillaLatex.final
		f.write(final)
		
		print("fitxer creat")
		







def main(data_inicial, data_final, boolea_crea_LaTeX, Borra_LateX_i_crea_PDF):
	#DATES ENTRE LES QUALS VOLEM OBTENIR INFORMES (dd/mm/aaaa). Pots posar zero davant IMPORTANTISSIM. Directori on es guarda.


	directori_informes = "informesPerUsuari"

	global df #--> declaro el dataframe variable global o no la puc fer servir dins la funció main
	#CONVERTIM LA COLUMNA DE STRINGS DE DATA (SERIES) A UNA COLUMNA DE TIPUS DATETIME (TAMBÉ SERIES) PER PODER FER OPERACIONS D'ORDENACIÓ AMB LES DATES. Després ordenem per data.
	df["DATA"] = pd.to_datetime(df["DATA"], format="%d/%m/%Y") #FORMAT dd/mm/aaaa (fins i tot cal el zero per l'esquerra si es una dia o mes de 1 a 9, ojo!)
	
	#time.sleep(10)
	df = df.sort_values(by="DATA")
	borra_columnes(df, ["BORRAR","dia","mes","any"]) #borro columnes superflues (si no hi són no fa res i dona avis, però no donarà error).
	
	#REVENTEM EL DATAFRAME ANTERIOR SUBSTITUINT-LO PEL QUE TÉ LES DATES FILTRADES ENTRE data_inicial i data_final (SINXATXI df[filtre1][filtre2]
	df = df[df["DATA"] >= pd.to_datetime(data_inicial, format="%d/%m/%Y")] #filtro des de la data inicial
	df = df[df["DATA"] <= pd.to_datetime(data_final, format="%d/%m/%Y")] #filtro fins a la data final
	
	#OBTINC LA LLISTA ÚNICA D'USUARIS EN AEL PERIODE DEMANAT I LA LLISTA ÚNICA D'ACOMPANYANTS (LLISTA ÚNOICA VOL DIR QUE NO HI HA REPETITS!)
	ll_acompanyants = obtenir_llista_ocurrencia_unica(df["ACOMPANYANT"])
	ll_usuaris = obtenir_llista_ocurrencia_unica(df["USUARI"])
	

	#CREO UN DIRECTORI ON GUARDAR LES COSES
	directori_ja_estava_creat = crea_directori(directori_informes)
	consentiment_esborra = False
	if directori_ja_estava_creat:
		os.system("cls")
		resposta = input("Directori ja creat amb dades dins!! Si dius que sí,\nsobreescriuràs dades amb la nova consulta. Vols fer-ho? [sí, no]:").lower().strip()
		consentiment_esborra = True
		if resposta == "s" or resposta == "si" or resposta == "sí":
			os.chdir("./"+directori_informes) 
			ll_fitxers_usaris = os.listdir()
			for fitxer in ll_fitxers_usaris:
				os.remove(fitxer)		
			os.chdir("../")
		else:
			os.system('cls')
			print("###################")
			print("# fi del programa!#")
			print("###################")
			time.sleep(2)
			return

	#canvio al directori on guardo els informes i genero un excel per cada usuari. Més un readme per informar
	with open("readme.txt","w") as f:
		f.write("""__Les Dates de tots els informes d'aquest directori aniran entre el """+data_inicial+""" i el """+data_final+""" com a mínim 
i com a màxim, respectivament. Tindràs tants arixus de tipus .tex, .xlsx i .pdf (segons configuris als paràmetres del main) com usuaris
hi hagi durant el període escollit """+directori_informes+""". Ccada firxer generat tindrà el nom d'un usuari del servei amb els seus
informes corresponents. Es generaran documents LaTeX""")
	
	os.chdir("./"+directori_informes) 

	if len(ll_usuaris) == 0:
		os.system("cls")
		print("NO HI HA USUARIS EN L'INTERVAL ESPECIFICAT! FES UN INTERVAL MÉS AMPLI!!")
		time.sleep(2)
		return
	ll_usuaris.sort()

	for usuari in ll_usuaris:
		df_usuari = df[df["USUARI"] == usuari]
		df_usuari["DATA"] = df_usuari["DATA"].apply(lambda x: x.strftime('%d/%m/%Y')) #AQUESTA LAMBDA EXPRESSION VE DE STACKOVERFLOW <3
		df_usuari = df_usuari[["DATA","ACOMPANYANT","DESCRIPCIO"]] #selecciono nomes aquest camps

		"""
		df_usuari.to_excel(usuari+".xlsx", sheet_name="de "+data_inicial.replace("/",".")+" a "+data_final.replace("/","."))
		"""
		#gracies a stackoverflow i l'usuari Ashu007 he pogut ajustar l'amplada de les files :)
		#https://stackoverflow.com/questions/17326973/is-there-a-way-to-auto-adjust-excel-column-widths-with-pandas-excelwriter/17811984
		nom_de_la_fulla_excel = "de "+data_inicial.replace("/",".")+" a "+data_final.replace("/",".")
		writer = pd.ExcelWriter(usuari+".xlsx", engine='xlsxwriter')
		df_usuari.to_excel(writer, sheet_name=nom_de_la_fulla_excel)
		workbook = writer.book
		worksheet = writer.sheets[nom_de_la_fulla_excel]
		

		#AMPLE DE COLUMNES
		worksheet.set_column("A:A",0) #0 PERQUÈ NO VULL QUE ES MOSTRI, PERÒ TAMPOC LA PUC ELIMINAR
		worksheet.set_column('B:C', 25)
		worksheet.set_column('D:D', 150)
		writer.save()

		#CREO DOCUMENT LATEX
		if boolea_crea_LaTeX:
			crea_LaTeX(df_usuari, usuari, data_inicial, data_final)

	#creo els pdf cridant a pdflatex	
	if Borra_LateX_i_crea_PDF:
		for usuari in ll_usuaris:
			subprocess.run(["pdflatex", "_"+usuari+".tex"]) 


		#ESBORRO TOTS ELS FITXER SUPERLFUS QUE GENERA LA COMPILACIÓ DE LATEX 
		#(DEIXANT NOMÉS ELS .txt, els .pdf i els .xlxs que haviem generat inicialment)
		ll_tipus_fitxer_a_eliminar = [".aux",".spl",".txt",".out",".log"]
		for string_fitxer in os.listdir():
			for extensio in ll_tipus_fitxer_a_eliminar:
				if extensio in string_fitxer:
					os.remove(string_fitxer)
					break

			

		


	
	#FILTREM EL DF PER DATES D'INICI I DE FINAL (PER ACOTAR. AMBDUES DATES ESTAN INCLOSES)
	print("###############################################################")
	print("\nEntre data " + data_inicial + " i data " + data_final + " tenim:\n")

	print("\nCOMPROVAR QUE TOT ESTÀ BÉ: NO HI HA D'HAVER NOMS REPETITS")
	print("\nSi n'hi haguessin caldria MIRAR L'EXCEL MARE i arreglar-ho!")
	print(df["ACOMPANYANT"].value_counts())
	print(df["USUARI"].value_counts())
	print("###############################################################")



""" PRIMERA COMUNICACIO DEL 19/04/2021 AL 30/05/2021 (INCLOU AMBDUES DATES) """
""" SEGONA COMUNICACIO DEL 31/05/2021 AL 29/06/2021"""
""" TERCERA COMUNCACIO FER-LA DEL 30/06/2021 al 31/07/2021 (AMBDUES DATES INCLOSES)"""
""" QUARTA COMUNCACIO FER-LA DEL 01/08/2021 al 31/08/2021 (AMBDUES DATES INCLOSES)"""
if __name__ == "__main__":	
	
	
	main(	data_inicial = "01/05/2021",
			data_final = "31/05/2021", #EN EL PROCESSAT DE LA PRIMERA CRIDA A LA FUNCIO obtenir_llista_ocurrencia_unica dóna error si poso, per exemple, data_final = "10/05/2021". En canvi, si poso data_final = "31/05/2021" no en dona.
			boolea_crea_LaTeX = True, #CREA ELS ARXIUS .TEX
			Borra_LateX_i_crea_PDF = True) #CREA ELS PDF DES DELS ARXIUS TEX