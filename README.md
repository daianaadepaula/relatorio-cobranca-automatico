# 📬 Relatório e Notificador Automático de Cobrança

Sistema automatizado em Python estruturado em arquitetura modular para identificação de pendências financeiras em planilhas Excel ou arquivos CSV, consolidação de métricas de inadimplência, disparo de notificações personalizadas por e-mail com templates em HTML e geração de relatório executivo em PDF com envio automático para o gestor.

---

## 🎯 Objetivo do Projeto

O objetivo principal deste projeto é automatizar a rotina do setor financeiro/administrativo na identificação e contato com clientes inadimplentes. Em vez de checar planilhas manualmente e redigir e-mails um a um, o sistema processa a base de dados (em **Excel** ou **CSV**), calcula o montante em aberto, valida os dados, envia lembretes formais e amigáveis diretamente para cada cliente e gera um relatório consolidado em PDF para auditoria e acompanhamento da gestão.

---

## 💡 O que este projeto resolve?

* **Elimina o trabalho manual:** Substitui o envio repetitivo e manual de avisos de cobrança por um fluxo 100% automatizado.
* **Flexibilidade de Entrada (Excel & CSV):** Reconhece automaticamente planilhas `.xlsx` ou arquivos `.csv`, permitindo que o time trabalhe com o formato de preferência.
* **Validação de Dados e Resiliência:** Valida o formato dos e-mails com Regex antes do envio e possui tratamento individual de exceções para que falhas pontuais não interrompam os demais disparos.
* **Confiabilidade com Testes Automatizados:** Suíte de testes unitários com `pytest` para garantir a estabilidade das funções críticas.
* **Reduz falhas humanas:** Garante que valores, nomes e datas de vencimento cheguem corretos a cada destinatário sem erros de digitação.
* **Auditoria e Acompanhamento em PDF:** Gera automaticamente um relatório executivo em PDF com KPIs de disparos (sucessos, falhas e e-mails inválidos) e log detalhado por horário, salvo na pasta `relatorios/`.
* **Notificação da Gestão:** Envia o relatório em PDF recém-gerado como anexo para o e-mail do remetente/responsável ao fim da execução.
* **Arquitetura Limpa e Modular:** Código separado em camadas de serviço (`config`, `email_service`, `pdf_service` e `app`).
* **Segurança de credenciais:** Armazena senhas e configurações de e-mail em variáveis de ambiente protegidas (`.env`), impedindo o vazamento acidental em repositórios de código.

---

## 🚀 Funcionalidades

- [x] **Leitura Híbrida de Dados:** Busca e processa automaticamente `dados/clientes.xlsx` ou `dados/clientes.csv` via `pandas` e `openpyxl`.
- [x] **Filtragem Inteligente:** Isola registros com status `Pendente` de forma insensível a maiúsculas/minúsculas.
- [x] **Validação Prévia com Regex:** Verifica se o endereço de e-mail do cliente possui sintaxe válida antes de tentar a conexão SMTP.
- [x] **Testes Automatizados:** Cobertura de testes unitários com `pytest` para validação de regras de validação de e-mails.
- [x] **Métricas Rápidas:** Apresenta no console o número total de inadimplentes e a quantia total devida.
- [x] **Templates de E-mail em HTML:** Permite a customização de layout com marcações dinâmicas (`{nome}`, `{valor_devido}`, `{data_vencimento}`).
- [x] **Envio Seguro via SMTP/TLS:** Conecta-se a servidores SMTP (como Gmail, Outlook ou corporativos) utilizando criptografia TLS.
- [x] **Relatório Executivo em PDF:** Gera um relatório com data e hora dinâmica, cartões de KPIs (total, enviados com sucesso e falhas) e tabela zebrada de auditoria usando `xhtml2pdf`.
- [x] **Organização de Arquivos Gerados:** Cria automaticamente o diretório `relatorios/` para armazenar o histórico dos PDFs gerados.
- [x] **Disparo do Relatório por E-mail:** Anexa e despacha o arquivo PDF gerado diretamente para a caixa de entrada do gestor/remetente.

---

## 📁 Estrutura do Repositório

