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
	Ultimos argumentos: ID do(s) paciente(s)
		Ex:001 002 003 ...
	
   No decorrer deste script serao realizados alguns processamentos de imagem para o projeto sobre EM
dentre elas estao os processamento de DTI, ANAT e RST.
"""

#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
#-| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"""			     	   		Funcoes					 	 """
def Existe(caminho):# Testar se existe a pasta.
	return os.path.exists(caminho)
def Esperar(tempo):# Esperar tantos segundos.
	time.sleep(tempo)
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
	
"""			     	   		Variaveis					 """
tamanho=len(sys.argv)
subject=[]
if (tamanho<5):
	os.system('clear')
	print 'Este arquivo baseia-se em argumentos como na linha abaixo:'
	print '		processamento_ANAT.py PROJETO PROJ visitx ID \n'
	print ' Lembre-se de usar os argumentos na ordem.'
	print '		Primeiro argumento: nome do projeto'
	print '			EX:ESCMUL'
	print '		Segundo argumento: sigla do projeto'
	print '			EX:ESCM'
	print '		Terceiro argumento: visita'
	print '			EX:visit1'
	print '		Ultimos argumentos: ID do paciente'
	print '			EX:001'
	print '			EX:001 002 003 [...]'
	quit()
elif (tamanho==5):
	project=sys.argv[1]
	project=project.upper()
	study=sys.argv[2]
	study=study.upper()
	visit=sys.argv[3]
	visit=visit.lower()
	subject.append(sys.argv[4])
else:
	project=sys.argv[1]
	project=project.upper()
	study=sys.argv[2]
	study=study.upper()
	visit=sys.argv[3]
	visit=visit.lower()
	for x in range(4, tamanho):
		subject.append(sys.argv[x])

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
"""			     		Looping de sujeitos					 """
cont=0
while(cont<len(subject)):
	ID=subject[cont]
	folder=study+ID
	# Definindo as pastas constantes
	scripts='/media/DATA/'+project+'/SCRIPTS'
	rm='/media/DATA/'+project+'/'+folder+'/'+visit+'/RM'
	dti=rm+'/DTI'
	anat=rm+'/ANAT'
	rst=rm+'/RST'
	inicio=datetime.now()
	'Hora de inicio: '+str(inicio)+'\n'
	Esperar(60)
	#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
	#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
	"""			 		Processamento DTI				 """
	# Vai para a pasta DTI do paciente
	os.chdir(dti)
	# Fazendo a correcao EDDY
	#### eddy_correct <4d_input> <4d_output> <reference_no>
	os.system('eddy_correct '+folder+'.DTI.nii.gz '+\
						folder+'.DTI_ecc.nii.gz 0')
						
	# Criando a mascara
	#### bet2 <input_fileroot> <output_fileroot> [options] 
	os.system('bet2 '+folder+'.DTI_ecc.nii.gz '+\
					 folder+'.DTI_ecc_brain -m -f 0.3')
					 
	# Processando a imagem DTI
	#### dtifit -k <dti data file> -o <output basename>
			 #### -m <brain mask> -r <gradient directions file>
					   #### -b <gradient b-values file> 
	os.system('dtifit -k '+folder+'.DTI_ecc.nii.gz -o '+folder+\
			   ' -m '+folder+'.DTI_ecc_brain_mask.nii.gz -r '+\
				folder+'.DTI.bvec -b  '+folder+'.DTI.bval')
	Esperar(60)
	print '|=========================================|'
	print '|=========================================|'
	print '| O processamento da imagem DTI finalizou.|'
	print '|=========================================|'
	print '|=========================================|'
	Esperar(60)
	#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
	#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
	"""			 		Processamento ANAT				 """
	# Vai para a pasta ANAT do paciente e utiliza unifromize+sienax
	os.chdir(anat)	
	
	#### 3dUniformize -anat <input_image> -prefix <output>
	os.system('3dUniformize -anat '+folder+'.ANAT.nii.gz -prefix '+\
					  folder+'.ANAT_uniformize.nii.gz')
	#### sienax <input>  -o <ouput> <options>[-B "-f 0.3"]
	os.system('sienax '+folder+'.ANAT_uniformize.nii.gz')
	
	Esperar(60)
	print '|==========================================|'
	print '|==========================================|'
	print '| O processamento da imagem ANAT finalizou.|'
	print '|==========================================|'
	print '|==========================================|'
	Esperar(60)
	#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
	#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
	"""			 		Processamento RST				 """
	# Vai para a pasta scripts e utiliza o script preproc.RST.NL.csh
	os.chdir(scripts)
	os.system('csh preproc.RST.NL.csh '+folder+' '+visit)
	
	Esperar(60)
	print '|=========================================|'
	print '|=========================================|'
	print '| O processamento da imagem RST finalizou.|'
	print '|=========================================|'
	print '|=========================================|'
	Esperar(60)
	#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
	#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
	"""			 		Organizando pastas				 """
	# Retornando para a pasta do paciente
	os.chdir(rm)
	
	# Criando as pastas para depositar as imagens processadas
	os.system('mkdir PROC.ANAT')
	os.system('mkdir PROC.DTI')
	
	
	# Retornando para a pasta DTI do paciente
	os.chdir(dti)
	
	# Movendo imagens para a nova pasta
	os.system('mv '+folder+'.DTI_ecc* '+rm+'/PROC.DTI')
	os.system('mv '+folder+'_* '+rm+'/PROC.DTI')
	
	# Retornando para a pasta ANAT do paciente
	os.chdir(anat)
	
	# Movendo imagens para a nova pasta
	os.system('mv p* '+rm+'/PROC.ANAT')
	os.system('mv vtou* '+rm+'/PROC.ANAT')
	os.system('mv '+folder+'.ANAT_* '+rm+'/PROC.ANAT')
	
	# Incrementando para o proximo paciente
	final=datetime.now()
	print '\nMuito obrigado por utilizar este programa!!\n'
	print ' O comando utilizado foi:'
	print ' processamento.py '+sys.argv[1]+' '+str(sys.argv[2])+' '+str(sys.argv[3])+' '+\
str(sys.argv[4])
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
		print ' O script demorou '+str(dif_mi)+' minutos e '+str(dif_s)+\
	' segundos para finalizar.'
	elif dif_d == 0:
		print ' O script demorou '+str(dif_h)+' horas, '+str(dif_mi)+\
	' minutos e '+str(dif_s)+' segundos para finalizar.'
	else:
		print ' O script demorou '+str(dif_d)+' dias, '+str(dif_h)+' horas, '+str(dif_mi)\
	+' minutos e '+str(dif_s)+' segundos para finalizar.'

	cont+=1
	
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
#-| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
	
