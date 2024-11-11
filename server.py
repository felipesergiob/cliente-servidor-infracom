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
    sequencia_esperada = 0
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
            if seq_num == sequencia_esperada and checksum_recebido == checksum_calculado:
                sequencia_esperada += 1
                resposta = f"ACK:{seq_num}".encode()
            else:
                resposta = f"NACK:{sequencia_esperada}".encode()
        except ValueError:
            resposta = f"NACK:{sequencia_esperada}".encode()
        
        conexao.send(resposta)
    conexao.close()
    print(f"Conexão com o cliente encerrada.")

if __name__ == '__main__':
    iniciar_servidor()
