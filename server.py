import socket

def iniciar_servidor(endereco='127.0.0.1', porta=50500):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((endereco, porta))
    servidor.listen()
    print(f'Servidor iniciado em {endereco}:{porta}')

    while True:
        conexao, cliente = servidor.accept()
        print(f'Conexão estabelecida com {cliente}')
        tratar_cliente(conexao)

def tratar_cliente(conexao):
    while True:
        mensagem = conexao.recv(1024)
        if not mensagem:
            break
        texto = mensagem.decode()
        print(f'Dados recebidos: {texto}')
        resposta = 'ACK'.encode()
        conexao.send(resposta)

    conexao.close()
    print('Conexão encerrada')

if __name__ == '__main__':
    iniciar_servidor()
