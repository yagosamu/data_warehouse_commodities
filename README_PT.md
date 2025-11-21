# 📊 Data Warehouse de Commodities

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue?logo=postgresql)](https://postgresql.org)
[![DBT](https://img.shields.io/badge/DBT-1.x-orange?logo=dbt)](https://getdbt.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)](https://streamlit.io)

> **Data warehouse moderno para análise de commodities com monitoramento em tempo real**

## 🎯 Visão Geral

Solução completa de data warehouse para análise de commodities usando **PostgreSQL**, **DBT**, **Python** e **Streamlit**. Extrai dados da API do Yahoo Finance, transforma com SQL e visualiza em dashboards profissionais.

## 🏗️ Arquitetura

```mermaid
graph TD
    A[📊 Yahoo Finance API] -->|Extract| B[🐍 Python ETL]
    B -->|Load| C[🐘 PostgreSQL]
    C -->|Transform| D[🔧 DBT Models]
    D -->|Staging| E[📊 Data Warehouse]
    E -->|Analytics| F[📈 Streamlit Dashboard]
    
    subgraph "Data Pipeline"
        B
        D
    end
    
    subgraph "Storage Layer"
        C
        E
    end
    
    subgraph "Presentation Layer"
        F
    end
```

### Componentes do Projeto

#### 1. **Extract & Load** (`src/`)
Responsável por extrair dados de APIs e carregar diretamente no banco PostgreSQL.
- **Script**: `extract_load.py`
- **Função**: Busca dados de commodities via API do Yahoo Finance e carrega no banco
- **Recursos**: Tratamento de erros, validação de dados, agendamento automatizado

#### 2. **Transform** (`dbsales/`)
Utiliza DBT para transformações de dados:
- **Models Staging**: Limpeza e padronização dos dados
- **Models Datamart**: Métricas de negócio e tabelas analíticas agregadas
- **Seeds**: Carregamento de dados CSV de movimentações de commodities
- **Tests**: Validação de qualidade e integridade dos dados

#### 3. **Dashboard** (Streamlit)
Interface visual para análise dos dados:
- **Visualizações Interativas**: Gráficos e charts em tempo real
- **Tabelas de Dados**: Exploração detalhada das commodities
- **Análise de Tendências**: Padrões históricos de preços e volumes
- **Monitoramento de KPIs**: ROI, P&L e acompanhamento de investimentos

### 🔄 Fluxo de Dados

```
Yahoo Finance API → Python ETL → PostgreSQL → DBT Transform → Data Warehouse → Streamlit Dashboard
```

#### **Processo ETL Detalhado:**

**1. Extract (Extração)**
   - Busca dados de commodities de APIs externas (Yahoo Finance)
   - Coleta informações de preços, volumes e timestamps
   - Gerencia limites de API e recuperação de erros

**2. Load (Carregamento)**
   - Carrega dados brutos em tabelas staging do PostgreSQL
   - Mantém dados originais para trilhas de auditoria
   - Garante consistência e integridade dos dados

**3. Transform (Transformação)**
   - DBT processa dados brutos através de models staging
   - Cria tabelas staging limpas e padronizadas
   - Gera tabelas datamart finais para análise
   - Aplica lógica de negócio e cálculos

**4. Visualização**
   - Dashboard Streamlit consome dados do data warehouse
   - Apresenta KPIs em tempo real e visualizações interativas
   - Permite exportação de dados e capacidades de filtragem

## 📈 Dashboard

![Dashboard](assets/dashboard.png)

**Funcionalidades Principais:**
- 💰 KPIs em tempo real (ROI, P&L, Total Investido)
- 📊 Gráficos interativos com Plotly
- 🎛️ Sistema de filtros avançado
- 📋 Funcionalidade de exportação CSV

## 🔄 Lineage dos Dados

![Lineage](assets/lineage_graph.png)

**Fluxo do Pipeline:**
1. **Extract**: API Yahoo Finance → Python
2. **Load**: Tabelas staging PostgreSQL
3. **Transform**: Modelos DBT (staging → datamart)
4. **Visualize**: Dashboard Streamlit

## 🚀 Início Rápido

```bash
# Clone o repositório
git clone https://github.com/yagosamu/data_warehouse_commodities.git
cd data_warehouse_commodities

# Configure o ambiente
python -m venv venv
venv\Scripts\activate
pip install -r app/requirements.txt

# Configure o banco (arquivo .env necessário)
python src/extract_load.py

# Execute as transformações
cd dbsales && dbt run

# Inicie o dashboard
cd ../app && streamlit run app.py
```

## 🛠️ Stack Tecnológico

| Componente | Tecnologia | Propósito |
|------------|------------|-----------|
| **Extract** | Python + yfinance | Extração de dados da API |
| **Storage** | PostgreSQL | Data warehouse |
| **Transform** | DBT | Transformações SQL |
| **Visualize** | Streamlit + Plotly | Dashboard interativo |

## 📁 Estrutura

```
├── src/extract_load.py     # Pipeline ETL
├── dbsales/               # Projeto DBT
│   ├── models/staging/    # Limpeza de dados
│   └── models/datamart/   # Métricas de negócio
├── app/app.py            # Dashboard Streamlit
└── assets/               # Screenshots
```

## 👨‍💻 Autor

**Yago Lopes** - [GitHub](https://github.com/yagosamu)

---
*⭐ Dê uma estrela se este projeto foi útil!*

---

### 🇺🇸 [English Version](README.md)