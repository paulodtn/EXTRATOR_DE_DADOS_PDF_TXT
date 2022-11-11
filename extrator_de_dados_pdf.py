import pdfplumber
import pandas as pd
import re
print(128*'-')

lixo = [' ATENCAO PRIMARIA',' CONSULTA MEDICA EM PRIMEIRA ','O INFORMADO T',
' CONSULTA MEDICA EMATENCAO PRIMARIA VEZ          ',' CONSULTA MEDICA EMATENCAO PRIMARIA PRIMEIRAVEZ ',' CONSULTA MEDICA EM PRIMEIRAVEZ',
' CONSULTA MEDICA EM PRIMEIRA VEZ',' CONSULTA MEDICA EM',' ATENCAO PRIMARIA PRIMEIRAVEZ DN','OUTROS ATENCAO PRIMARIA',
' CONSULTA MEDICA EM PRIMEIRA','OUTROS ATENCAO PRIMARIA VEZ ','OUTROS ATENCAO PRIMARIA PRIMEIRAVEZ',' CONSULTA MEDICA EM RETORNO']

with pdfplumber.open(r'D:\VSCode\Pyton\DESAFIO TASCOM\agenda_siga_medico.pdf') as pdf:
    first_page = pdf.pages[0]
    headerInfo = first_page.crop((0, 10, first_page.width, 100))
    name = re.search(r'Profissional: (.*)', headerInfo.extract_text()).group(1).split("  ")[0]
    cns = re.search(r'CNS:(.)+', headerInfo.extract_text()).group(0).split("  ")[0]
    especialidade = re.search(r'Especialidade:[A-Z]+[A-Z ]+', headerInfo.extract_text()).group(0).split("  ")[0]
    date = re.search(r'[0-9]{2}/[0-9]{2}/[0-9]{4}', headerInfo.extract_text()).group(0)
#REGEX PARA ENCONTRAR OS DADOS
with open(r'D:\VSCode\Pyton\DESAFIO TASCOM\agenda_siga_medico.txt', 'r') as texto:
    arquivo = texto.read()
pacientes = re.findall(r'[: ]*[A-Z]+[ ][A-Z]+[ A-Z]*', arquivo)
afiliacao = re.findall(r': [A-Z]+ [A-Z]+[ A-Z]*', arquivo)
hora = re.findall(r'[\d]{2}:[\d]{2}', arquivo)
data_nasc = re.findall(r'[\d]{2}/[\d]{2}/[\d]{4}', arquivo)
tel_com = re.findall(r'Tel Com: \w* \w*', arquivo)
tel_cel = re.findall(r'Tel Cel: \w* \w*', arquivo)
tel_res = re.findall(r'Tel Res: \w* ?\w*', arquivo)
tel_cont = re.findall(r'Tel Cont: \w* ?\w* ?[\s\d]+', arquivo)
raça_cor = re.findall(r'R/C: [\w]*', arquivo)
procedimento = re.findall(r'[\d]{9}-\d -[ A-Z*]{9} [ A-Z*]{6}', arquivo)
tipo = re.findall(r'[PR][A-Z]{6,7}', arquivo)
#TRATAR OS NOMES DOS PACIENTES
for x in lixo:
    def_lixo = x
    for x in range(pacientes.count(def_lixo)):
        pacientes.remove(def_lixo)
for x in afiliacao:
    def_lixo = x
    for x in range(pacientes.count(def_lixo)):
        pacientes.remove(def_lixo)
#TRATAR OS NOMES DAS MÃES DOS PACIENTES
afiliacao_tratadas = []
for x in afiliacao:
    afiliacao_tratadas.append(x[2:])
    afiliacao = afiliacao_tratadas  
procedimento_tratado = []
for x in procedimento:
    if x == '030101006-4 - CONSULTA MEDICA':
        x = '030101006-4 - CONSULTA MEDICA EM ATENCAO PRIMARIA'
        procedimento_tratado.append(x)
        procedimento = procedimento_tratado
tel_cel_tratado = []
for x in tel_cel:
    tel_cel_tratado.append(x[9:])
    tel_cel= tel_cel_tratado
tel_res_tratado = []
for x in tel_res:
    if x ==  'Tel Res: NÃƒO':
        tel_res_tratado.append('NÃO INFORMADO')  
    else:
        tel_res_tratado.append(x[9:])
        tel_res = tel_res_tratado
tel_com_tratado = []
for x in tel_com:
    if x == 'Tel Com: NÃƒO INFORMADO':
        tel_com_tratado.append('NÃO INFORMADO')
    else:
        tel_com_tratado.append(x[9:])
        tel_com = tel_com_tratado
tel_cont_tratado = []
for x in tel_cont:
    if 'NÃƒO' in x:
        tel_cont_tratado.append('NÃO INFORMADO')
    else:
        tel_cont_tratado.append(x[10:])
        tel_cont = tel_cont_tratado
raça_cor_tratado = []
for x in raça_cor:
    raça_cor_tratado.append(x[5:])
    raça_cor = raça_cor_tratado
especialidade_tratado = []
for x in range(len(pacientes)):
    especialidade_tratado.append(especialidade[14:])
name_tratado = []
for x in range(len(pacientes)):
    name_tratado.append(name)
cns_tratado = []
cns = cns[3:]
cns = cns[:16]
for x in range(len(pacientes)):  
    cns_tratado.append(cns)
date_consulta = []
for x in range(len(pacientes)):
    date_consulta.append(date)
tipo_tratado = []
for x in tipo:
    if x == 'PRIMEIRA' or x == 'RETORNO':
        tipo_tratado.append(x)
    #else:
        # for x in range(tipo.count(def_tipo)):
        #     tipo.remove(def_lixo)

tabela = pd.DataFrame(
    data = zip(date_consulta, hora, name_tratado, cns_tratado, especialidade_tratado, pacientes, afiliacao, data_nasc, raça_cor, tel_cel, tel_res, tel_com, tel_cont, procedimento, tipo_tratado),
    columns=['date_consulta','hora', 'name_tratado', 'cns_tratado', 'especialidade_tratado', 'pacientes', 'afiliacao', 'data_nasc', 'raça_cor', 'tel_cel', 'tel_res', 'tel_com', 'tel_cont', 'procedimento', 'tipo_tratado']
    )   
tabela.to_csv("agenda_siga_medico.csv")
print(tabela)
