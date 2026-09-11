import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do servidor SMTP
class Config:
    email_remetente = os.getenv("EMAIL_REMETENTE", "").strip()
    email_senha = os.getenv("EMAIL_SENHA", "").strip()
    email_assunto = os.getenv("EMAIL_ASSUNTO", "").strip()
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com").strip()
    smtp_port = int(os.getenv("SMTP_PORT", 587))
