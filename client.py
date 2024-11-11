import socket
import hashlib

def iniciar_cliente(endereco='127.0.0.1', porta=50500):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((endereco, porta))
    numero_sequencia = 0

    while True:
        print("\nEscolha uma opção:")
        print("1. Enviar um pacote único")
        print("2. Enviar pacotes em rajada")
        print("3. Simular erro de integridade")
        print("4. Simular perda de pacote")
        print("5. Sair")
        opcao = input("Digite o número da opção: ")

        if opcao == '1':
            conteudo = input("Digite a mensagem a ser enviada: ")
            enviar_pacote(cliente, numero_sequencia, conteudo)
            numero_sequencia += 1

        elif opcao == '2':
            num_pacotes = int(input("Quantos pacotes deseja enviar em rajada? "))
            conteudos = []
            for i in range(num_pacotes):
                conteudo = input(f"Digite o conteúdo para o pacote {i + 1}: ")
                conteudos.append(conteudo)
            
            for conteudo in conteudos:
                enviar_pacote(cliente, numero_sequencia, conteudo)
                numero_sequencia += 1

        elif opcao == '3':
            seq_num_erro = int(input("Informe o número de sequência para simular erro: "))
            conteudo = "Erro proposital"
            enviar_pacote(cliente, seq_num_erro, conteudo, erro=True)

        elif opcao == '4':
            print("Simulando perda de pacote...")
            numero_sequencia += 1

        elif opcao == '5':
            break

    cliente.close()

def calcular_soma_verificacao(dados):
    checksum = hashlib.md5(dados.encode()).hexdigest()
    return checksum

def enviar_pacote(cliente, seq_num, conteudo, erro=False):
    checksum = calcular_soma_verificacao(conteudo) if not erro else "00000000000000000000000000000000"
    mensagem = f"{seq_num}:{checksum}:{conteudo}".encode()
    cliente.send(mensagem)
    resposta = cliente.recv(1024)
    print(f"Resposta do servidor: {resposta.decode()}")

if __name__ == '__main__':
    iniciar_cliente()
