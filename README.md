# Mangalens 🎴🔍

O Mangalens é uma aplicação Full Stack focada na identificação de animes e mangás através de imagens, utilizando visão computacional, embeddings e integração com APIs especializadas.

Atualmente o projeto é capaz de identificar animes utilizando APIs especializadas e exibir automaticamente a capa da obra encontrada.

O projeto foi desenvolvido com foco em:

* Arquitetura Backend
* Integração com APIs externas
* Processamento de imagens
* Inteligência Artificial aplicada
* UX/UI
* Portfólio Full Stack

---

# ✨ Demonstração do Projeto 

## Upload da imagem

<p align="center">
  <img src="assets/demo-upload.png" width="80%" alt="Tela de upload do Mangalens">
</p>

## Resultado da identificação

<p align="center">
  <img src="assets/demo-result.png" width="80%" alt="Resultado da identificação no Mangalens">
</p>

---

# ✨ Funcionalidades atuais

✅ Upload de imagens

✅ Pré-processamento de imagens

✅ Geração de embeddings

✅ Busca por similaridade local

✅ Integração com Trace.moe

✅ Integração com SauceNAO

✅ Integração com AniList

✅ Busca automática de capas de anime

✅ Fallback automático entre APIs

✅ Validação de confiança e similaridade

✅ Interface web desenvolvida com Streamlit

✅ API REST desenvolvida com FastAPI

---

# 🧠 Como funciona

O sistema segue o seguinte fluxo:

```text
Imagem enviada
      ↓
Pré-processamento
      ↓
Tentativa de reconhecimento via Trace.moe
      ↓
Fallback para SauceNAO
      ↓
Busca da capa via AniList
      ↓
Retorno final para a interface
```

---

# 🛠️ Tecnologias utilizadas

## Backend

* Python
* FastAPI
* Uvicorn
* Requests
* Pydantic

## Frontend

* Streamlit

## Processamento de imagem

* Pillow
* NumPy

## APIs externas

* Trace.moe
* SauceNAO
* AniList

---

# 📂 Estrutura do projeto

```text
app/
├── config/
├── integrations/
├── routes/
├── schemas/
├── services/
├── uploads/
└── main.py

frontend/
├── components/
│   └── result_card.py
│
├── services/
│   └── api.py
│
└── streamlit_app.py

assets/
├── demo-upload.png
└── demo-resultado.png
```

---

# 🚀 Como executar o projeto

## 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
```

## 2. Acesse a pasta do projeto

```bash
cd Mangalens
```

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 4. Configure o arquivo .env

Crie um arquivo:

```text
.env
```

E adicione:

```env
SAUCENAO_API_KEY=sua_chave_aqui
```

## 5. Execute a API

```bash
uvicorn app.main:app --reload
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## 6. Execute o Frontend

```bash
streamlit run frontend/streamlit_app.py
```

---

# 📌 Status do projeto

🚧 Em desenvolvimento

### Próximas melhorias

* Banco próprio de capas de anime
* Reconhecimento de capas oficiais
* Reconhecimento de páginas e painéis de mangá
* Expansão do banco de dados de imagens
* Deploy em produção
* Melhorias contínuas de UX/UI

---

# 🎯 Objetivos de aprendizado

Este projeto foi criado para aprofundar conhecimentos em:

* Desenvolvimento Backend
* Desenvolvimento Frontend
* Integração com APIs
* Processamento de imagens
* Inteligência Artificial aplicada
* Arquitetura de Software
* UX/UI Design
* Desenvolvimento Full Stack

---

# 👨‍💻 Autor

**Nicolas Moraes**

Estudante de Análise e Desenvolvimento de Sistemas, com foco em desenvolvimento web, UX/UI e aplicações utilizando Inteligência Artificial.

Projeto desenvolvido para fins de estudo, prática e composição de portfólio.
