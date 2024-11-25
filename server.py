import socket
import threading

def iniciar_servidor(endereco='127.0.0.1', porta=50500):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((endereco, porta))
    servidor.listen()
    print(f"Servidor iniciado em {endereco}:{porta}")
    while True:
        conexao, cliente = servidor.accept()
        print(f"Conexão aceita de {cliente}")
        threading.Thread(target=tratar_cliente, args=(conexao,)).start()

def calcular_soma_verificacao(dados):
    checksum = sum(ord(c) for c in dados) % 256
    return str(checksum)

def tratar_cliente(conexao):
    protocolo = conexao.recv(1024).decode().strip()
    if protocolo not in ["Selective Repeat", "Go-Back-N"]:
        conexao.send("ERRO".encode())
        conexao.close()
        return
    conexao.send("OK".encode())
    print(f"Protocolo negociado: {protocolo}")
    print("-------------------------------------")

    sequencia_esperada = 0
    janela_recepcao = 5
    pacotes_recebidos = {}

    while True:
        mensagem = conexao.recv(1024)
        if not mensagem:
            break
        texto = mensagem.decode()
        print(f"Mensagem recebida: {texto}")

        if texto.startswith("FLAG_ERRO_ACK"):
            _, conteudo = texto.split(":", 1)
            resposta = f"ACK:{sequencia_esperada}:[{sequencia_esperada}-{sequencia_esperada + janela_recepcao - 1}]"
            checksum_incorreto = "000"
            print(f"Enviando ACK com checksum incorreto para o conteúdo: '{conteudo}'")
            conexao.send(f"{resposta}:{checksum_incorreto}".encode())
            continue

        if texto.startswith("FLAG_IGNORAR"):
            _, conteudo = texto.split(":", 1)
            print(f"Mensagem com flag para ignorar recebida. Conteúdo: '{conteudo}'. Ignorando.")
            continue

        if texto.startswith("FLAG_NO_ACK"):
            _, seq_num, checksum, conteudo = texto.split(":")
            print(f"Recebido pacote sem enviar ACK. Número de sequência: {seq_num}")
            continue

        if texto.startswith("LOTE"):
            _, seq_inicial, pacotes = texto.split(":", 2)
            seq_inicial = int(seq_inicial)
            pacotes = pacotes.split(",")
            erro = False

            for i, pacote in enumerate(pacotes):
                checksum_recebido, conteudo = pacote.split(":", 1)
                checksum_calculado = calcular_soma_verificacao(conteudo)
                if checksum_recebido != checksum_calculado:
                    erro = True
                    break

            if erro:
                resposta = f"NACK:{sequencia_esperada}:[{sequencia_esperada}-{sequencia_esperada + janela_recepcao - 1}]"
            else:
                sequencia_esperada += len(pacotes)
                resposta = f"ACK:{seq_inicial}:[{sequencia_esperada}-{sequencia_esperada + janela_recepcao - 1}]"

            checksum_resposta = calcular_soma_verificacao(resposta)
            print(f"Enviando {resposta.split(':')[0]}: {resposta} com checksum: {checksum_resposta}")
            conexao.send(f"{resposta}:{checksum_resposta}".encode())
            continue

        try:
            seq_num, checksum_recebido, dados = texto.split(":")
            seq_num = int(seq_num)
            checksum_calculado = calcular_soma_verificacao(dados)

            if checksum_recebido != checksum_calculado:
                resposta = f"NACK:{sequencia_esperada}:[{sequencia_esperada}-{sequencia_esperada + janela_recepcao - 1}]"
                checksum_resposta = calcular_soma_verificacao(resposta)
                print(f"Enviando NACK devido a erro de integridade: {resposta} com checksum: {checksum_resposta}")
                conexao.send(f"{resposta}:{checksum_resposta}".encode())
                continue

            if protocolo == "Go-Back-N":
                if seq_num == sequencia_esperada:
                    resposta = f"ACK:{seq_num}:[{sequencia_esperada + 1}-{sequencia_esperada + janela_recepcao}]"
                    sequencia_esperada += 1
                else:
                    resposta = f"NACK:{sequencia_esperada}:[{sequencia_esperada}-{sequencia_esperada + janela_recepcao - 1}]"
            elif protocolo == "Selective Repeat":
                if seq_num == sequencia_esperada:
                    sequencia_esperada += 1
                    while sequencia_esperada in pacotes_recebidos:
                        sequencia_esperada += 1
                    resposta = f"ACK:{seq_num}:[{sequencia_esperada}-{sequencia_esperada + janela_recepcao - 1}]"
                else:
                    pacotes_recebidos[seq_num] = dados
                    resposta = f"ACK:{seq_num}:[{sequencia_esperada}-{sequencia_esperada + janela_recepcao - 1}]"

            checksum_resposta = calcular_soma_verificacao(resposta)
            print(f"Enviando {resposta.split(':')[0]}: {resposta} com checksum: {checksum_resposta}")
            conexao.send(f"{resposta}:{checksum_resposta}".encode())

        except ValueError:
            resposta = f"NACK:{sequencia_esperada}:[{sequencia_esperada}-{sequencia_esperada + janela_recepcao - 1}]"
            checksum_resposta = calcular_soma_verificacao(resposta)
            print(f"Enviando NACK devido a erro de formato: {resposta} com checksum: {checksum_resposta}")
            conexao.send(f"{resposta}:{checksum_resposta}".encode())

    conexao.close()
    print("Conexão encerrada.")

if __name__ == '__main__':
    iniciar_servidor()