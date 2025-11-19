# DBT Documentation - Data Warehouse Commodities

## 📊 Generated Documentation

This folder contains automatically generated documentation by DBT for the Data Warehouse Commodities project.

### 📁 Main Files:

- **index.html**: Main interactive documentation page
- **manifest.json**: Complete DBT project metadata
- **catalog.json**: Data catalog with table information

### 🎯 Documented Models:

1. **stg_commodities**: Staging for raw commodities data
2. **stg_movimentacao_commodities**: Staging for commodities movements
3. **dm_commodities**: Final datamart for analytics

### 📈 Lineage Graph

The project has the following data flow:

```
Sources (API + Seeds) → Staging Models → Datamart Models → Analytics
```

### 🔗 How to View:

1. **Local**: Open `index.html` in a browser
2. **Server**: Use `dbt docs serve` in dbsales/ folder
3. **HTTP Server**: `python -m http.server 8080 --directory docs/`

### 📋 Statistics:

- ✅ **3 Models** processed
- ✅ **1 Seed** (movimentacao_commodities.csv)
- ✅ **2 Sources** configured
- ✅ **459 Macros** available

### 🎯 Data Warehouse Structure:

#### Staging Layer:
- Data cleaning and standardization
- Quality validations
- Preparation for transformations

#### Datamart Layer:  
- Business aggregations and metrics
- Ready-to-consume data
- Optimized for analytical queries

---

**Generated on**: November 19, 2025  
**DBT Version**: 1.10.15  
**Target**: PostgreSQL (AWS RDS)