import os
from xhtml2pdf import pisa

def carregar_template(caminho_template, dados):
    """Lê o arquivo HTML e substitui os marcadores de forma segura."""
    with open(caminho_template, "r", encoding="utf-8") as file:
        template = file.read()
    
    # Substituição manual para não conflitar com as chaves do CSS
    for chave, valor in dados.items():
        template = template.replace(f"{{{chave}}}", str(valor))
        
    return template

def gerar_pdf(corpo_html, caminho_saida_pdf):
    pasta_destino = os.path.dirname(caminho_saida_pdf)

    # Garante que a pasta exista, criando caso contrário
    if pasta_destino:
        os.makedirs(pasta_destino, exist_ok=True)
    
    # Cria o arquivo PDF
    with open(caminho_saida_pdf, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(corpo_html, dest=pdf_file)
    return not pisa_status.err
