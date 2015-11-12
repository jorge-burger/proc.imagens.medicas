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
if (tamanho<=4):
	os.system('clear')
	print """
	Programa de organizacao de imagens criado por Jorge Luiz Palmeiro Burger comecadono inicio 
de 2015.
   Este programa tem como funcao otimizar o processo de coleta de dados.
	Baseado em um sistema de argumentos, este recebe as informacoes basicas da imagem que deseja
utilizar, ou seja, recebe nome do projeto, sigla de estudo, numero da visita e ID do paciente.   
   No decorrer deste script serao realizadas:
	1. Criar pastas para os pacientes.
	2. Copiar arquivos do suite para a pasta do paciente.
	3. Converter as imagens PET e RM.
	4. Escrever o scanlog do paciente.	
	5. Verificar se alguma imagem dora coletada mais de uma vez
	6. Renomear arquivos conforme scanlog.
	7. Organizar as pastas dos pacientes conforme imagens.

	***==========================================================================***   
	***||Abaixo um exemplo de como utilizar este programa e tambem sua sintaxe:||***
	***||	conv_suite.py PROJETO PROJ visitx xxx				   ||***
	***||	Primeiro argumento: nome do projeto				   ||***
	***||		Ex:ESCMUL						   ||***
	***||	Segundo argumento: sigla do projeto				   ||***
	***||		Ex:ESCM							   ||***
	***||	Terceiro argumento: visita					   ||***
	***||		Ex:visit1						   ||***
	***||	Quarto argumento: ID do paciente				   ||***
	***||		Ex:001							   ||***
	***==========================================================================***
   Entretanto, para bom funcionamento do programa algumas regras devem ser seguidas.
	1) A pasta de saida do suite deve possuir a sigla do projeto e o ID do paciente;
		Ex: ESCM001

	2) As pastas Volumes xxxx devem estar renomeadas  para PET(se tiver) e RM e dentro de ID;
		OBS: PET possui 1 volume interno enquanto RM possui 2
   Ou seja:
   	~/DATA/DOWNLOADS_SUITE/ESCM001/RM/(volume\ 1 volume\ 2)

"""
	quit()

elif (tamanho>=6):
	os.system('clear')
	print ' Se voce deseja realizar esse script para mais de um pacien',
	print 'te entao utilize o script pacientes.py! '
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
"""			     			   Constantes					 """
folder=study+ID
projeto='/media/DATA/'+project
paciente=projeto+'/'+folder
visita=paciente+'/'+visit
PET=visita+'/PET'
RM=visita+'/RM'
scan=visita+'/scanlog_RM.txt'
scripts=projeto+'/SCRIPTS'
suite='/media/DATA/DOWNLOADS_SUITE/'+folder
backup='/media/DATA/jorge/scripts/backup'

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

def Remover_pasta(pasta):# Remover 'pasta'
	os.system('rm -rf '+pasta)

def Remover_arquivo(arquivo):# Remover 'arquivo'
	os.system('rm '+arquivo)

def Zipar(arquivo):# Compactar 'arquivo' em .tar.gz
	os.system('tar -zcvf dicom.tar.gz '+arquivo)
	os.system('chmod a-w dicom.tar.gz')

def Copiar_pasta(pasta,lugar):# Copiar pasta para 'lugar'.
	os.system('cp -r '+pasta+' '+lugar)

def Ir_para(lugar):# Entrar na pasta 'lugar'.
	os.chdir(lugar)

def Estou_em():# Mostrar o caminho da pasta em que o programa se localiza.
	print os.getcwd()

def Converter(pasta,onde,nome):# Converter dicom para nifti, em 'onde'
	os.system('dcm2nii -c -g -o '+onde+' '+pasta+'/* >'+pasta+'.'+nome)
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
# Mudando as permissoes do script
Ir_para(backup)
if Existe(backup+'/conv_suite.py')==True:
	os.system('chmod a+w conv_suite.py')
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
"""			  		   Verificando paciente					 """
print 'Etapa 1: Verificando a pasta do paciente'
# Verificando se existe a pasta do paciente
if Existe(paciente) == True:
	print '-->Ja existe a pasta do paciente: '+folder
	# Verificando se existe a pasta da visita
	if Existe(visita) == False:
		Ir_para(paciente)
		Criar(visit)
		print '-->Foi criada uma pasta visita para o sujeito: '+folder
