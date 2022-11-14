inici = """% !TeX spellcheck = en_US
 \\documentclass[a4paper,12pt]{{elsarticle}}  %elsarticleclas, classe per a les 
 %submissions als journals de l'editorial elsevier.
 \\usepackage[utf8]{{inputenc}} %Per si poso algun accent, en cas contrari ascii dona unicode


 \\usepackage{{subcaption}} % per a fer subfigures

 \\usepackage{{wrapfig}} % permet que les figures siguin envoltades per text
 \\usepackage{{hyperref}}%per a citar les URL que surtin amb link
 \\usepackage{{color}} %per a que surtin colors a la taula de l'anex
 \\usepackage[numbers]{{natbib}}% per tal de que les refereencies es generin amb nombres ([numbers]) i pq la bibliografia es generi amb estil Vancouver, carreguem natbib: 
 \\usepackage{{amsmath}} %necessari per tal Dobtenir formules sense errors i matrius
 \\usepackage{{eurosym}} %perquE surtin els euros com a tal.. puto unicode
 \\usepackage{{parskip}} %perquè surtin salts de linia sense posar \\par o \\\\ al final

 
 
 
 \\setlength{{\\parindent}}{{15pt}}
 %\\setlength{{\\parskip}}{{1em}} %per si vols canviar els salts definits per el paquet parksip entre paragrafs
 %\\renewcommand{{\\baselinestretch}}{{2.0}} % per si vulgués canviar l'interlineat
 
 %aconseguim que les parts (\\part{{nom part}}) es numerin amb nombres
 %i inicialitzin els contadors cada vegada que estem en una nova part
 \\usepackage{{chngcntr}} 
 \\counterwithin{{section}}{{part}}
 
 \\renewcommand{{\\thepart}}{{\\arabic{{part}}}}
% \\renewcommand{{\\figurename}}{{Figura}}
 
 \\usepackage{{graphicx}}%fem que es puguin mostrar els gràfics
 \\usepackage{{placeins}} %perque les figures flotants no se'n vagin al final. Et permet implementar la comanda \\FloatBarrier per evitar que les figures avancin d'un determinat punt.
 %http://osl.ugr.es/CTAN/macros/latex/contrib/placeins/placeins-doc.pdf
 
 %aconseguim que la table of contents (index)tingui solucionats els problemes de spacing
 \\usepackage{{tocloft}}% http://ctan.org/pkg/tocloft
 \\usepackage{{fancyref}} %PAQUET BRUTRAL PER CITAR A LES FIGURES 



\\usepackage{{longtable}} %per fer que una taula es talli i aparegui en multiples pagines en comptes de fer un overflow.








  \\usepackage{{blindtext}}


\\begin{{document}} 	


\\begin{{titlepage}}
	\\centering

	{{\\scshape\\LARGE Paeria de Balaguer \\par}}


			\\vfill


	{{\\scshape\\Large Treball als barris\\par}}

	
			\\vspace{{0.5cm}}

	
	{{\\Large Programa De La Mà: Acompanyament a la Gent Gran.\\par}}

			

			\\vfill



	{{\\Large\\bfseries {} \\par}}
	


			\\vfill



	{{\\large Interval de filtratge:\\par}}
	{{\\large del {} al {}.\\par}}
		

\\end{{titlepage}}



\\clearpage







\\FloatBarrier
\\begin{{figure}}[h]
	\\centering	
	\\includegraphics[width=1\\textwidth]{{../IMATGES/logoPaeriaMa.png}}
\\end{{figure}}
\\FloatBarrier	

\\vfill









\\noindent Benvolguts,

	\\vspace{{0.5cm}}

Des del \\textit{{Programa De La Mà: Acompanyament a la Gent Gran}}\\footnote{{Aquesta acció està subvencionada pel Servei Públic 
d'Ocupació de Catalunya en el marc del Programa de suport als territoris amb majors 
necessitats de reequilibri territorial i social: projecte``\\textbf{{treball als barris 2020}}'' (SOC032/20/000058).}} fem comunicacions mensuals
dirigides a la família i/o persona de contacte referent dels usuaris.


A la següent pàgina veureu una transcripció i adaptació de les actes que han escrit les treballadores associades
al Programa, en les que es mostra un breu informe de les activitats o accions que s'han fet amb (o per a) 
{} entre el període comprès entre el dia {} i el dia {}.

	\\vspace{{0.5cm}}

\\noindent Atentament,

\\noindent Santi Sánchez

\\noindent \\textit{{Coordinador Programa De La Mà:Acompanyament a la Gent Gran}}\\\\
\\textbf{{(T. anònim. | T. anònim)}}

	\\vspace{{0.5cm}}

\\noindent {}

	









\\vfill

\\FloatBarrier
\\begin{{figure}}[h]
	\\centering	
	\\includegraphics[width=1\\textwidth]{{../IMATGES/logosGeneMinisterAferssocialsSoc.png}}	
\\end{{figure}}
\\FloatBarrier	










\\clearpage




	\\begin{{longtable}}{{p{{0.15\\textwidth}}lp{{0.45\\textwidth}}}}
		

		
		\\hline
		\\textbf{{DATA}} & \\textbf{{ACOMPANYANT}} & \\textbf{{DESCRIPCIÓ}}\\\\
		\\hline\n"""





taula_long_variable = """\t\t\t {} & {} & {} \\\\ \n"""  





final = """		
	\\end{longtable}
\\end{document}"""