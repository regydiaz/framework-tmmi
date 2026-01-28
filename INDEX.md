# 📚 Framework TMMi - Índice de Arquivos

## 📋 Visão Geral

Este pacote contém tudo que você precisa para ter um **Dashboard Interativo** do Framework TMMi com capacidade de exportação para PDF e PowerPoint.

---

## 🗂️ Estrutura de Arquivos

### 🎯 COMECE AQUI

| Arquivo | Descrição | Quando usar |
|---------|-----------|-------------|
| **INICIO_RAPIDO.md** | ⭐ **LEIA PRIMEIRO** - Guia de 3 passos | Se é sua primeira vez |
| **PREVIEW.html** | Preview visual do dashboard | Para ver como ficará |

### 📱 Dashboard

| Arquivo | Descrição | Tipo |
|---------|-----------|------|
| **app.py** | Dashboard Streamlit principal | Python |
| **exporter.py** | Módulo de exportação (PDF/PPT) | Python |
| **Framework_-_TMMi-TAG.xlsx** | Planilha de dados do TMMi | Excel |

### 📖 Documentação

| Arquivo | Conteúdo |
|---------|----------|
| **README.md** | Documentação completa do projeto |
| **DEPLOY.md** | Guia detalhado de deploy (Streamlit Cloud, Heroku, etc) |
| **INICIO_RAPIDO.md** | Guia rápido para começar em 5 minutos |
| **INDEX.md** | Este arquivo - índice geral |

### 🛠️ Configuração

| Arquivo | Uso |
|---------|-----|
| **requirements.txt** | Dependências Python necessárias |
| **exemplos_exportacao.py** | Exemplos de uso da API de exportação |

---

## 🚀 Fluxo de Uso Recomendado

### Para Iniciantes:

```
1. Leia: INICIO_RAPIDO.md
   ↓
2. Abra: PREVIEW.html (no navegador)
   ↓
3. Faça deploy: Siga INICIO_RAPIDO.md ou DEPLOY.md
   ↓
4. Use o dashboard!
```

### Para Desenvolvedores:

```
1. Leia: README.md (documentação completa)
   ↓
2. Instale: pip install -r requirements.txt
   ↓
3. Rode: streamlit run app.py
   ↓
4. Customize: Edite app.py conforme necessário
   ↓
5. Use API: Veja exemplos_exportacao.py
```

---

## 📊 Funcionalidades do Dashboard

### Páginas Interativas:
- 🏠 Visão Geral (métricas executivas)
- 🏢 Visão Institucional (status por nível)
- 👥 Visão por Squads (progresso por equipe)
- 🗓️ Roadmap Trimestral (planejamento)
- 📈 Score TMMi (pontuação detalhada)
- 🗺️ Mapa do TMMi (descrição dos níveis)
- 📋 Critérios de Entrega (DoD)

### Exportação:
- 📄 PDF (relatório executivo)
- 📊 PowerPoint (apresentação para gestores)

---

## 🎓 Guias por Caso de Uso

### "Quero ver como ficará antes de instalar"
→ Abra `PREVIEW.html` no navegador

### "Quero colocar online GRÁTIS agora"
→ Siga `INICIO_RAPIDO.md` → Seção "Deploy Online"

### "Quero rodar no meu computador"
→ Siga `INICIO_RAPIDO.md` → Seção "Rodar Localmente"

### "Quero customizar cores/textos"
→ Edite `app.py` → Veja seção CSS (linha ~30)

### "Quero entender tudo em detalhes"
→ Leia `README.md` completo

### "Quero fazer deploy profissional"
→ Siga `DEPLOY.md` → Escolha sua plataforma

### "Quero automatizar exportação"
→ Use `exemplos_exportacao.py` como referência

### "Quero adicionar novos gráficos"
→ Edite `app.py` → Use Plotly (já importado)

### "Quero exportar PDF programaticamente"
→ Veja `exemplos_exportacao.py` → Exemplo 2

### "Quero enviar relatórios por email"
→ Veja `exemplos_exportacao.py` → Exemplo 6

---

