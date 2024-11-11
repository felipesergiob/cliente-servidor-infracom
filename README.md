# Checklist de Implementação - Aplicação Cliente-Servidor

### Cliente
- [x] Conectar ao servidor via localhost ou IP usando sockets.
- [x] Enviar pacotes isolados e em rajada.
- [x] Simular erros de integridade em pacotes específicos.
- [x] Simular perdas de pacotes antes da confirmação de chegada pelo servidor.
- [ ] Atualizar dinamicamente a janela de recepção do servidor.
- [ ] Atualizar a janela de congestionamento com base em perdas de pacotes e confirmações duplicadas.

### Servidor
- [x] Receber pacotes individuais ou em grupo.
- [x] Marcar pacotes não confirmados com `NACK`.
- [x] Validar integridade dos pacotes e enviar `NACK` em caso de erro.
- [x] Implementar confirmações negativas (NACK) para pacotes fora de ordem ou corrompidos.
- [ ] Implementar controle e negociação de repetição seletiva ou Go-Back-N com o cliente.
- [ ] Informar e atualizar dinamicamente a janela de recepção ao cliente.

### Transporte Confiável de Dados
- [x] Implementar soma de verificação para garantir a integridade dos dados.
- [x] Implementar número de sequência para controle de ordem de pacotes.
- [x] Implementar reconhecimento (ACK) e reconhecimento negativo (NACK) para controle de entrega.
- [x] Implementar janela e paralelismo usando multithreading no servidor.
- [ ] Implementar temporizador para gerenciamento de tempo limite de confirmação e retransmissão.

## Pontuação Extra
- [x] Implementar método de checagem de integridade (0,5 pontos adicionais).
