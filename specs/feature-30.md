# Spec: Prioridade nas Tarefas

Issue de origem: #30

## Necessidade de negócio

Gerentes de operações precisam classificar tarefas por prioridade (alta, média ou baixa) para identificar rapidamente quais itens são urgentes. Hoje todas as tarefas aparecem sem distinção, dificultando a organização da equipe. A feature permite definir, visualizar, filtrar e alterar a prioridade de qualquer tarefa.

## Contrato técnico

### Endpoints

**POST /tasks**
- Descrição: Criar tarefa com prioridade opcional
- Payload entrada: `{"title": "string", "description": "string|null", "priority": "alta|media|baixa"}` — `priority` é opcional
- Payload saída: objeto `Task` completo (com campo `priority`)
- Status codes: `201 Created`, `422 Unprocessable Entity`

**GET /tasks**
- Descrição: Listar tarefas, com filtro opcional por prioridade
- Query param: `priority` (opcional) — valores aceitos: `alta`, `media`, `baixa`
- Payload saída: lista de objetos `Task`
- Status codes: `200 OK`, `422 Unprocessable Entity` (valor inválido de priority)

**GET /tasks/{task_id}**
- Sem alterações além de incluir `priority` na resposta

**PATCH /tasks/{task_id}**
- Descrição: Permite alterar `priority` além dos campos já existentes
- Payload entrada: `{"title": "string|null", "description": "string|null", "completed": "bool|null", "priority": "alta|media|baixa|null"}`
- Payload saída: objeto `Task` atualizado
- Status codes: `200 OK`, `404 Not Found`, `422 Unprocessable Entity`

### Modelo de dados

```python
class Priority(str, Enum):
    alta = "alta"
    media = "media"
    baixa = "baixa"

# TaskCreate — campo novo:
priority: Priority = Field(default=Priority.media)

# TaskUpdate — campo novo:
priority: Optional[Priority] = None

# Task — campo novo:
priority: Priority = Priority.media
```

### Comportamento esperado

1. Ao criar uma tarefa sem informar `priority`, o sistema atribui `media` automaticamente.
2. Ao criar uma tarefa com `priority` inválida, o sistema retorna `422`.
3. Ao listar tarefas sem filtro, todas são retornadas com o campo `priority` visível.
4. Ao listar tarefas com `?priority=alta`, somente tarefas com `priority == "alta"` são retornadas.
5. Ao fazer PATCH informando `priority`, o campo é atualizado; os demais campos não informados permanecem inalterados.
6. A ordem de listagem continua sendo a de criação (sem ordenação por prioridade).

## Critérios de aceite

- [ ] `POST /tasks` sem `priority` → resposta inclui `"priority": "media"`
- [ ] `POST /tasks` com `priority: "alta"` → resposta inclui `"priority": "alta"`
- [ ] `POST /tasks` com `priority: "urgente"` → `422`
- [ ] `GET /tasks` sem filtro → todas as tarefas retornam com campo `priority`
- [ ] `GET /tasks?priority=baixa` → retorna somente tarefas com `priority == "baixa"`
- [ ] `GET /tasks?priority=invalido` → `422`
- [ ] `PATCH /tasks/{id}` com `priority: "alta"` → `priority` atualizada, demais campos inalterados
- [ ] `GET /tasks/{id}` → resposta inclui campo `priority`

## Riscos e perguntas em aberto

1. **Valor do enum `media` vs `média`**: usar `media` (sem acento) evita problemas de encoding em query strings — confirmar se o PM aceita esse nome.
2. **Persistência**: o storage atual é em memória (`storage.py`). A prioridade será perdida ao reiniciar — isso é aceitável para o MVP?
3. **Filtro por múltiplas prioridades**: a issue não pede, mas vale confirmar se `?priority=alta&priority=media` será necessário futuramente para não criar um contrato incompatível.
