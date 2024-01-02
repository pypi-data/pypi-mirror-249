q = (
    lemon.lemon_rag.KnowledgeBaseAccessTab
    .select(

    )
    .where(
        lemon.lemon_rag.KnowledgeBaseAccessTab.id < 0
    )
    .get()

)

