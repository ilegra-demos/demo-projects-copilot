# Spec: Prioridade nas Tarefas

Issue de origem: #22

## Necessidade de negócio

Gerentes de operações precisam classificar tarefas por prioridade (alta, média ou baixa) para identificar rapidamente o que é urgente na listagem da equipe. Hoje, todas as tarefas aparecem sem distinção de urgência, dificultando a gestão. A solução deve permitir definir, visualizar, filtrar e alterar a prioridade de uma tarefa, sem ordenação automática.

## Contrato técnico

### Endpoints

**POST `/tasks`** — Criar tarefa  
- Entrada: `TaskCreate` (campo `priority` opcional)  
- Saída: `Task` com `priority` preenchida  
- Status: `201 Created`, `422 Unprocessable Entity`

**GET `/tasks`** — Listar tarefas  
- Query param: `priority` (opcional) — filtra por valor exato (`alta`, `media`, `baixa`)  
- Saída: `List[Task]` — cada item inclui `priority`  
- Status: `200 OK`, `422 Unprocessable Entity` (valor inválido)

**GET `/tasks/{task_id}`** — Obter tarefa  
- Saída: `Task` com `priority`  
- Status: `200 OK`, `404 Not Found`

**PATCH `/tasks/{task_id}`** — Atualizar tarefa  
- Entrada: `TaskUpdate` (campo `priority` opcional)  
- Saída: `Task` atualizada com `priority`  
- Status: `200 OK`, `404 Not Found`, `422 Unprocessable Entity`

### Modelo de dados

**Novo `Enum` — `Priority`** (em `app/models.py`):
```
class Priority(str, Enum):
    alta  = "alta"
    media = "media"
    baixa = "baixa"
```

**`TaskCreate`** — campo adicionado:
| Campo | Tipo | Validação | Default |
|-------|------|-----------|---------|
| `priority` | `Priority` | valor do enum | `Priority.media` |

**`TaskUpdate`** — campo adicionado:
| Campo | Tipo | Validação | Default |
|-------|------|-----------|---------|
| `priority` | `Optional[Priority]` | valor do enum ou `None` | `None` |

**`Task`** — campo adicionado:
| Campo | Tipo | Validação | Default |
|-------|------|-----------|---------|
| `priority` | `Priority` | valor do enum | `Priority.media` |

### Comportamento esperado

1. Ao criar uma tarefa sem informar `priority`, o valor salvo é `"media"`.
2. Ao criar uma tarefa com `priority` inválida (ex.: `"urgente"`), a API retorna `422`.
3. Ao listar tarefas sem filtro, todas são retornadas com o campo `priority` visível.
4. Ao listar com `?priority=alta`, apenas tarefas com `priority == "alta"` são retornadas.
5. Ao chamar `PATCH` com `priority` informada, o campo é atualizado; demais campos não informados permanecem inalterados.
6. Ao chamar `PATCH` sem `priority`, a prioridade existente não é alterada.
7. Tarefas existentes (criadas antes da feature) devem assumir `priority = "media"` como valor padrão — sem quebra de compatibilidade no storage.

## Critérios de aceite

- [ ] `POST /tasks` sem `priority` → resposta contém `"priority": "media"`
- [ ] `POST /tasks` com `priority: "alta"` → resposta contém `"priority": "alta"`
- [ ] `POST /tasks` com `priority: "urgente"` → status `422`
- [ ] `GET /tasks` → todos os itens contêm o campo `priority`
- [ ] `GET /tasks?priority=alta` → retorna apenas tarefas com `priority == "alta"`
- [ ] `GET /tasks?priority=invalido` → status `422`
- [ ] `GET /tasks?priority=baixa` com storage vazio → retorna `[]`
- [ ] `PATCH /tasks/{id}` com `priority: "baixa"` → campo atualizado, outros inalterados
- [ ] `PATCH /tasks/{id}` sem `priority` → prioridade existente inalterada
- [ ] `GET /tasks/{id}` → resposta inclui `priority`

## Riscos e perguntas em aberto

1. **Migração de dados existentes**: o storage em memória não persiste, então não há impacto imediato; mas se o storage evoluir para persistência (banco/arquivo), será necessário definir estratégia de migração para registros sem `priority`.
2. **Ordenação futura**: a issue explicitamente dispensa ordenação automática por prioridade, mas é provável que seja pedida em seguida — vale considerar se a query param de filtro deve já suportar `sort_by=priority` ou se isso será um endpoint separado.
3. **Grafia de `media` vs `média`**: o enum usa `media` (sem acento) para compatibilidade com query params e JSON sem encoding; confirmar se o PM aceita esse formato na UI.
