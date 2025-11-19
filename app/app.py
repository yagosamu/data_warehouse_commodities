import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title='Commodities Dashboard', 
    layout='wide',
    page_icon='📊'
)

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Get environment variables
DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')

# Verify all variables were loaded
if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS, DB_SCHEMA]):
    st.error("❌ Error: Environment variables not loaded. Check the .env file")
    st.stop()

# Create database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create database engine
engine = create_engine(DATABASE_URL)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_data():
    query = f"""
    SELECT
        data,
        simbolo,
        valor_fechamento,
        acao,
        quantidade,
        valor,
        ganho
    FROM
        public.dm_commodities
    ORDER BY data DESC;
    """
    try:
        df = pd.read_sql(query, engine)
        df['data'] = pd.to_datetime(df['data'])
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return pd.DataFrame()

def format_commodity_name(symbol):
    """Map symbols to friendly names"""
    mapping = {
        'CL=F': 'Oil (WTI)',
        'GC=F': 'Gold',
        'SI=F': 'Silver'
    }
    return mapping.get(symbol, symbol)

def format_currency(value):
    """Format values as currency"""
    return f"${value:,.2f}"

def calculate_roi(df):
    """Calculate ROI"""
    if df['valor'].sum() > 0:
        return (df['ganho'].sum() / df['valor'].sum()) * 100
    return 0

# Dashboard Title
st.title('📊 Commodities Dashboard')
st.markdown('**Real-Time Investment Monitoring**')

# Load data
with st.spinner('Loading data...'):
    df = get_data()

if df.empty:
    st.error("❌ Could not load data. Check database connection.")
    st.stop()

