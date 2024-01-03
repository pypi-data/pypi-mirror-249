import peewee

print(lemon.lemon_rag.KnowledgeSentence.select(peewee.fn.Count(peewee.SQL('1'))).scalar())