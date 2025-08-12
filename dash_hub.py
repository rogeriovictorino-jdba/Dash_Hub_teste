import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# Configuração da página
st.set_page_config(
    page_title="Dashboard Comercial & Marketing - HubSpot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para layout profissional
st.markdown("""
<style>
    /* Layout principal */
    .main > div {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        max-height: 100vh;
        overflow-y: auto;
    }
    
    /* Remover espaçamento extra */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    /* Cards de métricas - Layout Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    
    /* Cards de métricas - Estilo base */
    .metric-card {
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Cards verdes (SDR) */
    .metric-card-green {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    }
    
    /* Cards laranja (Closer) */
    .metric-card-orange {
        background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
    }
    
    /* Cards azuis (Geral) */
    .metric-card-blue {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
    }
    
    /* Cards roxos (Marketing) */
    .metric-card-purple {
        background: linear-gradient(135deg, #9C27B0 0%, #7B1FA2 100%);
    }
    
    /* Cards vermelhos (Perdas) */
    .metric-card-red {
        background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        margin: 0;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.95;
        margin: 0;
        line-height: 1.1;
        margin-top: 8px;
    }
    
    /* Título das métricas */
    .metrics-title {
        font-size: 1.6rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 25px 0 15px 0;
        display: flex;
        align-items: center;
        border-bottom: 3px solid #667eea;
        padding-bottom: 10px;
    }
    
    .metrics-title::before {
        content: "📊";
        margin-right: 10px;
    }
    
    /* Container de filtros */
    .filter-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 25px;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Containers de gráficos */
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
        border: 1px solid #e9ecef;
    }
    
    /* Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0 0;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    
    /* Selectbox e inputs */
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 8px;
        border: 2px solid #e9ecef;
    }
    
    .stDateInput > div > div {
        background-color: white;
        border-radius: 8px;
        border: 2px solid #e9ecef;
    }
    
    /* Títulos das seções */
    .section-title {
        font-size: 1.4rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #667eea;
    }
    
    /* Funil de vendas */
    .funnel-container {
        display: flex;
        gap: 25px;
        margin: 25px 0;
    }
    
    .funnel-section {
        flex: 1;
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
    }
    
    .funnel-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .funnel-sdr {
        border-top: 4px solid #4CAF50;
    }
    
    .funnel-closer {
        border-top: 4px solid #FF9800;
    }
    
    /* Seções expansíveis */
    .expandable-section {
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
        border: 1px solid #e9ecef;
    }
    
    .expandable-header {
        padding: 20px;
        cursor: pointer;
        border-bottom: 1px solid #e9ecef;
        font-weight: bold;
        font-size: 1.1rem;
        color: #2c3e50;
    }
    
    .expandable-content {
        padding: 20px;
    }
    
    /* Responsividade */
    @media (max-width: 768px) {
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .metric-value {
            font-size: 1.6rem;
        }
        
        .metric-label {
            font-size: 0.8rem;
        }
        
        .funnel-container {
            flex-direction: column;
        }
    }
    
    /* Ocultar elementos desnecessários */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Ajustar altura dos gráficos */
    .js-plotly-plot {
        width: 100% !important;
    }
    
    /* Scrollbar customizada */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #5a6fd8;
    }
    
    /* Alertas customizados */
    .custom-alert {
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 5px solid;
    }
    
    .alert-info {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
        color: #1565c0;
    }
    
    .alert-success {
        background-color: #e8f5e8;
        border-left-color: #4caf50;
        color: #2e7d32;
    }
    
    .alert-warning {
        background-color: #fff3e0;
        border-left-color: #ff9800;
        color: #ef6c00;
    }
    
    /* Tooltip customizado */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
        color: #667eea;
        margin-left: 5px;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 300px;
        background-color: #555;
        color: white;
        text-align: left;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -150px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
        line-height: 1.4;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# MAPA DOS COLABORADORES
sdrs = {
    "76849116": "Matheus Rodrigues",
    "77424189": "Lidia Ferreira", 
    "78436803": "Gabriel Fazzio",
    "79765846": "Cris Trindade",
    "529189232": "Alessandra Baranyi",
    "1549404207": "Vitor Santana"
}

closers = {
    "76509023": "Rafael Fugita",
    "79878802": "Natalia Barros",
    "157948224": "Gabriela Sampaio",
    "1598039931": "Marcio Leal",
    "1639885623": "Herbert Sany"
}

todos_colaboradores = {**sdrs, **closers}

# MAPA COMPLETO DOS PIPELINES E SUAS FASES
pipelines = {
    "default": "CSE| Leads",
    "647912117": "MBN",
    "702880820": "Business Concierge",
    "714474841": "IA",
    "760934308": "Êxito",
    "765774454": "Imersão técnicas",
    "765893643": "Comercial JD"
}

# MAPEAMENTO DE CAMPOS DO HUBSPOT (baseado na planilha fornecida)
hubspot_fields = {
    'hs_ad_campaign_count': 'Número de campanhas de anúncio associado a esta campanha',
    'hs_automation_platform_flows_count': 'Número de fluxos de trabalho associados a esta campanha',
    'hs_blog_posts_count': 'Número de posts do blog associados a esta campanha',
    'hs_broadcast_count': 'Número de posts sociais associados a esta campanha',
    'hs_call_count': 'Número de chamadas associadas a esta campanha',
    'hs_case_study_count': 'Número de estudos de caso',
    'hs_cta_count': 'Número de CTAs (antigas)',
    'hs_document_count': 'Número de documentos',
    'hs_external_website_page_count': 'Número de páginas do site externo',
    'hs_feedback_survey_count': 'Número de pesquisas de feedback',
    'hs_file_manager_file_count': 'Número de arquivos',
    'hs_form_count': 'Número de formulários',
    'hs_knowledge_article_count': 'Número de artigos de conhecimento',
    'hs_landing_pages_count': 'Número de landing pages',
    'hs_list_count': 'Número de listas',
    'hs_marketing_emails_count': 'Número de e-mails',
    'hs_marketing_event_count': 'Número de eventos de marketing',
    'hs_meeting_count': 'Número de reuniões',
    'hs_number_of_external_social_posts': 'Número de posts sociais externos',
    'hs_number_of_tickets': 'Número de tickets',
    'hs_playbook_count': 'Número de manuais',
    'hs_podcast_count': 'Número de episódios de podcast',
    'hs_sales_email_count': 'Número de e-mails de vendas',
    'hs_sequence_count': 'Número de sequências',
    'hs_site_pages_count': 'Número de páginas de site',
    'hs_video_count': 'Número de vídeos',
    'hs_web_interactive_count': 'Número de CTAs',
    'hs_all_assigned_business_unit_ids': 'Marcas',
    'hs_audience': 'Público da campanha',
    'hs_budget_items_sum_amount': 'Total do orçamento da campanha',
    'hs_campaign_status': 'Status da campanha',
    'hs_color_hex': 'Cor da campanha',
    'hs_created_at': 'Criado em',
    'hs_created_by_user_id': 'Criado por ID do usuário',
    'hs_currency_code': 'Código de moeda',
    'hs_end_date': 'Data de término da campanha',
    'hs_merged_object_ids': 'IDs de objetos mesclados',
    'hs_name': 'Nome da campanha',
    'hs_notes': 'Observações da campanha',
    'hs_object_source_detail_1': 'Detalhe da fonte do registro 1',
    'hs_object_source_detail_2': 'Detalhe da fonte do registro 2',
    'hs_object_source_detail_3': 'Detalhe da fonte do registro 3',
    'hs_object_source_label': 'Fonte do registro',
    'hs_origin_asset_id': 'ID da campanha',
    'hs_owner': 'Proprietário da campanha',
    'hs_spend_items_sum_amount': 'Total de gastos da campanha',
    'hs_start_date': 'Data de início da campanha',
    'hs_updated_by_user_id': 'Atualizado por ID de usuário',
    'hs_utm': 'UTM da campanha',
    'hubspot_owner_assigneddate': 'Data de atribuição do proprietário',
    'hubspot_owner_id': 'Proprietário',
    'hs_object_id': 'ID do contato',
    'createdate': 'Data de criação do contato'
}

# --- FUNÇÕES AUXILIARES ---
def formatar_valor(valor):
    """Formata um valor numérico para o formato de moeda brasileira (R$)."""
    try:
        if valor:
            return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        pass
    return "R$ 0,00"

def formatar_tempo(horas):
    """Formata tempo em horas para formato legível (dias, horas, minutos)."""
    if horas == 0:
        return "0h"
    
    dias = int(horas // 24)
    horas_restantes = int(horas % 24)
    minutos = int((horas % 1) * 60)
    
    if dias > 0:
        return f"{dias}d {horas_restantes}h {minutos}m"
    elif horas_restantes > 0:
        return f"{horas_restantes}h {minutos}m"
    else:
        return f"{minutos}m"

def criar_card_metrica(valor, label, cor="blue", tooltip=""):
    """Cria um card de métrica HTML com tooltip opcional."""
    tooltip_html = ""
    if tooltip:
        tooltip_html = f'''
        <div class="tooltip">ℹ️
            <span class="tooltiptext">{tooltip}</span>
        </div>
        '''
    
    return f"""
    <div class="metric-card metric-card-{cor}">
        <div class="metric-value">{valor}</div>
        <div class="metric-label">{label} {tooltip_html}</div>
    </div>
    """

# --- GERAÇÃO DE DADOS DEMO ---
@st.cache_data
def gerar_dados_demo():
    np.random.seed(42)
    
    # Gerar dados de exemplo com base nos números fornecidos
    n_deals = 1765  # Total de leads baseado nos números fornecidos
    
    data = []
    for i in range(n_deals):
        # Garantir que temos 15 leads criados hoje
        if i < 15:
            createdate = datetime.now()
        else:
            createdate = datetime.now() - timedelta(days=np.random.randint(1, 90))
        
        # Selecionar pipeline e colaborador aleatoriamente
        pipeline_id = np.random.choice(list(pipelines.keys()))
        owner_id = np.random.choice(list(todos_colaboradores.keys()))
        
        # Definir estágio baseado no tipo de colaborador
        if owner_id in sdrs:
            # Distribuição mais realista para SDR
            stages = ["Novo", "Qualificação", "Agendado", "No-Show", "Reagendado", "Perdido"]
            stage_weights = [0.4, 0.25, 0.15, 0.1, 0.05, 0.05]
            stage = np.random.choice(stages, p=stage_weights)
            responsavel = "SDR"
        else:
            # Distribuição mais realista para Closer
            stages = ["Negociação", "Pagamento", "Ganho", "Perdido"]
            stage_weights = [0.4, 0.2, 0.2, 0.2]
            stage = np.random.choice(stages, p=stage_weights)
            responsavel = "Closer"
        
        # Gerar valores mais realistas
        if responsavel == "Closer":
            amount = np.random.uniform(1000, 10000)  # Ticket médio mais baixo para Closer
        else:
            amount = np.random.uniform(500, 5000)   # Valores menores para SDR
            
        faturamento_anterior = np.random.uniform(500000, 5000000) if np.random.random() > 0.3 else 0
        
        # UTM data baseado nos campos do HubSpot
        utm_sources = ["google", "facebook", "linkedin", "instagram", "direct", "email"]
        utm_mediums = ["cpc", "organic", "social", "email", "referral"]
        utm_campaigns = ["black_friday", "natal_2024", "leads_qualificados", "remarketing", "brand"]
        
        # Adicionando dados de atividades baseados nos campos do HubSpot
        hs_call_count = np.random.randint(0, 5)
        hs_meeting_count = np.random.randint(0, 3)
        hs_sales_email_count = np.random.randint(0, 10)
        hs_document_count = np.random.randint(0, 2)
        hs_marketing_emails_count = np.random.randint(0, 5)
        hs_form_count = np.random.randint(0, 3)
        
        # Calcular tempo médio baseado no estágio
        if stage in ["Agendado", "Negociação", "Ganho"]:
            tempo_medio_horas = np.random.uniform(24, 168)  # 1-7 dias
        else:
            tempo_medio_horas = np.random.uniform(1, 72)    # 1-3 dias

        # Definir produto baseado no pipeline
        produto_map = {
            "default": "CSE Leads",
            "647912117": "MBN",
            "702880820": "Business Concierge", 
            "714474841": "IA",
            "760934308": "Êxito",
            "765774454": "Imersão Técnicas",
            "765893643": "Comercial JD"
        }
        produto = produto_map.get(pipeline_id, "Produto Genérico")

        data.append({
            'hs_object_id': f"contact_{i}",  # ID correto do HubSpot
            'deal_name': f"Lead {i+1}",
            'amount': amount,
            'deal_stage': stage,
            'pipeline_id': pipeline_id,
            'pipeline_name': pipelines[pipeline_id],
            'produto': produto,  # Nova coluna para produto
            'hubspot_owner_id': owner_id,  # Campo correto do HubSpot
            'owner_name': todos_colaboradores[owner_id],
            'responsavel': responsavel,
            'createdate': createdate,  # Campo correto do HubSpot
            'close_date': createdate + timedelta(days=np.random.randint(7, 60)) if stage in ["Ganho", "Perdido"] else None,
            'last_modified': createdate + timedelta(days=np.random.randint(1, 30)),
            'faturamento_anterior': faturamento_anterior,
            # ALTERAÇÃO: Leads qualificados agora incluem todos que chegaram até "Agendado"
            'is_mql': stage in ["Agendado", "No-Show", "Reagendado"],  # Todos que chegaram até agendado
            'is_sql': faturamento_anterior >= 1000000 and stage in ["Agendado", "Negociação"],
            'source': np.random.choice(["Busca Orgânica", "Google Ads", "Facebook", "LinkedIn", "Indicação", "Site"]),
            'hs_utm': np.random.choice(utm_campaigns),  # Campo correto do HubSpot
            'utm_source': np.random.choice(utm_sources),
            'utm_medium': np.random.choice(utm_mediums),
            'utm_campaign': np.random.choice(utm_campaigns),
            'motivo_perda': np.random.choice(["Preço", "Timing", "Concorrência", "Orçamento", "Não Qualificado"]) if stage == "Perdido" else None,
            'dias_desde_criacao': (datetime.now() - createdate).days,
            'tempo_medio_horas': tempo_medio_horas,
            # Campos de atividades do HubSpot
            'hs_call_count': hs_call_count,
            'hs_meeting_count': hs_meeting_count,
            'hs_sales_email_count': hs_sales_email_count,
            'hs_document_count': hs_document_count,
            'hs_marketing_emails_count': hs_marketing_emails_count,
            'hs_form_count': hs_form_count,
            'hs_landing_pages_count': np.random.randint(0, 2),
            'hs_blog_posts_count': np.random.randint(0, 3),
            'hs_video_count': np.random.randint(0, 2),
            'hs_web_interactive_count': np.random.randint(0, 4)
        })
    
    df = pd.DataFrame(data)
    
    # Adicionar informações de tempo
    df['mes_criacao'] = df['createdate'].dt.to_period('M')
    df['semana_criacao'] = df['createdate'].dt.to_period('W')
    
    return df

# --- FUNÇÃO PARA CARREGAR DADOS REAIS DO HUBSPOT ---
def carregar_dados_hubspot():
    """
    Função para carregar dados reais do HubSpot.
    Substitua esta função pela implementação real da API do HubSpot.
    """
    try:
        # Aqui você implementaria a conexão real com o HubSpot
        # from hubspot import HubSpot
        # api_client = HubSpot(access_token="SEU_TOKEN_AQUI")
        # contacts = api_client.crm.contacts.get_all()
        # deals = api_client.crm.deals.get_all()
        
        # Por enquanto, retorna None para usar dados demo
        return None
    except Exception as e:
        st.error(f"Erro ao carregar dados do HubSpot: {e}")
        return None

# --- INTERFACE PRINCIPAL ---
def main():
    st.title("🚀 Dashboard - HubSpot")
    
    # Tentar carregar dados reais do HubSpot
    df_hubspot = carregar_dados_hubspot()
    
    if df_hubspot is not None:
        df = df_hubspot
        st.success("✅ Dados carregados do HubSpot com sucesso!")
    else:
        # Carregar dados demo
        with st.spinner("Carregando dados demo..."):
            df = gerar_dados_demo()
    
    # --- FILTROS ---
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    st.subheader("🔍 Filtros")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pipelines_disponiveis = ['Todos'] + list(df['pipeline_name'].unique())
        pipeline_selecionado = st.selectbox("Pipeline", pipelines_disponiveis)
    
    with col2:
        if pipeline_selecionado != 'Todos':
            fases_disponiveis = ['Todas'] + list(df[df['pipeline_name'] == pipeline_selecionado]['deal_stage'].unique())
        else:
            fases_disponiveis = ['Todas'] + list(df['deal_stage'].unique())
        fase_selecionada = st.selectbox("Fase", fases_disponiveis)
    
    with col3:
        colaboradores_disponiveis = ['Todos'] + list(df['owner_name'].unique())
        colaborador_selecionado = st.selectbox("Colaborador", colaboradores_disponiveis)
    
    with col4:
        tipo_data = st.selectbox("Tipo de Data", ["Data de Criação", "Data de Fechamento", "Última Atividade"])
    
    col5, col6 = st.columns(2)
    with col5:
        data_inicio = st.date_input("Data Início", value=datetime.now() - timedelta(days=30))
    with col6:
        data_fim = st.date_input("Data Fim", value=datetime.now())
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if pipeline_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['pipeline_name'] == pipeline_selecionado]
    
    if fase_selecionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['deal_stage'] == fase_selecionada]
    
    if colaborador_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['owner_name'] == colaborador_selecionado]
    
    # Filtro de data usando o campo correto do HubSpot
    campo_data = 'createdate' if tipo_data == "Data de Criação" else 'close_date' if tipo_data == "Data de Fechamento" else 'last_modified'
    df_filtrado = df_filtrado[
        (df_filtrado[campo_data].dt.date >= data_inicio) & 
        (df_filtrado[campo_data].dt.date <= data_fim)
    ]
    
    # --- MÉTRICAS PRINCIPAIS ---
    st.markdown('<div class="metrics-title">Métricas Principais</div>', unsafe_allow_html=True)
    
    # Filtrar dados por responsável
    df_sdr = df_filtrado[df_filtrado['responsavel'] == 'SDR']
    df_closer = df_filtrado[df_filtrado['responsavel'] == 'Closer']
    
    # Calcular métricas SDR
    total_leads_sdr = len(df_sdr)
    # ALTERAÇÃO: Leads qualificados agora incluem todos que chegaram até "Agendado"
    leads_qualificados_sdr = len(df_sdr[df_sdr['is_mql']])  # Todos que chegaram até agendado
    leads_perdidos_sdr = len(df_sdr[df_sdr['deal_stage'] == 'Perdido'])
    taxa_conversao_sdr = (leads_qualificados_sdr / total_leads_sdr * 100) if total_leads_sdr > 0 else 0
    taxa_perda_sdr = (leads_perdidos_sdr / total_leads_sdr * 100) if total_leads_sdr > 0 else 0
    tempo_medio_sdr = df_sdr['tempo_medio_horas'].mean() if not df_sdr.empty else 0
    
    # Calcular métricas Closer
    total_negocios_closer = len(df_closer)
    negocios_ganhos = len(df_closer[df_closer['deal_stage'] == 'Ganho'])
    taxa_conversao_closer = (negocios_ganhos / total_negocios_closer * 100) if total_negocios_closer > 0 else 0
    ticket_medio_closer = df_closer[df_closer['deal_stage'] == 'Ganho']['amount'].mean() if negocios_ganhos > 0 else 0
    tempo_medio_closer = df_closer['tempo_medio_horas'].mean() if not df_closer.empty else 0
    
    # Leads criados hoje usando o campo correto
    today = datetime.now().date()
    leads_criados_hoje = len(df_filtrado[df_filtrado['createdate'].dt.date == today])
    
    # NOVAS MÉTRICAS SOLICITADAS
    # Quantidade de contatos (ligação/whatsapp) - usando hs_call_count
    total_chamadas = df_filtrado['hs_call_count'].sum()
    total_reunioes = df_filtrado['hs_meeting_count'].sum()
    
    # Cards de métricas baseados no layout solicitado com tooltips
    st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        tooltip_sdr = hubspot_fields.get('hs_object_id', 'Total de leads atribuídos aos SDRs no período selecionado')
        st.markdown(criar_card_metrica(f"{total_leads_sdr:,}", "Total Leads SDR", "green", tooltip_sdr), unsafe_allow_html=True)
    with col2:
        tooltip_tma = "Tempo Médio de Atendimento - tempo médio entre criação do lead e primeira ação"
        st.markdown(criar_card_metrica(formatar_tempo(tempo_medio_sdr), "TMA SDR", "green", tooltip_tma), unsafe_allow_html=True)
    with col3:
        tooltip_closer = "Total de negócios atribuídos aos Closers no período selecionado"
        st.markdown(criar_card_metrica(f"{total_negocios_closer:,}", "Total Negócios Closer", "orange", tooltip_closer), unsafe_allow_html=True)
    with col4:
        tooltip_tmf = "Tempo Médio de Fechamento - tempo médio para conclusão de negócios"
        st.markdown(criar_card_metrica(formatar_tempo(tempo_medio_closer), "TMF Closer", "orange", tooltip_tmf), unsafe_allow_html=True)
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        tooltip_conv_sdr = "Percentual de leads que chegaram até o estágio 'Agendado' ou superior"
        st.markdown(criar_card_metrica(f"{taxa_conversao_sdr:.1f}%", "Taxa Conversão SDR", "green", tooltip_conv_sdr), unsafe_allow_html=True)
    with col6:
        tooltip_conv_closer = "Percentual de negócios fechados com sucesso pelos Closers"
        st.markdown(criar_card_metrica(f"{taxa_conversao_closer:.1f}%", "Taxa Conversão Closer", "orange", tooltip_conv_closer), unsafe_allow_html=True)
    with col7:
        tooltip_ticket = "Valor médio dos negócios fechados com sucesso"
        st.markdown(criar_card_metrica(formatar_valor(ticket_medio_closer), "Ticket Médio Closer", "orange", tooltip_ticket), unsafe_allow_html=True)
    with col8:
        tooltip_hoje = hubspot_fields.get('createdate', 'Leads criados na data atual')
        st.markdown(criar_card_metrica(f"{leads_criados_hoje:,}", "Leads Criados Hoje", "blue", tooltip_hoje), unsafe_allow_html=True)
    
    col9, col10, col11, col12 = st.columns(4)
    with col9:
        tooltip_qualif = "Leads que chegaram até o estágio 'Agendado', incluindo No-Show e Reagendado"
        st.markdown(criar_card_metrica(f"{leads_qualificados_sdr:,}", "Leads Qualificados SDR", "green", tooltip_qualif), unsafe_allow_html=True)
    with col10:
        tooltip_perda = "Percentual de leads marcados como 'Perdido'"
        st.markdown(criar_card_metrica(f"{taxa_perda_sdr:.1f}%", "Taxa Perda SDR", "red", tooltip_perda), unsafe_allow_html=True)
    with col11:
        tooltip_ganhos = "Total de negócios fechados com sucesso"
        st.markdown(criar_card_metrica(f"{negocios_ganhos:,}", "Negócios Ganhos", "green", tooltip_ganhos), unsafe_allow_html=True)
    with col12:
        # NOVA MÉTRICA: Total de contatos (chamadas)
        tooltip_chamadas = hubspot_fields.get('hs_call_count', 'Total de chamadas realizadas no período')
        st.markdown(criar_card_metrica(f"{total_chamadas:,}", "Total Chamadas", "purple", tooltip_chamadas), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- SEÇÃO EXPANSÍVEL DE DETALHES ---
    with st.expander("📊 Detalhamento das Métricas Principais", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribuição por Pipeline")
            pipeline_dist = df_filtrado.groupby('pipeline_name').agg({
                'hs_object_id': 'count',
                'amount': 'sum'
            }).reset_index()
            pipeline_dist.columns = ['Pipeline', 'Quantidade', 'Valor Total']
            pipeline_dist['Valor Total'] = pipeline_dist['Valor Total'].apply(formatar_valor)
            st.dataframe(pipeline_dist, use_container_width=True)
        
        with col2:
            st.subheader("Distribuição por Fase")
            fase_dist = df_filtrado.groupby('deal_stage').agg({
                'hs_object_id': 'count',
                'amount': 'sum'
            }).reset_index()
            fase_dist.columns = ['Fase', 'Quantidade', 'Valor Total']
            fase_dist['Valor Total'] = fase_dist['Valor Total'].apply(formatar_valor)
            st.dataframe(fase_dist, use_container_width=True)
    
    # --- ABAS PRINCIPAIS ---
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📈 Análise Temporal", 
        "👥 Performance SDR", 
        "🎯 Performance Closer", 
        "📊 Marketing & UTM", 
        "🔍 Análise ICP", 
        "⚡ Atividades",
        "🔧 Back-end"
    ])
    
    with tab1:
        st.subheader("📈 Análise Temporal")
        
        # Gráfico de evolução temporal usando campo correto
        df_temporal = df_filtrado.groupby(df_filtrado['createdate'].dt.date).agg({
            'hs_object_id': 'count',
            'amount': 'sum'
        }).reset_index()
        df_temporal.columns = ['Data', 'Quantidade', 'Valor']
        
        fig_temporal = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_temporal.add_trace(
            go.Scatter(x=df_temporal['Data'], y=df_temporal['Quantidade'], name="Quantidade de Leads"),
            secondary_y=False,
        )
        
        fig_temporal.add_trace(
            go.Scatter(x=df_temporal['Data'], y=df_temporal['Valor'], name="Valor Total", line=dict(color='orange')),
            secondary_y=True,
        )
        
        fig_temporal.update_xaxes(title_text="Data")
        fig_temporal.update_yaxes(title_text="Quantidade de Leads", secondary_y=False)
        fig_temporal.update_yaxes(title_text="Valor Total (R$)", secondary_y=True)
        fig_temporal.update_layout(title_text="Evolução Temporal de Leads e Valor")
        
        st.plotly_chart(fig_temporal, use_container_width=True)
        
        # NOVA FUNCIONALIDADE: Quantidade de leads por produto
        st.subheader("📦 Leads por Produto")
        leads_por_produto = df_filtrado.groupby('produto').agg({
            'hs_object_id': 'count',
            'amount': 'sum',
            'is_mql': 'sum'
        }).reset_index()
        leads_por_produto.columns = ['Produto', 'Total Leads', 'Valor Total', 'Leads Qualificados']
        leads_por_produto['Taxa Qualificação (%)'] = (leads_por_produto['Leads Qualificados'] / leads_por_produto['Total Leads'] * 100).round(2)
        
        col1, col2 = st.columns(2)
        with col1:
            fig_produto_leads = px.bar(leads_por_produto, x='Produto', y='Total Leads',
                                     title="Quantidade de Leads por Produto")
            st.plotly_chart(fig_produto_leads, use_container_width=True)
        
        with col2:
            fig_produto_valor = px.bar(leads_por_produto, x='Produto', y='Valor Total',
                                     title="Valor Total por Produto")
            st.plotly_chart(fig_produto_valor, use_container_width=True)
        
        st.dataframe(leads_por_produto, use_container_width=True)
        
        # Análise por período
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Análise Semanal")
            df_semanal = df_filtrado.groupby('semana_criacao').agg({
                'hs_object_id': 'count',
                'amount': 'sum'
            }).reset_index()
            df_semanal['semana_criacao'] = df_semanal['semana_criacao'].astype(str)
            
            fig_semanal = px.bar(df_semanal, x='semana_criacao', y='hs_object_id', 
                               title="Leads por Semana")
            st.plotly_chart(fig_semanal, use_container_width=True)
        
        with col2:
            st.subheader("Análise Mensal")
            df_mensal = df_filtrado.groupby('mes_criacao').agg({
                'hs_object_id': 'count',
                'amount': 'sum'
            }).reset_index()
            df_mensal['mes_criacao'] = df_mensal['mes_criacao'].astype(str)
            
            fig_mensal = px.bar(df_mensal, x='mes_criacao', y='hs_object_id',
                              title="Leads por Mês")
            st.plotly_chart(fig_mensal, use_container_width=True)
    
    with tab2:
        st.subheader("👥 Performance SDR")
        
        if not df_sdr.empty:
            # Métricas por SDR
            sdr_metrics = df_sdr.groupby('owner_name').agg({
                'hs_object_id': 'count',
                'amount': 'sum',
                'tempo_medio_horas': 'mean'
            }).reset_index()
            sdr_metrics.columns = ['SDR', 'Quantidade de Leads', 'Valor Total', 'TMA (horas)']
            
            # Adicionar métricas específicas
            agendamentos = df_sdr[df_sdr['deal_stage'] == 'Agendado'].groupby('owner_name').size()
            no_shows = df_sdr[df_sdr['deal_stage'] == 'No-Show'].groupby('owner_name').size()
            reagendamentos = df_sdr[df_sdr['deal_stage'] == 'Reagendado'].groupby('owner_name').size()
            perdidos = df_sdr[df_sdr['deal_stage'] == 'Perdido'].groupby('owner_name').size()
            
            sdr_metrics['Agendamentos'] = sdr_metrics['SDR'].map(agendamentos).fillna(0)
            sdr_metrics['No-Shows'] = sdr_metrics['SDR'].map(no_shows).fillna(0)
            sdr_metrics['Reagendamentos'] = sdr_metrics['SDR'].map(reagendamentos).fillna(0)
            sdr_metrics['Perdidos'] = sdr_metrics['SDR'].map(perdidos).fillna(0)
            
            # Calcular taxa de conversão e perda
            sdr_metrics['Taxa Conversão (%)'] = (sdr_metrics['Agendamentos'] / sdr_metrics['Quantidade de Leads'] * 100).round(2)
            sdr_metrics['Taxa Perda (%)'] = (sdr_metrics['Perdidos'] / sdr_metrics['Quantidade de Leads'] * 100).round(2)
            
            # Formatar valores
            sdr_metrics['Valor Total'] = sdr_metrics['Valor Total'].apply(formatar_valor)
            sdr_metrics['TMA'] = sdr_metrics['TMA (horas)'].apply(formatar_tempo)
            sdr_metrics = sdr_metrics.drop('TMA (horas)', axis=1)
            
            st.dataframe(sdr_metrics, use_container_width=True)
            
            # Gráficos de performance SDR
            col1, col2 = st.columns(2)
            
            with col1:
                sdr_leads_data = df_sdr.groupby('owner_name').size().reset_index()
                sdr_leads_data.columns = ['SDR', 'Quantidade']
                fig_sdr_leads = px.bar(sdr_leads_data, x='SDR', y='Quantidade',
                                     title="Quantidade de Leads por SDR")
                st.plotly_chart(fig_sdr_leads, use_container_width=True)
            
            with col2:
                sdr_tempo_data = df_sdr.groupby('owner_name')['tempo_medio_horas'].mean().reset_index()
                sdr_tempo_data.columns = ['SDR', 'TMA (horas)']
                fig_sdr_tempo = px.bar(sdr_tempo_data, x='SDR', y='TMA (horas)',
                                     title="Tempo Médio de Atendimento por SDR")
                st.plotly_chart(fig_sdr_tempo, use_container_width=True)
        else:
            st.info("Nenhum dado de SDR encontrado para os filtros selecionados.")
    
    with tab3:
        st.subheader("🎯 Performance Closer")
        
        if not df_closer.empty:
            # Métricas por Closer
            closer_metrics = df_closer.groupby('owner_name').agg({
                'hs_object_id': 'count',
                'amount': 'sum',
                'tempo_medio_horas': 'mean'
            }).reset_index()
            closer_metrics.columns = ['Closer', 'Quantidade de Negócios', 'Valor Total', 'TMF (horas)']
            
            # Adicionar métricas específicas
            negociacoes = df_closer[df_closer['deal_stage'] == 'Negociação'].groupby('owner_name').size()
            pagamentos = df_closer[df_closer['deal_stage'] == 'Pagamento'].groupby('owner_name').size()
            ganhos = df_closer[df_closer['deal_stage'] == 'Ganho'].groupby('owner_name').size()
            perdidos = df_closer[df_closer['deal_stage'] == 'Perdido'].groupby('owner_name').size()
            
            closer_metrics['Negociações'] = closer_metrics['Closer'].map(negociacoes).fillna(0)
            closer_metrics['Pagamentos'] = closer_metrics['Closer'].map(pagamentos).fillna(0)
            closer_metrics['Ganhos'] = closer_metrics['Closer'].map(ganhos).fillna(0)
            closer_metrics['Perdidos'] = closer_metrics['Closer'].map(perdidos).fillna(0)
            
            # Calcular taxa de conversão
            closer_metrics['Taxa de Conversão (%)'] = (closer_metrics['Ganhos'] / closer_metrics['Quantidade de Negócios'] * 100).round(2)
            
            # Formatar valores
            closer_metrics['Valor Total'] = closer_metrics['Valor Total'].apply(formatar_valor)
            closer_metrics['TMF'] = closer_metrics['TMF (horas)'].apply(formatar_tempo)
            closer_metrics = closer_metrics.drop('TMF (horas)', axis=1)
            
            st.dataframe(closer_metrics, use_container_width=True)
            
            # NOVA FUNCIONALIDADE: Vendas por produto x pipeline
            st.subheader("💰 Vendas por Produto x Pipeline")
            vendas_produto_pipeline = df_closer[df_closer['deal_stage'] == 'Ganho'].groupby(['produto', 'pipeline_name']).agg({
                'hs_object_id': 'count',
                'amount': 'sum'
            }).reset_index()
            vendas_produto_pipeline.columns = ['Produto', 'Pipeline', 'Quantidade Vendas', 'Valor Total']
            
            if not vendas_produto_pipeline.empty:
                # Criar matriz de vendas
                matriz_vendas = vendas_produto_pipeline.pivot_table(
                    index='Produto', 
                    columns='Pipeline', 
                    values='Valor Total', 
                    fill_value=0
                )
                
                fig_matriz = px.imshow(matriz_vendas, 
                                     title="Matriz de Vendas: Produto x Pipeline",
                                     color_continuous_scale="Blues")
                st.plotly_chart(fig_matriz, use_container_width=True)
                
                st.dataframe(vendas_produto_pipeline, use_container_width=True)
            else:
                st.info("Nenhuma venda encontrada para análise de produto x pipeline.")
            
            # Gráficos de performance Closer
            col1, col2 = st.columns(2)
            
            with col1:
                closer_valor_data = df_closer.groupby('owner_name')['amount'].sum().reset_index()
                closer_valor_data.columns = ['Closer', 'Valor Total']
                fig_closer_valor = px.bar(closer_valor_data, x='Closer', y='Valor Total',
                                        title="Valor Total por Closer")
                st.plotly_chart(fig_closer_valor, use_container_width=True)
            
            with col2:
                closer_taxa_data = df_closer.groupby('owner_name').apply(
                    lambda x: (len(x[x['deal_stage'] == 'Ganho']) / len(x) * 100) if len(x) > 0 else 0
                ).reset_index()
                closer_taxa_data.columns = ['Closer', 'Taxa de Conversão (%)']
                fig_closer_taxa = px.bar(closer_taxa_data, x='Closer', y='Taxa de Conversão (%)',
                                        title="Taxa de Conversão por Closer")
                st.plotly_chart(fig_closer_taxa, use_container_width=True)
        else:
            st.info("Nenhum dado de Closer encontrado para os filtros selecionados.")

    with tab4:
        st.subheader("📊 Marketing & UTM")
        
        # NOVA FUNCIONALIDADE: Percentual de conversão por canais de captação
        st.subheader("📈 Conversão por Canais de Captação")
        
        conversao_canais = df_filtrado.groupby(['utm_source', 'utm_medium']).agg({
            'hs_object_id': 'count',
            'is_mql': 'sum'
        }).reset_index()
        conversao_canais.columns = ['UTM Source', 'UTM Medium', 'Total Leads', 'Leads Qualificados']
        conversao_canais['Taxa Conversão (%)'] = (conversao_canais['Leads Qualificados'] / conversao_canais['Total Leads'] * 100).round(2)
        conversao_canais['Canal'] = conversao_canais['UTM Source'] + ' / ' + conversao_canais['UTM Medium']
        
        fig_conversao_canais = px.bar(conversao_canais, x='Canal', y='Taxa Conversão (%)',
                                    title="Taxa de Conversão por Canal de Captação")
        fig_conversao_canais.update_xaxes(tickangle=45)
        st.plotly_chart(fig_conversao_canais, use_container_width=True)
        
        st.dataframe(conversao_canais, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Leads por Fonte")
            source_dist = df_filtrado.groupby('source').size().reset_index(name='Quantidade')
            fig_source = px.pie(source_dist, values='Quantidade', names='source', title='Distribuição de Leads por Fonte')
            st.plotly_chart(fig_source, use_container_width=True)
        
        with col2:
            st.subheader("Leads por UTM Source")
            utm_source_dist = df_filtrado.groupby('utm_source').size().reset_index(name='Quantidade')
            fig_utm_source = px.bar(utm_source_dist, x='utm_source', y='Quantidade', title='Leads por UTM Source')
            st.plotly_chart(fig_utm_source, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Leads por UTM Medium")
            utm_medium_dist = df_filtrado.groupby('utm_medium').size().reset_index(name='Quantidade')
            fig_utm_medium = px.bar(utm_medium_dist, x='utm_medium', y='Quantidade', title='Leads por UTM Medium')
            st.plotly_chart(fig_utm_medium, use_container_width=True)

        with col4:
            st.subheader("Leads por UTM Campaign (HubSpot)")
            utm_campaign_dist = df_filtrado.groupby('hs_utm').size().reset_index(name='Quantidade')
            fig_utm_campaign = px.bar(utm_campaign_dist, x='hs_utm', y='Quantidade', title='Leads por UTM Campaign')
            st.plotly_chart(fig_utm_campaign, use_container_width=True)

    with tab5:
        st.subheader("🔍 Análise ICP")
        
        # NOVA FUNCIONALIDADE: Conversões por categoria de pipeline
        st.subheader("🎯 Conversões por Categoria de Pipeline")
        
        conversao_pipeline = df_filtrado.groupby('pipeline_name').agg({
            'hs_object_id': 'count',
            'is_mql': 'sum'
        }).reset_index()
        conversao_pipeline.columns = ['Pipeline', 'Total Leads', 'Leads Qualificados']
        conversao_pipeline['Taxa Conversão (%)'] = (conversao_pipeline['Leads Qualificados'] / conversao_pipeline['Total Leads'] * 100).round(2)
        
        fig_conversao_pipeline = px.bar(conversao_pipeline, x='Pipeline', y='Taxa Conversão (%)',
                                      title="Taxa de Conversão por Pipeline")
        fig_conversao_pipeline.update_xaxes(tickangle=45)
        st.plotly_chart(fig_conversao_pipeline, use_container_width=True)
        
        st.dataframe(conversao_pipeline, use_container_width=True)
        
        # Análise de leads qualificados (agendados)
        if not df_filtrado[df_filtrado['is_mql']].empty:
            st.subheader("Distribuição de Faturamento Anterior para Leads Qualificados")
            fig_mql_faturamento = px.histogram(df_filtrado[df_filtrado['is_mql']], x='faturamento_anterior',
                                               title='Faturamento Anterior de Leads Qualificados', nbins=20)
            st.plotly_chart(fig_mql_faturamento, use_container_width=True)
            
            # Análise de conversão por faixa de faturamento
            st.subheader("Taxa de Conversão por Faixa de Faturamento")
            df_filtrado['faixa_faturamento'] = pd.cut(df_filtrado['faturamento_anterior'], 
                                                     bins=[0, 500000, 1000000, 2000000, 5000000, float('inf')],
                                                     labels=['0-500K', '500K-1M', '1M-2M', '2M-5M', '5M+'])
            
            conversao_faixa = df_filtrado.groupby('faixa_faturamento').apply(
                lambda x: (len(x[x['is_mql']]) / len(x) * 100) if len(x) > 0 else 0
            ).reset_index()
            conversao_faixa.columns = ['Faixa de Faturamento', 'Taxa de Conversão (%)']
            
            fig_conversao_faixa = px.bar(conversao_faixa, x='Faixa de Faturamento', y='Taxa de Conversão (%)',
                                        title='Taxa de Conversão por Faixa de Faturamento')
            st.plotly_chart(fig_conversao_faixa, use_container_width=True)
        else:
            st.info("Nenhum lead qualificado encontrado para análise de ICP.")

    with tab6:
        st.subheader("⚡ Atividades do Time Comercial")

        # NOVA FUNCIONALIDADE: Quantidade de contatos detalhada
        st.subheader("📞 Detalhamento de Contatos")
        
        # Calcular total de atividades usando campos do HubSpot
        df_atividades = df_filtrado.copy()
        df_atividades['total_atividades'] = (df_atividades['hs_call_count'] + 
                                           df_atividades['hs_meeting_count'] + 
                                           df_atividades['hs_sales_email_count'] + 
                                           df_atividades['hs_document_count'] +
                                           df_atividades['hs_marketing_emails_count'] +
                                           df_atividades['hs_form_count'])
        
        # Métricas de contatos
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_chamadas = df_atividades['hs_call_count'].sum()
            st.metric("Total Chamadas", f"{total_chamadas:,}")
        with col2:
            total_reunioes = df_atividades['hs_meeting_count'].sum()
            st.metric("Total Reuniões", f"{total_reunioes:,}")
        with col3:
            total_emails = df_atividades['hs_sales_email_count'].sum()
            st.metric("Total E-mails", f"{total_emails:,}")
        with col4:
            total_contatos = total_chamadas + total_reunioes + total_emails
            st.metric("Total Contatos", f"{total_contatos:,}")
        
        if not df_atividades.empty:
            # Métricas de atividades por colaborador
            atividades_colaborador = df_atividades.groupby('owner_name').agg({
                'hs_call_count': 'sum',
                'hs_meeting_count': 'sum',
                'hs_sales_email_count': 'sum',
                'hs_document_count': 'sum',
                'hs_marketing_emails_count': 'sum',
                'hs_form_count': 'sum',
                'total_atividades': 'sum'
            }).reset_index()
            atividades_colaborador.columns = ['Colaborador', 'Chamadas', 'Reuniões', 'Emails de Vendas', 
                                             'Documentos', 'Emails Marketing', 'Formulários', 'Total de Atividades']
            st.dataframe(atividades_colaborador, use_container_width=True)

            # Gráfico de total de atividades por colaborador
            fig_total_atividades = px.bar(atividades_colaborador, x='Colaborador', y='Total de Atividades',
                                          title='Total de Atividades por Colaborador')
            st.plotly_chart(fig_total_atividades, use_container_width=True)

            # Gráfico de distribuição de tipos de atividades
            atividades_tipos = atividades_colaborador[['Chamadas', 'Reuniões', 'Emails de Vendas', 
                                                      'Documentos', 'Emails Marketing', 'Formulários']].sum().reset_index(name='Quantidade')
            atividades_tipos.columns = ['Tipo de Atividade', 'Quantidade']
            fig_tipos_atividades = px.pie(atividades_tipos, values='Quantidade', names='Tipo de Atividade',
                                          title='Distribuição de Tipos de Atividades')
            st.plotly_chart(fig_tipos_atividades, use_container_width=True)

        else:
            st.info("Nenhum dado de atividade encontrado para os filtros selecionados.")

    # NOVA ABA: Back-end
    with tab7:
        st.subheader("🔧 Back-end - Detalhamento para Verificação")
        st.info("Esta seção contém informações detalhadas para verificação da veracidade dos dados apresentados no dashboard.")
        
        # Seção 1: Configurações e Mapeamentos
        with st.expander("⚙️ Configurações e Mapeamentos", expanded=False):
            st.subheader("👥 Mapeamento de Colaboradores")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**SDRs:**")
                for id_sdr, nome in sdrs.items():
                    st.write(f"- {id_sdr}: {nome}")
            with col2:
                st.write("**Closers:**")
                for id_closer, nome in closers.items():
                    st.write(f"- {id_closer}: {nome}")
            
            st.subheader("🔄 Mapeamento de Pipelines")
            for id_pipeline, nome in pipelines.items():
                st.write(f"- {id_pipeline}: {nome}")
        
        # Seção 2: Campos do HubSpot
        with st.expander("📋 Campos do HubSpot Utilizados", expanded=False):
            st.subheader("Campos e Descrições")
            campos_df = pd.DataFrame(list(hubspot_fields.items()), columns=['Campo', 'Descrição'])
            st.dataframe(campos_df, use_container_width=True)
        
        # Seção 3: Dados Brutos Filtrados
        with st.expander("📊 Dados Brutos (Amostra)", expanded=False):
            st.subheader("Amostra dos Dados Filtrados")
            st.write(f"Total de registros: {len(df_filtrado):,}")
            st.dataframe(df_filtrado.head(100), use_container_width=True)
        
        # Seção 4: Cálculos de Métricas
        with st.expander("🧮 Detalhamento dos Cálculos", expanded=False):
            st.subheader("Cálculos das Métricas Principais")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Métricas SDR:**")
                st.write(f"- Total Leads SDR: {total_leads_sdr:,}")
                st.write(f"- Leads Qualificados: {leads_qualificados_sdr:,}")
                st.write(f"- Critério Qualificação: Estágios 'Agendado', 'No-Show', 'Reagendado'")
                st.write(f"- Taxa Conversão: {taxa_conversao_sdr:.2f}%")
                st.write(f"- Fórmula: (Qualificados / Total) * 100")
            
            with col2:
                st.write("**Métricas Closer:**")
                st.write(f"- Total Negócios: {total_negocios_closer:,}")
                st.write(f"- Negócios Ganhos: {negocios_ganhos:,}")
                st.write(f"- Taxa Conversão: {taxa_conversao_closer:.2f}%")
                st.write(f"- Ticket Médio: {formatar_valor(ticket_medio_closer)}")
        
        # Seção 5: Distribuições Estatísticas
        with st.expander("📈 Distribuições Estatísticas", expanded=False):
            st.subheader("Distribuição por Estágios")
            dist_estagios = df_filtrado['deal_stage'].value_counts().reset_index()
            dist_estagios.columns = ['Estágio', 'Quantidade']
            fig_dist_estagios = px.bar(dist_estagios, x='Estágio', y='Quantidade',
                                     title="Distribuição de Leads por Estágio")
            st.plotly_chart(fig_dist_estagios, use_container_width=True)
            
            st.subheader("Distribuição por Responsável")
            dist_responsavel = df_filtrado['responsavel'].value_counts().reset_index()
            dist_responsavel.columns = ['Responsável', 'Quantidade']
            fig_dist_responsavel = px.pie(dist_responsavel, values='Quantidade', names='Responsável',
                                        title="Distribuição de Leads por Tipo de Responsável")
            st.plotly_chart(fig_dist_responsavel, use_container_width=True)
        
        # Seção 6: Validação de Dados
        with st.expander("✅ Validação de Dados", expanded=False):
            st.subheader("Verificações de Integridade")
            
            # Verificar dados nulos
            st.write("**Campos com Valores Nulos:**")
            nulos = df_filtrado.isnull().sum()
            nulos_df = nulos[nulos > 0].reset_index()
            if not nulos_df.empty:
                nulos_df.columns = ['Campo', 'Quantidade Nulos']
                st.dataframe(nulos_df, use_container_width=True)
            else:
                st.success("Nenhum valor nulo encontrado nos dados filtrados.")
            
            # Verificar consistência de datas
            st.write("**Verificação de Datas:**")
            data_min = df_filtrado['createdate'].min()
            data_max = df_filtrado['createdate'].max()
            st.write(f"- Data mais antiga: {data_min}")
            st.write(f"- Data mais recente: {data_max}")
            st.write(f"- Período total: {(data_max - data_min).days} dias")
            
            # Verificar valores de amount
            st.write("**Verificação de Valores:**")
            valor_min = df_filtrado['amount'].min()
            valor_max = df_filtrado['amount'].max()
            valor_medio = df_filtrado['amount'].mean()
            st.write(f"- Valor mínimo: {formatar_valor(valor_min)}")
            st.write(f"- Valor máximo: {formatar_valor(valor_max)}")
            st.write(f"- Valor médio: {formatar_valor(valor_medio)}")
        
        # Seção 7: Logs de Filtros Aplicados
        with st.expander("🔍 Filtros Aplicados", expanded=False):
            st.subheader("Filtros Ativos")
            st.write(f"- Pipeline: {pipeline_selecionado}")
            st.write(f"- Fase: {fase_selecionada}")
            st.write(f"- Colaborador: {colaborador_selecionado}")
            st.write(f"- Tipo de Data: {tipo_data}")
            st.write(f"- Data Início: {data_inicio}")
            st.write(f"- Data Fim: {data_fim}")
            st.write(f"- Registros após filtros: {len(df_filtrado):,} de {len(df):,} total")


if __name__ == "__main__":
    main()

