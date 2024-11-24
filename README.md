# Checklist de Implementação - Aplicação Cliente-Servidor

### Cliente
- [x] Ajustar dinamicamente a janela de recepção com base nos valores informados pelo servidor.

### Servidor
- [x] Marcar pacotes que não serão confirmados.
- [x] Inserir erros de integridade nas confirmações enviadas (ex.: NACK com checksum inválido).
- [ ] Implementar confirmação em lote.
- [ ] Antes da confirmação de chegada por pacotes por parte do servidor, deve ser
possível marcar pacotes perdidos.

### Relatório e Manual:
- [ ] Desenvolver documentação para explicar como usar o sistema, incluindo exemplos.