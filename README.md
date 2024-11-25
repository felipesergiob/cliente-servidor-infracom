# Relatório e Manual de Utilização Projeto de Infraestrutura de Comunicação - Aplicação cliente - servidor

---

## 1. Introdução

Este projeto implementa uma aplicação cliente-servidor que simula um protocolo de transporte confiável com controle de fluxo e congestionamento. A aplicação fornece funcionalidades para envio e recepção de pacotes em um canal sujeito a perdas e erros simulados, permitindo testar diversos cenários e estratégias de recuperação.

A aplicação foi desenvolvida em Python utilizando sockets para comunicação entre cliente e servidor, com suporte a dois protocolos de controle: **Selective Repeat** e **Go-Back-N**.

## 1. Introdução
    Felipe Sergio
	Gabriel Antonio 
	Matheos Guerra
	Pedro dhalia
	Sergio Mariano
	Thiago Belo

---

## 2. Especificações Técnicas

### Objetivos

- **Conexão Cliente-Servidor:** Comunicação baseada em sockets via `localhost`.
- **Protocolo de Aplicação:** Regras definidas para requisições e respostas, incluindo:
  - Envio e recepção de pacotes com números de sequência.
  - Uso de soma de verificação para garantir integridade.
  - Suporte a ACKs e NACKs.
- **Simulação de Falhas:** Inclusão de erros e perdas de mensagens verificáveis.
- **Controle de Fluxo e Congestionamento:** Ajuste dinâmico das janelas de recepção e congestionamento.

### Funcionalidades

#### Cliente:

1. Envio de pacotes (únicos ou em lotes ou em rajadas).
2. Simulação de erros de integridade.
3. Manipulação de números de sequência.
4. Teste de timeout e retransmissão.
5. Seleção de protocolo (Selective Repeat ou Go-Back-N).

#### Servidor:

1. Recepção de pacotes com validação de integridade.
2. Envio de ACKs, NACKs e respostas com erros simulados.
3. Configuração dinâmica de janela de recepção.
4. Suporte a dois protocolos de controle.

---

## 3. Estrutura do Código

### Cliente

O cliente possui um menu interativo para realizar diversas operações, como envio de pacotes, simulação de erros e manipulação de números de sequência. As principais funções incluem:

- **`enviar_pacote`:** Envia um único pacote com número de sequência e checksum.
- **`enviar_em_rajada`:** Envia vários pacotes consecutivamente.
- **`enviar_em_lote`:** Envia um grupo de pacotes em um único lote.
- **`enviar_pacote_com_timeout`:** Testa a funcionalidade de timeout e retransmissão.
- **`enviar_pacote_com_checksum`:** Envia pacotes com checksum errado para simular erros.

### Servidor

O servidor gerencia múltiplas conexões simultâneas e processa pacotes recebidos com base no protocolo negociado. As principais funções incluem:

- **`tratar_cliente`:** Trata uma conexão individual, gerenciando pacotes e respondendo com ACKs ou NACKs.
- **`calcular_soma_verificacao`:** Gera um checksum para verificar a integridade dos dados.
- **`enviar_resposta`:** Responde ao cliente com mensagens contendo status (ACK/NACK) e informações sobre a janela de recepção.

---

## 4. Manual de Utilização

### 4.1 Configuração

1. **Pré-requisitos:**
   - Python 3.6 ou superior instalado.
   - Rede configurada para permitir comunicação via `localhost` ou IP.

2. **Execução:**
   - No terminal, execute o servidor:
     ```bash
     python servidor.py
     ```
   - Em outro terminal, execute o cliente:
     ```bash
     python cliente.py
     ```

---

### 4.2 Uso do Cliente

Ao iniciar o cliente, você verá um menu interativo. As opções disponíveis são:

1. **Enviar um pacote único:** Envia um pacote simples com número de sequência e checksum calculados.
2. **Enviar pacotes em rajada:** Envia vários pacotes consecutivamente.
3. **Simular erro de integridade:** Envia um pacote com checksum incorreto para testar a detecção de erros pelo servidor.
4. **Manipular número de sequência:** Permite enviar um pacote com número de sequência personalizado.
5. **Enviar pacote forçando NACK:** Envia um pacote propositalmente inválido para forçar uma resposta NACK do servidor.
6. **Forçar erro no ACK retornado:** Envia um pacote que força o servidor a responder com ACK incorreto.
7. **Enviar pacote que deve ser perdido:** Envia um pacote com flag para ser ignorado pelo servidor simulando assim uma perda.
8. **Enviar pacotes em lote único:** Envia múltiplos pacotes como um único grupo (modo batch).
9. **Enviar pacote com atraso proposital e sem ACK:** Testa o mecanismo de timeout com retransmissão.
10. **Sair:** Fecha a conexão com o servidor.

### 4.3 Uso do Servidor

O servidor inicia automaticamente em `127.0.0.1:50500` e espera conexões de clientes. Ele processa pacotes conforme o protocolo negociado, ajustando dinamicamente a janela de recepção e enviando ACKs ou NACKs.

---

## 5. Exemplos de Testes

### 5.1 Teste Básico de Conexão

1. Inicie o servidor.
2. Conecte o cliente e escolha o protocolo `Selective Repeat` ou `Go-Back-N`.
3. Envie um pacote único e observe a resposta do servidor.

### 5.2 Teste de Simulação de Erro

1. Escolha a opção "Simular erro de integridade".
2. Envie um pacote com checksum manual incorreto.
3. Verifique o NACK recebido pelo cliente.

### 5.3 Teste de Timeout

1. Escolha a opção "Enviar pacote com atraso proposital e sem ACK".
2. Observe a retransmissão automática após o timeout.

---

## 6. Conclusão

Este projeto demonstra os conceitos de transporte confiável em redes, oferecendo uma ferramenta prática para explorar mecanismos como controle de fluxo, janelas deslizantes e recuperação de erros. A aplicação pode ser estendida para suportar outros protocolos ou cenários específicos.
