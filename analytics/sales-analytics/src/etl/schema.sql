-- Criação da tabela de vendas
CREATE TABLE IF NOT EXISTS vendas (
    id SERIAL PRIMARY KEY,
    data_venda TIMESTAMP NOT NULL,
    valor_venda DECIMAL(10,2) NOT NULL,
    produto VARCHAR(100),
    categoria VARCHAR(50),
    vendedor VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_data_venda ON vendas(data_venda);
CREATE INDEX IF NOT EXISTS idx_categoria ON vendas(categoria);

-- View para métricas diárias
CREATE OR REPLACE VIEW vendas_diarias AS
SELECT 
    DATE(data_venda) as data,
    COUNT(*) as total_pedidos,
    SUM(valor_venda) as total_vendas,
    AVG(valor_venda) as ticket_medio
FROM vendas
GROUP BY DATE(data_venda); 