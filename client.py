import socket

def iniciar_cliente(endereco='127.0.0.1', porta=50500):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((endereco, porta))
    print(f'Conectado ao servidor em {endereco}:{porta}')

    while True:
        conteudo = input("Digite uma mensagem (ou 'sair' para encerrar): ")
        if conteudo.lower() == 'sair':
            break
        cliente.send(conteudo.encode())
        resposta = cliente.recv(1024)
        print(f'Resposta do servidor: {resposta.decode()}')

    cliente.close()
    print("Conexão encerrada")

if __name__ == '__main__':
    iniciar_cliente()
