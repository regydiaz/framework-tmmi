"""
EXEMPLOS DE USO - Exportador TMMi
Exemplos práticos de como usar o exportador para gerar relatórios
"""

# ============================================================================
# EXEMPLO 1: Exportar PDF e PowerPoint de uma vez
# ============================================================================

from exporter import export_framework
import pandas as pd

def exemplo_basico():
    """Exemplo mais simples - exporta tudo"""
    
    # Carregar dados da planilha
    file_path = 'Framework_-_TMMi-TAG.xlsx'
    
    data = {
        'institucional': pd.read_excel(file_path, 'TMMi - Visão Institucional', header=2),
        'squads': pd.read_excel(file_path, 'TMMi - Visão Squads', header=2),
        'roadmap': pd.read_excel(file_path, 'Roadmap Trimestral', header=1),
        'score': pd.read_excel(file_path, 'Score TMMi', header=2),
        'mapa': pd.read_excel(file_path, 'Mapa do TMMi', header=2),
        'criterios': pd.read_excel(file_path, 'Critérios TMMi', header=0)
    }
    
    # Exportar PDF e PowerPoint
    results = export_framework(data, export_pdf=True, export_ppt=True)
    
    print(f"✅ PDF gerado: {results['pdf']}")
    print(f"✅ PowerPoint gerado: {results['ppt']}")


# ============================================================================
# EXEMPLO 2: Exportar apenas PDF
# ============================================================================

def exemplo_so_pdf():
    """Gera apenas relatório PDF"""
    
    from exporter import TMMiExporter
    import pandas as pd
    
    file_path = 'Framework_-_TMMi-TAG.xlsx'
    
    data = {
        'institucional': pd.read_excel(file_path, 'TMMi - Visão Institucional', header=2),
        'roadmap': pd.read_excel(file_path, 'Roadmap Trimestral', header=1),
        'mapa': pd.read_excel(file_path, 'Mapa do TMMi', header=2),
        'squads': pd.DataFrame(),  # Pode deixar vazio se não precisar
        'score': pd.DataFrame(),
        'criterios': pd.DataFrame()
    }
    
    exporter = TMMiExporter(data)
    pdf_path = exporter.export_to_pdf('relatorio_mensal.pdf')
    
    print(f"✅ PDF salvo em: {pdf_path}")


# ============================================================================
# EXEMPLO 3: Exportar apenas PowerPoint
# ============================================================================

def exemplo_so_ppt():
    """Gera apenas apresentação PowerPoint"""
    
    from exporter import TMMiExporter
    import pandas as pd
    
    file_path = 'Framework_-_TMMi-TAG.xlsx'
    
    data = {
        'institucional': pd.read_excel(file_path, 'TMMi - Visão Institucional', header=2),
        'roadmap': pd.read_excel(file_path, 'Roadmap Trimestral', header=1),
        'squads': pd.DataFrame(),
        'score': pd.DataFrame(),
        'mapa': pd.DataFrame(),
        'criterios': pd.DataFrame()
    }
    
    exporter = TMMiExporter(data)
    ppt_path = exporter.export_to_powerpoint('apresentacao_executiva.pptx')
    
    print(f"✅ PowerPoint salvo em: {ppt_path}")


# ============================================================================
# EXEMPLO 4: Exportar com nomes personalizados
# ============================================================================

def exemplo_nomes_customizados():
    """Exporta com nomes de arquivo personalizados"""
    
    from exporter import TMMiExporter
    import pandas as pd
    from datetime import datetime
    
    file_path = 'Framework_-_TMMi-TAG.xlsx'
    
    # Carregar dados
    data = {
        'institucional': pd.read_excel(file_path, 'TMMi - Visão Institucional', header=2),
        'roadmap': pd.read_excel(file_path, 'Roadmap Trimestral', header=1),
        'mapa': pd.read_excel(file_path, 'Mapa do TMMi', header=2),
        'squads': pd.DataFrame(),
        'score': pd.DataFrame(),
        'criterios': pd.DataFrame()
    }
    
    # Gerar nomes com data
    hoje = datetime.now().strftime('%Y-%m-%d')
    
    exporter = TMMiExporter(data)
    
    pdf_path = exporter.export_to_pdf(f'TMMi_Relatorio_{hoje}.pdf')
    ppt_path = exporter.export_to_powerpoint(f'TMMi_Apresentacao_{hoje}.pptx')
    
    print(f"✅ Arquivos gerados:")
    print(f"   PDF: {pdf_path}")
    print(f"   PPT: {ppt_path}")


# ============================================================================
# EXEMPLO 5: Script automatizado (roda toda segunda-feira)
# ============================================================================

