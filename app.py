import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re

# Configuração da página
st.set_page_config(
    page_title="Framework TMMi - TAG IMF",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 1rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .hero-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .status-adotado {
        background-color: #d4edda;
        color: #155724;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.85rem;
        display: inline-block;
    }
    .status-desenvolvendo {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.85rem;
        display: inline-block;
    }
    .status-em-adocao {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.85rem;
        display: inline-block;
    }
    .status-nao-iniciado {
        background-color: #e2e3e5;
        color: #383d41;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.85rem;
        display: inline-block;
    }
    .area-box {
        background-color: #f8f9fa;
        border-left: 5px solid #667eea;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .nivel-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: bold;
    }
    .diff-box {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .match-box {
        background: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Funções de cálculo
def normalizar_area(area_raw):
    """Normaliza nome da área de processo"""
    if pd.isna(area_raw):
        return None, None
    
    area = str(area_raw).strip()
    
    # Se tem múltiplos níveis, pega o maior
    if '\n' in area:
        linhas = [l.strip() for l in area.split('\n') if l.strip()]
        niveis = []
        for linha in linhas:
            match = re.search(r'N(\d+)', linha)
            if match:
                niveis.append((int(match.group(1)), linha))
        
        if niveis:
            area = max(niveis, key=lambda x: x[0])[1]
    
    # Extrair nível
    nivel_match = re.search(r'N(\d+)', area)
    nivel = f"Nível {nivel_match.group(1)}" if nivel_match else None
    
    # Normalizar nome
    area_lower = area.lower()
    
    if 'política' in area_lower:
        nome_area = "Política e Estratégia de Testes"
    elif 'planejamento' in area_lower:
        nome_area = "Planejamento de Testes"
    elif 'monitoramento' in area_lower or 'controle' in area_lower:
        nome_area = "Monitoramento e Controle dos Testes"
    elif 'desenho' in area_lower or 'execução' in area_lower:
        nome_area = "Desenho e Execução de Testes"
    elif 'defeito' in area_lower or 'gerenciamento' in area_lower:
        nome_area = "Gerenciamento de Defeitos"
    elif 'ambiente' in area_lower:
        nome_area = "Ambiente de Testes"
    elif 'organização' in area_lower:
        nome_area = "Organização de Testes"
    elif 'treinamento' in area_lower:
        nome_area = "Programa de Treinamento em Testes"
    elif 'integração' in area_lower or 'sdlc' in area_lower:
        nome_area = "Integração dos Testes ao SDLC"
    elif 'não funcionais' in area_lower or 'nfr' in area_lower:
        nome_area = "Testes Não Funcionais"
    elif 'revisões' in area_lower or 'review' in area_lower or 'técnicas' in area_lower:
        nome_area = "Revisões Técnicas (Quality Review)"
    elif 'medição' in area_lower:
        nome_area = "Medição dos Testes"
    elif 'avaliação' in area_lower:
        nome_area = "Avaliação da Qualidade do Produto"
    elif 'prevenção' in area_lower:
        nome_area = "Prevenção de Defeitos"
    elif 'otimização' in area_lower:
        nome_area = "Otimização do Processo de Testes"
    elif 'controle da qualidade' in area_lower:
        nome_area = "Controle da Qualidade"
    elif 'avançadas' in area_lower:
        nome_area = "Revisões Avançadas"
    else:
        nome_area = area.split('–')[1].strip() if '–' in area else area
    
    return nivel, nome_area

def calcular_status(scores):
    """Calcula status baseado em lista de scores"""
    scores = [s for s in scores if pd.notna(s) and s > 0]
    
    if not scores:
        return "Não Iniciado", 0, {}
    
    total = len(scores)
    score_3 = sum(1 for s in scores if s >= 3)
    score_2_mais = sum(1 for s in scores if s >= 2)
    score_1_mais = sum(1 for s in scores if s >= 1)
    
    perc_3 = score_3 / total
    perc_2 = score_2_mais / total
    perc_1 = score_1_mais / total
    
    detalhes = {
        'total': total,
        'score_3': score_3,
        'score_2_mais': score_2_mais,
        'score_1_mais': score_1_mais,
        'perc_3': perc_3,
        'perc_2': perc_2,
        'perc_1': perc_1,
        'media': sum(scores) / total
    }
    
    if perc_3 >= 0.8:
        return "Adotado", perc_3, detalhes
    elif perc_2 >= 0.5:
        return "Em Adoção", perc_2, detalhes
    elif perc_1 >= 0.3:
        return "Desenvolvendo", perc_1, detalhes
    else:
        return "Não Iniciado", 0, detalhes

# Carregar dados
@st.cache_data
def load_data():
    file_path = 'Framework_-_TMMi-TAG__1_.xlsx'
    
    try:
        # Visão Institucional (Manual)
        df_inst = pd.read_excel(file_path, sheet_name='TMMi - Visão Institucional', skiprows=2)
        df_inst.columns = ['Col0', 'Nível TMMi', 'Área de Processo', 'Status Institucional', 'Observação']
        df_inst['Nível TMMi'] = df_inst['Nível TMMi'].ffill()
        df_inst = df_inst[df_inst['Área de Processo'].notna()].drop('Col0', axis=1)
        
        # Score TMMi (para cálculo automático)
        df_score = pd.read_excel(file_path, sheet_name='Score TMMi', skiprows=2)
        df_score_clean = df_score[
            (df_score['ID_MELHORIA'].notna()) & 
            (df_score['ID_MELHORIA'] != 'ID_MELHORIA') &
            (df_score['SCORE'].notna()) &
            (pd.to_numeric(df_score['SCORE'], errors='coerce').notna())
        ].copy()
        df_score_clean['SCORE'] = pd.to_numeric(df_score_clean['SCORE'])
        
        # Normalizar áreas no Score
        df_score_clean[['NIVEL', 'AREA_NOME']] = df_score_clean['NÍVEL E ÁREA DE PROCESSO'].apply(
            lambda x: pd.Series(normalizar_area(x))
        )
        
        # Calcular status automático por área
        status_calculado = {}
        for (nivel, area), group in df_score_clean.groupby(['NIVEL', 'AREA_NOME']):
            if nivel and area:
                scores = group['SCORE'].tolist()
                status, perc, detalhes = calcular_status(scores)
                status_calculado[f"{nivel}|{area}"] = {
                    'nivel': nivel,
                    'area': area,
                    'status': status,
                    'percentual': perc,
                    'detalhes': detalhes
                }
        
        # Roadmap
        df_roadmap = pd.read_excel(file_path, sheet_name='ANUAL - Roadmap por Squads')
        
        # Visão Squads
        df_squads = pd.read_excel(file_path, sheet_name='TMMi - Visão Squads', skiprows=3)
        
        return {
            'institucional': df_inst,
            'score': df_score_clean,
            'status_calculado': status_calculado,
            'roadmap': df_roadmap,
            'squads': df_squads
        }
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

def calcular_metricas(df):
    total = len(df)
    adotado = len(df[df['Status Institucional'] == 'Adotado'])
    desenvolvendo = len(df[df['Status Institucional'] == 'Desenvolvendo'])
    em_adocao = len(df[df['Status Institucional'] == 'Em Adoção'])
    nao_iniciado = len(df[df['Status Institucional'] == 'Não Iniciado'])
    
    score = (adotado * 3 + em_adocao * 2 + desenvolvendo * 1.5) / total
    score_5 = score / 3 * 5
    
    return {
        'total': total,
        'adotado': adotado,
        'desenvolvendo': desenvolvendo,
        'em_adocao': em_adocao,
        'nao_iniciado': nao_iniciado,
        'score_3': score,
        'score_5': score_5
    }

def calcular_nivel_completo(df, nivel):
    df_nivel = df[df['Nível TMMi'] == nivel]
    if len(df_nivel) == 0:
        return 0, 0, 0
    total = len(df_nivel)
    adotado = len(df_nivel[df_nivel['Status Institucional'] == 'Adotado'])
    percentual = (adotado / total * 100) if total > 0 else 0
    return adotado, total, percentual

try:
    data = load_data()
    
    if data is None:
        st.stop()
    
    df_inst = data['institucional']
    status_calc = data['status_calculado']
    metricas = calcular_metricas(df_inst)
    
    # Header
    st.markdown('<div class="main-header">🎯 Framework TMMi - TAG IMF</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><strong>De Subjetivo para Objetivo</strong> | <strong>De Percepção para Evidência</strong></div>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📊 Navegação")
    pagina = st.sidebar.radio(
        "Escolha a visualização:",
        [
            "🏠 Visão Executiva",
            "📋 Áreas por Nível",
            "🔍 Manual vs Automático",
            "👥 Visão por Squads",
            "🗓️ Roadmap 2026",
            "💡 Por que TMMi?"
        ]
    )
    
    # ================== VISÃO EXECUTIVA ==================
    if pagina == "🏠 Visão Executiva":
        
        nivel2_adotado, nivel2_total, nivel2_perc = calcular_nivel_completo(df_inst, 'Nível 2')
        nivel3_adotado, nivel3_total, nivel3_perc = calcular_nivel_completo(df_inst, 'Nível 3')
        
        st.markdown(f"""
        <div class="hero-box">
            <h1 style="margin: 0; font-size: 2.5rem;">🎉 TAG IMF: NÍVEL 2 DO TMMi ALCANÇADO!</h1>
            <p style="font-size: 1.3rem; margin: 1rem 0;">
                <strong>{nivel2_perc:.0f}%</strong> das áreas do Nível 2 (Gerenciado) adotadas<br/>
                Caminhando para Nível 3: <strong>{nivel3_perc:.0f}%</strong> já iniciado
            </p>
            <h2 style="font-size: 2rem; margin-top: 1rem;">Score: {metricas['score_5']:.1f}/5.0</h2>
            <p style="font-size: 1.1rem;">✅ Saímos do improviso para o processo gerenciado!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{metricas['total']}</div>
                <div class="metric-label">Áreas Mapeadas</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="border-color: #28a745;">
                <div class="metric-value" style="color: #28a745;">{metricas['adotado']}</div>
                <div class="metric-label">Adotado ({metricas['adotado']/metricas['total']*100:.0f}%)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card" style="border-color: #17a2b8;">
                <div class="metric-value" style="color: #17a2b8;">{metricas['em_adocao']}</div>
                <div class="metric-label">Em Adoção ({metricas['em_adocao']/metricas['total']*100:.0f}%)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card" style="border-color: #ffc107;">
                <div class="metric-value" style="color: #ffc107;">{metricas['desenvolvendo']}</div>
                <div class="metric-label">Desenvolvendo ({metricas['desenvolvendo']/metricas['total']*100:.0f}%)</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Maturidade por Nível")
            
            niveis_data = []
            for nivel in ['Nível 2', 'Nível 3', 'Nível 4', 'Nível 5']:
                adotado, total, perc = calcular_nivel_completo(df_inst, nivel)
                niveis_data.append({
                    'Nível': nivel.replace('Nível ', 'N'),
                    'Adotado': adotado,
                    'Pendente': total - adotado
                })
            
            df_niveis = pd.DataFrame(niveis_data)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Adotado',
                x=df_niveis['Nível'],
                y=df_niveis['Adotado'],
                marker_color='#28a745',
                text=df_niveis['Adotado'],
                textposition='auto'
            ))
            fig.add_trace(go.Bar(
                name='Pendente',
                x=df_niveis['Nível'],
                y=df_niveis['Pendente'],
                marker_color='#e0e0e0',
                text=df_niveis['Pendente'],
                textposition='auto'
            ))
            
            fig.update_layout(barmode='stack', height=400, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Distribuição de Status")
            
            labels = ['Adotado', 'Em Adoção', 'Desenvolvendo', 'Não Iniciado']
            values = [metricas['adotado'], metricas['em_adocao'], metricas['desenvolvendo'], metricas['nao_iniciado']]
            colors = ['#28a745', '#17a2b8', '#ffc107', '#6c757d']
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.4,
                marker_colors=colors,
                textinfo='label+percent',
                textfont_size=14
            )])
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Destaques
        st.markdown("---")
        st.subheader("📈 Destaques por Nível")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            ### ✅ Nível 2 - Gerenciado
            **{nivel2_adotado}/{nivel2_total} áreas adotadas ({nivel2_perc:.0f}%)**
            
            **Áreas Adotadas:**
            """)
            
            nivel2_areas = df_inst[df_inst['Nível TMMi'] == 'Nível 2']
            for idx, row in nivel2_areas.iterrows():
                if row['Status Institucional'] == 'Adotado':
                    st.markdown(f"- ✅ {row['Área de Processo']}")
            
            st.markdown("**Falta apenas:**")
            for idx, row in nivel2_areas.iterrows():
                if row['Status Institucional'] != 'Adotado':
                    st.markdown(f"- 🔄 {row['Área de Processo']} ({row['Status Institucional']})")
        
        with col2:
            st.markdown(f"""
            ### 🔄 Nível 3 - Definido
            **{nivel3_adotado}/{nivel3_total} áreas adotadas ({nivel3_perc:.0f}%)**
            
            **Em Progresso:**
            """)
            
            nivel3_areas = df_inst[df_inst['Nível TMMi'] == 'Nível 3']
            for idx, row in nivel3_areas.iterrows():
                status = row['Status Institucional']
                emoji = "✅" if status == "Adotado" else "📊" if status == "Em Adoção" else "🔄"
                st.markdown(f"- {emoji} {row['Área de Processo']} ({status})")
    
    # ================== ÁREAS POR NÍVEL ==================
    elif pagina == "📋 Áreas por Nível":
        st.header("📋 Áreas de Processo por Nível TMMi")
        
        for nivel in ['Nível 2', 'Nível 3', 'Nível 4', 'Nível 5']:
            df_nivel = df_inst[df_inst['Nível TMMi'] == nivel]
            
            if len(df_nivel) > 0:
                adotado, total, perc = calcular_nivel_completo(df_inst, nivel)
                
                st.markdown(f"""
                <div class="nivel-header">
                    {nivel} - {adotado}/{total} adotadas ({perc:.0f}%)
                </div>
                """, unsafe_allow_html=True)
                
                for idx, row in df_nivel.iterrows():
                    area = row['Área de Processo']
                    status = row['Status Institucional']
                    obs = row['Observação'] if pd.notna(row['Observação']) else 'N/A'
                    
                    status_class = "status-adotado" if status == "Adotado" else \
                                   "status-desenvolvendo" if status == "Desenvolvendo" else \
                                   "status-em-adocao" if status == "Em Adoção" else \
                                   "status-nao-iniciado"
                    
                    emoji = "✅" if status == "Adotado" else \
                            "🔄" if status == "Desenvolvendo" else \
                            "📊" if status == "Em Adoção" else "⏸️"
                    
                    st.markdown(f"""
                    <div class="area-box">
                        <strong>{emoji} {area}</strong>
                        <span class="{status_class}" style="float: right;">{status}</span>
                        <br/>
                        <small style="color: #666; margin-top: 0.5rem; display: block;">{obs}</small>
                    </div>
                    """, unsafe_allow_html=True)
    
    # ================== MANUAL VS AUTOMÁTICO ==================
    elif pagina == "🔍 Manual vs Automático":
        st.header("🔍 Comparação: Manual vs Automático")
        st.markdown("**Compare o status atual (manual) com o status calculado automaticamente baseado no Score TMMi**")
        
        st.info("💡 **Como funciona:** O status automático é calculado baseado nos scores das melhorias. Se 80%+ das melhorias têm Score 3, a área é 'Adotado'. Se 50%+ têm Score ≥2, é 'Em Adoção', e assim por diante.")
        
        for nivel in ['Nível 2', 'Nível 3']:
            df_nivel = df_inst[df_inst['Nível TMMi'] == nivel]
            
            if len(df_nivel) > 0:
                st.markdown(f"""
                <div class="nivel-header">
                    {nivel}
                </div>
                """, unsafe_allow_html=True)
                
                for idx, row in df_nivel.iterrows():
                    area = row['Área de Processo']
                    status_manual = row['Status Institucional']
                    
                    # Buscar status calculado
                    chave = f"{nivel}|{area}"
                    status_auto = None
                    detalhes = None
                    
                    for key, value in status_calc.items():
                        if value['area'] in area or area in value['area']:
                            if value['nivel'] == nivel:
                                status_auto = value['status']
                                detalhes = value['detalhes']
                                break
                    
                    # Verificar se bate
                    if status_auto:
                        match = status_manual == status_auto
                        box_class = "match-box" if match else "diff-box"
                        emoji = "✅" if match else "⚠️"
                        
                        st.markdown(f"""
                        <div class="{box_class}">
                            <strong>{emoji} {area}</strong>
                            <br/><br/>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                                <div>
                                    <strong>📋 Manual:</strong> {status_manual}
                                </div>
                                <div>
                                    <strong>🤖 Calculado:</strong> {status_auto}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if detalhes:
                            st.markdown(f"""
                            <br/>
                            <small style="color: #666;">
                                📊 Baseado em {detalhes['total']} melhorias | 
                                Score médio: {detalhes['media']:.1f} | 
                                Score 3: {detalhes['score_3']}/{detalhes['total']} ({detalhes['perc_3']*100:.0f}%)
                            </small>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        # Não encontrou cálculo automático
                        st.markdown(f"""
                        <div class="area-box">
                            <strong>❓ {area}</strong>
                            <br/><br/>
                            <strong>📋 Manual:</strong> {status_manual}<br/>
                            <strong>🤖 Calculado:</strong> <em>Sem melhorias mapeadas no Score TMMi</em>
                        </div>
                        """, unsafe_allow_html=True)
    
    # ================== VISÃO POR SQUADS ==================
    elif pagina == "👥 Visão por Squads":
        st.header("👥 Status das Melhorias por Squad")
        st.markdown("**Acompanhamento detalhado das iniciativas por equipe**")
        
        df_squads = data['squads']
        squad_cols = [col for col in df_squads.columns if col not in ['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5']]
        
        st.info(f"📊 **Squads mapeados:** {', '.join(squad_cols)}")
        st.dataframe(df_squads, use_container_width=True, height=600)
    
    # ================== ROADMAP ==================
    elif pagina == "🗓️ Roadmap 2026":
        st.header("🗓️ Roadmap Estratégico 2026")
        st.markdown("**Planejamento transparente de evolução**")
        
        df_roadmap = data['roadmap']
        
        if 'Trimestre' in df_roadmap.columns:
            trimestres = ['Todos'] + sorted(df_roadmap['Trimestre'].unique().tolist())
            trimestre_sel = st.selectbox("Filtrar por Trimestre:", trimestres)
            
            if trimestre_sel != 'Todos':
                df_filtrado = df_roadmap[df_roadmap['Trimestre'] == trimestre_sel]
            else:
                df_filtrado = df_roadmap
        else:
            df_filtrado = df_roadmap
        
        for idx, row in df_filtrado.iterrows():
            id_melhoria = row.get('ID Melhoria', 'N/A')
            entrega = row.get('Entrega', 'N/A')
            tmmi_area = row.get('TMMi (Nível – Área)', 'N/A')
            status = row.get('Status Geral', 'Planejado')
            responsavel = row.get('Responsável', 'N/A')
            
            status_class = "status-adotado" if 'Adotado' in str(status) else \
                          "status-desenvolvendo" if 'Desenvolvendo' in str(status) else \
                          "status-em-adocao" if 'Adoção' in str(status) else \
                          "status-nao-iniciado"
            
            st.markdown(f"""
            <div class="area-box">
                <strong>{id_melhoria}</strong>: {entrega}
                <span class="{status_class}" style="float: right;">{status}</span>
                <br/>
                <small style="color: #666;"><strong>TMMi:</strong> {tmmi_area}</small><br/>
                <small style="color: #666;"><strong>Responsável:</strong> {responsavel}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # ================== POR QUE TMMi? ==================
    elif pagina == "💡 Por que TMMi?":
        st.header("💡 Por que estruturar o Framework TMMi na TAG?")
        
        st.markdown("""
        <div class="hero-box">
            <h2 style="margin-top: 0;">🎯 O Problema que Resolvemos</h2>
            <p style="font-size: 1.3rem;">
            <strong>ANTES:</strong> Qualidade era percepção.<br/>
            <strong>AGORA:</strong> Qualidade é evidência.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ❌ ANTES (Sem Framework)
            
            **Visão de Qualidade**
            - Subjetiva, varia por squad
            - "Acho que tá bom"
            
            **Avaliação**
            - Percepção individual
            - Conflitos e "achismos"
            
            **Priorização**
            - Sem critério claro
            - "Tudo é importante"
            
            **Automação**
            - Pontual, sem direção
            
            **Incidentes**
            - Reativo, "apaga incêndio"
            """)
        
        with col2:
            st.markdown("""
            ### ✅ AGORA (Com Framework)
            
            **Visão de Qualidade**
            - Linguagem comum
            - Níveis objetivos (1-5)
            
            **Avaliação**
            - Score numérico
            - Baseado em evidências
            
            **Priorização**
            - Roadmap transparente
            - Foco em impacto
            
            **Automação**
            - Direcionada por risco
            
            **Incidentes**
            - Prevenção estruturada
            """)
        
        st.markdown("---")
        
        st.markdown("""
        ### 📊 Ganhos Diretos para a TAG
        
        - ✅ **Menos ruído:** QA, Dev, Produto e Gestão falam a mesma língua
        - ✅ **Avaliação justa:** Baseada em evidências, não em percepção
        - ✅ **Foco certo:** Priorização clara do que evolui primeiro
        - ✅ **Crescimento sustentável:** Práticas escaláveis
        - ✅ **Menos dependência:** Processo sustenta qualidade
        - ✅ **Automação inteligente:** ROI mensurável
        - ✅ **Menos incidentes:** Prevenção ao invés de reação
        - ✅ **Decisão baseada em dados:** Indicadores comparáveis
        - ✅ **Clareza para liderança:** Evolução em níveis claros
        - ✅ **Alinhamento estratégico:** Qualidade = crescimento
        
        ---
        
        ### 🎯 Resumo Executivo
        
        > **O framework TMMi na TAG não é sobre "seguir um modelo", é sobre criar 
        > previsibilidade, reduzir risco e sustentar o crescimento da empresa de 
        > forma prática e transparente.**
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>Framework TMMi - TAG IMF</strong></p>
        <p>Atualizado em: {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
        <p style='font-size: 0.9rem;'>De Subjetivo para Objetivo | De Percepção para Evidência</p>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ Erro: {str(e)}")
    st.info("💡 Certifique-se de que o arquivo 'Framework_-_TMMi-TAG__1_.xlsx' está no mesmo diretório do app.")
