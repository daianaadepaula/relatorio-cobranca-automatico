import os
import smtplib
import re
from email.message import EmailMessage
import pandas as pd
from dotenv import load_dotenv

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

    # 4. Conexão com o servidor SMTP e envio
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_remetente, email_senha)
            
            for _, cliente in pendentes.iterrows():
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

    except Exception as e:
        print(f"Erro ao enviar e-mails: {e}")

if __name__ == "__main__":
    processar_e_notificar()