# 🧠 WebApp - IA e Saúde Mental no Ambiente Corporativo

Projeto desenvolvido para a **Global Solution** da disciplina **Cloud Solutions** da FIAP.

## 📋 Sobre o Projeto

Aplicação web desenvolvida em Python/Flask hospedada na **Azure** que analisa dados sobre saúde mental no setor de tecnologia, utilizando o dataset "Mental Health in Tech Survey" do Kaggle.

O objetivo é demonstrar como a **Inteligência Artificial** pode ser aplicada para identificar padrões de risco relacionados ao burnout e estresse ocupacional no ambiente corporativo.

## 🎯 Tema

**IA Preditiva para Saúde Mental no Ambiente Corporativo**

## 🚀 Tecnologias Utilizadas

- **Python 3.12**
- **Flask** - Framework web
- **Pandas** - Manipulação de dados
- **Azure App Service** - Hospedagem
- **Azure CLI** - Provisionamento de infraestrutura
- **GitHub Actions** - CI/CD

## 📊 Funcionalidades

- ✅ Dashboard com métricas de saúde mental
- ✅ Visualização de dados do dataset Kaggle
- ✅ Upload de arquivos CSV personalizados
- ✅ Análise estatística automatizada
- ✅ Interface responsiva e moderna

## 🏗️ Infraestrutura Azure

A infraestrutura foi provisionada utilizando **Azure CLI** com os seguintes recursos:

- **Resource Group:** `rg-saudemental-gs`
- **App Service Plan:** `plan-saudemental-gs` (Linux, B1)
- **WebApp:** `webapp-saudemental-antonio`
- **Runtime:** Python 3.12
- **Localização:** Brazil South

## 📂 Estrutura do Projeto

```
.
├── app.py                          # Aplicação Flask
├── requirements.txt                # Dependências Python
├── startup.txt                     # Comando de inicialização
├── data/
│   └── mental_health_tech_survey.csv
├── templates/
│   ├── index.html                  # Dashboard principal
│   ├── upload.html                 # Página de upload
│   └── view_csv.html              # Visualização de CSV
├── uploads/                        # CSVs enviados pelos usuários
└── .github/
    └── workflows/
        └── main_webapp-*.yml       # GitHub Actions
```

## 🔧 Como Executar Localmente

```bash
# Clonar o repositório
git clone https://github.com/Degocardoso/displaycsv.git
cd displaycsv

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python app.py
```

Acesse: http://localhost:5000

## ☁️ Deploy na Azure

### Provisionamento de Infraestrutura

Execute o script disponível na pasta `/infra`:

**Linux/Mac:**
```bash
chmod +x deploy-azure-simples.sh
./deploy-azure-simples.sh
```

**Windows:**
```powershell
.\deploy-azure-simples.ps1
```

### Deploy Contínuo

O deploy é automatizado via **GitHub Actions**. Toda alteração na branch `main` dispara o workflow de deploy.

## 🌐 URL da Aplicação

https://webapp-saudemental-antonio.azurewebsites.net

## 📊 Dataset

**Fonte:** Mental Health in Tech Survey (Kaggle - OSMI)  
**Link:** https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey

O dataset contém respostas de profissionais de tecnologia sobre:
- Histórico de problemas de saúde mental
- Tratamento recebido
- Ambiente de trabalho
- Benefícios oferecidos pelas empresas
- Interferência no trabalho

## 🎓 Equipe

**Disciplina:** Cloud Solutions  
**Turma:** 2TSC  
**Instituição:** FIAP  
**Projeto:** Global Solution 2024

**Integrantes:**
- RM557806 - Antônio Carlos Cardoso
- RM557325 - Lucas Favaro
- RM556261 - Guilherme Canella

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos.

---

Desenvolvido com 💙 para a Global Solution - FIAP
