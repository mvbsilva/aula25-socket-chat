# -*- coding: utf-8 -*-
import threading
import socket


def main():
  # Cria um objeto de soquete para o cliente
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


  try:
      # Tenta se conectar ao servidor na porta 7777
      client.connect(('localhost', 7777))
  except:
      # Se não conseguir se conectar, exibe uma mensagem e encerra o programa
      return print('\nNão foi possível se conectar ao servidor!\n')


  # Solicita ao usuário inserir um nome de usuário
  username = input('Usuário> ')
  print('\nConectado')


  # Cria duas threads para lidar com a recepção e envio de mensagens simultaneamente
  thread1 = threading.Thread(target=receiveMessages, args=[client])
  thread2 = threading.Thread(target=sendMessages, args=[client, username])


  # Inicia as threads
  thread1.start()
  thread2.start()


def receiveMessages(client):
  # Loop para receber mensagens do servidor
  while True:
      try:
          # Recebe uma mensagem codificada em UTF-8 e a decodifica
          msg = client.recv(2048).decode('utf-8')
          # Exibe a mensagem recebida
          print(msg+'\n')
      except:
          # Se houver um erro ao receber mensagens, exibe uma mensagem e encerra a conexão
          print('\nNão foi possível permanecer conectado no servidor!\n')
          print('Pressione <Enter> Para continuar...')
          client.close()
          break


def sendMessages(client, username):
  # Loop para enviar mensagens para o servidor
  while True:
      try:
          # Solicita ao usuário inserir uma mensagem
          msg = input('\n')
          # Envia a mensagem formatada com o nome de usuário ao servidor
          client.send(f'<{username}> {msg}'.encode('utf-8'))
      except:
          # Se houver um erro ao enviar mensagens, encerra a thread
          return


# Chama a função main para iniciar o cliente
main()