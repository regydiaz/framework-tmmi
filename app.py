import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

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
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .status-adotado {
        background-color: #d4edda;
        color: #155724;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .status-desenvolvendo {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .status-planejado {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .status-em-adocao {
        background-color: #e2e3e5;
        color: #383d41;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Carregar dados
@st.cache_data
def load_data():
    file_path = '/mnt/user-data/uploads/Framework_-_TMMi-TAG.xlsx'
    
    # Visão Institucional
    df_institucional = pd.read_excel(file_path, sheet_name='TMMi - Visão Institucional', header=2)
    df_institucional.columns = ['Nível TMMi', 'Área de Processo', 'Status Institucional', 'Observação', 'Extra']
    df_institucional = df_institucional.dropna(subset=['Área de Processo'])
    
    # Visão Squads
    df_squads = pd.read_excel(file_path, sheet_name='TMMi - Visão Squads', header=2)
    
    # Roadmap Trimestral
    df_roadmap = pd.read_excel(file_path, sheet_name='Roadmap Trimestral', header=1)
    
    # Score TMMi
    df_score = pd.read_excel(file_path, sheet_name='Score TMMi', header=2)
    
    # Mapa do TMMi
    df_mapa = pd.read_excel(file_path, sheet_name='Mapa do TMMi', header=2)
    
    # Critérios TMMi
    df_criterios = pd.read_excel(file_path, sheet_name='Critérios TMMi', header=0)
    
    return {
        'institucional': df_institucional,
        'squads': df_squads,
        'roadmap': df_roadmap,
        'score': df_score,
        'mapa': df_mapa,
        'criterios': df_criterios
    }

try:
    data = load_data()
    
    # Header
    st.markdown('<div class="main-header">🎯 Framework TMMi - TAG IMF</div>', unsafe_allow_html=True)
    
    # Sidebar para navegação
    st.sidebar.title("📊 Navegação")
    pagina = st.sidebar.radio(
        "Escolha a visualização:",
        [
            "🏠 Visão Geral",
            "🏢 Visão Institucional", 
            "👥 Visão por Squads",
            "🗓️ Roadmap Trimestral",
            "📈 Score TMMi",
            "🗺️ Mapa do TMMi",
            "📋 Critérios de Entrega"
        ]
    )
    
    # Seção de exportação
    st.sidebar.markdown("---")
    st.sidebar.title("📥 Exportar")
    st.sidebar.markdown("Gere relatórios para apresentação")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("📄 PDF", use_container_width=True):
            with st.spinner("Gerando PDF..."):
                try:
                    from exporter import TMMiExporter
                    exporter = TMMiExporter(data)
                    pdf_path = exporter.export_to_pdf()
                    st.sidebar.success("✅ PDF gerado!")
                    with open(pdf_path, 'rb') as f:
                        st.sidebar.download_button(
                            label="⬇️ Baixar PDF",
                            data=f,
                            file_name="Framework_TMMi_Relatorio.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                except Exception as e:
                    st.sidebar.error(f"Erro: {str(e)}")
    
    with col2:
        if st.button("📊 PPT", use_container_width=True):
            with st.spinner("Gerando PowerPoint..."):
                try:
                    from exporter import TMMiExporter
                    exporter = TMMiExporter(data)
                    ppt_path = exporter.export_to_powerpoint()
                    st.sidebar.success("✅ PPT gerado!")
                    with open(ppt_path, 'rb') as f:
                        st.sidebar.download_button(
                            label="⬇️ Baixar PPT",
                            data=f,
                            file_name="Framework_TMMi_Apresentacao.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            use_container_width=True
                        )
                except Exception as e:
                    st.sidebar.error(f"Erro: {str(e)}")
    
    # ================== VISÃO GERAL ==================
    if pagina == "🏠 Visão Geral":
        st.header("📊 Dashboard Executivo")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        # Calcular métricas
        df_inst = data['institucional']
        total_areas = len(df_inst)
        adotado = len(df_inst[df_inst['Status Institucional'] == 'Adotado'])
        desenvolvendo = len(df_inst[df_inst['Status Institucional'] == 'Desenvolvendo'])
        em_adocao = len(df_inst[df_inst['Status Institucional'] == 'Em Adoção'])
        
        with col1:
            st.metric("Total de Áreas", total_areas, help="Total de áreas de processo TMMi mapeadas")
        with col2:
            st.metric("Adotado", adotado, delta=f"{(adotado/total_areas*100):.0f}%", help="Áreas totalmente adotadas")
        with col3:
            st.metric("Desenvolvendo", desenvolvendo, delta=f"{(desenvolvendo/total_areas*100):.0f}%", help="Áreas em desenvolvimento")
        with col4:
            st.metric("Em Adoção", em_adocao, delta=f"{(em_adocao/total_areas*100):.0f}%", help="Áreas em processo de adoção")
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Status por Nível TMMi")
            
            # Agrupar por nível e status
            status_por_nivel = df_inst.groupby(['Nível TMMi', 'Status Institucional']).size().reset_index(name='count')
            
            fig = px.bar(
                status_por_nivel, 
                x='Nível TMMi', 
                y='count',
                color='Status Institucional',
                title="Distribuição de Status por Nível",
                color_discrete_map={
                    'Adotado': '#28a745',
                    'Desenvolvendo': '#ffc107',
                    'Em Adoção': '#6c757d',
                    'Planejado': '#17a2b8'
                }
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Progresso Geral")
            
            # Pizza chart de status
            status_counts = df_inst['Status Institucional'].value_counts()
            
            fig = go.Figure(data=[go.Pie(
                labels=status_counts.index,
                values=status_counts.values,
                hole=.3,
                marker_colors=['#28a745', '#ffc107', '#6c757d', '#17a2b8']
            )])
            fig.update_layout(height=400, title_text="Distribuição de Status")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Resumo do Roadmap
        st.subheader("🗓️ Próximas Entregas (TRI 1)")
        df_roadmap = data['roadmap']
        
        if not df_roadmap.empty:
            # Filtrar apenas TRI 1
            df_tri1 = df_roadmap[df_roadmap['Trimestre'].str.contains('TRI 1', na=False)]
            
            if not df_tri1.empty:
                # Mostrar tabela simplificada
                roadmap_display = df_tri1[['Fase', 'Entrega', 'Status', 'Responsável']].copy()
                
                # Aplicar cores baseado no status
                def colorir_status(status):
                    if pd.isna(status):
                        return 'background-color: white'
                    status_lower = str(status).lower()
                    if 'planejado' in status_lower:
                        return 'background-color: #d1ecf1'
                    elif 'desenvolvendo' in status_lower or 'andamento' in status_lower:
                        return 'background-color: #fff3cd'
                    elif 'adotado' in status_lower or 'concluído' in status_lower:
                        return 'background-color: #d4edda'
                    return 'background-color: white'
                
                st.dataframe(
                    roadmap_display.style.applymap(colorir_status, subset=['Status']),
                    use_container_width=True,
                    height=300
                )
            else:
                st.info("Nenhuma entrega planejada para TRI 1")
        else:
            st.warning("Dados de roadmap não disponíveis")
    
    # ================== VISÃO INSTITUCIONAL ==================
    elif pagina == "🏢 Visão Institucional":
        st.header("🏢 Visão Institucional do TMMi")
        st.markdown("Status de adoção das áreas de processo por nível de maturidade")
        
        df = data['institucional']
        
        # Filtros
        col1, col2 = st.columns([1, 3])
        with col1:
            niveis_disponiveis = df['Nível TMMi'].dropna().unique()
            nivel_selecionado = st.multiselect(
                "Filtrar por Nível:",
                options=sorted(niveis_disponiveis),
                default=sorted(niveis_disponiveis)
            )
        
        # Aplicar filtro
        if nivel_selecionado:
            df_filtrado = df[df['Nível TMMi'].isin(nivel_selecionado)]
        else:
            df_filtrado = df
        
        # Exibir tabela detalhada
        st.subheader("📋 Detalhamento por Área de Processo")
        
        # Preparar dados para exibição
        df_display = df_filtrado[['Nível TMMi', 'Área de Processo', 'Status Institucional', 'Observação']].copy()
        df_display = df_display.dropna(subset=['Área de Processo'])
        
        # Aplicar formatação condicional
        def highlight_status(row):
            status = str(row['Status Institucional']).lower()
            if 'adotado' in status:
                return ['background-color: #d4edda'] * len(row)
            elif 'desenvolvendo' in status:
                return ['background-color: #fff3cd'] * len(row)
            elif 'adoção' in status or 'adocao' in status:
                return ['background-color: #e2e3e5'] * len(row)
            else:
                return [''] * len(row)
        
        st.dataframe(
            df_display.style.apply(highlight_status, axis=1),
            use_container_width=True,
            height=500
        )
        
        # Resumo por status
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        status_summary = df_filtrado['Status Institucional'].value_counts()
        
        with col1:
            st.markdown("### ✅ Adotado")
            st.markdown(f"**{status_summary.get('Adotado', 0)}** áreas")
            if 'Adotado' in status_summary.index:
                areas_adotadas = df_filtrado[df_filtrado['Status Institucional'] == 'Adotado']['Área de Processo'].tolist()
                for area in areas_adotadas:
                    st.markdown(f"- {area}")
        
        with col2:
            st.markdown("### 🔄 Desenvolvendo")
            st.markdown(f"**{status_summary.get('Desenvolvendo', 0)}** áreas")
            if 'Desenvolvendo' in status_summary.index:
                areas_dev = df_filtrado[df_filtrado['Status Institucional'] == 'Desenvolvendo']['Área de Processo'].tolist()
                for area in areas_dev:
                    st.markdown(f"- {area}")
        
        with col3:
            st.markdown("### 📊 Em Adoção")
            st.markdown(f"**{status_summary.get('Em Adoção', 0)}** áreas")
            if 'Em Adoção' in status_summary.index:
                areas_adocao = df_filtrado[df_filtrado['Status Institucional'] == 'Em Adoção']['Área de Processo'].tolist()
                for area in areas_adocao:
                    st.markdown(f"- {area}")
    
    # ================== VISÃO POR SQUADS ==================
    elif pagina == "👥 Visão por Squads":
        st.header("👥 Visão por Squads")
        st.markdown("Acompanhamento das melhorias por squad e trimestre")
        
        df = data['squads']
        
        # Extrair nomes das colunas de squads (a partir da coluna 6)
        if df.shape[1] > 6:
            squads_cols = df.columns[6:].tolist()
            st.info(f"Squads identificados: {', '.join([str(s) for s in squads_cols if not pd.isna(s)])}")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'Trimestre' in df.columns or 1 in df.columns:
                trimestre_col = 'Trimestre' if 'Trimestre' in df.columns else 1
                trimestres = df[trimestre_col].dropna().unique()
                trimestre_selecionado = st.selectbox("Trimestre:", options=['Todos'] + list(trimestres))
        
        with col2:
            if 'Fase' in df.columns or 2 in df.columns:
                fase_col = 'Fase' if 'Fase' in df.columns else 2
                fases = df[fase_col].dropna().unique()
                fase_selecionada = st.selectbox("Fase:", options=['Todas'] + list(fases))
        
        # Exibir dados
        st.subheader("📊 Status das Melhorias por Squad")
        st.dataframe(df, use_container_width=True, height=600)
    
    # ================== ROADMAP TRIMESTRAL ==================
    elif pagina == "🗓️ Roadmap Trimestral":
        st.header("🗓️ Roadmap Trimestral")
        st.markdown("Planejamento de entregas por trimestre")
        
        df = data['roadmap']
        
        if not df.empty:
            # Filtro de trimestre
            if 'Trimestre' in df.columns:
                trimestres = df['Trimestre'].dropna().unique()
                trimestre_filtro = st.selectbox("Selecione o Trimestre:", options=['Todos'] + list(trimestres))
                
                if trimestre_filtro != 'Todos':
                    df_filtrado = df[df['Trimestre'] == trimestre_filtro]
                else:
                    df_filtrado = df
            else:
                df_filtrado = df
            
            # Exibir roadmap
            st.subheader("📋 Entregas Planejadas")
            
            # Selecionar colunas relevantes
            colunas_display = ['Trimestre', 'Fase', 'Entrega', 'TMMi (Nível – Área)', 'Envolvidos', 'Status', 'Responsável']
            colunas_existentes = [col for col in colunas_display if col in df_filtrado.columns]
            
            df_display = df_filtrado[colunas_existentes].copy()
            
            # Aplicar cores por status
            def colorir_roadmap(row):
                if 'Status' in row.index:
                    status = str(row['Status']).lower()
                    if 'planejado' in status:
                        return ['background-color: #d1ecf1'] * len(row)
                    elif 'andamento' in status or 'desenvolvendo' in status:
                        return ['background-color: #fff3cd'] * len(row)
                    elif 'concluído' in status or 'adotado' in status:
                        return ['background-color: #d4edda'] * len(row)
                    elif 'despriorizado' in status:
                        return ['background-color: #f8d7da'] * len(row)
                return [''] * len(row)
            
            st.dataframe(
                df_display.style.apply(colorir_roadmap, axis=1),
                use_container_width=True,
                height=600
            )
            
            # Estatísticas do roadmap
            st.markdown("---")
            st.subheader("📊 Estatísticas do Roadmap")
            
            if 'Status' in df_filtrado.columns:
                col1, col2, col3 = st.columns(3)
                
                status_counts = df_filtrado['Status'].value_counts()
                
                with col1:
                    st.metric("Total de Entregas", len(df_filtrado))
                
                with col2:
                    planejado = status_counts.get('Planejado', 0)
                    st.metric("Planejado", planejado)
                
                with col3:
                    if 'Fase' in df_filtrado.columns:
                        fases_unicas = df_filtrado['Fase'].nunique()
                        st.metric("Fases Diferentes", fases_unicas)
        else:
            st.warning("Dados de roadmap não disponíveis")
    
    # ================== SCORE TMMi ==================
    elif pagina == "📈 Score TMMi":
        st.header("📈 Score TMMi")
        st.markdown("Pontuação e progresso das melhorias")
        
        df = data['score']
        
        st.subheader("📊 Scores por Squad e Melhoria")
        st.dataframe(df, use_container_width=True, height=600)
        
        # Análise de scores
        if 'SCORE' in df.columns:
            st.markdown("---")
            st.subheader("📈 Análise de Pontuação")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Score médio
                score_medio = df['SCORE'].mean()
                st.metric("Score Médio", f"{score_medio:.2f}")
                
                # Distribuição de scores
                fig = px.histogram(df, x='SCORE', title='Distribuição de Scores', nbins=10)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Status vs Score
                if 'STATUS' in df.columns:
                    score_por_status = df.groupby('STATUS')['SCORE'].mean().reset_index()
                    fig = px.bar(score_por_status, x='STATUS', y='SCORE', title='Score Médio por Status')
                    st.plotly_chart(fig, use_container_width=True)
    
    # ================== MAPA DO TMMi ==================
    elif pagina == "🗺️ Mapa do TMMi":
        st.header("🗺️ Mapa do TMMi")
        st.markdown("Entendendo os níveis e áreas de processo do TMMi")
        
        df = data['mapa']
        
        # Organizar por nível
        if 'Nível' in df.columns:
            niveis = df['Nível'].dropna().unique()
            
            for nivel in sorted(niveis):
                df_nivel = df[df['Nível'] == nivel]
                
                st.subheader(f"📚 Nível {nivel}")
                
                for idx, row in df_nivel.iterrows():
                    area = row.get('Área de Processo', 'N/A')
                    descricao = row.get('Descrição', 'Sem descrição')
                    
                    with st.expander(f"📖 {area}"):
                        st.markdown(descricao)
                
                st.markdown("---")
        else:
            st.dataframe(df, use_container_width=True, height=600)
    
    # ================== CRITÉRIOS DE ENTREGA ==================
    elif pagina == "📋 Critérios de Entrega":
        st.header("📋 Critérios de Entrega (Definition of Done)")
        st.markdown("Critérios detalhados para validação das melhorias")
        
        df = data['criterios']
        
        # Filtros
        if 'ID MELHORIA' in df.columns:
            melhorias = df['ID MELHORIA'].dropna().unique()
            melhoria_selecionada = st.selectbox("Filtrar por Melhoria:", options=['Todas'] + list(melhorias))
            
            if melhoria_selecionada != 'Todas':
                df_filtrado = df[df['ID MELHORIA'] == melhoria_selecionada]
            else:
                df_filtrado = df
        else:
            df_filtrado = df
        
        # Exibir critérios
        st.subheader("📝 Critérios Detalhados")
        st.dataframe(df_filtrado, use_container_width=True, height=600)
        
        # Estatísticas de atendimento
        if 'ATENDIDO' in df_filtrado.columns:
            st.markdown("---")
            st.subheader("📊 Taxa de Atendimento")
            
            col1, col2, col3 = st.columns(3)
            
            total_criterios = len(df_filtrado)
            atendidos = df_filtrado['ATENDIDO'].notna().sum()
            
            with col1:
                st.metric("Total de Critérios", total_criterios)
            with col2:
                st.metric("Critérios Atendidos", atendidos)
            with col3:
                if total_criterios > 0:
                    taxa = (atendidos / total_criterios) * 100
                    st.metric("Taxa de Atendimento", f"{taxa:.1f}%")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Framework TMMi - TAG IMF | Atualizado em: {}</p>
    </div>
    """.format(datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)

except Exception as e:
    st.error(f"Erro ao carregar dados: {str(e)}")
    st.info("Certifique-se de que o arquivo 'Framework_-_TMMi-TAG.xlsx' está no diretório correto.")
