# -*- coding: utf-8 -*-
import vimeo
import csv
from math import floor

#converte a resposata do vimeo(link do vídeo, a duração e nome) em um json
def retornaJsonVimeo(clientVimeo, idUsuario,pagina):
    resp = clientVimeo.get("https://api.vimeo.com/users/"+idUsuario+"/videos", params={"fields": "link,duration,name", "per_page": 100,"page":pagina})
    data = resp.json()
    return data

#gera o csv a partir das informações passadas pelo vímeo
def geraCSVfromJSON(dataJson):
    f = csv.writer(open("listagemAulas.csv", "a+"),lineterminator='')

    
    for x in dataJson["data"]:
        tempoVideo = str(int(floor(x["duration"]/60)))+":" + str(x["duration"]%60)
        f.writerow([x["link"].encode("utf8"), tempoVideo,x["name"].encode("utf8")+"\n"])
        
    


#faz a autenticaçao na conta do vimeo com base no app criado na conta
tokenAcesso = raw_input("Adicione o token de acesso:\n")
idCliente = raw_input("Adicione a identificador:\n")
segredo = raw_input("Adicione o segredo:\n")
idUsuario = raw_input("Adicione o id de usuario:\n")

usuarioVimeo = vimeo.VimeoClient(
  token=tokenAcesso,
  key=idCliente,
  secret=segredo
)


#abre o arquivo para esvaziar e escrever o header
arq = open("listagemAulas.csv", "w")
arq.write("Link,duração,Nome\n")
arq.close()

#salva as infors nos arquivos com base na quantidade de paginas
pagina=1
jsonVideosVimeo = retornaJsonVimeo(usuarioVimeo, idUsuario,pagina)
while "error_code" not in jsonVideosVimeo:
    print(jsonVideosVimeo)
    geraCSVfromJSON(jsonVideosVimeo)
    pagina+=1
    jsonVideosVimeo = retornaJsonVimeo(usuarioVimeo, idUsuario,pagina)

