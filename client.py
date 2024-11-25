import socket
import time

def iniciar_cliente(endereco='127.0.0.1', porta=50500):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((endereco, porta))
    numero_sequencia = 0
    janela_congestionamento = 1
    janela_recepcao = (0, 0)

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
        print("5. Enviar pacote forçando NACK")
        print("6. Forçar erro no ACK retornado")
        print("7. Enviar pacote que deve ser perdido")
        print("8. Enviar pacotes em lote único")
        print("9. Enviar pacote com atraso proposital e sem ACK (testar timeout)")
        print("10. Sair")
        opcao = input("Digite o número da opção: ")

        if opcao == '1':
            conteudo = input("Digite o conteúdo para o pacote: ")
            numero_sequencia, janela_congestionamento, janela_recepcao = enviar_pacote(
                cliente, numero_sequencia, conteudo, janela_congestionamento, janela_recepcao
            )

        elif opcao == '2':
            num_pacotes = int(input("Quantos pacotes deseja enviar em rajada? "))
            conteudos = []
            for i in range(num_pacotes):
                conteudo = input(f"Digite o conteúdo para o pacote {i + 1}: ")
                conteudos.append(conteudo)
            numero_sequencia, janela_congestionamento, janela_recepcao = enviar_em_rajada(
                cliente, conteudos, numero_sequencia, janela_congestionamento, janela_recepcao
            )

        elif opcao == '3':
            checksum_errado = input("Digite o checksum manualmente para simular erro: ")
            conteudo = input("Digite o conteúdo para o pacote: ")
            numero_sequencia, janela_congestionamento, janela_recepcao = enviar_pacote_com_checksum(
                cliente, numero_sequencia, conteudo, checksum_errado, janela_congestionamento, janela_recepcao
            )

        elif opcao == '4':
            seq_num_manipulado = int(input("Informe o número de sequência que deseja enviar: "))
            if seq_num_manipulado < janela_recepcao[0] or seq_num_manipulado >= janela_recepcao[1]:
                print(f"Erro: Número de sequência {seq_num_manipulado} fora da janela de recepção ({janela_recepcao[0]}-{janela_recepcao[1] - 1}).")
            else:
                conteudo = input("Digite o conteúdo para o pacote: ")
                enviar_pacote(cliente, seq_num_manipulado, conteudo, janela_congestionamento, janela_recepcao)

        elif opcao == '5':
            conteudo = input("Digite o conteúdo para o pacote que causará NACK: ")
            numero_sequencia, janela_congestionamento, janela_recepcao = enviar_pacote_forcando_nack(
                cliente, numero_sequencia, conteudo, janela_congestionamento, janela_recepcao
            )

        elif opcao == '6':
            forcar_erro_no_ack_nack(cliente)

        elif opcao == '7':
            enviar_pacote_para_ignorar(cliente)

        elif opcao == '8':
            num_pacotes = int(input("Quantos pacotes deseja enviar no lote? "))
            conteudos = []
            for i in range(num_pacotes):
                conteudo = input(f"Digite o conteúdo para o pacote {i + 1}: ")
                conteudos.append(conteudo)
            numero_sequencia, janela_congestionamento, janela_recepcao = enviar_em_lote(
                cliente, conteudos, numero_sequencia, janela_congestionamento, janela_recepcao
            )

        elif opcao == '9':
            conteudo = input("Digite o conteúdo para o pacote: ")
            numero_sequencia = enviar_pacote_com_timeout(cliente, numero_sequencia, conteudo)

        elif opcao == '10':
            break

        print("----------------------")

    cliente.close()

def calcular_soma_verificacao(dados):
    checksum = sum(ord(c) for c in dados) % 256
    return str(checksum)

def enviar_pacote(cliente, seq_num, conteudo, janela_congestionamento, janela_recepcao):
    checksum = calcular_soma_verificacao(conteudo)
    mensagem = f"{seq_num}:{checksum}:{conteudo}".encode()
    print(f"Enviando pacote: {mensagem.decode()}")
    cliente.send(mensagem)
    resposta = cliente.recv(1024).decode()
    print(f"Resposta do servidor: {resposta}")
    seq_num, janela_congestionamento, janela_recepcao = processar_resposta(
        resposta, seq_num, janela_congestionamento, janela_recepcao
    )
    return seq_num, janela_congestionamento, janela_recepcao

def enviar_pacote_com_checksum(cliente, seq_num, conteudo, checksum_errado, janela_congestionamento, janela_recepcao):
    mensagem = f"{seq_num}:{checksum_errado}:{conteudo}".encode()
    print(f"Enviando pacote com erro de integridade: {mensagem.decode()}")
    cliente.send(mensagem)
    resposta = cliente.recv(1024).decode()
    print(f"Resposta do servidor: {resposta}")
    seq_num, janela_congestionamento, janela_recepcao = processar_resposta(resposta, seq_num, janela_congestionamento, janela_recepcao, atualizar_sequencia=False)
    return seq_num, janela_congestionamento, janela_recepcao