```text
relatorio-cobranca-automatico/
│
├── dados/
│   ├── clientes.csv          # Base de dados em CSV
│   └── clientes.xlsx         # Base de dados em Excel (prioritária caso exista)
│
├── relatorios/               # Diretório onde os relatórios gerados em PDF são salvos (ignorado no Git)
│
├── src/
│   ├── __init__.py           # Identificador do pacote Python
│   ├── app.py                # Orquestrador principal do fluxo de automação
│   ├── config.py             # Configurações centralizadas e leitura do .env
│   ├── email_service.py      # Serviços de validação e disparo de e-mails (cliente e gestor)
│   └── pdf_service.py        # Serviços de renderização de template e compilação do PDF
│
├── templates/
│   ├── email.html            # Template do corpo do e-mail de cobrança (HTML/CSS)
│   └── relatorio_pdf.html    # Template do relatório executivo em PDF (HTML/CSS com KPIs)
│
├── tests/
│   └── test_email_service.py # Testes automatizados com pytest
│
├── .env.example              # Exemplo de configuração das variáveis de ambiente
├── .gitignore                # Arquivos e pastas ignorados pelo Git (.venv, .env, relatorios/, etc.)
├── requirements.txt          # Dependências do projeto (pandas, openpyxl, pytest, xhtml2pdf, etc.)
└── README.md                 # Documentação do projeto
```

---

## 🛠️ Pré-requisitos

* **Python 3.10+** instalado na máquina.
* Uma conta de e-mail para envio (caso utilize o **Gmail**, é necessário gerar uma **Senha de Aplicativo** nas configurações de segurança da sua Conta Google).

---

## ⚙️ Instalação e Configuração

Siga os passos abaixo para configurar o projeto no Windows:

### 1. Clonar ou Abrir a Pasta do Projeto
Abra o terminal (PowerShell, CMD ou Git Bash) no diretório do projeto:
```powershell
cd c:\Users\Daiana\Desktop\python\relatorio-cobranca-automatico
```

### 2. Criar o Ambiente Virtual (`venv`)
Crie um ambiente virtual isolado para o projeto:
```powershell
python -m venv .venv
```

### 3. Ativar o Ambiente Virtual

* **No PowerShell:**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  *(Caso receba aviso de restrição de script no PowerShell, execute primeiro `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` e tente novamente).*

* **No Prompt de Comando (CMD):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```

* **No Git Bash:**
  ```bash
  source .venv/Scripts/activate
  ```

> Quando ativado, o terminal exibirá o prefixo `(.venv)` no início da linha.

### 4. Instalar as Dependências
Com o ambiente ativado, instale os pacotes listados no `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### 5. Configurar as Variáveis de Ambiente (`.env`)
Crie uma cópia do arquivo `.env.example` com o nome `.env`:
```powershell
Copy-Item .env.example .env
```
Abra o arquivo `.env` e preencha suas configurações de e-mail:
```env
# Configurações de E-mail
EMAIL_REMETENTE=seu_email@gmail.com
EMAIL_SENHA=sua_senha_de_app_de_16_digitos
EMAIL_ASSUNTO=Aviso de Pendência Financeira
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

> **Dica para o Gmail:** A `EMAIL_SENHA` não é a senha do seu e-mail padrão. Acesse **Gerenciar Conta Google > Segurança > Verificação em 2 etapas > Senhas de app**, crie uma nova chave de 16 caracteres e cole no `.env`.

---

## 🖥️ Como Usar

### 1. Atualizar a base de dados
Insira os clientes e suas pendências no arquivo `dados/clientes.xlsx` ou `dados/clientes.csv`:
```csv
nome,email,valor_devido,data_vencimento,status
Ana Silva,ana@email.com,250.00,10-08-2026,Pendente
Beatriz Souza,beatriz@email.com,450.00,15-08-2026,Pago
Carlos Lima,carlos@email.com,120.50,01-09-2026,Pago
Daniel Rodrigues,daniel@email.com,500.50,10-09-2026,Pendente
Eduarda Dias,eduarda@email.com,750.50,10-09-2026,Pendente
Felipe Santos,felipe@email.com,300.00,10-09-2026,Pago
```

### 2. Executar os Testes Automatizados
Para garantir que as regras e funções de validação estão funcionando corretamente:
```powershell
python -m pytest
```

### 3. Executar a Automação
Com o ambiente virtual ativado, execute o módulo a partir da raiz do projeto:
```powershell
python -m src.app
```

### 4. Exemplo de Saída no Terminal
```text
[INFO] Lendo dados da planilha Excel...
Encontrados 3 clientes em atraso. Total pendente: R$ 1801.00
[E-MAIL ENVIADO COM SUCESSO] Para: ana@email.com | Valor: R$ 250.00
[E-MAIL ENVIADO COM SUCESSO] Para: daniel@email.com | Valor: R$ 500.50
[E-MAIL ENVIADO COM SUCESSO] Para: eduarda@email.com | Valor: R$ 750.50

