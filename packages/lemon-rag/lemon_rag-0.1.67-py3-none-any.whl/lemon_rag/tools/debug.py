import lemon_rag
print(dir(lemon_rag))
file = lemon_rag.lemon_runtime.wrappers.file_system.create_file(b"abc", "abc.txt")
print(file)
print(dir(file))