# -*- coding: utf-8 -*-
import threading
import socket


def main():
  # Cria um objeto de soquete para o cliente
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


  try:
      # Tenta se conectar ao servidor na porta 7777
      client.connect(('192.168.10.52', 7777))
  except:
      # Se não conseguir se conectar, exibe uma mensagem e encerra o programa
      return print('\nNão foi possível se conectar ao servidor!\n')


  # Solicita ao usuário inserir um nome de usuário
  username = input('Usuário> ')

  client.send(f'{username}'.encode('utf-8'))
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
 def sendMessages(client, username):
    while True:
        try:
            user_input = input('').strip()

            if not user_input:
                continue

            if user_input.lower() == 'quit':
                client.close()
                break

            # ✅ Mensagem privada: para:destino mensagem
            if user_input.startswith('para:'):
                try:
                    header, message = user_input.split(' ', 1)
                    dest = header.split(':', 1)[1]

                    payload = f'{username}/{dest} {message}'
                    client.send(payload.encode('utf-8'))
                except ValueError:
                    print("Uso correto: para:usuario mensagem")
                continue

            # ✅ Lista de usuários
            if user_input == 'list':
                payload = f'{username}/list '
                client.send(payload.encode('utf-8'))
                continue

            # ✅ Broadcast padrão
            payload = f'{username}/all {user_input}'
            client.send(payload.encode('utf-8'))

        except:
            break



# Chama a função main para iniciar o cliente
main()