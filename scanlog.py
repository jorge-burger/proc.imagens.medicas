#! /usr/bin/env python
from datetime import *
import sys
import commands
import os
import time
import dicom

#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
#-| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.

"""
  Programa de otimizacao de organizacao de imagens criado por Jorge Luiz Palmeiro Burger comecado 
no inicio de 2015.
   Este programa tem como funcao escrever o Scanlog do paciente. Recebe de argumentos o nome do pro-
jeto, o tipo de imagem que serao retirados dados para analises e por ultimo o ID do paciente a ser
estudado.
   Abaixo um exemplo de como utilizar este programa e tambem sua sintaxe:
	python scanlog.py PROJETO IMAGEM IDxxx
	Primeiro argumento: nome do projeto
		Ex:ESCMUL
	Segundo argumento: Pasta contendo imagens
		Ex:PET
		Ex:RM
	Terceiro argumento: ID do paciente
		Ex:ESCM001
		
"""

#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
#-| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.

"""-------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
				 	     Variaveis,Constantes e Funcoes
----------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------"""

#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"""			     	   		Variaveis			    	         """
tamanho=len(sys.argv)
if (tamanho<=4):
	os.system('clear')
	print 'Este arquivo baseia-se em argumentos como na linha abaixo:'
	print '		scanlog.py PROJETO PROJ visitx ID \n'
	print ' Lembre-se de usar os argumentos na ordem.'
	print '		Primeiro argumento: nome do projeto'
	print '			Ex:ESCMUL'
	print '		Segundo argumento: Pasta contendo imagens'
	print '			Ex:PET'
	print '		Terceiro argumento: folder'
	print '			Ex:ESCM001'
	quit()

elif (tamanho == 5):
	project=sys.argv[1]
	project=project.upper()
	pasta=sys.argv[2]
	pasta=pasta.upper()
	folder=sys.argv[3]
	folder=folder.upper()
	visit=sys.argv[4]
	visit=visit.lower()
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"""					     	     Constantes			    		 """
projeto='/media/DATA/'+project
scripts=projeto+'/SCRIPTS'
suite='/media/DATA/DOWNLOADS_SUITE/'+folder
backup='/media/DATA/jorge/scripts/backup'
# Favor colocar o nome do sua pasta pessoal do marfim no lugar de 'jorge'

#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"""				   		     Funcoes				         """
def Existe(caminho):# Testar se existe a pasta.
	return os.path.exists(caminho)

def Esperar(tempo):# Esperar tantos segundos.
	time.sleep(tempo)

def Copiar_arquivo(arquivo,lugar):# Copiar arquivo para 'lugar'.
	os.system('cp '+arquivo+' '+lugar)

def Remover_arquivo(arquivo):# Remover 'arquivo'
	os.system('rm '+arquivo)

def Ir_para(lugar):# Entrar na pasta 'lugar'.
	os.chdir(lugar)

def Estou_em():# Mostrar o caminho da pasta em que o programa se localiza.
	print os.getcwd()


def Renomear(arquivo,nome):# Renomear arquivo para 'nome'.
	os.system('mv '+arquivo+' '+nome)


#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
#-| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.

"""-------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
				 			Perfumaria
----------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------"""
print '\nVoce esta usando o script: scanlog.py\n'
inicio=datetime.now()
print 'Iniciou em: '+ str(datetime.now())+'\n'
Ir_para(backup)
if Existe(backup+'/fazer_scanlog.py') == True:
	os.system('chmod a+w fazer_scanlog.py')
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
#-| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
"""-------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
				 		Inicio do programa
----------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------"""

#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#<----------------------------------------------------------------------------COMENTAR E DESCOMENTAR
Ir_para(scripts)
aux=open('auxiliar_'+pasta+'.txt','w')
Ir_para(suite+'/'+pasta)
ls=commands.getoutput('ls')
volume=ls.count('volume')
cont=1
while cont<=volume:
	total=0
	caminho=suite+'/'+pasta+'/volume'+str(cont)
	cont+=1 # Preparando para o proximo volume
	Ir_para(caminho)# Entrando na pasta volume
	ls=commands.getoutput('ls')
	caminho=caminho+'/'+ls[0 : ls.find('\n')]
	Ir_para(caminho)# Entrando na pasta numerica
	ls=commands.getoutput('ls')
	caminho=caminho+'/'+ls
	Ir_para(caminho)# Entrando na pasta do estudo
	ls=commands.getoutput('ls')
	# Vendo quantas series a pasta tem
	cont2=int(ls.count('serie'))+1
	ls=ls.replace('serie','').replace('\n',' ')
	# Encontrando a primeira serie
	first=int(min(ls.split(' ')))
	for x in range((first-cont2),(first+cont2)):
		cam=caminho+'/serie'+str(x)
		if Existe(cam)  ==  True:# Entrando nas pastas serie
			Ir_para(cam)
			ls=commands.getoutput('ls')
			# Quantidade de imagens da serie
			qnt=ls.count('.dcm')
			total=total+qnt
			ls=ls.replace('.dcm','').replace('\n',' ')
			# Encontrando a primeira imagem
			I1=int(min(ls.split(' ')))
			for y in range((I1-qnt),(I1+qnt)):
				teste=cam+'/'+str(y)+'.dcm'
				if Existe(teste) == True:
					I1=y
					break
			# Lendo a primeira imagem da serie
			imagem=dicom.read_file(str(I1)+'.dcm')
			####print imagem
			####quit()
			Ir_para(scripts)
			scanlog=open('scanlog_'+pasta+'.txt','w')
			# EScrevendo a saida do dcm2nii
			scanlog.write('Saida dcm2nii:\n')
			V0= imagem.StudyDate+'_'+imagem.StudyTime+\
