class Note:
    title: str
    description: str

    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description
        print("Создана заметка")

note = Note("Это title", "Это description")
print(note.title)
print(note.description)