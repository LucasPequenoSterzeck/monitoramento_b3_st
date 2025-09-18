# Projeto de Monitoramento de Ações com Docker e VPS

Este projeto tem como objetivo monitorar, analisar e notificar sobre a movimentação de ações brasileiras utilizando um sistema modular e conteinerizado. Ele serve como uma aplicação prática dos meus conhecimentos em **Docker**, **VPS**, e **Machine Learning**.

---

## 🎯 Objetivos do Projeto

O projeto é dividido em módulos, cada um com uma função específica, o que permite a prática de arquitetura de **micro-serviços**. Os principais objetivos são:

* **Praticar Docker e Docker Compose**: Criar e orquestrar múltiplos contêineres que se comunicam entre si.
* **Utilizar uma VPS**: Implantar a aplicação em um servidor virtual privado na nuvem, simulando um ambiente de produção.
* **Integração de Tecnologias**: Conectar diferentes serviços, como coleta de dados financeiros, um modelo de Machine Learning e APIs externas (Google Sheets e Telegram).
* **Automação**: Criar um sistema que opera de forma autônoma, coletando dados e gerando insights em horários pré-determinados.

---

## 🏗️ Arquitetura do Sistema

O sistema é composto por quatro serviços principais, cada um rodando em seu próprio contêiner Docker:

### 1. Coletor de Dados (`coletor-dados`)
* **Função**: Coleta dados de mercado de 5 ações brasileiras selecionadas.
* **Tecnologia**: Python com a biblioteca `yfinance`.
* **Execução**: Programado para ser executado no início do pregão da B3.

### 2. Modelo de Machine Learning (`modelo-ml`)
* **Função**: Analisa os dados coletados para prever se uma ação é uma boa oportunidade de compra ou venda.
* **Tecnologia**: Python com o modelo **XGBoost**.

### 3. Google Sheets (`google-sheets`)
* **Função**: Registra os resultados da análise em uma planilha Google, criando um histórico acessível de todas as operações.
* **Tecnologia**: Python com a API do Google Sheets.

### 4. Notificador Telegram (`telegram-bot`)
* **Função**: Envia notificações automáticas para um grupo do Telegram, informando sobre as previsões de compra/venda do dia.
* **Tecnologia**: Python com a API do Telegram.

---

## 🐳 Como Executar o Projeto

1.  **Clone o repositório:**
    `git clone <URL_DO_SEU_REPOSITORIO>`

2.  **Acesse o diretório do projeto:**
    `cd <NOME_DO_SEU_PROJETO>`

3.  **Inicie os contêineres com Docker Compose:**
    `docker compose up -d --build`

Isso irá construir as imagens e iniciar todos os serviços em segundo plano na sua VPS.

---

## 🚀 Status do Projeto

* **Coletor de Dados**: ✅
* **Modelo XGBoost**: 🚧 (em desenvolvimento)
* **Integração Google Sheets**: 🚧 (em desenvolvimento)
* **Notificador Telegram**: 🚧 (em desenvolvimento)

---

## 🤝 Contato

Qualquer dúvida ou sugestão, entre em contato. Este projeto é uma jornada de aprendizado contínua!
