# Checklist de Implementação - Aplicação Cliente-Servidor

## Cliente
- [x] Conectar ao servidor via localhost ou IP (usando sockets).
- [x] Implementar envio de pacotes isolados e em rajada.
- [x] Simular erros de integridade em pacotes específicos.
- [ ] Atualizar dinamicamente a janela de recepção do servidor.
- [ ] Implementar atualização da janela de congestionamento com base em perdas de pacotes e confirmações duplicadas.
- [x] Simular perdas de pacotes antes da confirmação de chegada pelo servidor.

## Servidor
- [x] Configurar recepção de pacotes individuais ou em grupo.
- [x] Marcar pacotes não confirmados com `NACK`.
- [x] Incluir erros de integridade nas confirmações enviadas ao cliente (`NACK`).
- [x] Implementar confirmações negativas.
- [ ] Implementar controle e negociação de repetição seletiva ou Go-Back-N com o cliente.
- [ ] Informar e atualizar dinamicamente a janela de recepção ao cliente.

## Transporte Confiável de Dados
- [x] Implementar soma de verificação.
- [x] Implementar temporizador.
- [x] Implementar número de sequência.
- [x] Implementar reconhecimento (ACK) e reconhecimento negativo (NACK).
- [x] Implementar janela e paralelismo (uso de multithreading no servidor).

## Pontuação Extra
- [x] Implementar método de checagem de integridade (0,5 pontos adicionais).