# Criando uma pasta para o paciente
else:
	Ir_para(projeto)
	Criar(folder)
	Ir_para(paciente)
	Criar(visit)
	print '-->Foi criada uma pasta para o sujeito: '+folder
	print '-->Tambem foi criada uma pasta visita para o mesmo'
print 'Fim da Etapa 1'
print '----------------------------------------------------------------------'
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"""						Copiando dados					 """
#<-------------------------------------------------------------------------COMENTAR E DESCOMENTAR
print 'Etapa 2: Copiando as pastas do suite'
Ir_para(suite)
ls=commands.getoutput('ls').replace(' ','\n')
# Colocando em caps lock as pastas RM e PET
if (ls[0] == 'R' or ls[0] == 'r') and ls[0:2] != 'RM':	Renomear(ls[0:2],'RM')
if (ls[0] == 'P' or ls[0] == 'p') and ls[0:3] != 'PET':	Renomear(ls[0:3],'PET')
if len(ls)>3  and ls[4:6] != 'RM' and (ls[4] == 'R' or ls[4] == 'r'):	Renomear(ls[4:6],'RM')
pastas=[]
ls=commands.getoutput('ls')
# Descobrindo quantos conjuntos de imagens estao sendo enviados
if len(ls) == 6 and ls[0] == 'P' and ls[4] == 'R':
	pastas.append('PET')
	pastas.append('RM')
elif len(ls) < 6 and ls[0] == 'P':
	pastas.append('PET')
elif len(ls) < 6 and ls[0] == 'R':
	pastas.append('RM')
for x in range(0,len(pastas)):
	# Renomeando as pastas volumes, internas a pasta baixada
	Ir_para(suite+'/'+pastas[x])
	volume=commands.getoutput('ls')
	tozip=''
	quantidade=volume.count('volume')
	for valor in range(1,int(quantidade)+1):
		Renomear('volume\ '+str(valor),'volume'+str(valor))
		if valor != quantidade:	tozip+='volume'+str(valor)+' '
		else:	tozip+='volume'+str(valor)
	lugar=visita+'/'+str(pastas[x])
	if Existe(lugar) == False:
		Ir_para(suite)
		Copiar_pasta(pastas[x],visita)
		print '-->Pasta '+str(pastas[x])+' copiada com sucesso!'
		# Convertendo as imagens
		Ir_para(visita)
		Converter(str(pastas[x]),lugar,folder+'_'+visit)
		print '-->Imagens '+str(pastas[x])+' convertidas com sucesso!'
		Esperar(1)
		Mover(str(pastas[x])+'.'+folder+'_'+visit,scripts)
		# Ir para a pasta, zipar e apagar a pasta original
		Ir_para(lugar)
		Zipar(tozip)
		Remover_pasta(tozip)
		print '-->Pasta(s) original(is) '+pastas[x]+' zipada(s) e apagada(s) do marfim.'
print 'Fim da Etapa 2'
print '----------------------------------------------------------------------'

#<-------------------------------------------------------------------------COMENTAR E DESCOMENTAR
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"""			     		 Escrevendo scanlog					 """
#<-------------------------------------------------------------------------COMENTAR E DESCOMENTAR
print 'Etapa 3: Escrevendo o scanlog'
if Existe(scan) == False:
	Ir_para(scripts)
	for x in range(0,len(pastas)):
		os.system('fazer_scanlog.py '+project+' '+pastas[x]+' '+folder+' '+visit)
		Ir_para(scripts)
		Mover('scanlog_'+str(pastas[x])+'.txt',visita)
		Mover('auxiliar_'+str(pastas[x])+'.txt',visita)
		Renomear(str(pastas[x])+'.'+folder+'_'+visit,'dcm2nii_'+str(pastas[x])+'.txt')
		Mover('dcm2nii_'+str(pastas[x])+'.txt',visita)
