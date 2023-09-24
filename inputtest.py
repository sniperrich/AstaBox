from PyQt5.Qt import *
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QLineEdit-使用')
        self.resize(500, 400)
        self.setup_ui()

    def setup_ui(self):
        ql_a = QLineEdit(self)
        ql_a.setPlaceholderText('测试。。。')
        action = QAction(self)
        action.setIcon(QIcon('xxx.png'))
        ql_a.addAction(action, QLineEdit.TrailingPosition)
        ql_a.setEchoMode(QLineEdit.Password)
        ql_a.move(100, 100)

        ql_b = QLineEdit(self)
        ql_b.move(100, 150)

        btn = QPushButton(self)
        btn.setText('复制')
        btn.move(100, 200)

        btn1 = QPushButton(self)
        btn1.setText('取消')
        btn1.move(200, 200)

        def cancel():
            # 取消选中
            ql_a.deselect()

        btn1.clicked.connect(cancel)

        def copy():
            text = ql_a.text()
            ql_a.setSelection(0, len(text))
            ql_b.setText(text)

        btn.clicked.connect(copy)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())