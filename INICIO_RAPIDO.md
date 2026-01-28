# 🚀 INÍCIO RÁPIDO - Framework TMMi

## 📦 O que você recebeu

```
Framework-TMMi-Dashboard/
├── app.py                          # Dashboard Streamlit principal ⭐
├── exporter.py                     # Exportador PDF/PowerPoint
├── requirements.txt                # Dependências Python
├── Framework_-_TMMi-TAG.xlsx      # Sua planilha de dados
├── README.md                       # Documentação completa
├── DEPLOY.md                       # Guia de deploy detalhado
└── PREVIEW.html                    # Preview estático (abra no navegador)
```

## ⚡ 3 Formas de Usar

### 1️⃣ MAIS RÁPIDO: Ver Preview (30 segundos)

```bash
# Abra o arquivo PREVIEW.html no navegador
# Duplo-clique no arquivo ou arraste para o navegador
```

✅ Mostra como ficará o dashboard
❌ Não é interativo, é só uma visualização

---

### 2️⃣ RECOMENDADO: Deploy Online GRÁTIS (5 minutos)

**Streamlit Cloud** - Grátis para sempre!

1. **Crie conta no GitHub** (se não tiver)
   - https://github.com → Sign up

2. **Crie repositório**
   - New repository → Nome: `framework-tmmi`
   - Public → Create

3. **Upload dos arquivos**
   - Add file → Upload files
   - Arraste TODOS os arquivos desta pasta
   - Commit changes

4. **Deploy no Streamlit**
   - https://streamlit.io/cloud → Sign up (use GitHub)
   - New app → Selecione seu repositório
   - Main file: `app.py` → Deploy!

5. **PRONTO! 🎉**
   - Em 2 minutos terá uma URL tipo:
   - `https://seu-nome-framework-tmmi.streamlit.app`
   - Compartilhe com quem quiser!

📖 **Guia detalhado:** Veja `DEPLOY.md`

---

### 3️⃣ AVANÇADO: Rodar no Seu Computador (10 minutos)

#### Pré-requisitos
- Python 3.8+ instalado
- Acesso à internet para instalar pacotes

#### Instalação

**Windows (PowerShell ou CMD):**
```cmd
cd C:\caminho\para\esta\pasta
pip install -r requirements.txt
streamlit run app.py
```

**Mac/Linux (Terminal):**
```bash
cd /caminho/para/esta/pasta
pip3 install -r requirements.txt
streamlit run app.py
```

#### Acessar
- Abre automaticamente no navegador
- Ou acesse: `http://localhost:8501`

---

## 🎯 Funcionalidades do Dashboard

### Páginas Disponíveis:
- 🏠 **Visão Geral**: Métricas e gráficos executivos
- 🏢 **Visão Institucional**: Status por nível TMMi
- 👥 **Visão por Squads**: Progresso de cada equipe
- 🗓️ **Roadmap**: Entregas planejadas
- 📈 **Score TMMi**: Pontuação detalhada
- 🗺️ **Mapa do TMMi**: Descrição dos níveis
- 📋 **Critérios**: Definition of Done

### Exportação:
- 📄 **PDF**: Relatório executivo completo
- 📊 **PowerPoint**: Apresentação para gestores

---

## 🔄 Como Atualizar os Dados

### Se está online (Streamlit Cloud):
1. Edite `Framework_-_TMMi-TAG.xlsx` no Excel
2. Faça upload no GitHub (substitui o arquivo)
3. Dashboard atualiza sozinho em ~1 minuto ✨

### Se está rodando local:
1. Edite `Framework_-_TMMi-TAG.xlsx`
2. Salve o arquivo
3. Recarregue a página do dashboard (F5)

---

## 🎨 Customizações Rápidas

### Mudar o título:
Edite `app.py`, linha ~20:
```python
st.set_page_config(
    page_title="SEU TÍTULO AQUI",
    page_icon="🎯",  # Mude o emoji
)
```

### Mudar cores:
Edite `app.py`, linha ~30 (seção CSS):
```python
.main-header {
    color: #1f77b4;  # Mude para sua cor favorita
}
```

### Adicionar logo:
Adicione no início do app.py:
```python
st.image("logo.png", width=200)
```

---

## 🆘 Problemas Comuns

### "pip não é reconhecido" (Windows)
```cmd
# Use py ao invés de python:
py -m pip install -r requirements.txt
```

### "Permission denied" (Mac/Linux)
```bash
# Use sudo ou pip3 com --user:
pip3 install --user -r requirements.txt
```

### Dashboard não abre
- Verifique se porta 8501 está livre
- Tente: `streamlit run app.py --server.port 8502`

### Erro ao carregar planilha
- Certifique-se que `Framework_-_TMMi-TAG.xlsx` está na mesma pasta
- Verifique se o nome está correto (com hífen, não underscore)

---

## 📊 Dicas de Uso

### Para Apresentações:
1. Use o botão "📊 PPT" no dashboard
2. Baixe o PowerPoint gerado
3. Apresente para gestores!

### Para Relatórios:
1. Use o botão "📄 PDF" no dashboard
2. Compartilhe o PDF por email

### Para Compartilhar:
- **Link público**: URL do Streamlit Cloud
- **QR Code**: Gere em qr-code-generator.com
- **Embed**: Cole em sites (veja DEPLOY.md)

---

## 🎓 Próximos Passos

1. ✅ Abra o PREVIEW.html para ver como ficará
2. ✅ Faça deploy no Streamlit Cloud (5 min)
3. ✅ Compartilhe com o time
4. ✅ Customize as cores/textos
5. ✅ Adicione logo da empresa
6. ✅ Configure alertas/automações

---

## 📚 Mais Ajuda

- **README.md**: Documentação completa
- **DEPLOY.md**: Guia detalhado de deploy
- **Streamlit Docs**: https://docs.streamlit.io
- **Galeria de Exemplos**: https://streamlit.io/gallery

---

## 💡 Dica Final

**Melhor jeito de aprender?** 
→ Deploy no Streamlit Cloud AGORA (5 min)
→ Brinque com o dashboard
→ Customize depois

Não precisa ser perfeito na primeira vez! 🚀

---

**Dúvidas?** Consulte os arquivos:
- 📖 README.md (documentação)
- 🚀 DEPLOY.md (deploy detalhado)
- 💻 app.py (código principal - com comentários)

**Boa sorte! 🎉**
