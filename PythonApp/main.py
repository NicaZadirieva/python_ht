class Task:
    """Задача"""
    done: bool = False
    title: str

    def get_info(self):
        """Получение данных задачи"""
        print("Задача")
    
    def set_info(self, text: str):
        """Установка title"""
        self.title = text

task = Task()

task.set_info("Сделать лекцию")

print(task.title)

task.get_info()
Task.get_info(task) # то как будет обработан вызов выше интерпретатором