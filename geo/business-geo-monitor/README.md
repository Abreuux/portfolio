# Monitoramento Geográfico de Negócios

Sistema de monitoramento geográfico de negócios desenvolvido com Django e PostGIS, permitindo visualizar e analisar a distribuição espacial de estabelecimentos comerciais.

## Funcionalidades

- Visualização de negócios em mapa interativo
- Filtros por tipo de negócio, cidade e estado
- Análise de cobertura por região
- Cálculo de distâncias e áreas de atuação
- API REST para integração com outros sistemas
- Dashboard com métricas de negócios

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- PostGIS 3+
- GDAL 3+

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/business-geo-monitor.git
cd business-geo-monitor
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados PostgreSQL com PostGIS:
```sql
CREATE DATABASE business_geo;
\c business_geo
CREATE EXTENSION postgis;
```

5. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

6. Execute as migrações:
```bash
python manage.py migrate
```

7. Crie um superusuário:
```bash
python manage.py createsuperuser
```

8. Inicie o servidor:
```bash
python manage.py runserver
```

## Uso

1. Acesse o sistema em `http://localhost:8000`
2. Faça login com o superusuário criado
3. Adicione negócios através do painel administrativo
4. Visualize os negócios no mapa interativo
5. Use os filtros para analisar dados específicos

## API

O sistema disponibiliza uma API REST com os seguintes endpoints:

- `GET /api/businesses/` - Lista todos os negócios
- `POST /api/businesses/` - Cria um novo negócio
- `GET /api/businesses/{id}/` - Obtém detalhes de um negócio
- `PUT /api/businesses/{id}/` - Atualiza um negócio
- `DELETE /api/businesses/{id}/` - Remove um negócio

Endpoints adicionais:

- `GET /api/businesses/nearby/` - Busca negócios próximos a um ponto
- `GET /api/businesses/coverage_analysis/` - Análise de cobertura por região

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 