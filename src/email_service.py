import os
import smtplib
import re
from email.message import EmailMessage
from src.config import Config

def email_valido(email:str) -> bool:
    """Valida formato do e-mail."""
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(padrao, str(email)))

def enviar_email_cliente(server: smtplib.SMTP, destinatario: str, corpo_html: str):
    """Monta e dispara o e-mail de cobrança individual."""
    msg = EmailMessage()
    msg["Subject"] = Config.email_assunto
    msg["From"] = Config.email_remetente
    msg["To"] = destinatario
    msg.add_alternative(corpo_html, subtype="html")
    server.send_message(msg)

def enviar_relatorio_gestao(caminho_pdf:str, data_hoje:str):
    # Envio do relatório com o pdf anexado para o remetente
        try:
            with smtplib.SMTP(Config.smtp_server, Config.smtp_port) as server:
                server.starttls()
                server.login(Config.email_remetente, Config.email_senha)

                msg_relatorio = EmailMessage()
                msg_relatorio["Subject"] = f"📊 Relatório de Disparos RPA - {data_hoje}"
                msg_relatorio["From"] = str(Config.email_remetente)
                msg_relatorio["To"] = str(Config.email_remetente)

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
        