## 🔧 Configurações Rápidas

### Mudar título do dashboard:
```python
# Em app.py, linha ~20
st.set_page_config(
    page_title="Seu Título Aqui"
)
```

### Mudar cores principais:
```python
# Em app.py, linha ~30
.main-header {
    color: #SUA_COR;  # Exemplo: #FF5733
}
```

### Adicionar logo:
```python
# No início do app.py, após imports
st.image("logo.png", width=200)
```

---

## 📦 Dependências (requirements.txt)

```
streamlit       → Framework do dashboard
pandas          → Manipulação de dados
openpyxl        → Leitura de Excel
plotly          → Gráficos interativos
reportlab       → Geração de PDF
python-pptx     → Geração de PowerPoint
numpy           → Cálculos numéricos
```

---

## 🔄 Atualizar Dados

### Se rodando local:
1. Edite `Framework_-_TMMi-TAG.xlsx`
2. Salve
3. Recarregue o dashboard (F5)

### Se no Streamlit Cloud:
1. Edite a planilha
2. Faça upload no GitHub (substitui arquivo)
3. Dashboard atualiza automaticamente

---

## 💡 Dicas Importantes

### ✅ FAÇA:
- Comece pelo `INICIO_RAPIDO.md`
- Teste o `PREVIEW.html` primeiro
- Use Streamlit Cloud (é grátis!)
- Leia os comentários no código
- Customize aos poucos

### ❌ NÃO FAÇA:
- Pular o `INICIO_RAPIDO.md`
- Tentar rodar sem instalar dependências
- Mudar muita coisa de uma vez
- Deletar `Framework_-_TMMi-TAG.xlsx`
- Esquecer de fazer backup antes de customizar

---

## 🆘 Problemas Comuns e Soluções

| Problema | Solução |
|----------|---------|
| "Não sei por onde começar" | Leia `INICIO_RAPIDO.md` |
| "Erro ao instalar dependências" | Verifique se tem Python 3.8+ |
| "Dashboard não abre" | Veja troubleshooting no `README.md` |
| "Não consigo fazer deploy" | Siga passo-a-passo do `DEPLOY.md` |
| "Quero mudar algo mas não sei como" | Veja exemplos no código (app.py tem comentários) |

---

## 📞 Ordem de Leitura Recomendada

### Se tem pressa (15 minutos):
1. `INICIO_RAPIDO.md` (5 min)
2. `PREVIEW.html` (2 min)
3. Deploy no Streamlit Cloud (5 min)
4. Use! (3 min testando)

### Se quer entender tudo (1 hora):
1. `INICIO_RAPIDO.md` (10 min)
2. `README.md` (20 min)
3. `DEPLOY.md` (15 min)
4. `app.py` (leitura do código, 15 min)

### Se é desenvolvedor:
1. `README.md`
2. `app.py` (ler código completo)
3. `exporter.py` (ler código completo)
4. `exemplos_exportacao.py`
5. Customizar conforme necessário

---

## 🎯 Próximos Passos Sugeridos

Depois de ter o dashboard rodando:

- [ ] Compartilhe a URL com o time
- [ ] Configure exportação automática
- [ ] Personalize cores/logo
- [ ] Adicione autenticação (se necessário)
- [ ] Agende relatórios semanais
- [ ] Integre com ferramentas existentes
- [ ] Colete feedback do time
- [ ] Itere e melhore!

---

## 📚 Recursos Adicionais

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Docs**: https://plotly.com/python/
- **Pandas Docs**: https://pandas.pydata.org/docs/
- **Galeria de Apps**: https://streamlit.io/gallery

---

## ✨ Resumo Final

**Você tem agora:**
- ✅ Dashboard interativo completo
- ✅ Exportação PDF/PowerPoint
- ✅ Documentação detalhada
- ✅ Exemplos de uso
- ✅ Guias de deploy
- ✅ Preview para mostrar

**Próximo passo:**
→ Abra `INICIO_RAPIDO.md` e siga o passo-a-passo!

---

**Criado com ❤️ para TAG IMF**  
**Janeiro 2026**
