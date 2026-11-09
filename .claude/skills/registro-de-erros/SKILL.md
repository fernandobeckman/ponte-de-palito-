---
name: registro-de-erros
description: Como ler e atualizar o arquivo ERROS.md do repositório, que guarda erros já cometidos por Claude e pela equipe para não repeti-los. Use no início de cada tarefa e sempre que um erro, falha ou retrabalho acontecer.
---

# Registro de erros

## No início de cada tarefa
Leia `ERROS.md` na raiz e siga as regras de prevenção de cada entrada relevante.

## Quando algo der errado
Adicione uma entrada **no topo da tabela** em `ERROS.md`:

| data | contexto | erro | causa | como evitar |
|---|---|---|---|---|

- Seja específico (comando, arquivo, número errado).
- "Como evitar" deve ser uma regra verificável, não um desejo ("conferir equilíbrio = 0 antes de reportar", e não "ter mais atenção").
- Erros de cálculo estrutural: inclua o valor errado e o correto.
- Não apague entradas antigas; marque como resolvidas se a regra virou automatizada.
