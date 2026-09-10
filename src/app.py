import os
import smtplib
import re
from datetime import datetime
from email.message import EmailMessage
import pandas as pd
from dotenv import load_dotenv
from xhtml2pdf import pisa

load_dotenv()

def email_valido(email):
    """Valida formato do e-mail."""
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(padrao, str(email)))

def carregar_template(caminho_template, dados):
    """Lê o arquivo HTML e substitui os marcadores de forma segura."""
    with open(caminho_template, "r", encoding="utf-8") as file:
        template = file.read()
    
    # Substituição manual para não conflitar com as chaves do CSS
    for chave, valor in dados.items():
        template = template.replace(f"{{{chave}}}", str(valor))
        
    return template

def gerar_pdf(corpo_html, caminho_saida_pdf):
    with open(caminho_saida_pdf, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(corpo_html, dest=pdf_file)
    return not pisa_status.err

def processar_e_notificar():
    # 1. Lê a base de dados
    df = pd.read_csv("dados/clientes.csv")
    
    # 2. Filtra apenas os clientes inadimplentes
    pendentes = df[df["status"].str.lower() == "pendente"]
    
    if pendentes.empty:
        print("Nenhuma pendência encontrada.")
        return

    # 3. Métrica de impacto
    total_devido = pendentes["valor_devido"].sum()
    print(f"Encontrados {len(pendentes)} clientes em atraso. Total pendente: R$ {total_devido:.2f}")

    # Configurações do servidor SMTP
    email_remetente = os.getenv("EMAIL_REMETENTE", "").strip()
    email_senha = os.getenv("EMAIL_SENHA", "").strip()
    email_assunto = os.getenv("EMAIL_ASSUNTO", "").strip()
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com").strip()
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    log_disparos = []
    total_enviados = 0
    total_falhas = 0

    # 4. Conexão com o servidor SMTP e envio
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_remetente, email_senha)
            
            # Loop de envio dos e-mails de cobrança
            for _, cliente in pendentes.iterrows():
                hora_envio = datetime.now().strftime("%H:%M:%S")

                try:
                    msg = EmailMessage()
                    msg["Subject"] = email_assunto
                    msg["From"] = email_remetente
                    msg["To"] = cliente["email"]
                
                    # Monta os dados para o template
                    dados_cliente = {
                        "nome": cliente["nome"],
                        "valor_devido": f"{cliente['valor_devido']:.2f}",
                        "data_vencimento": cliente["data_vencimento"]
                    }
                
                    # Gera o corpo HTML dinâmico
                    corpo_html = carregar_template("templates/email.html", dados_cliente)
                    
                    # Define o conteúdo da mensagem como HTML
                    msg.add_alternative(corpo_html, subtype="html")
                
                    server.send_message(msg)
                    print(f"[E-MAIL ENVIADO COM SUCESSO] Para: {cliente['email']} | Valor: R$ {cliente['valor_devido']:.2f}")

                    log_disparos.append({
                        "hora": hora_envio,
                        "cliente": cliente["nome"],
                        "email": cliente["email"],
                        "valor": f"R$ {cliente['valor_devido']:.2f}",
                        "status": "Sucesso",
                        "classe": "status-sucesso"
                    })
                    total_enviados += 1

                except Exception as e:
                    print(f"[ERRO] Falha ao enviar para {cliente['email']}: {e}")
                    log_disparos.append({
                        "hora": hora_envio,
                        "cliente": cliente["nome"],
                        "email": cliente["email"],
                        "valor": f"R$ {cliente['valor_devido']:.2f}",
                        "status": "Erro",
                        "classe": "status-erro"
                    })
                    total_falhas += 1
            
        # 5. Gera relatorio
        agora = datetime.now()
        data_hoje = agora.strftime("%d/%m/%Y às %H:%M:%S")

        # Criação do nome dinâmico do arquivo com data e hora
        timestamp_arquivo = agora.strftime("%d_%m_%Y_%H-%M-%S")
        caminho_pdf = f"relatorio_execucao_{timestamp_arquivo}.pdf"

        linhas_html = ""
        sucessos = sum(1 for l in log_disparos if l["status"] == "Sucesso")
        falhas = len(log_disparos) - sucessos

        for i, log in enumerate(log_disparos):
            classe_linha = "row-even" if i % 2 == 0 else ""
            
            linhas_html += f"""
                <tr class="{classe_linha}">
                    <td>{log['hora']}</td>
                    <td>{log['cliente']}</td>
                    <td>{log['email']}</td>
                    <td>{log['valor']}</td>
                    <td class="{log['classe']}">{log['status']}</td>
                </tr>
                """
        
        dados_pdf = {
            "data_execucao": str(data_hoje),
            "total_processados": str(len(log_disparos)),
            "total_sucesso": str(sucessos),
            "total_falhas": str(falhas),
            "linhas_tabela": str(linhas_html)
        }

        # Carrega o template do PDF e gera o arquivo
        corpo_pdf = carregar_template("templates/relatorio_pdf.html", dados_pdf)
        gerar_pdf(corpo_pdf, caminho_pdf)

        print(f"\n[PDF Gerado]: {caminho_pdf}")

        # Envio do relatório com o pdf anexado para o remetente
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_remetente, email_senha)

                msg_relatorio = EmailMessage()
                msg_relatorio["Subject"] = f"📊 Relatório de Disparos RPA - {data_hoje}"
                msg_relatorio["From"] = str(email_remetente)
                msg_relatorio["To"] = str(email_remetente)

                # Garantindo texto formatado estritamente como String
                texto_corpo = f"Olá!\n\nSegue em anexo o relatório consolidado de envios realizado em {data_hoje}."
                msg_relatorio.set_content(texto_corpo)

                # Anexando o PDF ao relatorio
                with open(caminho_pdf, "rb") as f:
                    pdf_data = f.read()
                    msg_relatorio.add_attachment(
                        pdf_data,
                        maintype="application",
                        subtype="pdf",
                        filename=os.path.basename(caminho_pdf)
                    )

                server.send_message(msg_relatorio)
                print("\n[SUCESSO] Relatório de acompanhamento em PDF enviado para o remetente!")

        except Exception as e:
            print(f"Erro ao processar fluxo: {e}")
            

    except Exception as e:
        print(f"Erro ao enviar e-mails: {e}")

if __name__ == "__main__":
    processar_e_notificar()