# Sidebar for filters
with st.sidebar:
    st.header('🎛️ Controls')
    
    # Update button
    if st.button('🔄 Refresh Data'):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    # Commodity filter
    st.subheader('Filters')
    commodities = df['simbolo'].unique()
    commodity_options = ['All'] + [f"{symbol} ({format_commodity_name(symbol)})" for symbol in commodities]
    selected_commodity = st.selectbox('Commodity:', commodity_options)
    
    # Period filter
    if not df.empty:
        min_date = df['data'].dt.date.min()
        max_date = df['data'].dt.date.max()
        
        date_range = st.date_input(
            'Period:',
            value=[min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )
    
    # Action filter
    action_filter = st.selectbox('Operation Type:', ['All', 'Buy', 'Sell'])
    
    st.divider()
    
    # System status
    st.subheader('📊 Status')
    st.success(f"✅ {len(df)} records loaded")
    st.info(f"📅 Last update: {datetime.now().strftime('%m/%d/%Y %H:%M')}")
    
    if not df.empty:
        st.info(f"📈 Data period: {min_date} to {max_date}")

# Apply filters
df_filtered = df.copy()

# Filter by commodity
if selected_commodity != 'All':
    symbol = selected_commodity.split(' (')[0]
    df_filtered = df_filtered[df_filtered['simbolo'] == symbol]

# Filter by period
if len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df_filtered[
        (df_filtered['data'].dt.date >= start_date) & 
        (df_filtered['data'].dt.date <= end_date)
    ]

# Filter by action
if action_filter != 'All':
    action_map = {'Buy': 'buy', 'Sell': 'sell'}
    df_filtered = df_filtered[df_filtered['acao'] == action_map[action_filter]]

# Main KPIs
if not df_filtered.empty:
    st.subheader('📈 Key Performance Indicators')
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_valor = df_filtered['valor'].sum()
    total_ganho = df_filtered['ganho'].sum()
    roi = calculate_roi(df_filtered)
    num_transacoes = len(df_filtered)
    
    with col1:
        st.metric(
            label="💰 Total Invested",
            value=format_currency(total_valor)
        )
    
    with col2:
        delta_color = "normal" if total_ganho >= 0 else "inverse"
        st.metric(
            label="📊 Total P&L",
            value=format_currency(total_ganho),
            delta=f"{total_ganho:+.2f}",
            delta_color=delta_color
        )
    
    with col3:
        roi_color = "normal" if roi >= 0 else "inverse"
        st.metric(
            label="📈 ROI",
            value=f"{roi:.1f}%",
            delta=f"{roi:+.1f}%",
            delta_color=roi_color
        )
    
    with col4:
        st.metric(
            label="🔄 Transactions",
            value=f"{num_transacoes:,}"
        )
    
    st.divider()
    
    # Charts in tabs
    tab1, tab2, tab3 = st.tabs(['📈 Price Evolution', '💰 Profit & Loss', '📊 Detailed Data'])
    
    with tab1:
        st.subheader('Closing Price Evolution')
        
        # Prepare data for chart
        price_data = df_filtered.pivot_table(
            index='data', 
            columns='simbolo', 
            values='valor_fechamento', 
            aggfunc='mean'
        )
        
        if not price_data.empty:
            st.line_chart(price_data)
        else:
            st.warning("Insufficient data to display price chart.")
    
    with tab2:
        st.subheader('Profit & Loss Analysis')
        
        # Gains by date
        ganho_por_data = df_filtered.groupby('data')['ganho'].sum()
        
        if not ganho_por_data.empty:
            st.bar_chart(ganho_por_data)
            
            # Summary by commodity
            st.subheader('Summary by Commodity')
            resumo = df_filtered.groupby('simbolo').agg({
                'ganho': 'sum',
                'valor': 'sum',
                'quantidade': 'sum'
            }).reset_index()
            
            resumo['commodity'] = resumo['simbolo'].apply(format_commodity_name)
            resumo['roi_individual'] = (resumo['ganho'] / resumo['valor'] * 100).round(1)
            
            # Display as metrics
            cols = st.columns(len(resumo))
            for i, (_, row) in enumerate(resumo.iterrows()):
                with cols[i]:
                    color = "normal" if row['ganho'] >= 0 else "inverse"
                    st.metric(
                        label=row['commodity'],
                        value=format_currency(row['ganho']),
                        delta=f"ROI: {row['roi_individual']}%",
                        delta_color=color
                    )
        else:
            st.warning("No profit/loss data to display.")
    
    with tab3:
        st.subheader('Detailed Data')
        
        # Display options
        col1, col2 = st.columns(2)
        with col1:
            show_summary = st.checkbox('Show summary only', value=False)
        with col2:
            download_csv = st.button('📥 Download CSV')
        
        if show_summary:
            # Show aggregated summary
            summary_df = df_filtered.groupby(['data', 'simbolo']).agg({
                'valor_fechamento': 'mean',
                'quantidade': 'sum',
                'valor': 'sum',
                'ganho': 'sum'
            }).reset_index()
            
            summary_df['commodity'] = summary_df['simbolo'].apply(format_commodity_name)
            summary_df = summary_df.drop('simbolo', axis=1)
            summary_df = summary_df[['data', 'commodity', 'valor_fechamento', 'quantidade', 'valor', 'ganho']]
            
            st.dataframe(
                summary_df.style.format({
                    'valor_fechamento': '${:.2f}',
                    'quantidade': '{:,.0f}',
                    'valor': '${:,.2f}',
                    'ganho': '${:,.2f}'
                }).map(
                    lambda x: 'color: green' if x > 0 else 'color: red' if x < 0 else 'color: black',
                    subset=['ganho']
                ),
                width='stretch'
            )
        else:
            # Show complete data
            display_df = df_filtered.copy()
            display_df['commodity'] = display_df['simbolo'].apply(format_commodity_name)
            display_df['action_en'] = display_df['acao'].map({'buy': 'Buy', 'sell': 'Sell'})
            
            # Reorganize columns
            display_df = display_df[['data', 'commodity', 'action_en', 'quantidade', 'valor_fechamento', 'valor', 'ganho']]
            display_df.columns = ['Date', 'Commodity', 'Action', 'Quantity', 'Close Price', 'Value', 'P&L']
            
            st.dataframe(
                display_df.style.format({
                    'Close Price': '${:.2f}',
                    'Quantity': '{:,.0f}',
                    'Value': '${:,.2f}',
                    'P&L': '${:,.2f}'
                }).map(
                    lambda x: 'color: green' if x > 0 else 'color: red' if x < 0 else 'color: black',
                    subset=['P&L']
                ),
                width='stretch'
            )
        
        # Download CSV
        if download_csv:
            csv = df_filtered.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"commodities_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

else:
    st.warning("⚠️ No data found with applied filters.")

# Footer
st.divider()
st.markdown(
    f"<div style='text-align: center; color: #666; font-size: 0.8em;'>"
    f"Commodities Dashboard | Last update: {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}"
    f"</div>", 
    unsafe_allow_html=True
)
