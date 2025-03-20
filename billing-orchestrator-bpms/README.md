# Orquestrador de Faturamento SaaS

Sistema de orquestração de faturamento SaaS desenvolvido com Spring Boot e Camunda, integrando Stripe e Protheus para gerenciamento de assinaturas e pagamentos.

## Funcionalidades

- Gerenciamento de assinaturas
- Integração com Stripe para pagamentos
- Integração com Protheus para faturamento
- Processo de faturamento automatizado
- Notificações automáticas
- Monitoramento de status de pagamentos
- Gestão de cancelamentos e atualizações

## Requisitos

- Java 17+
- Maven 3.8+
- PostgreSQL 12+
- Camunda Platform 8.3+
- Stripe API Key
- Protheus API Key

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/billing-orchestrator.git
cd billing-orchestrator
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

3. Configure o banco de dados:
```sql
CREATE DATABASE billing_orchestrator;
```

4. Compile o projeto:
```bash
mvn clean package
```

5. Execute o projeto:
```bash
java -jar target/billing-orchestrator-1.0.0.jar
```

## Configuração

### Variáveis de Ambiente

- `STRIPE_SECRET_KEY`: Chave secreta da API do Stripe
- `STRIPE_WEBHOOK_SECRET`: Chave secreta para webhooks do Stripe
- `PROTHEUS_BASE_URL`: URL base da API do Protheus
- `PROTHEUS_API_KEY`: Chave de API do Protheus

### Camunda

O sistema utiliza o Camunda Platform 8.3 com Zeebe para orquestração. Certifique-se de que o broker Zeebe está em execução e acessível na porta 26500.

## API

### Endpoints

#### Assinaturas

- `POST /api/subscriptions` - Criar nova assinatura
- `GET /api/subscriptions/{id}` - Obter detalhes da assinatura
- `PUT /api/subscriptions/{id}` - Atualizar assinatura
- `DELETE /api/subscriptions/{id}` - Cancelar assinatura

#### Faturas

- `GET /api/invoices` - Listar faturas
- `GET /api/invoices/{id}` - Obter detalhes da fatura
- `POST /api/invoices/{id}/retry` - Tentar novamente o pagamento

#### Webhooks

- `POST /api/webhooks/stripe` - Webhook para eventos do Stripe
- `POST /api/webhooks/protheus` - Webhook para eventos do Protheus

## Processo de Faturamento

O sistema implementa um processo BPMN para orquestrar o faturamento:

1. Validação da Assinatura
2. Verificação de Status
3. Criação de Fatura
4. Processamento de Pagamento
5. Notificação ao Cliente
6. Atualização de Status

## Monitoramento

O sistema utiliza o Camunda Operate para monitoramento de processos e o Camunda Optimize para análise de performance.

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 