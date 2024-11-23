# Checklist de Implementação - Aplicação Cliente-Servidor

### Cliente
- [ ] Ajustar dinamicamente a janela de recepção com base nos valores informados pelo servidor.

### Servidor
- [ ] Marcar pacotes que não serão confirmados.
- [ ] Inserir erros de integridade nas confirmações enviadas (ex.: NACK com checksum inválido).
- [ ] Implementar confirmação em lote (opcional, se o grupo decidir por isso).
- [ ] Antes da confirmação de chegada por pacotes por parte do servidor, deve ser
possível marcar pacotes perdidos;
- [ ] Temporizador;

### Relatório e Manual:
- [ ] Desenvolver documentação para explicar como usar o sistema, incluindo exemplos.