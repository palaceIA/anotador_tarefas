import streamlit as st 

def run_task_app(manager):
    st.title("📝 Anotador de Tarefas")
    st.subheader("Adicionar nova tarefa")
    with st.form("add_task_form"):
        text = st.text_area("Descrição da tarefa", height=50) 
        priority = st.number_input("Prioridade (1-5)", min_value=1, max_value=5, value=1, step=1) 
        submitted = st.form_submit_button("Adicionar Tarefa")
        if submitted and text:
            manager.add_task(text=text, priority=priority)
            st.rerun() 

    st.subheader("Tarefas existentes")
    show_completed = st.checkbox("Mostrar tarefas concluídas?", value=True)
    tasks = manager.list_tasks(show_completed=None if show_completed else False)
    if not tasks:
        st.info("Nenhuma tarefa encontrada. Que tal adicionar uma?")
    
    for task in tasks:
        with st.expander(
            f"**Prioridade: {task['priority']}** | Criada em: {task['created_at']}",
            expanded=False
        ):
            new_text = st.text_area(
                "Descrição da Tarefa",
                value=task["text"],
                key=f"text_{task['_id']}"
            )

            if st.button("💾 Salvar Alterações ", key=f"save_{task['_id']}"):
                current_text = task["text"]
                if new_text != current_text:
                    manager.update_task(task["_id"], text=new_text)
                    st.success("Texto da tarefa atualizado com sucesso!")
                    st.rerun() 
                else:
                    st.warning("Nenhuma alteração de texto detectada para salvar.")
            st.markdown("---")
            col_comp, col_del, _ = st.columns([2, 1, 3])
        
            with col_comp:
                st.checkbox(
                    "Concluída",
                    value=task["completed"],
                    key=f"chk_{task['_id']}",
                    on_change=lambda tid=task["_id"], val=task["completed"]: manager.update_task(tid, completed=not val),
                    help="Marque para concluir ou desmarque para reabrir."
                )
            with col_del:
                if st.button(
                    "🗑️ Deletar",
                    key=f"del_{task['_id']}",
                    on_click=lambda tid=task["_id"]: manager.delete_task(tid)
                ):
                    st.rerun()