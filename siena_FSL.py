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

"""-------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
					Funcoes, variaveis e constantes
----------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------"""

#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"""			    		 	   Variaveis					 """
tamanho=len(sys.argv)
if (tamanho!=6):
	os.system('clear')
	print """
	Programa de organizacao de imagens criado por Jorge Luiz Palmeiro Burger comecadono inicio 
de 2015.
   Este programa tem como funcao realizar a funcao siena do FSL.

	***==========================================================================***   
	***||Abaixo um exemplo de como utilizar este programa e tambem sua sintaxe:||***
	***||	conv_suite.py PROJETO PROJ visitx xxx				   ||***
	***||	Primeiro argumento: nome do projeto				   ||***
	***||		Ex:ESCMUL						   ||***
	***||	Segundo argumento: sigla do projeto				   ||***
	***||		Ex:ESCM							   ||***
	***||	Terceiro argumento: ID do paciente				   ||***
	***||		Ex:001							   ||***
	***||	Ultimos argumentos: visitas a se trabalhar			   ||***
	***||		Ex:visit1 visit2					   ||***
	***==========================================================================***
"""
	quit()

elif (tamanho==6):
	project=sys.argv[1]
	project=project.upper()
	study=sys.argv[2]
	study=study.upper()
	ID=sys.argv[3]
	visit1=sys.argv[4]
	visit1=visit1.lower()
	visit2=sys.argv[5]
	visit2=visit2.lower()

#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"""			     			   Constantes					 """
folder=study+ID
projeto='/media/DATA/'+project
paciente=projeto+'/'+folder
siena=paciente+'/siena'
visita1=paciente+'/'+visit1+'/RM/ANAT'
visita2=paciente+'/'+visit2+'/RM/ANAT'
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"""				 		   Funcoes					 """
def Existe(caminho):# Testar se existe a pasta.
	return os.path.exists(caminho)

def Esperar(tempo):# Esperar tantos segundos.
	time.sleep(tempo)

def Criar(pasta):# Criar 'pasta'.
	os.mkdir(pasta)

def Renomear(arquivo,nome):# Renomear arquivo para 'nome'.
	os.system('mv '+arquivo+' '+nome)

def Copiar_arquivo(arquivo,lugar):# Copiar arquivo para 'lugar'.
	os.system('cp '+arquivo+' '+lugar)

def Mover(arquivo,lugar):# Mover arquivo para 'lugar'.
	os.system('mv '+arquivo+' '+lugar)
	
def Ir_para(lugar):# Entrar na pasta 'lugar'.
	os.chdir(lugar)

def Estou_em():# Mostrar o caminho da pasta em que o programa se localiza.
	print os.getcwd()
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
print '\nBem vindo ao programa de otimizacao do Jorge Luiz Palmeiro Burger\n'
print 'Hora de inicio: '+str(inicio)+'\n'
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
#-| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.

"""-------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
			      		Inicio do programa
----------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------"""
Ir_para(paciente)
# Criando a pasta siena
if Existe(siena) == False:	Criar(siena)
# Nome da primeira imagem
if visit1 == 'visit1':	N1='V1.ANAT.nii.gz'
elif visit1 == 'visit2':	N1='V2.ANAT.nii.gz'
elif visit1 == 'visit3':	N1='V3.ANAT.nii.gz'
elif visit1 == 'visit4':	N1='V4.ANAT.nii.gz'
# Nome da segunda imagem
if visit2 == 'visit1':	N2='V1.ANAT.nii.gz'
elif visit2 == 'visit2':	N2='V2.ANAT.nii.gz'
elif visit2 == 'visit3':	N2='V3.ANAT.nii.gz'
elif visit2 == 'visit4':	N2='V4.ANAT.nii.gz'
# Copiando a primeira imagem para a pasta siena
Ir_para(siena)
if Existe(N1) != True:
	Ir_para(visita1)
	Copiar_arquivo(folder+'.ANAT.nii.gz',siena)
	print 'Arquivo da '+visit1+' foi copiado com sucesso.'
	Ir_para(siena)
	Renomear(folder+'.ANAT.nii.gz',N1)
# Copiando a segunda imagem para a pasta siena
Ir_para(siena)
if Existe(N2) != True:
	Ir_para(visita2)
	Copiar_arquivo(folder+'.ANAT.nii.gz',siena)
	print 'Arquivo da '+visit2+' foi copiado com sucesso.'
	Ir_para(siena)
	Renomear(folder+'.ANAT.nii.gz',N2)
# fazendo o siena
Ir_para(siena)
if Existe(N1[0:2]+'_'+N2[0:2]) == False and Existe(N2[0:2]+'_'+N1[0:2]) == False:
	# siena <input1> <input2> [-o <output_dir>]
	os.system('siena '+N1+' '+N2+' -o '+N1[0:2]+'_'+N2[0:2])
else:
	print 'Ja foi realizado um processamento com a funcao siena entre as visitas:'
	print visit1+' e '+visit2

#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\


"""-------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
			      		Fim do programa
----------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------"""
final=datetime.now()
print '\nMuito obrigado por utilizar este programa!!\n'
dif_d=int(final.day)-int(inicio.day)
dif_h=int(final.hour)-int(inicio.hour)
dif_mi=int(final.minute)-int(inicio.minute)
dif_s=int(final.second)-int(inicio.second)

if dif_h<0:
	dif_d-=1
	dif_h=24+dif_h
if dif_mi<0:
	dif_h-=1
	dif_mi=60+dif_mi
if dif_s<0:
	dif_mi-=1
	dif_s=60+dif_s

if dif_d == 0 and dif_h == 0 and dif_mi == 0:
	print ' O script demorou '+str(dif_s)+' segundos para finalizar.'
elif dif_d == 0 and dif_h == 0:
	print ' O script demorou '+str(dif_mi)+' minutos e '+str(dif_s)+' segundos para finalizar.'
elif dif_d == 0:
	print ' O script demorou '+str(dif_h)+' horas, '+str(dif_mi)+' minutos e '+str(dif_s)+\
	' segundos para finalizar.'
else:
	print ' O script demorou '+str(dif_d)+' dias, '+str(dif_h)+' horas, '+str(dif_mi)+\
	' minutos e '+str(dif_s)+' segundos para finalizar.'
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
#-| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
