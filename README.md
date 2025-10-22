# 📝 Anotador de Tarefas Moderno (To-Do App)

Um app moderno de **gestão de tarefas** (To-Do App) desenvolvido em **Python**, com backend em **MongoDB**, **cache inteligente Redis** e uma **interface interativa Streamlit**.

Projetado para ser **rápido, escalável e intuitivo** 🔥

---

## 🚀 Tecnologias Utilizadas

Este projeto integra as seguintes tecnologias para garantir alto desempenho e uma experiência de usuário fluida:

| Camada | Tecnologia | Descrição |
|:-------|:------------|:-----------|
| 💻 **Frontend** | [Streamlit](https://streamlit.io) | Interface reativa e simples de usar |
| 🧠 **Lógica de Negócio** | Python + Classes customizadas | Gestão de tarefas, cache e atualização |
| 🗄️ **Banco de Dados** | [MongoDB](https://www.mongodb.com) | Armazena as tarefas de forma persistente |
| ⚡ **Cache** | [Redis](https://redis.io) | Acelera a listagem e melhora o desempenho |

---

## 🧠 Principais Funcionalidades

| Função | Descrição |
|:-------|:-----------|
| ➕ **Adicionar Tarefa** | Crie novas tarefas com prioridade de 1 a 5 |
| 🧾 **Listar Tarefas** | Visualize todas as tarefas — cacheadas para velocidade máxima |
| ✏️ **Editar Descrição** | Atualize o texto de uma tarefa existente |
| ✅ **Concluir/Reabrir** | Marque tarefas como concluídas ou reabra facilmente |
| 🗑️ **Excluir Tarefa** | Remova uma tarefa definitivamente do banco |

---

## ⚡ Estratégia de Cache com Redis

O desempenho é otimizado utilizando o Redis para armazenar a lista de tarefas em memória.

A chave utilizada é: `TASK_LIST_CACHE_KEY = "task_list"`

**Invalidando o Cache:** Toda vez que uma tarefa é **adicionada, atualizada ou excluída**, o cache é **invalidado automaticamente**. Isso garante que os dados listados sejam sempre os mais atualizados, mantendo as consultas ultrarrápidas ⚙️.

#### Lógica Interna Simplificada (Exemplo):

```python
# Exemplo de fluxo dentro do TaskManager

def list_tasks(self, show_completed=None):
    # 1️⃣ Tenta buscar no cache Redis
    tasks = cache_manager.get_cache(TASK_LIST_CACHE_KEY)
    if tasks:
        return tasks

    # 2️⃣ Busca no MongoDB se não houver cache
    tasks = list(self.collection.find())
    cache_manager.set_cache(TASK_LIST_CACHE_KEY, tasks)
    return tasks
```
