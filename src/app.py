import os
import smtplib
from datetime import datetime
import pandas as pd
from src.config import Config
from src.email_service import email_valido, enviar_email_cliente, enviar_relatorio_gestao
from src.pdf_service import carregar_template, gerar_pdf

def carregar_dados_clientes():
    """Busca e carrega automaticamente clientes.xlsx ou clientes.csv."""
    caminho_excel = os.path.join("dados", "clientes.xlsx")
    caminho_csv = os.path.join("dados", "clientes.csv")

    if os.path.exists(caminho_excel):
        print("[INFO] Lendo dados da planilha Excel...")
        return pd.read_excel(caminho_excel)
    elif os.path.exists(caminho_csv):
        print("[INFO] Lendo dados do arquivo CSV...")
        return pd.read_csv(caminho_csv)
    else:
        raise FileNotFoundError("Nenhum arquivo 'clientes.xlsx' ou 'clientes.csv' foi encontrado na pasta 'dados/'.")

def processar_e_notificar():
    # 1. Leitura e filtragem dos dados (aceita CSV ou Excel)
    df = carregar_dados_clientes()  
    # 2. Filtra apenas os clientes inadimplentes
    pendentes = df[df["status"].str.lower() == "pendente"]
    
    if pendentes.empty:
        print("Nenhuma pendência encontrada.")
        return

    # 3. Métrica de impacto
    total_devido = pendentes["valor_devido"].sum()
    print(f"Encontrados {len(pendentes)} clientes em atraso. Total pendente: R$ {total_devido:.2f}")

    log_disparos = []
    total_enviados = 0
    total_falhas = 0

    # 3. Conexão com o servidor SMTP e envio
    try:
        with smtplib.SMTP(Config.smtp_server, Config.smtp_port) as server:
            server.starttls()
            server.login(Config.email_remetente, Config.email_senha)
            
            # Loop de envio dos e-mails de cobrança
            for _, cliente in pendentes.iterrows():
                hora_envio = datetime.now().strftime("%H:%M:%S")
                email_destino = str(cliente["email"]).strip()

                if not email_valido(email_destino):
                    print(f"[ERRO] E-mail inválido para: {cliente['nome']}")
                    log_disparos.append({
                        "hora": hora_envio, "cliente": cliente["nome"],
                        "email": email_destino, "valor": f"R$ {cliente['valor_devido']:.2f}",
                        "status": "E-mail Inválido", "classe": "status-erro"
                    })

                    continue

                try:                
                    # Monta os dados para o template
                    dados_cliente = {
                        "nome": cliente["nome"],
                        "valor_devido": f"{cliente['valor_devido']:.2f}",
                        "data_vencimento": cliente["data_vencimento"]
                    }
                
                    # Gera o corpo HTML dinâmico
                    corpo_html = carregar_template("templates/email.html", dados_cliente)
                    # Define o conteúdo da mensagem como HTML
                    enviar_email_cliente(server, email_destino, corpo_html)
                                    
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
        nome_arquivo = f"relatorio_execucao_{timestamp_arquivo}.pdf"
        caminho_pdf = os.path.join("relatorios", nome_arquivo)

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

        # 6. Envio de relatório final para a gestão
        enviar_relatorio_gestao(caminho_pdf, data_hoje)
        print("\n[SUCESSO] Relatório enviado para o gestor!")
    
    except Exception as e:
        print(f"Erro ao enviar e-mails: {e}")

    
if __name__ == "__main__":
    processar_e_notificar()