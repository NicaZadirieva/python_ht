from dataclasses import dataclass
from datetime import datetime

@dataclass()
class Task:
    title: str
    priority: int = 3
    done: bool = False
    created_at: datetime | None = None  # Python 3.10+ (иначе: Optional[datetime])

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

task = Task("Сделать лекцию")
print(task)

task2 = Task("Сделать лекцию")
print(task == task2)