# -*- coding: utf-8 -*-
import threading
import socket

# Lista de clientes conectados ao servidor
clients = []
username_conection = {}

# Função para lidar com as mensagens de um cliente
def handle_client(client):
  usr = client.recv(2048).decode('utf-8')
  username = usr.strip('')
  username_conection[username] = client
  print('Novo usuário: ', username)
  while True:
      try:
          msg = client.recv(2048).decode('utf-8')
          print(msg)
          src, msg = msg.split('/')
          dst, msg = msg.split(' ')
          
          print(src, dst, msg)
          if dst == 'list':
             send_user_list(client)
          elif dst == 'all':
            broadcast(msg, client)
          else:
            send_to_user(src, dst, msg, client)
      except:
          remove_client(client)
          break

# Função para transmitir mensagens para todos os clientes
def send_to_user(src, dst, msg, sender):
  if(dst in username_conection.keys()):
    dst_conn = username_conection[dst]
    try:
      dst_conn.send(f'<{src}> {msg}'.encode('utf-8'))
    except:
      pass
  
# Função para transmitir mensagens para todos os clientes
def broadcast(msg, sender):
  for client in clients:
      if client != sender:
          try:
              client.send(msg)
          except:
              remove_client(client)

# Função para enviar a lista de usuários
def send_user_list(client):
   print("debug")
   users = '\n'.join(username_conection.keys())
   client.send(f'{users}'.encode('utf-8'))
   

# Função para remover um cliente da lista
def remove_client(client):
  clients.remove(client)

# Função principal
def main():
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  print("Iniciou o servidor de bate-papo")

  try:
      server.bind(("0.0.0.0", 7777))
      server.listen()
  except:
      return print('\nNão foi possível iniciar o servidor!\n')

  while True:
      client, addr = server.accept()
      clients.append(client)
      print(f'Cliente conectado com sucesso. IP: {addr}')

      # Inicia uma nova thread para lidar com as mensagens do cliente
      thread = threading.Thread(target=handle_client, args=(client,))
      thread.start()

# Executa o programa
main()
