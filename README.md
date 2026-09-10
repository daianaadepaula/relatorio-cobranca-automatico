# 📬 Relatório e Notificador Automático de Cobrança

Sistema automatizado em Python para identificação de pendências financeiras, consolidação de métricas de inadimplência e disparo de notificações personalizadas por e-mail com templates em HTML.

---

## 🎯 Objetivo do Projeto

O objetivo principal deste projeto é automatizar a rotina do setor financeiro/administrativo na identificação e contato com clientes inadimplentes. Em vez de checar planilhas manualmente e redigir e-mails um a um, o sistema processa a base de dados, calcula o montante em aberto e envia lembretes formais e amigáveis diretamente para cada cliente.

---

## 💡 O que este projeto resolve?

* **Elimina o trabalho manual:** Substitui o envio repetitivo e manual de avisos de cobrança por um fluxo 100% automatizado.
* **Reduz falhas humanas:** Garante que valores, nomes e datas de vencimento cheguem corretos a cada destinatário sem erros de digitação.
* **Visibilidade imediata do caixa:** Calcula instantaneamente quantos clientes estão em atraso e o valor total acumulado da pendência.
* **Comunicação profissional:** Utiliza um template HTML visualmente limpo, responsivo e seguro, transmitindo credibilidade na cobrança.
* **Segurança de credenciais:** Armazena senhas e configurações de e-mail em variáveis de ambiente protegidas (`.env`), impedindo o vazamento acidental em repositórios de código.

---

## 🚀 Funcionalidades

- [x] **Leitura Dinâmica de Dados:** Processa bases de clientes em formato CSV através da biblioteca `pandas`.
- [x] **Filtragem Inteligente:** Isola registros com status `Pendente` de forma insensível a maiúsculas/minúsculas.
- [x] **Métricas Rápidas:** Apresenta no console o número total de inadimplentes e a quantia total devida.
- [x] **Templates de E-mail em HTML:** Permite a customização de layout com marcações dinâmicas (`{nome}`, `{valor_devido}`, `{data_vencimento}`).
- [x] **Envio Seguro via SMTP/TLS:** Conecta-se a servidores SMTP (como Gmail, Outlook ou corporativos) utilizando criptografia TLS.

---

## 📁 Estrutura do Repositório

```text
relatorio-cobranca-automatico/
│
├── dados/
│   └── clientes.csv          # Base de dados (nome, email, valor_devido, vencimento, status)
│
├── src/
│   └── app.py                # Script principal de execução da automação
│
├── templates/
│   └── email.html            # Template do corpo do e-mail em HTML/CSS
│
├── .env.example              # Exemplo de configuração das variáveis de ambiente
├── .gitignore                # Arquivos e pastas ignorados pelo Git (.venv, .env, etc.)
├── requirements.txt          # Dependências do projeto (pandas, python-dotenv)
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
Insira os clientes e suas pendências no arquivo `dados/clientes.csv`:
```csv
nome,email,valor_devido,data_vencimento,status
Ana Silva,ana@email.com,250.00,10-08-2026,Pendente
Carlos Lima,carlos@email.com,120.50,01-09-2026,Pago
Beatriz Souza,beatriz@email.com,450.00,15-08-2026,Pendente
```

### 2. Executar a Automação
Com o ambiente virtual ativado, execute o script:
```powershell
python src/app.py
```

### 3. Exemplo de Saída no Terminal
```text
Encontrados 2 clientes em atraso. Total pendente: R$ 950.50
[E-MAIL ENVIADO COM SUCESSO] Para: ana@email.com | Valor: R$ 250.00
[E-MAIL ENVIADO COM SUCESSO] Para: beatriz@email.com | Valor: R$ 450.00
```

### 4. Como Desativar o Ambiente Virtual
Após a utilização, basta digitar no terminal:
```powershell
deactivate
```

---

## 📦 Tecnologias Utilizadas

* [Python](https://www.python.org/) - Linguagem de programação.
* [Pandas](https://pandas.pydata.org/) - Manipulação e análise da base de dados.
* [python-dotenv](https://pypi.org/project/python-dotenv/) - Gerenciamento de variáveis de ambiente.
* [smtplib & email.message](https://docs.python.org/3/library/email.message.html) - Conexão SMTP e composição de mensagens.
* **HTML5 & CSS3** - Estruturação e estilização do template de e-mail.
