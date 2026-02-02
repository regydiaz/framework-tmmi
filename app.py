import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="QA Accelerate - TAG IMF",
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
        background-color: #f8d7da;
        color: #721c24;
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
</style>
""", unsafe_allow_html=True)

# Carregar dados
@st.cache_data
def load_data():
    file_path = 'Framework_-_TMMi-TAG__1_.xlsx'
    
    try:
        # Visão Institucional
        df_inst = pd.read_excel(file_path, sheet_name='TMMi - Visão Institucional', skiprows=2)
        df_inst.columns = ['Col0', 'Nível TMMi', 'Área de Processo', 'Status Institucional', 'Observação']
        df_inst['Nível TMMi'] = df_inst['Nível TMMi'].ffill()
        df_inst = df_inst[df_inst['Área de Processo'].notna()].drop('Col0', axis=1)
        
        # Visão Squads
        df_squads = pd.read_excel(file_path, sheet_name='TMMi - Visão Squads', skiprows=3)
        
        # Renomear colunas Unnamed
        rename_map = {}
        squad_names = ['ID', 'Trimestre', 'Fase', 'Nível e Área', 'Envolvidos', 'Status', 
                       'Ativos', 'Demonstrações', 'Operações', 'Plataforma', 'Interop', 'Negotiation', 'Consent']
        
        for i, col in enumerate(df_squads.columns):
            if i < len(squad_names):
                rename_map[col] = squad_names[i]
        
        df_squads = df_squads.rename(columns=rename_map)
        df_squads = df_squads.dropna(how='all')
        
        # Roadmap
        df_roadmap = pd.read_excel(file_path, sheet_name='ANUAL - Roadmap por Squads')
        
        return {
            'institucional': df_inst,
            'squads': df_squads,
            'roadmap': df_roadmap
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
    
    score = (adotado * 3 + em_adocao * 2 + desenvolvendo * 1.5) / total if total > 0 else 0
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
        return 0, 0, 0, 0, 0
    
    total = len(df_nivel)
    adotado = len(df_nivel[df_nivel['Status Institucional'] == 'Adotado'])
    desenvolvendo = len(df_nivel[df_nivel['Status Institucional'] == 'Desenvolvendo'])
    em_adocao = len(df_nivel[df_nivel['Status Institucional'] == 'Em Adoção'])
    nao_iniciado = len(df_nivel[df_nivel['Status Institucional'] == 'Não Iniciado'])
    
    percentual = (adotado / total * 100) if total > 0 else 0
    return adotado, desenvolvendo, em_adocao, nao_iniciado, percentual

def estilizar_squads_df(df):
    """Aplica cores nas células baseado no status"""
    
    # Colunas de squads (últimas 7)
    squad_cols = ['Ativos', 'Demonstrações', 'Operações', 'Plataforma', 'Interop', 'Negotiation', 'Consent']
    
    def color_status(val):
        val_str = str(val).strip().upper()
        
        if 'ADOTADO' in val_str or 'ADOTADA' in val_str:
            return 'background-color: #d4edda; color: #155724; font-weight: bold;'
        elif 'PLANEJADO' in val_str or 'PLANEJADA' in val_str:
            return 'background-color: #fff3cd; color: #856404; font-weight: bold;'
        elif 'DESENVOLVENDO' in val_str:
            return 'background-color: #ffe5b4; color: #856404; font-weight: bold;'
        elif 'ADOÇÃO' in val_str or 'EM ADOÇÃO' in val_str:
            return 'background-color: #d1ecf1; color: #0c5460; font-weight: bold;'
        elif 'NÃO INICIADO' in val_str or 'NAO INICIADO' in val_str:
            return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
        else:
            return ''
    
    # Aplicar estilo apenas nas colunas de squads
    styled_df = df.style.applymap(color_status, subset=squad_cols)
    
    return styled_df

try:
    data = load_data()
    
    if data is None:
        st.stop()
    
    df_inst = data['institucional']
    df_squads = data['squads']
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
            "👥 Visão por Squads",
            "🗓️ Roadmap 2026",
            "💡 Por que TMMi?"
        ]
    )
    
    # ================== VISÃO EXECUTIVA ==================
    if pagina == "🏠 Visão Executiva":
        
        nivel2_adotado, nivel2_desenv, nivel2_em_adocao, nivel2_nao_init, nivel2_perc = calcular_nivel_completo(df_inst, 'Nível 2')
        nivel3_adotado, nivel3_desenv, nivel3_em_adocao, nivel3_nao_init, nivel3_perc = calcular_nivel_completo(df_inst, 'Nível 3')
        
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
        
        # Métricas em cards
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
            
            # CORRIGIDO: Mostrar TODOS os status
            niveis_data = []
            for nivel in ['Nível 2', 'Nível 3', 'Nível 4', 'Nível 5']:
                adot, desenv, em_adoc, nao_init, perc = calcular_nivel_completo(df_inst, nivel)
                niveis_data.append({
                    'Nível': nivel.replace('Nível ', 'N'),
                    'Adotado': adot,
                    'Em Adoção': em_adoc,
                    'Desenvolvendo': desenv,
                    'Não Iniciado': nao_init
                })
            
            df_niveis = pd.DataFrame(niveis_data)
            
            fig = go.Figure()
            
            # Adotado (verde)
            fig.add_trace(go.Bar(
                name='Adotado',
                x=df_niveis['Nível'],
                y=df_niveis['Adotado'],
                marker_color='#28a745',
                text=df_niveis['Adotado'],
                textposition='auto'
            ))
            
            # Em Adoção (azul)
            fig.add_trace(go.Bar(
                name='Em Adoção',
                x=df_niveis['Nível'],
                y=df_niveis['Em Adoção'],
                marker_color='#17a2b8',
                text=df_niveis['Em Adoção'],
                textposition='auto'
            ))
            
            # Desenvolvendo (amarelo)
            fig.add_trace(go.Bar(
                name='Desenvolvendo',
                x=df_niveis['Nível'],
                y=df_niveis['Desenvolvendo'],
                marker_color='#ffc107',
                text=df_niveis['Desenvolvendo'],
                textposition='auto'
            ))
            
            # Não Iniciado (cinza)
            fig.add_trace(go.Bar(
                name='Não Iniciado',
                x=df_niveis['Nível'],
                y=df_niveis['Não Iniciado'],
                marker_color='#dc3545',
                text=df_niveis['Não Iniciado'],
                textposition='auto'
            ))
            
            fig.update_layout(
                barmode='stack',
                height=400,
                showlegend=True,
                xaxis_title="Nível TMMi",
                yaxis_title="Número de Áreas"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Distribuição de Status")
            
            labels = ['Adotado', 'Em Adoção', 'Desenvolvendo', 'Não Iniciado']
            values = [metricas['adotado'], metricas['em_adocao'], metricas['desenvolvendo'], metricas['nao_iniciado']]
            colors = ['#28a745', '#17a2b8', '#ffc107', '#dc3545']
            
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
        
        # Destaques por nível
        st.markdown("---")
        st.subheader("📈 Destaques por Nível")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nivel2_total = nivel2_adotado + nivel2_desenv + nivel2_em_adocao + nivel2_nao_init
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
            nivel3_total = nivel3_adotado + nivel3_desenv + nivel3_em_adocao + nivel3_nao_init
            st.markdown(f"""
            ### 🔄 Nível 3 - Definido
            **{nivel3_adotado}/{nivel3_total} áreas adotadas ({nivel3_perc:.0f}%)**
            
            **Em Progresso:**
            """)
            
            nivel3_areas = df_inst[df_inst['Nível TMMi'] == 'Nível 3']
            for idx, row in nivel3_areas.iterrows():
                status = row['Status Institucional']
                emoji = "✅" if status == "Adotado" else \
                        "📊" if status == "Em Adoção" else \
                        "🔄" if status == "Desenvolvendo" else "⏸️"
                st.markdown(f"- {emoji} {row['Área de Processo']} ({status})")
    
    # ================== ÁREAS POR NÍVEL ==================
    elif pagina == "📋 Áreas por Nível":
        st.header("📋 Áreas de Processo por Nível TMMi")
        
        for nivel in ['Nível 2', 'Nível 3', 'Nível 4', 'Nível 5']:
            df_nivel = df_inst[df_inst['Nível TMMi'] == nivel]
            
            if len(df_nivel) > 0:
                adot, desenv, em_adoc, nao_init, perc = calcular_nivel_completo(df_inst, nivel)
                total = adot + desenv + em_adoc + nao_init
                
                st.markdown(f"""
                <div class="nivel-header">
                    {nivel} - {adot}/{total} adotadas ({perc:.0f}%)
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
    
    # ================== VISÃO POR SQUADS ==================
    elif pagina == "👥 Visão por Squads":
        st.header("👥 Status das Melhorias por Squad")
        st.markdown("**Acompanhamento detalhado das iniciativas por equipe**")
        
        squad_cols = ['Ativos', 'Demonstrações', 'Operações', 'Plataforma', 'Interop', 'Negotiation', 'Consent']
        
        st.info(f"📊 **Squads mapeados:** {', '.join(squad_cols)}")
        
        # Aplicar cores
        styled_df = estilizar_squads_df(df_squads)
        
        st.dataframe(styled_df, use_container_width=True, height=600)
        
        st.markdown("""
        **Legenda:**
        - 🟢 **Verde**: Adotado
        - 🔵 **Azul**: Em Adoção
        - 🟡 **Amarelo**: Planejado
        - 🟠 **Laranja**: Desenvolvendo
        - 🔴 **Vermelho**: Não Iniciado
        """)
    
    # ================== ROADMAP ==================
    elif pagina == "🗓️ Roadmap 2026":
        st.header("🗓️ Roadmap Estratégico 2026")
        st.markdown("**Planejamento transparente de evolução**")
        
        df_roadmap = data['roadmap']
        
        if 'Trimestre' in df_roadmap.columns:
            trimestres = ['Todos'] + sorted(df_roadmap['Trimestre'].dropna().unique().tolist())
            trimestre_sel = st.selectbox("Filtrar por Trimestre:", trimestres)
            
            if trimestre_sel != 'Todos':
                df_filtrado = df_roadmap[df_roadmap['Trimestre'] == trimestre_sel]
            else:
                df_filtrado = df_roadmap
        else:
            df_filtrado = df_roadmap
        
        for idx, row in df_filtrado.iterrows():
            if pd.isna(row.get('ID Melhoria')):
                continue
                
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
            
            - Visão subjetiva, varia por squad
            - Avaliação baseada em percepção
            - Sem critério claro de priorização
            - Automação pontual, sem direção
            - Reativo: "apaga incêndio"
            """)
        
        with col2:
            st.markdown("""
            ### ✅ AGORA (Com Framework)
            
            - Linguagem comum, níveis objetivos
            - Score numérico baseado em evidências
            - Roadmap transparente, foco em impacto
            - Automação direcionada por risco
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
    import traceback
    st.code(traceback.format_exc())
