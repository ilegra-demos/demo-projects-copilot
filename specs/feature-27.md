# Spec: Adicionar prioridade nas tarefas

Issue de origem: #27

## Necessidade de negócio

Gerentes de operações precisam indicar a urgência de cada tarefa (alta, média ou baixa) para
organizar o trabalho da equipe. Atualmente a listagem não fornece nenhum sinal de criticidade,
fazendo com que itens urgentes se percam entre tarefas rotineiras. O campo de prioridade deve
ser visível na listagem e filtrável, sem impacto na ordenação automática.

## Contrato técnico

### Endpoints

**POST /tasks** — criar tarefa com prioridade
- Payload de entrada: `{ "title": "...", "description": "...", "priority": "alta" | "média" | "baixa" }` (priority opcional)
- Payload de saída: `Task` completo com campo `priority`
- Status codes: `201 Created`, `422 Unprocessable Entity`

**GET /tasks** — listar tarefas (com filtro opcional)
- Query param: `priority: "alta" | "média" | "baixa"` (opcional)
- Payload de saída: `List[Task]`
- Status codes: `200 OK`, `422 Unprocessable Entity` (valor inválido no query param)

**GET /tasks/{task_id}** — sem alteração de interface; `priority` passa a integrar a resposta

**PATCH /tasks/{task_id}** — atualizar prioridade
- Payload de entrada: `{ "priority": "alta" | "média" | "baixa" }` (opcional, junto com campos já existentes)
- Payload de saída: `Task` atualizado
- Status codes: `200 OK`, `404 Not Found`, `422 Unprocessable Entity`

### Modelo de dados

```
class Priority(str, Enum):
    alta  = "alta"
    media = "média"
    baixa = "baixa"
```

Alterações nos modelos Pydantic existentes:

| Modelo       | Campo      | Tipo               | Validação        | Default   |
|--------------|------------|--------------------|------------------|-----------|
| `TaskCreate` | `priority` | `Priority`         | valor do enum    | `"média"` |
| `TaskUpdate` | `priority` | `Optional[Priority]` | valor do enum  | `None`    |
| `Task`       | `priority` | `Priority`         | valor do enum    | `"média"` |

### Comportamento esperado

1. Ao criar uma tarefa sem informar `priority`, o sistema salva com `priority = "média"`.
2. Ao criar uma tarefa informando `priority`, o valor é persistido.
3. Ao listar tarefas sem filtro (`GET /tasks`), todas as tarefas são retornadas com o campo `priority`.
4. Ao listar tarefas com `?priority=alta`, apenas tarefas com `priority == "alta"` são retornadas.
5. Ao atualizar uma tarefa via `PATCH`, informar `priority` altera o valor; omitir mantém o valor atual.
6. Valor inválido para `priority` (criação, atualização ou filtro) resulta em `422`.
7. Tarefas criadas antes da feature (estado legado / storage resetado nos testes) assumem o default `"média"`.

## Critérios de aceite

- [ ] **CA-1** — `POST /tasks` sem `priority` retorna `201` com `priority == "média"`.
- [ ] **CA-2** — `POST /tasks` com `priority = "alta"` retorna `201` com `priority == "alta"`.
- [ ] **CA-3** — `POST /tasks` com `priority = "invalido"` retorna `422`.
- [ ] **CA-4** — `GET /tasks` retorna todas as tarefas, cada uma com o campo `priority`.
- [ ] **CA-5** — `GET /tasks?priority=baixa` retorna somente as tarefas de prioridade baixa.
- [ ] **CA-6** — `GET /tasks?priority=invalido` retorna `422`.
- [ ] **CA-7** — `PATCH /tasks/{id}` com `priority = "baixa"` atualiza e retorna o campo alterado.
- [ ] **CA-8** — `PATCH /tasks/{id}` sem `priority` não altera o valor existente.

## Riscos e perguntas em aberto

1. **Enum em português** — usar `"média"` com acento pode gerar inconsistências em URLs e JSON.
   Alternativa: aceitar `"media"` (sem acento) internamente e exibir com acento. Precisa de decisão do PM.
2. **Migração de dados persistidos** — se futuramente o storage deixar de ser in-memory (banco de dados), tarefas
   existentes precisarão de estratégia de migração. Fora do escopo agora, mas deve ser documentado.
3. **Ordenação por prioridade** — o PM explicitou que *não* precisa de ordenação automática agora. Confirmar se
   um query param `?sort=priority` deve ser previsto no modelo de dados para não exigir breaking change depois.
