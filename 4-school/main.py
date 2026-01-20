from repositories.journal_repo import InMemoryJournalRepo
from services.journal_service import JournalService
from services.notification_service import ConsoleNotificationService
from services.stat_service import ScoreStatistics

def run():
    journalRepo = InMemoryJournalRepo()
    notificationService = ConsoleNotificationService()
    journalService = JournalService(journalRepo, notificationService)
    scoreStatistics = ScoreStatistics(journalRepo)

    # заполнение данными
    journalService.add_lesson("Физика")
    journalService.add_lesson("Математика")
    journalService.add_lesson("Русский язык")

    journalService.add_student("Вероника Иванова")
    journalService.add_student("Павел Иванов")

    journalService.add_student_score("Вероника Иванова", "Физика", 3)
    journalService.add_student_score("Вероника Иванова", "Математика", 3)
    journalService.add_student_score("Вероника Иванова", "Русский язык", 3)

    journalService.add_student_score("Павел Иванов", "Физика", 3)
    journalService.add_student_score("Павел Иванов", "Математика", 3)
    journalService.add_student_score("Павел Иванов", "Русский язык", 3)

    scoreStatistics.print_stat()

run()