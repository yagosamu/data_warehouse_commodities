"""
# Projeto de Data Warehouse de Commodities

Quanto sua empresa vendeu ontem?
Se você demorar mais de 3 segundos para responder esse workshop de hoje é para você!

## 🎯 Objetivo
Este projeto tem como objetivo criar um Data Warehouse (DW) para armazenar e analisar dados de commodities, 
utilizando uma arquitetura moderna de ETL (Extract, Transform, Load).

## 🔗 Links Úteis
- Documentação do DBT: https://lvgalvao.github.io/workshop-aberto-dw-do-zero/#!/overview
- Dashboard: https://lvgalvao-workshop-aberto-dw-do-zero-appapp-vp0gw4.streamlit.app/

## 🏗️ Arquitetura do Projeto

### 1. Extract_Load (app/)
Responsável por extrair dados de uma API e carregar diretamente no banco de dados PostgreSQL.
- Script: extract_load.py
- Função: Busca dados de commodities via API e carrega no banco

### 2. Transform (datawarehouse/)
Utiliza DBT para transformações de dados:
- Models de staging: Limpeza e padronização dos dados
- Models de datamart: Criação de métricas agregadas e tabelas analíticas
- Seeds: Carregamento de dados CSV de movimentações de commodities

### 3. Dashboard (Streamlit)
Interface visual para análise dos dados:
- Visualizações interativas
- Tabelas de dados das commodities
- Gráficos de tendências e análises

## 📋 Estrutura de Pastas
```
workshop-aberto-dw-do-zero/
├── app/                    # Scripts de Extract & Load
│   └── extract_load.py     # Extração de dados da API
├── datawarehouse/          # Projeto DBT
│   ├── models/             # Transformações de dados
│   │   ├── staging/        # Tabelas de staging
│   │   └── datamart/       # Tabelas finais para análise
│   └── seeds/              # Dados CSV para carregamento
├── src/                    # Código fonte adicional
├── profiles.yml            # Configuração DBT
└── README.md              # Documentação
```

## 🔄 Fluxo de Dados
```
API de Commodities → Extract_Load → PostgreSQL → DBT Transform → Data Warehouse → Streamlit Dashboard
```

### Processo ETL Detalhado:

1. **Extract (Extração)**
   - Busca dados de commodities de APIs externas
   - Coleta informações de preços, volumes, datas

2. **Load (Carregamento)**
   - Carrega dados brutos no PostgreSQL
   - Mantém dados originais para auditoria

3. **Transform (Transformação)**
   - DBT processa os dados brutos
   - Cria tabelas de staging com dados limpos
   - Gera tabelas de datamart para análise

4. **Visualização**
   - Dashboard Streamlit consome dados do DW
   - Apresenta KPIs e visualizações interativas

## 🛠️ Tecnologias Utilizadas
- **PostgreSQL**: Banco de dados principal
- **DBT (Data Build Tool)**: Ferramenta de transformação
- **Python**: Linguagem de programação para ETL
- **Streamlit**: Framework para dashboard
- **Git**: Controle de versão
- **APIs**: Fontes de dados de commodities

## 📊 Funcionalidades
- Extração automatizada de dados de commodities
- Transformações de dados com DBT
- Armazenamento estruturado em Data Warehouse
- Dashboard interativo para análise
- Documentação automática do DBT
- Controle de qualidade dos dados

## 🚀 Como Executar
1. Configurar ambiente Python
2. Instalar dependências
3. Configurar conexão PostgreSQL
4. Executar extract_load.py
5. Executar transformações DBT
6. Iniciar dashboard Streamlit
"""

def print_summary():
    """Imprime o resumo do projeto de Data Warehouse de Commodities"""
    print(__doc__)

def get_project_info():
    """Retorna informações principais do projeto"""
    return {
        "nome": "Data Warehouse de Commodities",
        "objetivo": "Criar DW para análise de dados de commodities",
        "tecnologias": ["PostgreSQL", "DBT", "Python", "Streamlit"],
        "componentes": ["Extract_Load", "Transform", "Dashboard"],
        "links": {
            "documentacao": "https://lvgalvao.github.io/workshop-aberto-dw-do-zero/#!/overview",
            "dashboard": "https://lvgalvao-workshop-aberto-dw-do-zero-appapp-vp0gw4.streamlit.app/"
        }
    }

if __name__ == "__main__":
    print_summary()