def gerar_relatorio_semanal():
    """
    Script para gerar relatórios semanais automaticamente
    Pode ser agendado com cron (Linux/Mac) ou Task Scheduler (Windows)
    """
    
    from exporter import export_framework
    import pandas as pd
    from datetime import datetime
    import os
    
    # Configurações
    file_path = 'Framework_-_TMMi-TAG.xlsx'
    output_dir = 'relatorios_semanais'
    
    # Criar pasta se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Data atual
    hoje = datetime.now()
    semana = hoje.strftime('%Y-W%U')  # Exemplo: 2026-W04
    
    print(f"📊 Gerando relatório da semana {semana}...")
    
    try:
        # Carregar dados
        data = {
            'institucional': pd.read_excel(file_path, 'TMMi - Visão Institucional', header=2),
            'squads': pd.read_excel(file_path, 'TMMi - Visão Squads', header=2),
            'roadmap': pd.read_excel(file_path, 'Roadmap Trimestral', header=1),
            'score': pd.read_excel(file_path, 'Score TMMi', header=2),
            'mapa': pd.read_excel(file_path, 'Mapa do TMMi', header=2),
            'criterios': pd.read_excel(file_path, 'Critérios TMMi', header=0)
        }
        
        # Exportar com nomes da semana
        from exporter import TMMiExporter
        exporter = TMMiExporter(data)
        
        pdf_path = exporter.export_to_pdf(f'{output_dir}/TMMi_{semana}.pdf')
        ppt_path = exporter.export_to_powerpoint(f'{output_dir}/TMMi_{semana}.pptx')
        
        print(f"✅ Relatório semanal gerado com sucesso!")
        print(f"   📄 PDF: {pdf_path}")
        print(f"   📊 PPT: {ppt_path}")
        
        # Opcional: Enviar por email (requer configuração de SMTP)
        # enviar_por_email([pdf_path, ppt_path])
        
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")


# ============================================================================
# EXEMPLO 6: Integração com email (opcional)
# ============================================================================

def enviar_por_email(arquivos, destinatarios=None):
    """
    Envia os relatórios por email
    Requer configuração de SMTP
    """
    
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email import encoders
    
    # Configurações de email (substitua pelos seus dados)
    SMTP_SERVER = 'smtp.gmail.com'  # ou smtp.office365.com
    SMTP_PORT = 587
    EMAIL_FROM = 'seu-email@empresa.com'
    EMAIL_PASSWORD = 'sua-senha'  # Use variáveis de ambiente!
    
    if destinatarios is None:
        destinatarios = ['gestor1@empresa.com', 'gestor2@empresa.com']
    
    # Criar mensagem
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = ', '.join(destinatarios)
    msg['Subject'] = f'Relatório TMMi - {datetime.now().strftime("%d/%m/%Y")}'
    
    # Corpo do email
    body = """
    Olá,
    
    Segue em anexo o relatório TMMi atualizado.
    
    Arquivos inclusos:
    - Relatório executivo (PDF)
    - Apresentação executiva (PowerPoint)
    
    Este email é gerado automaticamente.
    
    Atenciosamente,
    Sistema TMMi
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Anexar arquivos
    for arquivo in arquivos:
        with open(arquivo, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(arquivo)}')
            msg.attach(part)
    
    # Enviar
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email enviado para: {', '.join(destinatarios)}")
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")


# ============================================================================
# EXEMPLO 7: Agendar execução automática
# ============================================================================

"""
LINUX/MAC - Adicionar ao crontab:

# Gerar relatório toda segunda-feira às 8h
0 8 * * 1 cd /caminho/do/projeto && /usr/bin/python3 exemplos_exportacao.py

Para editar: crontab -e
"""

"""
WINDOWS - Task Scheduler:

1. Abra Task Scheduler
2. Create Basic Task
3. Nome: "Relatório TMMi Semanal"
4. Trigger: Weekly, Monday, 8:00 AM
5. Action: Start a program
   Program: C:\Python\python.exe
   Arguments: C:\caminho\do\projeto\exemplos_exportacao.py
6. Finish
"""


# ============================================================================
# EXEMPLO 8: Comparar relatórios de diferentes períodos
# ============================================================================

def comparar_periodos():
    """
    Compara métricas entre dois períodos
    """
    
    import pandas as pd
    
    # Carregar relatório atual
    data_atual = {
        'institucional': pd.read_excel('Framework_-_TMMi-TAG.xlsx', 'TMMi - Visão Institucional', header=2),
    }
    
    # Carregar relatório anterior (você precisa ter salvo antes)
    # data_anterior = {
    #     'institucional': pd.read_excel('Framework_-_TMMi-TAG_JAN.xlsx', 'TMMi - Visão Institucional', header=2),
    # }
    
    # Comparar
    df_atual = data_atual['institucional']
    # df_anterior = data_anterior['institucional']
    
    print("📊 Métricas Atuais:")
    print(f"Total de áreas: {len(df_atual)}")
    print(f"Adotado: {len(df_atual[df_atual['Status Institucional'] == 'Adotado'])}")
    print(f"Desenvolvendo: {len(df_atual[df_atual['Status Institucional'] == 'Desenvolvendo'])}")
    
    # Para comparação completa, você precisaria ter salvado versões anteriores


# ============================================================================
# EXECUTAR EXEMPLOS
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("EXEMPLOS DE USO - Exportador TMMi")
    print("=" * 70)
    print()
    print("Escolha o exemplo para executar:")
    print("1. Exportar PDF + PowerPoint (básico)")
    print("2. Exportar apenas PDF")
    print("3. Exportar apenas PowerPoint")
    print("4. Exportar com nomes personalizados")
    print("5. Gerar relatório semanal (automático)")
    print()
    
    escolha = input("Digite o número do exemplo (1-5): ").strip()
    
    if escolha == '1':
        exemplo_basico()
    elif escolha == '2':
        exemplo_so_pdf()
    elif escolha == '3':
        exemplo_so_ppt()
    elif escolha == '4':
        exemplo_nomes_customizados()
    elif escolha == '5':
        gerar_relatorio_semanal()
    else:
        print("❌ Opção inválida!")