print 'Fim da Etapa 3'
print '----------------------------------------------------------------------'
#<-------------------------------------------------------------------------COMENTAR E DESCOMENTAR
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"""				  		Organizando PET		            		 """
#<-------------------------------------------------------------------------COMENTAR E DESCOMENTAR
if len(pastas)==2 or pastas==['PET']:
	# Criando pastas para organizar os dados
	print 'Etapa 4: Criando pastas das imagens de PET'
	Ir_para(PET)
	if Existe(PET+'/RX') == False:
		Criar('RX')
		print 'Criando a pasta RX do PET'
	if Existe(PET+'/CTAC') == False:
		Criar('CTAC')
		print 'Criando a pasta CTAC do PET'
	if Existe(PET+'/CT') == False:
		Criar('CT')
		print 'Criando a pasta CT do PET'
	if Existe(PET+'/MAC') == False:
		Criar('MAC')
		print 'Criando a pasta MAC do PET'
	if Existe(PET+'/NAC') == False:
		Criar('NAC')
		print 'Criando a pasta NAC do PET'
	####(se tiver PET)if Existe(PET+'/???') == False:
	####(se tiver PET)	Criar('???')
	####(se tiver PET)	print 'Criando a pasta ???'
		print 'Fim da Etapa 4'
		print '----------------------------------------------------------------------'
	Ir_para(visita)
	dic={}
	scanlog=open('scanlog_PET.txt','r')
	var= scanlog.readlines()
	# Pegando todos os nomes dos arquivos
	for x in range(1,len(var)):
		print x
		print var[x]
		if x == 1:
			dcm2nii_out=var[x]
		if var[x][0]=='0':
			dic[var[x][0:3]]=var[x][5:var[x].find('\n')]
	
	Ir_para(PET)
	name={}
	repetido=[]
	# Confirmando se foi repetido um exame
	for x in dic:
		for y in dic:
			if int(y)>int(x) and dic[x]==dic[y]:
				repetido.append(x)
	for x in range(0,len(repetido)):
		del dic[repetido[x]]
	# Verificando para cada nome deve ser renomeado
	ls=commands.getoutput('ls').split('\n')
	for x in range(0,len(ls)):
		if ls[x][0:len(dcm2nii_out)-2] == dcm2nii_out[0:-2]:
			if ls[x][len(dcm2nii_out)] == '0':
				for y in dic:
					if ls[x][len(dcm2nii_out):len(dcm2nii_out)+3]==y:
						if dic[y]=='MAC' or dic[y]=='NAC':
							name[ls[x]]=folder+'.'+dic[y]+ls[x][-8:]
						else:
							name[ls[x]]=folder+'.'+dic[y]+ls[x][-7:]
						break
					else:
						name[ls[x]]='nada'
					
			elif ls[x][len(dcm2nii_out)] == 's':
				for y in dic:
					if ls[x][len(dcm2nii_out)+1:len(dcm2nii_out)+4]==y:
						if dic[y]=='MAC' or dic[y]=='NAC':
							name[ls[x]]=folder+'.'+dic[y]+ls[x][-8:]
						else:
							name[ls[x]]=folder+'.'+dic[y]+ls[x][-7:]
						break
					else:
						name[ls[x]]='nada'
			else:
				name[ls[x]]='nada'				
		elif ls[x][0] == 'c' or ls[x][0] == 'o':
			name[ls[x]]='nada'
	
	# Renomeando e movendo arquivos
	V0=len(str(folder)+'.')
	if Existe(PET+'/CT/'+folder+'.CT.nii.gz') == False:
		print 'Etapa 5: Renomeando e movendo arquivos PET'
		for x in name:
			if name[x]=='nada':
				Remover_arquivo(x)
			else:
				Renomear(x,name[x])
				print 'Arquivo renomeado com sucesso!'
				if name[x][V0:(V0+3)]=='MAC':
					Mover(name[x],PET+'/MAC')
					print 'Arquivo MAC movido com sucesso!'
				elif name[x][V0:(V0+3)]=='NAC':
					Mover(name[x],PET+'/NAC')
					print 'Arquivo NAC movido com sucesso!'
				elif name[x][V0:(V0+4)]=='CTAC':
					Mover(name[x],PET+'/CTAC')
					print 'Arquivo CTAC movido com sucesso!'
				elif name[x][V0:(V0+2)]=='RX':
					Mover(name[x],PET+'/RX')
					print 'Arquivo RX movido com sucesso!'
				elif name[x][V0:(V0+2)]=='CT':
					Mover(name[x],PET+'/CT')
					print 'Arquivo CT movido com sucesso!'
				####(se tiver PET)elif name[x][V0:(V0+len(???))]=='???':
				####(se tiver PET)	Mover(name[x],PET+'/???')
				####(se tiver PET)	print 'Arquivo ??? movido com sucesso!'
	print 'Fim da Etapa 5'
	print '----------------------------------------------------------------------'
	# Removendo pastas vazias
	print 'Etapa 6: Removendo pastas vazias da PET'
	Ir_para(PET)
	ls=commands.getoutput('ls')
	ls=ls.split('\n')
	for x in range(0,len(ls)):
		if ls[x] != 'dicom.tar.gz':
			Ir_para(PET+'/'+ls[x])
			if len(commands.getoutput('ls'))==0:
				Remover_pasta(PET+'/'+ls[x])
				print '-->Pasta '+ls[x]+' removida.'
	print 'Fim da Etapa 6'
	print '----------------------------------------------------------------------'

