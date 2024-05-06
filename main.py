import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QCheckBox,
    QComboBox,
)

todo = []
done = []


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyDo")
        self.justLaunched = True
        self.show_UI()

    def show_UI(self):
        if not self.justLaunched:
            self.clear_layout()
        self.justLaunched = False
        self.displaytodoordone = 0
        self.windowlayout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(self.windowlayout)
        self.setCentralWidget(central_widget)
        self.plusButton = QPushButton("+")
        self.plusButton.clicked.connect(self.add_task)

        top_bar = QHBoxLayout()
        self.choicetodoordoneshown = QComboBox()
        self.choicetodoordoneshown.addItems(["Todo & done", "Todo", "Done"])
        self.choicetodoordoneshown.currentIndexChanged.connect(
            self.change_todo_done_visibility
        )
        top_bar.addWidget(self.choicetodoordoneshown)
        top_bar.addWidget(self.plusButton)
        self.windowlayout.addLayout(top_bar)
        self.tododonelayout = QHBoxLayout()
        self.change_todo_done_visibility()
        self.windowlayout.addLayout(self.tododonelayout)

    def change_todo_done_visibility(self, index=0):
        self.displaytodoordone = index
        while self.tododonelayout.count() > 0:
            item = self.tododonelayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.tasklistwidget = QListWidget()
        self.tododonelayout.addWidget(self.tasklistwidget)
        if self.displaytodoordone < 2:
            self.show_tasks_on_lists(todo)
        if self.displaytodoordone % 2 == 0:
            self.show_tasks_on_lists(done)

    def clear_layout(self):
        while self.windowlayout.count() > 0:
            item = self.windowlayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def add_task(self):
        task = Task()
        todo.append(task)
        print(todo)
        self.change_todo_done_visibility()

    def show_tasks_on_lists(self, tasklist):
        for task in tasklist:
            item = TaskWidget(task, self.tasklistwidget, self)
            self.tasklistwidget.addItem(item)

    def show_task_settings(self, task):
        self.taskSettingsWindow = TaskSettingsWindow(task, self)
        self.taskSettingsWindow.show()


class TaskSettingsWindow(QWidget):
    def __init__(self, task, parentWindow):
        super().__init__()
        self.task = Task()
        self.task = task
        self.parentWindow = MainWindow()
        self.parentWindow = parentWindow
        self.tasksettingslayout = QVBoxLayout()
        self.show_name_editor()
        self.show_date_editor()
        self.show_importance_and_urgency_toggles()
        self.show_ok_button()
        self.setLayout(self.tasksettingslayout)

    def show_name_editor(self):
        self.nameeditorlabel = QLabel("Name")
        self.nameeditorfield = QLineEdit(self.task.text)
        self.nameeditorlayout = QHBoxLayout()
        self.nameeditorlayout.addWidget(self.nameeditorlabel)
        self.nameeditorlayout.addWidget(self.nameeditorfield)
        self.tasksettingslayout.addLayout(self.nameeditorlayout)

    def show_date_editor(self):
        self.dateeditorlabel = QLabel("Time")
        self.dateeditorfield = QLineEdit("dd/mm/yy")
        self.dateeditorlayout = QHBoxLayout()
        self.dateeditorlayout.addWidget(self.dateeditorlabel)
        self.dateeditorlayout.addWidget(self.dateeditorfield)
        self.tasksettingslayout.addLayout(self.dateeditorlayout)

    def show_importance_and_urgency_toggles(self):
        self.importanceeditorlabel = QLabel("Importance")
        self.importanceeditorfield = QComboBox()
        self.importanceeditorfield.addItems(self.task.importanceList)
        self.urgencyeditorlabel = QLabel("Urgency")
        self.urgencyeditorfield = QComboBox()
        self.urgencyeditorfield.addItems(self.task.urgencyList)
        self.importanceandurgencylayout = QHBoxLayout()
        self.importanceandurgencylayout.addWidget(self.importanceeditorlabel)
        self.importanceandurgencylayout.addWidget(self.importanceeditorfield)
        self.importanceandurgencylayout.addWidget(self.urgencyeditorlabel)
        self.importanceandurgencylayout.addWidget(self.urgencyeditorfield)
        self.tasksettingslayout.addLayout(self.importanceandurgencylayout)

    def show_ok_button(self):
        self.ok_button = QPushButton("OK")
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.ok_button)
        self.tasksettingslayout.addLayout(self.buttonLayout)
        self.ok_button.clicked.connect(self.save_changes)

    def save_changes(self):
        self.task.text = self.nameeditorfield.text()
        self.task.taskDate = self.dateeditorfield.text()
        self.task.importance = self.task.importanceList[
            self.importanceeditorfield.currentIndex()
        ]
        self.task.urgency = self.task.urgencyList[
            self.urgencyeditorfield.currentIndex()
        ]
        self.parentWindow.change_todo_done_visibility()


class Task:
    def __init__(self):
        self.text = ""
        self.isDone = False
        self.taskDate = ""
        self.taskPlace = ""
        self.importanceList = ["High", "Medium", "Low"]
        self.importance = self.importanceList[2]
        self.urgencyList = ["High", "Medium", "Low"]
        self.urgency = self.urgencyList[2]


class TaskWidget(QListWidgetItem):
    def __init__(self, task, listwidget, window):
        super().__init__()
        self.task = task
        self.listwidget = listwidget
        self.window = window

        self.check = QCheckBox()
        self.check.stateChanged.connect(self.task_done_state_change)
        if self.task.isDone == False:
            self.name = QLineEdit(self.task.text)
            self.name.textChanged.connect(self.text_changed)
            self.burgermenubutton = QPushButton("☰")
            self.burgermenubutton.clicked.connect(
                lambda: self.window.show_task_settings(self.task)
            )
        else:
            self.name = QLabel()
            self.name.setText(self.task.text)
            self.name.setStyleSheet(
                "text-decoration: line-through; color: #999999; margin-right: 200px; padding-top: 2px;"
            )

        widget = QWidget()

        self.tasklayout = QHBoxLayout(widget)
        self.tasklayout.setAlignment(Qt.AlignLeft)
        self.tasklayout.addWidget(self.check)
        self.tasklayout.addWidget(self.name)
        if isinstance(self.name, QLineEdit):
            self.tasklayout.addWidget(self.burgermenubutton)
        self.name.setAlignment(Qt.AlignLeft)
        self.setSizeHint(widget.sizeHint())
        self.listwidget.addItem(self)
        self.listwidget.setItemWidget(self, widget)

    def text_changed(self, text):
        self.task.text = text

    def task_done_state_change(self, state):
        if not self.task.isDone:
            todo.remove(self.task)
            done.append(self.task)
            self.task.isDone = True
        else:
            done.remove(self.task)
            todo.append(self.task)
            self.task.isDone = False
        self.window.change_todo_done_visibility()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
