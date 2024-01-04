from typing import Optional


class RuntimeFile:
    name: str
    status: bool
    body: bytes
    file_path: str
    url: str

    def save(self):
        pass

    def load(self):
        pass


class FileSystem:
    def create_file(
            self,
            body: bytes,
            name: str,
            file_path: Optional[str] = None,
            url: Optional[str] = None
    ) -> RuntimeFile:
        pass


file_system: FileSystem
