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
	Baseado em um sistema de argumentos, este recebe as informacoes basicas da imagem que deseja
utilizar, ou seja, recebe nome do projeto, sigla de estudo, numero da visita e ID do paciente.
   Abaixo um exemplo de como utilizar este programa e tambem sua sintaxe:
	python conv_suite.py PROJETO PROJ visitx xxx
	Primeiro argumento: nome do projeto
		Ex:ESCMUL
	Segundo argumento: sigla do projeto
		Ex:ESCM
	Terceiro argumento: visita
		Ex:visit1
	Quarto argumento: ID do paciente
		Ex:001
   No decorrer deste script sera realizada uma conferencia para vaveriguar se todas as imagens foram
coletadas e organizadas corretamente.
"""

#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
#-| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.


"""-------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
					Funcoes, variaveis e constantes
----------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------"""

#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"""			     	 		  Variaveis				 	 """
tamanho=len(sys.argv)
if (tamanho<=4):
	os.system('clear')
	print 'Este arquivo baseia-se em argumentos como na linha abaixo:'
	print '		conv_suite.py PROJETO PROJ visitx ID\n'
	print ' Lembre-se de usar os argumentos na ordem.'
	print '		Primeiro argumento: nome do projeto'
	print '			Ex:ESCMUL'
	print '		Segundo argumento: sigla do projeto'
	print '			Ex:ESCM'
	print '		Terceiro argumento: visita'
	print '			Ex:visit1'
	print '		ultimos argumentos: ID do paciente'
	print '			Ex:001'
	quit()

elif (tamanho>=6):
	os.system('clear')
	print ' este programa verifica se existem todas as imagens para 1 \
paciente apenas' 
	quit()

elif (tamanho==5):
	project=sys.argv[1]
	project=project.upper()
	study=sys.argv[2]
	study=study.upper()
	visit=sys.argv[3]
	visit=visit.lower()
	ID=sys.argv[4]

#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"""			     	   		Caminhos				   	 """
folder=study+ID
projeto='/media/DATA/'+project
paciente=projeto+'/'+folder
visita=paciente+'/'+visit
scripts=projeto+'/SCRIPTS'
PET=visita+'/PET'
RM=visita+'/RM'
#--------------------------------------------------------------------------
backup='/media/DATA/jorge/scripts/backup'
# Favor colocar o nome do sua pasta pessoal do marfim no lugar de 'jorge'

#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"""				    		Funcoes					 	 """
def Existe(caminho):# Testar se existe a pasta.
	return os.path.exists(caminho)
	
def Copiar_arquivo(arquivo,lugar):# Copiar arquivo para 'lugar'.
	os.system('cp '+arquivo+' '+lugar)
	
def Ir_para(lugar):# Entrar na pasta 'lugar'.
	os.chdir(lugar)
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
os.system('clear')
inicio=datetime.now()
print '\nBem vindo ao programa de otimizacao do Jorge\n'
print 'Hora de inicio: '+str(inicio)+'\n'
# Mudando as permissoes do script
##.##Ir_para(backup)
##.##if Existe(backup+'/verificador.py')==True:
##.##	os.system('chmod a+w verificador.py')

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
"""			     		 Verificando paciente					 """
if Existe(visita) == True:
	if Existe(PET) == True:
		Ir_para(PET)
		ls=commands.getoutput('ls').split('\n')
		for x in range(0,len(ls)):
			if ls[x] != 'dicom.tar.gz' and ls[x] != 'nohup.out':
				Ir_para(PET+'/'+ls[x])
				if len(commands.getoutput('ls'))==0:
					print '***A pasta '+ls[x]+' esta vazia.'
					print '------------------------------------------'
				else:
					print 'A pasta '+ls[x]+' possui as seguintes imagens:'
					ls1=commands.getoutput('ls').split('\n')
					for y in range(0, len(ls1)):
						print ls1[y]
					print '------------------------------------------'
	else:
		print '------------------------------------'
		print "= O projeto nao possui imagens PET ="
		print '------------------------------------'
	
	if Existe(RM) == True:
		Ir_para(RM)
		ls=commands.getoutput('ls').split('\n')
		for x in range(0,len(ls)):
			if ls[x] != 'dicom.tar.gz' and ls[x] != 'nohup.out':
				Ir_para(RM+'/'+ls[x])
				if len(commands.getoutput('ls'))==0:
					print '***A pasta '+ls[x]+' esta vazia.'
					print '------------------------------------------'
				else:
					print 'A pasta '+ls[x]+' possui as seguintes imagens:'
					ls1=commands.getoutput('ls').split('\n')
					for y in range(0, len(ls1)):
						print ls1[y]
					print '------------------------------------------'
	elif Existe(visita+'/dicom.tar.gz') == True:
		ls=commands.getoutput('ls').split('\n')
		for x in range(0,len(ls)):
			if ls[x] != 'dicom.tar.gz' and ls[x] != 'nohup.out':
				Ir_para(visita+'/'+ls[x])
				if len(commands.getoutput('ls'))==0:
					print '***A pasta '+ls[x]+' esta vazia.'
					print '------------------------------------------'
				else:
					print 'A pasta '+ls[x]+' possui as seguintes imagens:'
					ls1=commands.getoutput('ls').split('\n')
					for y in range(0, len(ls1)):
						print ls1[y]
					print '------------------------------------------'
	else:
		print '------------------------------------'
		print "= O projeto nao possui imagens RM ="
		print '------------------------------------'
	
else:
	print '---------------------------------------------------'
	print "= Nao existe a pasta '"+str(visit)+"' do paciente "+str(folder)+" ="
	print '---------------------------------------------------'

#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
#-| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.

"""-------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
					 Fim do programa
----------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------"""
# Fazendo Backup do script
##.##Ir_para(scripts)
##.##Copiar_arquivo('verificador.py',backup)
# Mudando as permissoes dos scripts
##.##Ir_para(backup)
##.##os.system('chmod a-w verificador.py')
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
#-| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
