from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QListWidgetItem
import threading
from core import get_objs, db, table, columns
from model import Database


class Ui(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("src/main.ui", self)
        self.show()
        self.setup()
        self.thread(self.view)

    def setup(self):
        self.add_btn.clicked.connect(lambda: self.thread(self.add))
        self.update_btn.clicked.connect(lambda: self.thread(self.update))
        self.delete_btn.clicked.connect(lambda: self.thread(self.delete))
        self.view_btn.clicked.connect(lambda: self.thread(self.view))

    def get(self, val: str):
        if val == "name":
            return self.name_input.text()
        elif val == "desc":
            return self.desc_input.text()
        elif val == "status":
            return self.status_input.text()
        elif val == "id":
            return int(self.id_input.text())
        else:
            return None

    def thread(self, func):
        thread = threading.Thread(target=lambda: self.exception(func))
        thread.start()

    def exception(self, func):
        try:
            func()
        except Exception as error:
            self.system_view.clear()
            self.system_view.addItem(QListWidgetItem(str(error)))

    def view(self):
        self.system_view.clear()
        for i in sorted(
            get_objs(Database.select(db=db, table=table, columns=columns)),
            key=lambda obj: obj.id,
        ):
            self.system_view.addItem(QListWidgetItem(str(i)))

    def add(self):
        Database.insert(
            db=db,
            table=table,
            columns=columns,
            values=[self.get("name"), self.get("desc"), self.get("status")],
        )
        self.thread(self.view)

    def update(self):
        Database.update(
            db=db,
            table=table,
            columns=columns,
            values=[self.get("name"), self.get("desc"), self.get("status")],
            id=self.get("id"),
        )
        self.thread(self.view)

    def delete(self):
        Database.delete(
            db=db,
            table=table,
            id=self.get("id"),
        )
        self.thread(self.view)
