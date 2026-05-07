# Setup da Demo

## Estrutura final do repositório

```
seu-repo/
├── .github/
│   └── workflows/
│       ├── analista.md         # agente analista (gh-aw)
│       ├── arquiteto.md        # agente arquiteto (gh-aw)
│       ├── ci.yml              # roda pytest em PRs
│       └── triagem.md          # sua PoC atual (mantém)
├── app/
│   ├── __init__.py             # vazio
│   ├── main.py
│   ├── models.py
│   └── storage.py
├── tests/
│   ├── __init__.py             # vazio
│   └── test_main.py
├── specs/
│   └── .gitkeep                # vazio - vai encher na demo
├── requirements.txt
└── README.md
```

## Passo a passo

### 1. Crie a estrutura do repositório (15 min)

```bash
mkdir minha-demo-agentes && cd minha-demo-agentes
git init
mkdir -p app tests specs .github/workflows
touch app/__init__.py tests/__init__.py specs/.gitkeep
```

Cole os arquivos que eu gerei nos lugares certos:
- `analista.md` e `arquiteto.md` em `.github/workflows/`
- `ci.yml` em `.github/workflows/`
- `app/main.py`, `app/models.py`, `app/storage.py`
- `tests/test_main.py`
- `requirements.txt`
- `README.md`

### 2. Valide localmente (10 min)

```bash
pip install -r requirements.txt
pytest -v
```

Os 9 testes devem passar. Se algum quebrar, ajuste antes de seguir — o agente arquiteto depende dessa base saudável.

### 3. Suba pro GitHub (5 min)

Cria um repo novo no GitHub (privado), commita tudo, e habilita:

- **Settings → Actions → General**: permite "Read and write permissions" pro `GITHUB_TOKEN`
- **Settings → Code security**: certifique que GitHub Actions está habilitado
- **Settings → Copilot**: confirme que Copilot está habilitado pro repo

### 4. Crie as labels que os agentes usam (3 min)

No menu Issues → Labels do repo, cria:

- `precisa-spec` — gatilho do agente analista
- `spec` — aplicada nos PRs do analista
- `precisa-revisao` — aplicada em todos os PRs de agente
- `implementação` — aplicada nos PRs do arquiteto

### 5. Configure branch protection (5 min)

**Settings → Branches → Add rule** em `main`:
- Require a pull request before merging
- Require approvals: 1
- Require status checks to pass: marque o job `test` do `ci.yml`

Isso garante que os PRs dos agentes não fazem merge sem você aprovar e sem testes passando.

### 6. Compile e ative os workflows gh-aw (10 min)

Se você ainda não tem o gh-aw CLI:

```bash
gh extension install github/gh-aw
```

Compila os workflows agênticos:

```bash
gh aw compile
```

Isso gera os arquivos `.lock.yml` correspondentes. Commita e dá push.

### 7. Faça uma rodada de teste antes da demo (40 min)

Use o texto de issue de exemplo abaixo. Veja o ciclo inteiro funcionar uma vez. Se algo quebrar (agente travou, prompt confuso, teste falhou), ajuste agora — não na frente do cliente.

---

## Issue de exemplo pra demo

Cole o texto abaixo numa nova issue do repo:

**Título:** `Adicionar prioridade nas tarefas`

**Corpo:**

```
Como gerente de operações, preciso conseguir marcar tarefas como prioridade alta, média ou baixa, pra organizar o trabalho da minha equipe.

Hoje todas as tarefas aparecem na listagem em ordem de criação, sem nenhum sinal de quais são mais urgentes. Isso faz com que coisas críticas fiquem perdidas no meio de tarefas rotineiras.

O que eu preciso:

- Ao criar uma tarefa, poder definir a prioridade (alta / média / baixa)
- Se eu não definir, a prioridade default é média
- Ao listar tarefas, ver a prioridade de cada uma
- Conseguir filtrar a listagem por prioridade (ex: só ver as de prioridade alta)
- Conseguir alterar a prioridade de uma tarefa existente

Não precisa de ordenação automática nem de notificação — só preciso ver e filtrar.
```

Depois de criar a issue, **adicione a label `precisa-spec`**. O analista dispara em segundos.

---

## Roteiro da demo (≈ 7 minutos)

**0:00 — Abertura (45s)**

> "Esse é um repositório de uma API de tarefas, código simples em FastAPI, suite de testes verde. O diferencial está aqui: dois arquivos markdown em `.github/workflows/` — um agente analista e um agente arquiteto. Markdown puro, versionado igual código. Olha o tamanho disso aqui."

