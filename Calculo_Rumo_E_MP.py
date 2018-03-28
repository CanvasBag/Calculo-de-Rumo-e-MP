'''
Created on 15/11/2017

@author: Peter
'''

import progressbar
from time import sleep
from math import atan2, sin, cos, pi, sqrt
import os

basepath = os.getcwd()

paraGraus = 180.0 / pi
zona = "11"
'''
ficheiroPerfis = open("PTV_25m_Zona" + str(zona) + ".txt",'r')
ficheiroEixo = open("Eixo_25m_Zona" + str(zona) + ".txt",'r')
ficheiroCentrosM = open(basepath + "\PTV 25m Zona " + str(zona) + "\Centros_de_PerfisM_" + str(zona) + ".txt", 'w+')
ficheiroCentrosP = open(basepath + "\PTV 25m Zona " + str(zona) + "\Centros_de_PerfisP_" + str(zona) + ".txt", 'w+')
ficheiroRumos = open(basepath + "\PTV 25m Zona " + str(zona) + "\Rumos_de_Perfis_" + str(zona) + ".txt", 'w+')
ficheiroListagem = open(basepath + "\PTV 25m Zona " + str(zona) + "\Listagem_de_Perfis_Zona_" + str(zona) + ".txt", 'w+')
'''
ficheiroPerfis = open("PTV_100m.txt", 'r')
ficheiroEixo = open("Eixo_Total.txt", 'r')
ficheiroCentrosM = open(basepath + "\Centros_de_PerfisM.txt", 'w+')
ficheiroCentrosP = open(basepath + "\Centros_de_PerfisP.txt", 'w+')
ficheiroRumos = open(basepath + "\Rumos_de_Perfis.txt", 'w+')
ficheiroListagem = open(basepath + "\Listagem_de_Perfis_Zona.txt", 'w+')

linesPerfis = ficheiroPerfis.readlines()
pontosEixo = ficheiroEixo.readlines()
listaDePerfis = []
j = 0

bar = progressbar.ProgressBar(maxval=20, widgets=[progressbar.Bar(
    '=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()

while j < len(linesPerfis):
    bar.update(round(j * 20 / len(linesPerfis), 2))
    # calculo de centroides dos perfis
    ponto1 = [float(linesPerfis[j].split(' ')[0]),
              float(linesPerfis[j].split(' ')[1])]
    ponto2 = [float(linesPerfis[j + 1].split(' ')[0]),
              float(linesPerfis[j + 1].split(' ')[1])]
    centroidX = ponto1[0] - (ponto1[0] - ponto2[0]) / 2
    centroidY = ponto1[1] - (ponto1[1] - ponto2[1]) / 2
    # calculo de rumos dos perfis
    rumo = atan2((ponto1[0] - ponto2[0]), (ponto1[1] - ponto2[1]))
    if rumo < 0:
        rumo += pi
    # escrever em ficheiros para dgn
    afastM = sin(rumo) * 13
    afastP = cos(rumo) * 13
    ficheiroCentrosM.write(str.format('M:{0:.2f}', centroidX) + " " + str(
        ponto2[0] - afastM) + " " + str(ponto2[1] - afastP) + " 0" + "\n")
    ficheiroCentrosP.write(str.format('P:{0:.2f}', centroidY) + " " + str(
        ponto2[0] - afastM) + " " + str(ponto2[1] - afastP - 2) + " 0" + "\n")
    ficheiroRumos.write(str.format('R:{0:.3f}', rumo * paraGraus) + " " + str(
        ponto2[0] - afastM) + " " + str(ponto2[1] - afastP + 2) + " 0" + "\n")
    pk = 20700.0
    for i in range(0, len(pontosEixo) - 1):
        pontoEixoAnterior = [float(pontosEixo[i].split(
            ' ')[0]), float(pontosEixo[i].split(' ')[1])]
        pontoEixoPosterior = [
            float(pontosEixo[i + 1].split(' ')[0]), float(pontosEixo[i + 1].split(' ')[1])]
        pk += sqrt((pontoEixoAnterior[0] - pontoEixoPosterior[0])
                   ** 2 + (pontoEixoAnterior[1] - pontoEixoPosterior[1])**2)
        if pontoEixoAnterior[0] >= centroidX >= pontoEixoPosterior[0] and pontoEixoAnterior[1] >= centroidY >= pontoEixoPosterior[1] \
                or pontoEixoAnterior[0] >= centroidX >= pontoEixoPosterior[0] and pontoEixoAnterior[1] <= centroidY <= pontoEixoPosterior[1] \
                or pontoEixoAnterior[0] <= centroidX <= pontoEixoPosterior[0] and pontoEixoAnterior[1] <= centroidY <= pontoEixoPosterior[1] \
                or pontoEixoAnterior[0] <= centroidX <= pontoEixoPosterior[0] and pontoEixoAnterior[1] >= centroidY >= pontoEixoPosterior[1]:
            pkPerfil = int(round(
                pk + sqrt((pontoEixoAnterior[0] - centroidX)**2 + (pontoEixoAnterior[1] - centroidY)**2)))
            listaDePerfis.append(
                [pkPerfil, centroidX, centroidY, rumo * paraGraus, round(pkPerfil, -2)])
            break
            # ficheiroListagem.write("PK " + str(int(pkPerfil/1000)) + "+" + str.format('{0:03}',pkPerfil-int(pkPerfil/1000)*1000) + " " + str.format('{0:.2f}', centroidX) \
            #                       + " " + str.format('{0:.2f}', centroidY) + " " + str.format('{0:.3f}', rumo*paraGraus)+ "\n")

    j += 2

listaDePerfisOrdenadaPk = sorted(listaDePerfis, key=lambda x: x[0])
for linha in listaDePerfisOrdenadaPk:
    ficheiroListagem.write("PK " + str(int(linha[0] / 1000)) + "+" + str.format('{0:03}', linha[0] - int(linha[0] / 1000) * 1000) + " " + str.format('{0:.2f}', linha[1])
                           + " " + str.format('{0:.2f}', linha[2]) + " " + str.format('{0:.5f}', linha[3]) + " " + str(linha[4]) + "\n")

bar.finish()
ficheiroCentrosP.close()
ficheiroCentrosM.close()
ficheiroRumos.close()
ficheiroListagem.close()
ficheiroPerfis.close()
