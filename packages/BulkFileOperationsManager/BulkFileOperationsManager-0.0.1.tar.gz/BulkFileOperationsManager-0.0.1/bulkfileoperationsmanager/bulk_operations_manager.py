# bulk_operations_manager.py
from filechunkcrud import FileHandler
from queue import Queue
import threading

class BulkOperationsManager:
    def __init__(self):
        self.tasks_queue = Queue()

    def add_task(self, task):
        """Добавление задания в очередь."""
        self.tasks_queue.put(task)

    def run(self):
        """Запуск обработки заданий."""
        while not self.tasks_queue.empty():
            task = self.tasks_queue.get()
            self._execute_task(task)

    def _execute_task(self, task):
        """Выполнение одного задания."""
        operation, file_path, *args = task
        file_handler = FileHandler(file_path)

        if operation == "create":
            file_handler.create_file(*args)
        elif operation == "read":
            for chunk in file_handler.read_chunks(*args):
                print(chunk)  # или другой способ обработки данных
        elif operation == "update":
            file_handler.update_file(*args)
        elif operation == "delete":
            file_handler.delete_file()
        else:
            raise ValueError("Неизвестная операция")

        self.tasks_queue.task_done()