def enviar_pacote_forcando_nack(cliente, seq_num, conteudo, janela_congestionamento, janela_recepcao):
    checksum_errado = "000"
    mensagem = f"{seq_num}:{checksum_errado}:{conteudo}".encode()
    print(f"Enviando pacote para forçar NACK: {mensagem.decode()}")
    cliente.send(mensagem)
    resposta = cliente.recv(1024).decode()
    print(f"Resposta do servidor: {resposta}")
    seq_num, janela_congestionamento, janela_recepcao = processar_resposta(resposta, seq_num, janela_congestionamento, janela_recepcao, atualizar_sequencia=False)
    return seq_num, janela_congestionamento, janela_recepcao

def enviar_pacote_com_timeout(cliente, seq_num, conteudo, timeout=15):
    checksum = calcular_soma_verificacao(conteudo)
    mensagem = f"FLAG_NO_ACK:{seq_num}:{checksum}:{conteudo}".encode()
    print(f"Enviando pacote sem ACK esperado: {mensagem.decode()}")
    cliente.send(mensagem)

    inicio = time.time()
    while True:
        print("Aguardando resposta do servidor...", end="\r", flush=True)
        try:
            cliente.settimeout(1)
            resposta = cliente.recv(1024).decode()
            print("\nResposta recebida do servidor.")
            print(f"Resposta do servidor: {resposta}")
            return seq_num + 1
        except socket.timeout:
            if time.time() - inicio >= timeout:
                print("\nTimeout atingido. Retransmitindo pacote...")
                print("Retransmitindo...")
                return enviar_pacote(cliente, seq_num, conteudo, 1, (0, 0))

def enviar_em_rajada(cliente, conteudos, seq_num, janela_congestionamento, janela_recepcao):
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
            seq_num, janela_congestionamento, janela_recepcao = processar_resposta(
                resposta, seq_num, janela_congestionamento, janela_recepcao
            )
            pacotes_enviados += 1

        if pacotes_enviados < len(conteudos):
            pacotes_rejeitados = conteudos[pacotes_enviados:]
            print(f"Rede congestionada. Pacotes rejeitados: {len(pacotes_rejeitados)} ({pacotes_rejeitados})")
            break

    return seq_num, janela_congestionamento, janela_recepcao

def processar_resposta(resposta, seq_num, janela_congestionamento, janela_recepcao, atualizar_sequencia=True):
    try:
        conteudo_resposta, checksum_recebido = resposta.rsplit(":", 1)
        checksum_calculado = calcular_soma_verificacao(conteudo_resposta)

        if checksum_recebido != checksum_calculado:
            print(f"Erro de integridade no ACK/NACK. Checksum esperado: {checksum_calculado}, recebido: {checksum_recebido}")
            return seq_num, janela_congestionamento, janela_recepcao

        ack, recebido, janela_info = conteudo_resposta.split(":")
        recebido = int(recebido)
        janela_inicio, janela_fim = map(int, janela_info.strip("[]").split("-"))

        janela_recepcao = (janela_inicio, janela_fim + 1)

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
    return seq_num, janela_congestionamento, janela_recepcao

def forcar_erro_no_ack_nack(cliente):
    flag_erro_ack = "FLAG_ERRO_ACK"
    conteudo = input("Digite o conteúdo para enviar junto com a flag de erro no ACK/NACK: ")
    mensagem = f"{flag_erro_ack}:{conteudo}"
    print(f"Enviando mensagem para forçar erro no ACK: {mensagem}")
    cliente.send(mensagem.encode())
    resposta = cliente.recv(1024).decode()
    print(f"Resposta do servidor (com erro forçado): {resposta}")

def enviar_pacote_para_ignorar(cliente):
    flag_ignorar = "FLAG_IGNORAR"
    conteudo = input("Digite o conteúdo para o pacote que será ignorado pelo servidor: ")
    mensagem = f"{flag_ignorar}:{conteudo}"
    print(f"Enviando mensagem com flag para ser ignorada: {mensagem}")
    cliente.send(mensagem.encode())
    print("Mensagem enviada. Não haverá resposta do servidor para esta mensagem.")

def enviar_em_lote(cliente, conteudos, seq_num, janela_congestionamento, janela_recepcao):
    flag_lote = "LOTE"
    pacotes_enviados = 0
    pacotes_rejeitados = []

    while pacotes_enviados < len(conteudos):
        pacotes_para_enviar = min(janela_congestionamento, len(conteudos) - pacotes_enviados)
        lote = conteudos[pacotes_enviados:pacotes_enviados + pacotes_para_enviar]
        mensagem = f"{flag_lote}:{seq_num}:" + ",".join(f"{calcular_soma_verificacao(c)}:{c}" for c in lote)
        print(f"Enviando lote de pacotes: {mensagem}")
        cliente.send(mensagem.encode())
        resposta = cliente.recv(1024).decode()
        print(f"Resposta do servidor: {resposta}")

        pacotes_enviados += pacotes_para_enviar
        seq_num += pacotes_para_enviar

        seq_num, janela_congestionamento, janela_recepcao = processar_resposta(
            resposta, seq_num - 1, janela_congestionamento, janela_recepcao
        )

        if pacotes_enviados < len(conteudos):
            pacotes_rejeitados = conteudos[pacotes_enviados:]
            print(f"Rede congestionada. Pacotes rejeitados: {len(pacotes_rejeitados)} ({pacotes_rejeitados})")
            break

    return seq_num, janela_congestionamento, janela_recepcao


if __name__ == '__main__':
    iniciar_cliente()
