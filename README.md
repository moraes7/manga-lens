# Mangalens 🎴🔍

O Mangalens é uma aplicação backend/frontend focada em reconhecimento de animes através de imagens.

O projeto foi desenvolvido com foco em:

* arquitetura backend,
* integração com APIs externas,
* processamento de imagens,
* aprendizado de IA aplicada,
* e experiência de portfólio para desenvolvimento full stack.

---

# ✨ Funcionalidades atuais

✅ Upload de imagens de anime

✅ Processamento e pré-processamento de imagem

✅ Geração de embeddings

✅ Busca por similaridade local

✅ Integração com trace.moe

✅ Integração com SauceNAO

✅ Fallback automático entre APIs

✅ Validação de confiança/similaridade

✅ Interface web com Streamlit

✅ API REST com FastAPI

---

# 🧠 Como funciona

O sistema segue este fluxo:

```text
Imagem enviada
      ↓
Pré-processamento
      ↓
Tentativa de reconhecimento via trace.moe
      ↓
Se falhar:
      ↓
Fallback para SauceNAO
      ↓
Validação de similaridade
      ↓
Retorno final da API
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

* trace.moe
* SauceNAO

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
```

---

# 🚀 Como executar o projeto

## 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
```

---

## 2. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 3. Configure o arquivo .env

Crie um arquivo:

```text
.env
```

E adicione:

```env
SAUCENAO_API_KEY=sua_chave_aqui
```

---

## 4. Execute a API

```bash
uvicorn app.main:app --reload
```

---

## 5. Execute o Streamlit

```bash
streamlit run app/streamlit_app.py
```

---

# 📌 Status do projeto

🚧 Em desenvolvimento

Próximas melhorias:

* melhoria visual da interface
* deploy em produção
* padronização de schemas
* suporte avançado para capas oficiais
* integração com AniList
* banco próprio de capas de anime
* reconhecimento também de painéis de mangá

---

# 👨‍💻 Autor

Nicolas Moraes

Projeto desenvolvido para estudos de:

* Backend
* IA aplicada
* APIs
* Arquitetura de software
* UX/UI
* Portfólio Full Stack
