## Checklist de Implementação

1. **Conexão Cliente-Servidor**
   - [x] O cliente pode se conectar ao servidor via localhost ou IP.
   - [x] A comunicação ocorre via sockets (TCP).

2. **Envio de Pacotes**
   - [ ] O cliente pode enviar pacotes únicos para o servidor.
   - [ ] O cliente pode enviar pacotes em rajadas para o servidor.
   - [ ] O cliente pode marcar pacotes específicos para simular erros de integridade.

3. **Recepção e Confirmação**
   - [ ] O servidor pode processar pacotes recebidos individualmente.
   - [ ] O servidor pode confirmar a recepção de pacotes com ACK.
   - [ ] O servidor pode enviar confirmações negativas (NACK) quando erros de integridade são detectados.
   - [ ] O servidor pode ser configurado para confirmar pacotes individualmente ou em grupo (rajada).

4. **Simulação de Erros e Perdas**
   - [ ] O cliente pode simular perdas de pacotes antes da confirmação de chegada.
   - [ ] O cliente pode inserir erros de integridade nos pacotes enviados.
   - [ ] O servidor pode simular erros nas confirmações enviadas ao cliente.

5. **Controle de Fluxo e Congestionamento**
   - [ ] O cliente pode ajustar dinamicamente a janela de recepção com base nas respostas do servidor.
   - [ ] O servidor atualiza dinamicamente sua janela de recepção.
   - [ ] O servidor ajusta a janela de congestionamento com base em perdas de pacotes e confirmações duplicadas.

6. **Protocolos de Repetição**
   - [ ] O cliente e o servidor podem negociar o uso de repetição seletiva (Selective Repeat).
   - [ ] O cliente e o servidor podem negociar o uso do Go-Back-N.

7. **Soma de Verificação e Temporizador**
   - [ ] O cliente calcula e envia a soma de verificação junto com os pacotes.
   - [ ] O servidor valida a soma de verificação para detectar erros de integridade.
   - [ ] O cliente implementa um temporizador para retransmissão de pacotes após um timeout.

### Extras para Pontuação Adicional
- [ ] Implementar um método de checagem de integridade adicional para garantir 0,5 pontos extras.
