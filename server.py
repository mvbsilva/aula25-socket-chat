# -*- coding: utf-8 -*-
import threading
import socket

# Lista de clientes conectados ao servidor
clients = []
username_connection = {}

# Função para lidar com as mensagens de um cliente
def handle_client(client):
    username = None
    try:
        usr = client.recv(2048).decode('utf-8')
        username = usr.strip()
        username_connection[username] = client
        print(f'Novo usuário conectado: {username}')
        
        # Notifica o usuário sobre a conexão bem-sucedida
        client.send(f'Bem-vindo, {username}!\n'.encode('utf-8'))
        
        # Notifica todos os outros usuários sobre a entrada
        broadcast_system(f'*** {username} entrou no chat ***')
        
        while True:
            try:
                msg = client.recv(2048).decode('utf-8')
                if not msg:
                    break
                
                print(f'Mensagem recebida: {msg}')
                
                # Verifica se é mensagem privada (formato: remetente/destinatário mensagem)
                if '/' in msg:
                    # Parse da mensagem privada: remetente/destinatário mensagem
                    parts = msg.split('/', 1)
                    if len(parts) < 2:
                        continue
                        
                    src = parts[0].strip()
                    rest = parts[1].strip()
                    
                    # Separa destinatário e mensagem
                    msg_parts = rest.split(' ', 1)
                    if len(msg_parts) < 2:
                        continue
                    
                    dst = msg_parts[0].strip()
                    message = msg_parts[1].strip()
                    
                    print(f'[PRIVADO] De: {src} | Para: {dst} | Mensagem: {message}')
                    send_to_user(src, dst, message, client)
                else:
                    # Mensagem broadcast (formato: remetente mensagem)
                    msg_parts = msg.split(' ', 1)
                    if len(msg_parts) < 2:
                        continue
                    
                    src = msg_parts[0].strip()
                    message = msg_parts[1].strip()
                    
                    print(f'[BROADCAST] De: {src} | Mensagem: {message}')
                    broadcast(src, message, client)
            except Exception as e:
                print(f'Erro ao processar mensagem: {e}')
                break
    except Exception as e:
        print(f'Erro na conexão com cliente: {e}')
    finally:
        remove_client(client, username)

# Função para enviar mensagem privada para um usuário específico
def send_to_user(src, dst, msg, sender):
    if dst in username_connection.keys():
        dst_conn = username_connection[dst]
        try:
            dst_conn.send(f'[PRIVADO] <{src}>: {msg}\n'.encode('utf-8'))
            # Confirma ao remetente que a mensagem foi enviada
            sender.send(f'[Enviado para {dst}]: {msg}\n'.encode('utf-8'))
        except Exception as e:
            print(f'Erro ao enviar para {dst}: {e}')
            sender.send(f'[ERRO] Não foi possível enviar mensagem para {dst}\n'.encode('utf-8'))
    else:
        sender.send(f'[ERRO] Usuário "{dst}" não encontrado\n'.encode('utf-8'))

# Função para transmitir mensagens para todos os clientes
def broadcast(src, msg, sender):
    formatted_msg = f'[TODOS] <{src}>: {msg}\n'.encode('utf-8')
    for username, client in username_connection.items():
        if client != sender:
            try:
                client.send(formatted_msg)
            except Exception as e:
                print(f'Erro ao enviar broadcast para {username}: {e}')
    # Confirma ao remetente
    try:
        sender.send(f'[Enviado para todos]: {msg}\n'.encode('utf-8'))
    except:
        pass

# Função para transmitir mensagens do sistema para todos
def broadcast_system(msg):
    formatted_msg = f'{msg}\n'.encode('utf-8')
    for username, client in username_connection.items():
        try:
            client.send(formatted_msg)
        except Exception as e:
            print(f'Erro ao enviar mensagem do sistema para {username}: {e}')

# Função para remover um cliente da lista
def remove_client(client, username):
    try:
        if client in clients:
            clients.remove(client)
        if username and username in username_connection:
            del username_connection[username]
            print(f'Usuário desconectado: {username}')
            # Notifica todos sobre a saída
            broadcast_system(f'*** {username} saiu do chat ***')
        client.close()
    except Exception as e:
        print(f'Erro ao remover cliente: {e}')

# Função principal
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Servidor de bate-papo iniciado")
    print("Aguardando conexões na porta 7777...\n")

    try:
        server.bind(("0.0.0.0", 7777))
        server.listen()
    except Exception as e:
        return print(f'\nNão foi possível iniciar o servidor: {e}\n')

    while True:
        try:
            client, addr = server.accept()
            clients.append(client)
            print(f'Nova conexão de: {addr}')

            # Inicia uma nova thread para lidar com as mensagens do cliente
            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
        except Exception as e:
            print(f'Erro ao aceitar conexão: {e}')

# Executa o programa
main()