imagem.ProtocolName.replace('.','').replace(' ','').replace('_','').replace('-','').replace('/','')
			## Todo e qualquer sinal deve ser retirado do protocolo adicionando acima:
			## .replace('sinal','')
			scanlog.write(V0)
			"""-----------------------Escrevendo dados pessoais----------------------"""
			# Escrevendo o nome do paciente
			scanlog.write('\n\n\nNome: ')
			scanlog.write(imagem.PatientName)
			# Escrevendo a idade do paciente
			scanlog.write('\nIdade: ')
			scanlog.write(imagem.PatientAge[1:-1])
			scanlog.write(' anos')
			# Escrevendo a data de nascimento
			scanlog.write('\nAniversario: ')
			var=imagem.PatientBirthDate[-2:]+'/'
			var=var+imagem.PatientBirthDate[-4:-2]+'/'
			var=var+imagem.PatientBirthDate[0:-4]
			scanlog.write(var)
			# Escrevendo o sexo do paciente
			scanlog.write('\nSexo: ')
			var=imagem.PatientSex
			scanlog.write(var)
			if var == 'F':
				scanlog.write('eminino\n')
			elif var == 'M':
				scanlog.write('asculino\n')
			# Escrevendo o tipo do paciente
			if project == 'ESCMUL':
				scanlog.write('Tipo: ')
				if folder[-3] == '0':
					scanlog.write('Paciente ')
					scanlog.write('em ')
					scanlog.write('tratamento ')
					scanlog.write('previo.')
					scanlog.write('\n\n')
				elif folder[-3] == '1':
					scanlog.write('Paciente ')
					scanlog.write('virgem de ')
					scanlog.write('tratamento.')
					scanlog.write('\n\n')
				elif folder[-3] == '5':
					scanlog.write('Controle.')
					scanlog.write('\n\n')
			elif project == 'SCHOOLS':
				scanlog.write('Tipo: ')
				if folder[3] == 'B':
					scanlog.write('Bom leitor')
					scanlog.write('\n\n')
				elif folder[3] == 'M':
					scanlog.write('Mau leitor')
					scanlog.write('\n\n')
			elif project == 'PFERREIRA':
				scanlog.write(' sem diferenca entre pacientes')
				scanlog.write('\n\n')
			####elif project == '???':
			####	scanlog.write('Tipo: ')
			####	if folder[???] == '???':
			####		scanlog.write('TIPO 1')
			####		scanlog.write('\n\n')
			####	elif folder[???] == '???':
			####		scanlog.write('TIPO 2')
			####		scanlog.write('\n\n')
			####	elif folder[???] == '???':
			####		scanlog.write('TIPO x')
			####		scanlog.write('\n\n')
			# Escrevendo a data do exame
			scanlog.write('Data de exame: ')
			var=imagem.StudyDate[-2:]+'/'
			var=var+imagem.StudyDate[-4:-2]+'/'
			var=var+imagem.StudyDate[0:-4]
			scanlog.write(var+'\n\n')
			scanlog.close
			"""-------------------------Escrevendo auxiliar--------------------------"""
			aux.write('----------')
			aux.write(pasta)
			aux.write('----------\n')
			aux.write('\nserie'+str(x)+':\n')
			aux.write('Numero de imagens: '+str(qnt)+'\n')
			aux.write('Primeira imagem: '+str(I1)+'\n')
			aux.write('Modalidade: ')
			aux.write(imagem.Modality+'\n')
			aux.write('Tipo: ')
			aux.write(imagem.SeriesDescription+'\n')
	aux.write('\n\nTotal de imagens no volume: ')
	aux.write(str(total)+'\n\n')			