[PDF Gerado]: relatorios\relatorio_execucao_10_09_2026_20-58-30.pdf

[SUCESSO] Relatório de acompanhamento em PDF enviado para o remetente!

[SUCESSO] Relatório enviado para o gestor!
```

### 5. Como Desativar o Ambiente Virtual
Após a utilização, basta digitar no terminal:
```powershell
deactivate
```

---

## 📦 Tecnologias Utilizadas

* [Python](https://www.python.org/) - Linguagem de programação principal.
* [Pandas](https://pandas.pydata.org/) - Manipulação e análise dos dados tabulares.
* [openpyxl](https://openpyxl.readthedocs.io/) - Leitura e manipulação de planilhas Excel (.xlsx).
* [pytest](https://docs.pytest.org/) - Framework para testes automatizados.
* [xhtml2pdf](https://github.com/xhtml2pdf/xhtml2pdf) / [ReportLab](https://www.reportlab.com/) - Conversão de templates HTML/CSS em relatórios PDF executivos.
* [python-dotenv](https://pypi.org/project/python-dotenv/) - Gerenciamento de variáveis de ambiente.
* [smtplib & email.message](https://docs.python.org/3/library/email.message.html) - Conexão SMTP segura (TLS), composição de mensagens e anexação de relatórios.
* **HTML5 & CSS3** - Estruturação visual dos templates de e-mail e relatórios impressos.

---

## 🛠️ Desafios Encontrados e Soluções Implementadas

Durante o desenvolvimento da automação, surgiram desafios técnicos práticos de renderização, concorrência SMTP e resolução de pacotes. Abaixo estão documentadas as principais dificuldades e como foram superadas:

### 1. Incompatibilidades do Renderizador HTML/CSS (`xhtml2pdf`)
* **Desafio:** Ao estilizar o relatório em PDF com CSS moderno, o console apresentava avisos e falhas silenciosas devido à falta de suporte a propriedades como `border-radius`, `border-collapse` e seletores avançados como `@bottom-right` com `counter(page)`. Em alguns cenários, colunas de e-mail sobrepunham os valores monetários.
* **Solução:** O template `relatorio_pdf.html` foi refatorado para utilizar estritamente regras de CSS 2.1 e layout baseados em tabelas HTML com larguras percentuais explícitas (`width="%"`) em cada coluna. Isso garantiu a renderização visual idêntica em qualquer sistema operacional sem sobreposição de textos.

### 2. Tratamento de Exceções no Envio SMTP do Relatório
* **Desafio:** O envio do e-mail de cobrança individual para os clientes e o disparo final do relatório em PDF compartilhavam a mesma conexão SMTP. Caso a conexão sofresse um timeout durante a geração do PDF local, a tentativa de reaproveitar o socket gerava exceções como `'NotImplementedType' object is not iterable` ao montar o cabeçalho.
* **Solução:** A arquitetura do `email_service.py` foi estruturada para isolar o ciclo de vida da conexão do relatório final em um bloco de contexto dedicado (`with smtplib.SMTP(...) as server_relatorio`). Além disso, todas as propriedades dinamizadas do template foram explicitamente convertidas para `str()`.

### 3. Falha de Importação do Pacote `src` na Suíte de Testes (`pytest`)
* **Desafio:** Ao executar a suíte de testes com o comando `pytest`, o interpretador não reconhecia a pasta `src/` como um módulo acessível, resultando no erro `ModuleNotFoundError: No module named 'src'`.
* **Solução:** Foi adicionado o arquivo de configuração `pytest.ini` definindo `pythonpath = .`, garantindo que o diretório raiz seja adicionado ao caminho de importação do Python. Alternativamente, padronizou-se a chamada da suíte pelo terminal via módulo nativo: `python -m pytest`.

### 4. Validação Prévia de Dados e Redirecionamento Indevido
* **Desafio:** Registros da planilha com e-mails malformatados ou ausentes geravam exceções no servidor SMTP e, em fluxos anteriores, tentavam enviar mensagens para o próprio remetente como *fallback*, inflando o log como "Sucesso".
* **Solução:** Implementou-se a validação prévia com Regex via `email_valido()` antes do bloco `try/except` de envio. Registros inválidos são descartados do envio imediatamente, contabilizados como `E-mail Inválido` no resumo executivo e destacados em vermelho no relatório final.