#<-------------------------------------------------------------------------COMENTAR E DESCOMENTAR
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"""						Organizando RM					 """
#<-------------------------------------------------------------------------COMENTAR E DESCOMENTAR
if len(pastas)==2 or pastas==['RM']:
	# Criando pastas para organizar os dados
	print 'Etapa 7: Criando pastas das imagens de RM'
	Ir_para(RM)
	if Existe(RM+'/RST') == False:
		Criar('RST')
		print 'Criando a pasta RST'
	if Existe(RM+'/ANAT') == False:
		Criar('ANAT')
		print 'Criando a pasta ANAT'
	if Existe(RM+'/DTI') == False:
		Criar('DTI')
		print 'Criando a pasta DTI'
	if Existe(RM+'/FLAIR') == False:
		Criar('FLAIR')
		print 'Criando a pasta FLAIR'
	if Existe(RM+'/T1SC') == False:
		Criar('T1SC')
		print 'Criando a pasta T1SC'
	if Existe(RM+'/DIFFC') == False:
		Criar('DIFFC')
		print 'Criando a pasta DIFFC'
	if Existe(RM+'/T2CC') == False:
		Criar('T2CC')
		print 'Criando a pasta T2CC'
	if Existe(RM+'/T1CC') == False:
		Criar('T1CC')
		print 'Criando a pasta T1CC'
	if Existe(RM+'/MgT') == False:
		Criar('MgT')
		print 'Criando a pasta MgT'
	if Existe(RM+'/SENNUM') == False:
		Criar('SENNUM')
		print 'Criando a pasta SENNUM'
	if Existe(RM+'/PALA1') == False:
		Criar('PALA1')
		print 'Criando a pasta PALA1'
	if Existe(RM+'/PALA2') == False:
		Criar('PALA2')
		print 'Criando a pasta PALA2'
	if Existe(RM+'/ON1') == False:
		Criar('ON1')
		print 'Criando a pasta ON1'
	if Existe(RM+'/ON2') == False:
		Criar('ON2')
		print 'Criando a pasta ON2'
	if Existe(RM+'/ON3') == False:
		Criar('ON3')
		print 'Criando a pasta ON3'
	if Existe(RM+'/OFF1') == False:
		Criar('OFF1')
		print 'Criando a pasta OFF1'
	if Existe(RM+'/OFF2') == False:
		Criar('OFF2')
		print 'Criando a pasta OFF2'
	if Existe(RM+'/OFF3') == False:
		Criar('OFF3')
		print 'Criando a pasta OFF3'
	if Existe(RM+'/RMET1') == False:
		Criar('RMET1')
		print 'Criando a pasta RMET1'
	if Existe(RM+'/RMET2') == False:
		Criar('RMET2')
		print 'Criando a pasta RMET2'
	if Existe(RM+'/DOTP1') == False:
		Criar('DOTP1')
		print 'Criando a pasta DOTP1'
	if Existe(RM+'/DOTP2') == False:
		Criar('DOTP2')
		print 'Criando a pasta DOTP2'
	if Existe(RM+'/PALA1') == False:
		Criar('PALA1')
		print 'Criando a pasta PALA1'
	if Existe(RM+'/PALA2') == False:
		Criar('PALA2')
		print 'Criando a pasta PALA2'
	if Existe(RM+'/PALA3') == False:
		Criar('PALA3')
		print 'Criando a pasta PALA3'
	if Existe(RM+'/HIST1') == False:
		Criar('HIST1')
		print 'Criando a pasta HIST1'
	if Existe(RM+'/HIST2') == False:
		Criar('HIST2')
		print 'Criando a pasta HIST2'
	if Existe(RM+'/HIST3') == False:
		Criar('HIST3')
		print 'Criando a pasta HIST3'
	if Existe(RM+'/PRIM1') == False:
		Criar('PRIM1')
		print 'Criando a pasta PRIM1'
	if Existe(RM+'/PRIM2') == False:
		Criar('PRIM2')
		print 'Criando a pasta PRIM2'
	####if Existe(RM+'/???') == False:
	####	Criar('???')
	####	print 'Criando a pasta ???'
		print 'Fim da Etapa 7'
		print '----------------------------------------------------------------------'
	Ir_para(visita)
	dic={}
	scanlog=open('scanlog_RM.txt','r')
	var= scanlog.readlines()
	# Pegando todos os nomes dos arquivos
	for x in range(1,len(var)):
		if x == 1:
			dcm2nii_out=var[x]
		if var[x][0]=='0':
			dic[var[x][0:3]]=var[x][5:var[x].find('\n')]
	
	Ir_para(RM)
	name={}
	repetido=[]
	# Confirmando se foi repetido um exame
	for x in dic:
		for y in dic:
			if int(y)>int(x) and dic[x]==dic[y]:
				repetido.append(x)
	for x in range(0,len(repetido)):
		del dic[repetido[x]]
	# Verificando para cada nome deve ser renomeado
	ls=commands.getoutput('ls').split('\n')
	for x in range(0,len(ls)):
		if ls[x][0:len(dcm2nii_out)-2] == dcm2nii_out[0:-2]:
			if ls[x][len(dcm2nii_out)] == '0':
				for y in dic:
					if ls[x][len(dcm2nii_out):len(dcm2nii_out)+3]==y:
						#pegando a extensao
						if ls[x].endswith('.bval'):
							name[ls[x]]=folder+'.'+dic[y]+ls[x][-5:]
						elif ls[x].endswith('.bvec'):
							name[ls[x]]=folder+'.'+dic[y]+ls[x][-5:]
						else:
							name[ls[x]]=folder+'.'+dic[y]+ls[x][-7:]
						break
					else:
						name[ls[x]]='nada'
					
			elif ls[x][len(dcm2nii_out)] == 's':
				for y in dic:
					if ls[x][len(dcm2nii_out)+1:len(dcm2nii_out)+4]==y:
						#pegando a extensao
						if ls[x].endswith('.bval'):
							name[ls[x]]=folder+'.'+dic[y]+ls[x][-5:]
						elif ls[x].endswith('.bvec'):
							name[ls[x]]=folder+'.'+dic[y]+ls[x][-5:]
						else:
							name[ls[x]]=folder+'.'+dic[y]+ls[x][-7:]
						break
					else:
						name[ls[x]]='nada'
			else:
				name[ls[x]]='nada'				
		elif ls[x][0] == 'c' or ls[x][0] == 'o':
			name[ls[x]]='nada'
	# Renomeando e movendo arquivos
	V0=len(str(folder)+'.')
	print 'Etapa 8: Renomeando e movendo os arquivos RM'
	for x in name:
		if name[x]=='nada':
			Remover_arquivo(x)
		else:
			Renomear(x,name[x])
			print 'Arquivo renomeado com sucesso!'
			if name[x][V0:(V0+3)]=='RST':
				Mover(name[x],RM+'/RST')
				print 'Arquivo RST movido com sucesso!'
			elif name[x][V0:(V0+3)]=='DTI':
				Mover(name[x],RM+'/DTI')
				print 'Arquivo DTI movido com sucesso!'
			elif name[x][V0:(V0+4)]=='T1CC':
				Mover(name[x],RM+'/T1CC')
				print 'Arquivo T1CC movido com sucesso!'
			elif name[x][V0:(V0+4)]=='T1SC':
				Mover(name[x],RM+'/T1SC')
				print 'Arquivo T1SC movido com sucesso!'
			elif name[x][V0:(V0+4)]=='T2CC':
				Mover(name[x],RM+'/T2CC')
				print 'Arquivo T2CC movido com sucesso!'
			elif name[x][V0:(V0+4)]=='ANAT':
				Mover(name[x],RM+'/ANAT')
				print 'Arquivo ANAT movido com sucesso!'
			elif name[x][V0:(V0+5)]=='DIFFC':
				Mover(name[x],RM+'/DIFFC')
				print 'Arquivo DIFFC movido com sucesso!'
			elif name[x][V0:(V0+5)]=='FLAIR':
				Mover(name[x],RM+'/FLAIR')
				print 'Arquivo FLAIR movido com sucesso!'
			elif name[x][V0:(V0+6)]=='T1CMgT':
				Mover(name[x],RM+'/MgT')
				print 'Arquivo T1CMgT movido com sucesso!'
			elif name[x][V0:(V0+6)]=='T1SMgT':
				Mover(name[x],RM+'/MgT')
				print 'Arquivo T1SMgT movido com sucesso!'
			elif name[x][V0:(V0+6)]=='SENNUM':
				Mover(name[x],RM+'/SENNUM')
				print 'Arquivo SENNUM movido com sucesso!'
			elif name[x][V0:(V0+5)]=='PALA1':
				Mover(name[x],RM+'/PALA1')
				print 'Arquivo PALA1 movido com sucesso!'
			elif name[x][V0:(V0+5)]=='PALA2':
				Mover(name[x],RM+'/PALA2')
				print 'Arquivo PALA2 movido com sucesso!'
			elif name[x][V0:(V0+3)]=='ON1':
				Mover(name[x],RM+'/ON1')
				print 'Arquivo ON1 movido com sucesso!'
			elif name[x][V0:(V0+3)]=='ON2':
				Mover(name[x],RM+'/ON2')
				print 'Arquivo ON2 movido com sucesso!'
			elif name[x][V0:(V0+3)]=='ON3':
				Mover(name[x],RM+'/ON3')
				print 'Arquivo ON3 movido com sucesso!'
			elif name[x][V0:(V0+4)]=='OFF1':
				Mover(name[x],RM+'/OFF1')
				print 'Arquivo OFF1 movido com sucesso!'
			elif name[x][V0:(V0+4)]=='OFF2':
				Mover(name[x],RM+'/OFF2')
				print 'Arquivo OFF2 movido com sucesso!'
			elif name[x][V0:(V0+4)]=='OFF3':
				Mover(name[x],RM+'/OFF3')
				print 'Arquivo OFF3 movido com sucesso!'
			elif name[x][V0:(V0+5)]=='RMET1':
				Mover(name[x],RM+'/RMET1')
				print 'Arquivo RMET1 movido com sucesso!'
			elif name[x][V0:(V0+5)]=='RMET2':
				Mover(name[x],RM+'/RMET2')
				print 'Arquivo RMET2 movido com sucesso!'
			elif name[x][V0:(V0+5)]=='DOTP1':
				Mover(name[x],RM+'/DOTP1')
				print 'Arquivo DOTP1 movido com sucesso!'
			elif name[x][V0:(V0+5)]=='DOTP2':
				Mover(name[x],RM+'/DOTP2')
				print 'Arquivo DOTP2 movido com sucesso!'
			elif name[x][V0:(V0+5)]=='PALA1':
				Mover(name[x],RM+'/PALA1')
				print 'Arquivo PALA1 movido com sucesso!'
			elif name[x][V0:(V0+5)]=='PALA2':
				Mover(name[x],RM+'/PALA2')
				print 'Arquivo PALA2 movido com sucesso!'
			elif name[x][V0:(V0+5)]=='PALA3':
				Mover(name[x],RM+'/PALA3')
				print 'Arquivo PALA3 movido com sucesso!'
			elif name[x][V0:(V0+5)]=='HIST1':
				Mover(name[x],RM+'/HIST1')
				print 'Arquivo HIST1 movido com sucesso!'
			elif name[x][V0:(V0+5)]=='HIST2':
				Mover(name[x],RM+'/HIST2')
				print 'Arquivo HIST2 movido com sucesso!'
			elif name[x][V0:(V0+5)]=='HIST3':
				Mover(name[x],RM+'/HIST3')
				print 'Arquivo HIST3 movido com sucesso!'
			elif name[x][V0:(V0+5)]=='PRIM1':
				Mover(name[x],RM+'/PRIM1')
				print 'Arquivo PRIM1 movido com sucesso!'
			elif name[x][V0:(V0+5)]=='PRIM2':
				Mover(name[x],RM+'/PRIM2')
				print 'Arquivo PRIM2 movido com sucesso!'
			####elif name[x][V0:(V0+len(???))]=='???':
			####	Mover(name[x],RM+'/???')
			####	print 'Arquivo ??? movido com sucesso!'
	print 'Fim da Etapa 8'
	print '----------------------------------------------------------------------'

	# Removendo pastas vazias
	print '-->Etapa 9: Removendo pastas vazias da RM'
	Ir_para(RM)
	ls=commands.getoutput('ls')
	ls=ls.split('\n')
	for x in range(0,len(ls)):
		if ls[x] != 'dicom.tar.gz':
			Ir_para(RM+'/'+ls[x])
			if len(commands.getoutput('ls'))==0:
				Remover_pasta(RM+'/'+ls[x])
				print 'Pasta '+ls[x]+' removida.'
	print 'Fim da Etapa 9'
	print '----------------------------------------------------------------------'
