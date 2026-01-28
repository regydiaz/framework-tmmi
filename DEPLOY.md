# 🚀 Guia de Deploy - Framework TMMi

## Opção 1: Deploy no Streamlit Cloud (RECOMENDADO) ⭐

### Vantagens
- ✅ Grátis
- ✅ Deploy automático
- ✅ Compartilhamento fácil (link público)
- ✅ Atualizações automáticas quando você editar

### Passo a Passo

#### 1. Criar conta no GitHub (se não tiver)
- Acesse: https://github.com
- Clique em "Sign up"

#### 2. Criar repositório
1. No GitHub, clique em "New repository"
2. Nome: `framework-tmmi-tag`
3. Marque "Public"
4. Clique em "Create repository"

#### 3. Upload dos arquivos
Faça upload destes arquivos para o repositório:
- `app.py`
- `exporter.py`
- `requirements.txt`
- `README.md`
- `Framework_-_TMMi-TAG.xlsx`

**Como fazer upload:**
1. No repositório, clique em "Add file" → "Upload files"
2. Arraste todos os arquivos
3. Clique em "Commit changes"

#### 4. Deploy no Streamlit Cloud
1. Acesse: https://streamlit.io/cloud
2. Clique em "Sign up" (use sua conta GitHub)
3. Clique em "New app"
4. Selecione:
   - Repository: `framework-tmmi-tag`
   - Branch: `main`
   - Main file: `app.py`
5. Clique em "Deploy!"

#### 5. Pronto! 🎉
Em 2-3 minutos seu dashboard estará online em uma URL tipo:
`https://seu-usuario-framework-tmmi-tag.streamlit.app`

---

## Opção 2: Rodar Localmente (No seu computador)

### Requisitos
- Python 3.8+
- pip

### Instalação

#### Windows
```cmd
# Abrir PowerShell ou CMD
cd C:\caminho\para\pasta\do\projeto

# Instalar dependências
pip install -r requirements.txt

# Rodar dashboard
streamlit run app.py
```

#### Mac/Linux
```bash
# Abrir Terminal
cd /caminho/para/pasta/do/projeto

# Instalar dependências
pip3 install -r requirements.txt

# Rodar dashboard
streamlit run app.py
```

### Acessar
Abra o navegador em: `http://localhost:8501`

---

## Opção 3: Deploy no Heroku (Alternativa)

### 1. Criar arquivos adicionais

**Procfile** (novo arquivo):
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**setup.sh** (novo arquivo):
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"seu-email@example.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

### 2. Deploy
1. Crie conta no Heroku: https://heroku.com
2. Instale Heroku CLI
3. Execute:
```bash
heroku login
heroku create framework-tmmi-tag
git init
git add .
git commit -m "Deploy inicial"
git push heroku main
```

---

## Opção 4: Compartilhar via Google Colab

### 1. Criar notebook
Crie um novo notebook no Google Colab e cole:

```python
!pip install streamlit pandas openpyxl plotly reportlab python-pptx

# Upload da planilha
from google.colab import files
uploaded = files.upload()  # Upload Framework_-_TMMi-TAG.xlsx

# Criar app.py
%%writefile app.py
[Cole todo o conteúdo do app.py aqui]

# Criar exporter.py  
%%writefile exporter.py
[Cole todo o conteúdo do exporter.py aqui]

# Rodar
!streamlit run app.py & npx localtunnel --port 8501
```

---

## 🔐 Segurança e Acesso

### Dashboard Público
- Streamlit Cloud: Qualquer pessoa com o link pode acessar
- Adicione senha se necessário (ver seção abaixo)

### Adicionar Autenticação (Opcional)

Edite `app.py` e adicione no início:

```python
import streamlit as st

def check_password():
    def password_entered():
        if st.session_state["password"] == "tmmi2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Senha", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Senha", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Senha incorreta")
        return False
    else:
        return True

if not check_password():
    st.stop()

# Resto do código aqui...
```

---

## 📊 Atualizar Dados

### Método 1: Upload Manual (Streamlit Cloud)
1. Atualize `Framework_-_TMMi-TAG.xlsx` no seu computador
2. Faça upload no GitHub (substitua o arquivo antigo)
3. O dashboard atualiza automaticamente em ~1 minuto

### Método 2: Google Sheets Sync (Avançado)
Converta para Google Sheets e use a API para sync automático.

---

## 🎯 Customizações Rápidas

### Mudar Cores
Em `app.py`, linha ~30:

```python
st.markdown("""
<style>
    .main-header {
        color: #SEU_COR_AQUI;  # Exemplo: #FF5733
    }
</style>
""")
```

### Adicionar Logo
```python
from PIL import Image
logo = Image.open('logo.png')
st.image(logo, width=200)
```

### Personalizar Título
Linha ~20:
```python
st.set_page_config(
    page_title="Seu Título Aqui",
    page_icon="🎯",  # Seu emoji
)
```

---

## 📱 Compartilhamento

### Gerar QR Code para o Dashboard
1. Acesse: https://www.qr-code-generator.com/
2. Cole a URL do seu dashboard
3. Baixe o QR Code
4. Compartilhe com o time!

### Embedar em Site/Intranet
```html
<iframe 
  src="https://sua-url.streamlit.app" 
  width="100%" 
  height="800px"
  frameborder="0">
</iframe>
```

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'X'"
```bash
pip install -r requirements.txt
```

### Dashboard muito lento
- Reduza o tamanho da planilha
- Use @st.cache_data em funções pesadas

### Erro ao exportar PDF/PPT
Verifique se todas as bibliotecas estão instaladas:
```bash
pip install reportlab python-pptx
```

---

## 📞 Suporte

**Dúvidas?**
1. Consulte a documentação do Streamlit: https://docs.streamlit.io
2. Veja exemplos: https://streamlit.io/gallery
3. Entre em contato com a equipe de QA

---

**Boa sorte com o deploy! 🚀**