Abre `analista.md`, mostra o frontmatter e o prompt. 30 segundos.

**0:45 — PM abre a issue (30s)**

> "Vou fazer o papel do PM agora. Preciso de uma feature: poder marcar prioridade nas tarefas."

Cola o texto da issue de exemplo, salva, **aplica a label `precisa-spec`**.

**1:15 — Analista trabalha (90s)**

> "Em background, o analista já está rodando. Vou aproveitar pra mostrar o que está acontecendo."

Abre a aba **Actions**. Mostra o workflow `analista` em execução. Volta na issue depois de uns 60-90 segundos — comentário do agente apareceu, com link pro PR.

**2:45 — Revisa a spec (90s)**

Abre o PR. Abre o arquivo `specs/feature-N.md`. Lê em voz alta:

> "Olha o que ele entregou. Necessidade de negócio em linguagem de negócio. Contrato técnico com endpoints, payloads, modelo de dados. Critérios de aceite — cada um vai virar um teste. E aqui no final, riscos e perguntas em aberto: o agente foi honesto sobre o que não dá pra decidir sozinho."

> "Isso aqui é o que um analista júnior levaria meio dia pra escrever. Levou 90 segundos."

**4:15 — Aprova e merge da spec (30s)**

> "Eu como tech lead reviso, faço alguma sugestão pequena se quiser, e aprovo. Esse é o primeiro ponto de aprovação humana — antes do código existir."

Aprova o PR e clica merge.

**4:45 — Arquiteto dispara automático (90s)**

> "O merge dispara o segundo agente — o arquiteto. Ele vai ler a spec que acabamos de aprovar e implementar."

Abre Actions, mostra o workflow `arquiteto` rodando. Espera 1-2 minutos.

**6:15 — Revisa o PR de implementação (60s)**

PR aparece. Abre os arquivos modificados:

> "Código novo em `app/` com a feature. Testes novos em `tests/` cobrindo cada critério de aceite. README atualizado."

Mostra o badge verde do CI: testes passaram.

> "E aqui no corpo do PR — ele lista quais critérios de aceite foram cobertos por quais testes. E declara as decisões que tomou pra resolver os pontos abertos da spec. Auditável."

**7:15 — Merge final e fechamento (30s)**

Aprova, faz merge.

> "Olha aqui — a issue original fechou automaticamente. Tudo isso aqui virou histórico no Git: comentário do PM, spec aprovada, código implementado, testes verdes, decisões documentadas. Um único trilho de auditoria."

**Fechamento:**

> "Da issue do PM até a feature em produção: dois PRs, duas aprovações humanas, zero linha de código digitada por dev. O humano nunca saiu do circuito — aprovou a spec, aprovou o código. O agente fez o trabalho repetitivo no meio. E tudo isso configurado em dois arquivos markdown."

---

## Plano B (se algo travar ao vivo)

Cliente regulado vai querer ver o que acontece quando o agente erra. Ter um plano B ajuda:

- Se o analista travar/demorar: tenha uma spec pronta no `specs/` de uma rodada anterior, faz o "merge" na hora pra disparar o arquiteto.
- Se o arquiteto entregar código quebrado: aprovação humana é justamente isso — abra o PR, mostre o teste falhando, comente o que mudaria, mostre que o agente ajusta.
- Se o Copilot estourar quota: tenha screenshots de uma rodada anterior bem-sucedida.

Honestidade vende. "Os agentes erram às vezes, e é por isso que existem dois pontos de aprovação humana" é uma resposta forte, não fraca.

## Objeções previsíveis e respostas curtas

**"E se o agente apagar código importante?"** Branch protection bloqueia. Sem aprovação humana o PR não merge. CODEOWNERS pode forçar revisor específico em pastas sensíveis (`/billing/`, `/security/`).

**"E o custo?"** Cada rodada do agente consome premium requests do Copilot e minutos de Actions. Pra esse demo: ~5-10 premium requests por ciclo completo. Em escala enterprise, dá pra colocar quota por equipe.

**"E código legado mal testado?"** Aí o agente sofre, é honesto. A regra de ouro é: ele brilha onde os testes existem. Em legado, primeiro plante testes (com agente também), depois delega features.

**"Funciona com Java/C#/Go?"** Sim. O exemplo é Python por simplicidade do demo. A arquitetura agente é stack-agnóstica.

**"Como controlar dados sensíveis?"** Os agentes rodam em sandbox isolado em GitHub Actions. Logs auditáveis. Network firewall do gh-aw permite restringir domínios que o agente acessa. MCP servers podem ser allowlist-ed.