aux.close
Ir_para(scripts)
scanlog=open('scanlog_'+pasta+'.txt','a')
aux1=open('auxiliar_'+pasta+'.txt','r')
aux=open(pasta+'.'+folder+'_'+visit,'r')
scanlog.write('imagens '+pasta+':\n')
# Verificando quantas linhas tem o script auxiliar
var=aux.readlines()
var1=aux1.readlines()
for x in range(0,len(var)):
	# Encontrando a linha que informa a imagem convertida
	if var[x][-5 : -1] == '.nii':
		# imagem convertida
		imagem=int(var[x][0:var[x].find('.')])
		for y in range(0, len(var1)):
			# Copiando o intervalo de imagens da serie
			if var1[y][0:6] == 'Numero':
				# Numero de imagens dentro da serie
				qnt=int(var1[y][var1[y].find(':')+2 :-1])
			# Copiando o valor da primeira imagem da serie
			if var1[y][0:8] == 'Primeira':
				# Primeira imagem da serie
				I1=int(var1[y][var1[y].find(':')+2 :-1])
				# Testando cada serie  com  valor
				for z in range(I1,I1+qnt):
					# se for igual, a serie convertida foi encontrada
					if imagem == z:
						imagem=0
						# Pegando o numero
						numero=var[x][var[x].find('>')+1:-1]
						if numero[len(V0)] =='0':
							numero = numero[len(V0):len(V0)+2]
						elif numero[len(V0)] == 'S':
							numero = numero[len(V0)+2:len(V0)+5]
						elif numero[len(V0)] == 's':
							numero = numero[len(V0)+1:len(V0)+4]
						####elif numero[len(V0)] =='???':
						####	numero = numero[len(V0)(num1):len(V0)+2(num3)]
						seq=var1[y+2][var1[y+2].find(':')+2:-1]
						# Pegando a sequencia
						
						##--------------------Imagens PET-------------------
						if \
		    			 seq  ==  'e+1 CT SCOUT BRAIN' or seq  ==  'CT SCOUT BRAIN':
							nome = 'RX'
						elif  \
		  		       seq  ==  'e+1 CTAC 3.75 Thick' or seq  ==  'CTAC 3.75 Thick':
							nome = 'CTAC'
						elif \
		    			 seq  ==  'e+1 Brain Standard' or seq  ==  'Brain Standard':
							nome = 'CT'
						elif \
	  		       seq  ==  'e+1 Static Brain 3D MAC' or seq  ==  'Static Brain 3D MAC':
							nome = 'MAC'
						elif \
	  		       seq  ==  'e+1 Static Brain 3D NAC' or seq  ==  'Static Brain 3D NAC':
							nome = 'NAC'
							
						##---------------------Imagens RM-------------------
              					####Se no auxiliar for diferente dos citados
              					####trocar ':' por ' or\' e numa nova linha adiciona
              					####seq == 'e+1 ???' or seq == '???':   
						elif \
						     seq  ==  'e+1 FMRI RST' or seq  ==  'FMRI RST':
							nome = 'RST'
						elif \
	    			 seq  ==  'e+1 AXI 3D FSPGR BRAVO' or seq  ==  'AXI 3D FSPGR BRAVO':
							nome = 'ANAT'
						elif \
		  		    seq  ==  'e+1 DTI GE 2.4 B750' or seq  ==  'DTI GE 2.4 B750' or\
		  		     seq  ==  'e+1 DTI GE 2.4 B-750' or seq  ==  'DTI GE 2.4 B-750':
							nome = 'DTI'
						elif \
		        	         seq  ==  'e+1 S Flair Cube' or seq  ==  'S Flair Cube' or \
		        	     seq  ==  'e+1 S Flair Cube + C' or seq  ==  'S Flair Cube + C':
							nome = 'FLAIR'
						elif \
		      			   seq  ==  'e+1 A 3D FSPGR FS' or seq  ==  'A 3D FSPGR FS':
							nome = 'T1SC'
						elif \
			  		       seq  ==  'e+1 A DWI DSE+C' or seq  ==  'A DWI DSE+C':
							nome = 'DIFFC'
						elif \
			    			 seq  ==  'e+1 A T2 FSE+C' or seq  ==  'A T2 FSE+C':
							nome = 'T2CC'
						elif \
		    		  seq  ==  'e+1 A 3D FSPGR FS+C' or   seq  ==  'A 3D FSPGR FS+C' or\
		    		   seq  ==  'e+1 A 3D FSPGR FS + C' or seq  ==  'A 3D FSPGR FS + C':
							nome = 'T1CC'
						elif \
              			   seq  ==  'e+1 A 3D SPGR COM MgT' or seq  ==  'A 3D SPGR COM MgT':
							nome = 'T1CMgT'
						elif \
              			   seq  ==  'e+1 A 3D SPGR SEM MgT' or seq  ==  'A 3D SPGR SEM MgT':
							nome = 'T1SMgT'
						elif \
              					   seq  ==  'e+1 SENSO NUM' or seq  ==  'SENSO NUM':
							nome = 'SENNUM'
						elif \
              					     seq  ==  'e+1 PSEUDO I' or seq  ==  'PSEUDO I':
							nome = 'PALA1'
						elif \
              					   seq  ==  'e+1 PSEUDO II' or seq  ==  'PSEUDO II':       					   			nome = 'PALA2'
						elif seq  ==  'e+1 RST1' or seq  ==  'RST1':       					   			nome = 'RST1'
						elif seq  ==  'e+1 RST2' or seq  ==  'RST2':       					   			nome = 'RST2'
						elif seq  ==  'e+1 ULT1' or seq  ==  'ULT1':       					   			nome = 'ULT1'
						elif seq  ==  'e+1 ULT2' or seq  ==  'ULT2':       					   			nome = 'ULT2'
						elif seq  ==  'e+1 ON1' or seq  ==  'ON1':       					   			nome = 'ON1'
						elif seq  ==  'e+1 ON2' or seq  ==  'ON2':       					   			nome = 'ON2'
						elif seq  ==  'e+1 ON3' or seq  ==  'ON3':       					   			nome = 'ON3'
						elif seq  ==  'e+1 OFF1' or seq  ==  'OFF1':       					   			nome = 'OFF1'
						elif seq  ==  'e+1 OFF2' or seq  ==  'OFF2':       					   			nome = 'OFF2'
						elif seq  ==  'e+1 OFF3' or seq  ==  'OFF3':       					   			nome = 'OFF3'
						elif \
					     seq  ==  'e+1 FMRI RMET I' or seq  ==  'FMRI RMET I':       					   			nome = 'RMET1'
						elif \
					     seq  ==  'e+1 FMRI RMET II' or seq  ==  'FMRI RMET II':       					   			nome = 'RMET2'
						elif \
					     seq  ==  'e+1 DOT-PROB 1' or seq  ==  'DOT-PROB 1':       					   			nome = 'DOTP1'
						elif \
					     seq  ==  'e+1 DOT-PROB 2' or seq  ==  'DOT-PROB 2':       					   			nome = 'DOTP2'
						elif \
					     seq  ==  'e+1 PALATAVEIS 1' or seq  ==  'PALATAVEIS 1':       					   			nome = 'PALA1'
						elif \
					     seq  ==  'e+1 PALATAVEIS 2' or seq  ==  'PALATAVEIS 2':       					   			nome = 'PALA2'
						elif \
					     seq  ==  'e+1 PALATAVEIS 3' or seq  ==  'PALATAVEIS 3':       					   			nome = 'PALA3'
						elif \
					     seq  ==  'e+1 HISTORIAS 1' or seq  ==  'HISTORIAS 1':       					   			nome = 'HIST1'
						elif \
					     seq  ==  'e+1 HISTORIAS 2' or seq  ==  'HISTORIAS 2':       					   			nome = 'HIST2'
						elif \
					     seq  ==  'e+1 HISTORIAS 3' or seq  ==  'HISTORIAS 3':       					   			nome = 'HIST3'
						####elif \
              					####seq  ==  'e+1 ???(auxiliar_RM.txt)' or seq  ==  '???(auxiliar_RM.txt)':
						####	nome = '???(pasta)'
						
						
						else:
							nome = 'nada'
						# Se for sequencia indesejada
						if nome != 'nada':
							scanlog.write(numero+': '+nome+'\n')
scanlog.write('\n')	
aux.close
aux1.close
scanlog.close
# Escrevendo o scanlog, com as sequencias e seus respectivos numeros
Ir_para(scripts)
scanlog=open('scanlog_'+pasta+'.txt','r')
scanlog2=open('scanlog2.txt','w')
var=scanlog.readlines()
for x in range(1,len(var)):
	# Escrevendo as sequencias e numeros
	if var[x]!=var[x-1]:
		scanlog2.write(var[x-1])
scanlog.close
scanlog2.close
Remover_arquivo('scanlog_'+str(pasta)+'.txt')
Renomear('scanlog2.txt','scanlog_'+str(pasta)+'.txt')
#<----------------------------------------------------------------------------COMENTAR E DESCOMENTAR
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
#-| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.

"""-------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
				 	Fim do programa
----------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------"""
# Fazendo Backup do script
Ir_para(scripts)
Copiar_arquivo('fazer_scanlog.py',backup)
# Mudando as permissoes dos scripts
Ir_para(backup)
os.system('chmod a-w fazer_scanlog.py')
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
#-| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.