#<-------------------------------------------------------------------------COMENTAR E DESCOMENTAR
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"""					Organizando pastas					 """
#<-------------------------------------------------------------------------COMENTAR E DESCOMENTAR
# Removendo pasta RM se for somente um conjunto de imagens
print 'Etapa 10: Organizando pastas criadas'
if pastas == ['RM'] and projeto != 'ESCMUL':
	print ' Seu projeto possui somente imagens de ressonancia, por isso'
	print 'transferi todas as pastas criadas anteriormente para a pasta'
	print visit+' do paciente '+folder+', tambem removi a pasta RM para'
	print 'nao atrapalhar outros scripts seu.'
	Ir_para(RM)
	Mover('*',visita)
	Ir_para(visita)
	Remover_pasta('RM')
	Renomear('auxiliar_RM.txt','.auxiliar_RM.txt')
	Renomear('dcm2nii_RM.txt','.dcm2nii_RM.txt')
elif pastas == ['PET']:
	Ir_para(visita)
	Renomear('auxiliar_PET.txt','.auxiliar_PET.txt')
	Renomear('dcm2nii_PET.txt','.dcm2nii_PET.txt')
else:
	print 'Pastas organizadas com sucesso nas pastas RM e PET da visita '+visit
	print 'do paciente '+folder+'.'
	Ir_para(visita)
	Renomear('auxiliar_RM.txt','.auxiliar_RM.txt')
	Renomear('dcm2nii_RM.txt','.dcm2nii_RM.txt')
	Renomear('auxiliar_PET.txt','.auxiliar_PET.txt')
	Renomear('dcm2nii_PET.txt','.dcm2nii_PET.txt')
print 'Fim da Etapa 10'
print '----------------------------------------------------------------------'

#<-------------------------------------------------------------------------COMENTAR E DESCOMENTAR
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

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
Copiar_arquivo('conv_suite.py',backup)
# Mudando as permissoes dos scripts
Ir_para(backup)
os.system('chmod a-w conv_suite.py')
final=datetime.now()
print '\nMuito obrigado por utilizar este programa!!\n'
print ' O comando utilizado foi:'
print ' conv_suite.py '+sys.argv[1]+' '+str(sys.argv[2])+' '+str(sys.argv[3])+' '+str(sys.argv[4])
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

print ' \n\nAconselho verificar se todas as imagens foram coletadas com:'
print 'verificador.py '+sys.argv[1]+' '+str(sys.argv[2])+' '+str(sys.argv[3])+' '+str(sys.argv[4])
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
#-| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----| |----
#.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.....||.
