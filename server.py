import socket
import threading
import hashlib

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
    checksum = hashlib.md5(dados.encode()).hexdigest()
    return checksum

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

        try:
            seq_num, checksum_recebido, dados = texto.split(":")
            seq_num = int(seq_num)
            checksum_calculado = calcular_soma_verificacao(dados)

            if seq_num < sequencia_esperada or seq_num >= sequencia_esperada + janela_recepcao:
                resposta = f"NACK:{sequencia_esperada}:[{sequencia_esperada}-{sequencia_esperada + janela_recepcao - 1}]".encode()
                conexao.send(resposta)
                continue

            if checksum_recebido != checksum_calculado:
                resposta = f"NACK:{seq_num}:[{sequencia_esperada}-{sequencia_esperada + janela_recepcao - 1}]".encode()
                conexao.send(resposta)
                continue

            if protocolo == "Go-Back-N":
                if seq_num == sequencia_esperada:
                    sequencia_esperada += 1
                    resposta = f"ACK:{seq_num}:[{sequencia_esperada}-{sequencia_esperada + janela_recepcao - 1}]".encode()
                else:
                    resposta = f"NACK:{sequencia_esperada}:[{sequencia_esperada}-{sequencia_esperada + janela_recepcao - 1}]".encode()

            elif protocolo == "Selective Repeat":
                if seq_num == sequencia_esperada:
                    sequencia_esperada += 1
                    while sequencia_esperada in pacotes_recebidos:
                        sequencia_esperada += 1
                    resposta = f"ACK:{seq_num}:[{sequencia_esperada}-{sequencia_esperada + janela_recepcao - 1}]".encode()
                else:
                    pacotes_recebidos[seq_num] = dados
                    resposta = f"ACK:{seq_num}:[{sequencia_esperada}-{sequencia_esperada + janela_recepcao - 1}]".encode()

            conexao.send(resposta)

        except ValueError:
            resposta = f"NACK:{sequencia_esperada}:[{sequencia_esperada}-{sequencia_esperada + janela_recepcao - 1}]".encode()
            conexao.send(resposta)

    conexao.close()
    print("Conexão encerrada.")

if __name__ == '__main__':
    iniciar_servidor()
