# Aplicação de Processamento de Currículos com API e Frontend Django

Este projeto consiste em uma API backend (FastAPI) para processar currículos em PDF e um frontend web (Django) para interagir com a API.

## Funcionalidades

- **Backend API (FastAPI):**
    - Recebe um arquivo PDF e uma lista de palavras-chave.
    - Extrai o texto do PDF.
    - Busca as palavras-chave no texto (case-insensitive).
    - Retorna a contagem de cada palavra-chave encontrada.
- **Frontend (Django):**
    - Interface web para upload de currículo (PDF).
    - Campo para inserir palavras-chave (separadas por vírgula).
    - Envia os dados para a API backend.
    - Exibe os resultados:
        - Nome do arquivo processado.
        - Porcentagem de match (palavras encontradas / total de palavras enviadas).
        - Lista de palavras-chave encontradas (com contagem).
        - Lista de palavras-chave não encontradas.

## Estrutura do Projeto

```
/
├── resume_processor_simple/    # Backend API (FastAPI)
│   ├── api/
│   ├── pdf_processor/
│   ├── data/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
├── resume_frontend_django/     # Frontend (Django)
│   ├── frontend_config/        # Configurações do projeto Django
│   ├── processor_interface/    # App Django
│   │   ├── migrations/
│   │   ├── static/
│   │   ├── templates/
│   │   └── ...
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   └── ...
└── docker-compose.yml          # Orquestração dos containers
```

## Pré-requisitos

- Docker
- Docker Compose

## Como Executar

1.  **Clone o repositório** (ou certifique-se de que as pastas `resume_processor_simple` e `resume_frontend_django` e o arquivo `docker-compose.yml` estejam no mesmo diretório).
2.  **Navegue até o diretório raiz** que contém o `docker-compose.yml`.
3.  **Execute o comando:**
    ```bash
    docker-compose up --build -d
    ```
    O comando `--build` garante que as imagens Docker sejam construídas (necessário na primeira vez ou após alterações no código/Dockerfile). O `-d` executa os containers em segundo plano.

4.  **Acesse os serviços:**
    - **Frontend:** Abra seu navegador e acesse `http://localhost:8001`
    - **API:** A API estará rodando em `http://localhost:8000` (o frontend se comunica com ela internamente pela rede Docker).

## Usando o Frontend

1.  Acesse `http://localhost:8001`.
2.  Use o formulário para selecionar um arquivo PDF.
3.  Insira as palavras-chave desejadas, separadas por vírgula.
4.  Clique em "Processar".
5.  Os resultados (porcentagem de match, palavras encontradas e não encontradas) serão exibidos na mesma página.

## Parando a Aplicação

Para parar os containers, execute no mesmo diretório do `docker-compose.yml`:

```bash
docker-compose down
```
