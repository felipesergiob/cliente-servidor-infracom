import socket

def iniciar_cliente(endereco='127.0.0.1', porta=50500):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((endereco, porta))
    print(f'Conectado ao servidor em {endereco}:{porta}')

    while True:
        print("\nEscolha uma opção:")
        print("1. Enviar um pacote único")
        print("2. Enviar pacotes em rajada")
        print("3. Sair")

        opcao = input("Digite o número da opção: ")

        if opcao == '1':
            conteudo = input("Digite a mensagem a ser enviada: ")
            cliente.send(conteudo.encode())
            resposta = cliente.recv(1024)
            print(f"Resposta do servidor: {resposta.decode()}")

        elif opcao == '2':
            num_pacotes = int(input("Quantos pacotes deseja preparar para a rajada? "))
            pacotes = []

            for i in range(num_pacotes):
                conteudo = input(f"Digite o conteúdo do pacote {i+1}: ")
                pacotes.append(conteudo)

            print("\nEnviando todos os pacotes...")

            for i, pacote in enumerate(pacotes):
                cliente.send(pacote.encode())
                resposta = cliente.recv(1024)
                print(f"Resposta do servidor ao pacote {i+1}: {resposta.decode()}")

        elif opcao == '3':
            break

    cliente.close()
    print("Conexão encerrada")

if __name__ == '__main__':
    iniciar_cliente()
