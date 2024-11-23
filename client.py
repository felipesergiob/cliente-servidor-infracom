import socket
import hashlib

def iniciar_cliente(endereco='127.0.0.1', porta=50500):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((endereco, porta))
    numero_sequencia = 0
    janela_congestionamento = 1

    protocolo = input("Escolha o protocolo (Selective Repeat / Go-Back-N): ").strip()
    cliente.send(protocolo.encode())
    resposta = cliente.recv(1024).decode()
    if resposta != "OK":
        print("Negociação falhou. Encerrando conexão.")
        cliente.close()
        return
    print(f"Protocolo negociado: {protocolo}")
    print("----------------------")

    while True:
        print("Escolha uma opção:")
        print("1. Enviar um pacote único")
        print("2. Enviar pacotes em rajada")
        print("3. Simular erro de integridade")
        print("4. Manipular número de sequência")
        print("5. Sair")
        opcao = input("Digite o número da opção: ")

        if opcao == '1':
            conteudo = input("Digite o conteúdo para o pacote: ")
            numero_sequencia, janela_congestionamento = enviar_pacote(
                cliente, numero_sequencia, conteudo, janela_congestionamento
            )

        elif opcao == '2':
            num_pacotes = int(input("Quantos pacotes deseja enviar em rajada? "))
            conteudos = []
            for i in range(num_pacotes):
                conteudo = input(f"Digite o conteúdo para o pacote {i + 1}: ")
                conteudos.append(conteudo)
            numero_sequencia, janela_congestionamento = enviar_em_rajada(
                cliente, conteudos, numero_sequencia, janela_congestionamento
            )

        elif opcao == '3':
            checksum_errado = input("Digite o checksum manualmente para simular erro: ")
            conteudo = input("Digite o conteúdo para o pacote: ")
            numero_sequencia, janela_congestionamento = enviar_pacote_com_checksum(
                cliente, numero_sequencia, conteudo, checksum_errado, janela_congestionamento
            )

        elif opcao == '4':
            seq_num_manipulado = int(input("Informe o número de sequência que deseja enviar: "))
            conteudo = input("Digite o conteúdo para o pacote: ")
            enviar_pacote(cliente, seq_num_manipulado, conteudo, janela_congestionamento)

        elif opcao == '5':
            break

        print("----------------------")

    cliente.close()

def calcular_soma_verificacao(dados):
    checksum = hashlib.md5(dados.encode()).hexdigest()
    return checksum

def enviar_pacote(cliente, seq_num, conteudo, janela_congestionamento):
    checksum = calcular_soma_verificacao(conteudo)
    mensagem = f"{seq_num}:{checksum}:{conteudo}".encode()
    print(f"Enviando pacote: {mensagem.decode()}")
    cliente.send(mensagem)
    resposta = cliente.recv(1024).decode()
    print(f"Resposta do servidor: {resposta}")
    seq_num, janela_congestionamento = processar_resposta(resposta, seq_num, janela_congestionamento)
    return seq_num, janela_congestionamento

def enviar_pacote_com_checksum(cliente, seq_num, conteudo, checksum_errado, janela_congestionamento):
    mensagem = f"{seq_num}:{checksum_errado}:{conteudo}".encode()
    print(f"Enviando pacote com erro de integridade: {mensagem.decode()}")
    cliente.send(mensagem)
    resposta = cliente.recv(1024).decode()
    print(f"Resposta do servidor: {resposta}")
    seq_num, janela_congestionamento = processar_resposta(resposta, seq_num, janela_congestionamento, atualizar_sequencia=False)
    return seq_num, janela_congestionamento

def enviar_em_rajada(cliente, conteudos, seq_num, janela_congestionamento):
    pacotes_enviados = 0
    pacotes_rejeitados = []

    while pacotes_enviados < len(conteudos):
        pacotes_para_enviar = min(janela_congestionamento, len(conteudos) - pacotes_enviados)

        for i in range(pacotes_para_enviar):
            conteudo = conteudos[pacotes_enviados]
            checksum = calcular_soma_verificacao(conteudo)
            mensagem = f"{seq_num}:{checksum}:{conteudo}".encode()
            print(f"Enviando pacote: {mensagem.decode()}")
            cliente.send(mensagem)
            resposta = cliente.recv(1024).decode()
            print(f"Resposta do servidor: {resposta}")
            seq_num, janela_congestionamento = processar_resposta(resposta, seq_num, janela_congestionamento)
            pacotes_enviados += 1

        if pacotes_enviados < len(conteudos):
            pacotes_rejeitados = conteudos[pacotes_enviados:]
            print(f"Rede congestionada. Pacotes rejeitados: {len(pacotes_rejeitados)} ({pacotes_rejeitados})")
            break

    return seq_num, janela_congestionamento

def processar_resposta(resposta, seq_num, janela_congestionamento, atualizar_sequencia=True):
    try:
        ack, recebido, _ = resposta.split(":")
        recebido = int(recebido)

        if ack == "ACK":
            if atualizar_sequencia:
                seq_num = recebido + 1
            janela_congestionamento += 1
            print(f"Janela de Congestionamento Atualizada: {janela_congestionamento} (ACK recebido)")
        elif ack == "NACK":
            print(f"NACK recebido para o número de sequência {seq_num}.")
            janela_congestionamento = max(1, janela_congestionamento // 2)
            print(f"Janela de Congestionamento Reduzida: {janela_congestionamento} (NACK recebido)")
    except ValueError:
        print("Erro ao processar a resposta do servidor.")
    return seq_num, janela_congestionamento

if __name__ == '__main__':
    iniciar_cliente()
