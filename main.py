import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QLineEdit, QCheckBox, QComboBox

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
        self.choicetodoordoneshown.currentIndexChanged.connect(self.change_todo_done_visibility)
        top_bar.addWidget(self.choicetodoordoneshown)
        top_bar.addWidget(self.plusButton)
        self.windowlayout.addLayout(top_bar)
        self.tododonelayout = QHBoxLayout()
        self.show_todo()
        self.show_done()
        self.change_todo_done_visibility()
        self.windowlayout.addLayout(self.tododonelayout)

    def change_todo_done_visibility(self, index=0):
        self.displaytodoordone = index
        while self.tododonelayout.count() > 0:
            item = self.tododonelayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        if self.displaytodoordone == 0:
            self.show_todo()
            self.show_done()
        elif self.displaytodoordone == 1:
            self.show_todo()
        elif self.displaytodoordone == 2:
            self.show_done()

    def show_todo(self):
        if not hasattr(self, 'labeltodo'):
            self.labeltodo = QLabel("To do")
        self.todoListWidget = QListWidget()

        self.showtodobox = QCheckBox("Show pending")
        self.showtodobox.setCheckState(Qt.CheckState.Checked)
        self.showtodobox.stateChanged.connect(lambda state: self.show_list(self.showtodo))
        self.showtodo = True

        todolayout = QVBoxLayout()
        todolayout.addWidget(self.labeltodo)
        todolayout.addWidget(self.todoListWidget)
        self.tododonelayout.addLayout(todolayout)

    def show_done(self):
        if not hasattr(self, 'labeldone'):
            self.labeldone = QLabel("Done")
        self.doneListWidget = QListWidget()
        self.showdonebox = QCheckBox("Show completed")        
        self.showdonebox.stateChanged.connect(lambda state: self.show_list(self.showdone))
        self.showdone = False
        donelayout = QVBoxLayout()
        donelayout.addWidget(self.labeldone)
        donelayout.addWidget(self.doneListWidget)
        self.tododonelayout.addLayout(donelayout)

    def clearLayout(self):
        while self.windowlayout.count() > 0:
            item = self.windowlayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
    def show_list(self, todoordone):
        todoordone = not todoordone

    def addTask(self):
        task = Task()
        todo.append(task)
        print(todo)
        self.updateLists()

    def updateLists(self):
        self.todoListWidget.clear()
        self.doneListWidget.clear()
        for task in todo:
            item = TaskWidget(task, self.todoListWidget, self)
            self.todoListWidget.addItem(item)
        for task in done:
            item = TaskWidget(task, self.doneListWidget, self)
            self.doneListWidget.addItem(item)            

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
        self.name = QLineEdit(self.task.text)
        self.name.textChanged.connect(self.text_changed)

        widget = QWidget()

        self.tasklayout = QHBoxLayout(widget)
        self.tasklayout.addWidget(self.check)
        self.tasklayout.addWidget(self.name)

        self.setSizeHint(widget.sizeHint())
        self.listwidget.addItem(self)
        self.listwidget.setItemWidget(self, widget)  

    def text_changed(self, text):
        self.task.text = text

    def taskDoneStateChange(self, state):
        if self.task.isDone == False:
            todo.remove(self.task)
            done.append(self.task)
            self.task.isDone = True
        else:
            done.remove(self.task)
            todo.append(self.task)
            self.task.isDone = False
        self.window.updateLists()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
