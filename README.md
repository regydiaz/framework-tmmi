# Framework TMMi - TAG IMF

Dashboard interativo e sistema de exportação para acompanhamento do Framework TMMi.

## 🚀 Funcionalidades

### Dashboard Web (Streamlit)
- **Visão Geral**: Métricas executivas e gráficos de progresso
- **Visão Institucional**: Status de adoção por nível e área de processo
- **Visão por Squads**: Acompanhamento de melhorias por equipe
- **Roadmap Trimestral**: Planejamento de entregas
- **Score TMMi**: Pontuação e análise de progresso
- **Mapa do TMMi**: Descrição dos níveis e áreas
- **Critérios de Entrega**: Definition of Done detalhado

### Exportação
- **PDF**: Relatório executivo completo
- **PowerPoint**: Apresentação para gestores

## 📦 Instalação

### 1. Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

## 🎯 Como Usar

### Rodar o Dashboard

1. Coloque o arquivo `Framework_-_TMMi-TAG.xlsx` no mesmo diretório
2. Execute o comando:

```bash
streamlit run app.py
```

3. O dashboard abrirá automaticamente no navegador em `http://localhost:8501`

### Exportar Relatórios

#### Pelo Dashboard:
1. Use os botões na barra lateral:
   - **📄 PDF**: Gera relatório em PDF
   - **📊 PPT**: Gera apresentação em PowerPoint
2. Clique em "Baixar" para salvar o arquivo

#### Por Script Python:
```python
from exporter import export_framework
import pandas as pd

# Carregar dados
data = {
    'institucional': pd.read_excel('Framework_-_TMMi-TAG.xlsx', 'TMMi - Visão Institucional'),
    'roadmap': pd.read_excel('Framework_-_TMMi-TAG.xlsx', 'Roadmap Trimestral'),
    # ... outros sheets
}

# Exportar
results = export_framework(data, export_pdf=True, export_ppt=True)
print(f"PDF gerado: {results['pdf']}")
print(f"PPT gerado: {results['ppt']}")
```

## 📂 Estrutura de Arquivos

```
.
├── app.py                          # Dashboard Streamlit principal
├── exporter.py                     # Módulo de exportação (PDF/PPT)
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
└── Framework_-_TMMi-TAG.xlsx      # Planilha de dados (necessária)
```

## 🎨 Personalizações

### Cores e Estilos

Edite as cores no arquivo `app.py` na seção de CSS customizado:

```python
st.markdown("""
<style>
    .main-header {
        color: #1f77b4;  # Azul principal
        ...
    }
</style>
""")
```

### Adicionar Novas Páginas

1. Adicione a opção no `st.sidebar.radio()`
2. Crie a seção com `elif pagina == "Nova Página":`
3. Implemente a lógica de visualização

## 📊 Visualizações Disponíveis

### Gráficos
- Barras: Status por nível
- Pizza: Distribuição geral de status
- Histogramas: Distribuição de scores
- Tabelas interativas com filtros

### Filtros Dinâmicos
- Por trimestre
- Por squad
- Por nível TMMi
- Por status

## 🔧 Troubleshooting

### Erro: "File not found"
- Certifique-se que `Framework_-_TMMi-TAG.xlsx` está no diretório correto
- Verifique o caminho no código

### Erro ao gerar PDF/PPT
- Instale todas as dependências: `pip install -r requirements.txt`
- Verifique permissões de escrita na pasta `/mnt/user-data/outputs/`

### Dashboard não abre
- Verifique se a porta 8501 está disponível
- Tente: `streamlit run app.py --server.port 8502`

## 📈 Próximos Passos

- [ ] Adicionar filtros por data
- [ ] Gráficos de evolução temporal
- [ ] Dashboard de comparação entre squads
- [ ] Alertas automáticos de prazos
- [ ] Integração com APIs externas

## 👥 Suporte

Para dúvidas ou sugestões:
- Abra uma issue no repositório
- Entre em contato com a equipe de QA

## 📝 Licença

Uso interno - TAG IMF

---

**Última atualização**: Janeiro 2026
**Versão**: 1.0.0
