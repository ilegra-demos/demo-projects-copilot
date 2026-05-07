# API de Tarefas

API REST simples de gestão de tarefas. Usada como repositório de demonstração de fluxo AI-First com agentes (Analista + Arquiteto).

## Domínio

Cada **tarefa** (`Task`) tem:

- `id` — identificador numérico, gerado automaticamente
- `title` — título obrigatório, 1 a 200 caracteres
- `description` — descrição opcional, até 2000 caracteres
- `completed` — booleano, default `false`
- `created_at` — timestamp UTC, gerado automaticamente

## Endpoints atuais

| Método | Path | Descrição |
|--------|------|-----------|
| `GET` | `/health` | Health check |
| `POST` | `/tasks` | Cria uma nova tarefa |
| `GET` | `/tasks` | Lista todas as tarefas |
| `GET` | `/tasks/{id}` | Busca uma tarefa por ID |
| `PATCH` | `/tasks/{id}` | Atualiza campos de uma tarefa |
| `DELETE` | `/tasks/{id}` | Remove uma tarefa |

## Stack

- Python 3.12
- FastAPI + Pydantic v2
- Armazenamento in-memory (sem banco — é demo)
- pytest + httpx para testes

## Como rodar

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Documentação interativa em http://localhost:8000/docs.

## Como rodar os testes

```bash
pytest -v
```

## Fluxo de evolução do produto (AI-First)

Toda nova feature ou alteração segue o fluxo abaixo:

1. **PM abre uma issue** descrevendo a necessidade em linguagem de negócio e adiciona a label `precisa-spec`.
2. **Agente Analista** (`.github/workflows/analista.md`) lê a issue, explora o código existente, e abre um PR criando o arquivo de especificação técnica em `specs/feature-N.md`.
3. **Humano revisa e merge** a spec — esse é o primeiro ponto de aprovação.
4. **Agente Arquiteto** (`.github/workflows/arquiteto.md`) é disparado pelo merge da spec, lê o documento, e abre um PR implementando código + testes.
5. **Humano revisa e merge** a implementação — segundo ponto de aprovação. A issue original fecha automaticamente via `Fixes #N`.

Os agentes são definidos em arquivos markdown em `.github/workflows/`. Os prompts e ferramentas são versionados como código.
