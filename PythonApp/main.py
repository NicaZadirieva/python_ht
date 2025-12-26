from dataclasses import dataclass, field
from datetime import datetime

@dataclass()
class Task:
    title: str
    priority: int = 3
    done: bool = False
    created_at: datetime = field(default_factory=datetime.now, repr=True, compare=False)  

task = Task("Сделать лекцию")
print(task)

task2 = Task("Сделать лекцию")
print(task == task2)  # Теперь будет True!