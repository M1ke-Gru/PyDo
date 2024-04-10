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
            self.clearLayout()
        self.justLaunched = False
        self.displaytodoordone = 0
        self.windowlayout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(self.windowlayout)
        self.setCentralWidget(central_widget)
        self.plusButton = QPushButton("+")
        self.plusButton.clicked.connect(self.addTask)

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
            self.showTasksOnLists(todo)
        if self.displaytodoordone % 2 == 0:
            self.showTasksOnLists(done)

    def clearLayout(self):
        while self.windowlayout.count() > 0:
            item = self.windowlayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def addTask(self):
        task = Task()
        todo.append(task)
        print(todo)
        self.change_todo_done_visibility()

    def showTasksOnLists(self, tasklist):
        for task in tasklist:
            item = TaskWidget(task, self.tasklistwidget, self)
            self.tasklistwidget.addItem(item)


class Task:
    def __init__(self):
        self.text = ""
        self.isDone = False


class TaskWidget(QListWidgetItem):
    def __init__(self, task, listwidget, window):
        super().__init__()
        self.task = task
        self.listwidget = listwidget
        self.window = window

        self.check = QCheckBox()
        self.check.stateChanged.connect(self.taskDoneStateChange)
        if (self.task.isDone == False):
            self.name = QLineEdit(self.task.text)
            self.name.textChanged.connect(self.text_changed)
        else:
            self.name = QLabel()
            self.name.setText(self.task.text)
            self.name.setStyleSheet("text-decoration: line-through; color: #999999; margin-right: 200px; padding-top: 2px;")

        widget = QWidget()

        self.tasklayout = QHBoxLayout(widget)
        self.tasklayout.setAlignment(Qt.AlignLeft)
        self.tasklayout.addWidget(self.check)
        self.tasklayout.addWidget(self.name)
        self.name.setAlignment(Qt.AlignLeft)
        self.setSizeHint(widget.sizeHint())
        self.listwidget.addItem(self)
        self.listwidget.setItemWidget(self, widget)

    def text_changed(self, text):
        self.task.text = text

    def taskDoneStateChange(self, state):
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
