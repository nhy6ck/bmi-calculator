from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QDesktopWidget, QDialog, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QFont, QIcon, QColor
import sys
import os

# history button hover effect
class HistoryButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bg_color = QColor(0, 0, 0, 0)
        self.setStyleSheet("border: none;")
        self.anim = QPropertyAnimation(self, b"bg_color")
        self.anim.setDuration(180)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._bg_color)
        self.anim.setEndValue(QColor(0, 0, 0, 40))
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._bg_color)
        self.anim.setEndValue(QColor(0, 0, 0, 0))
        self.anim.start()
        super().leaveEvent(event)

    def get_bg_color(self):
        return self._bg_color

    def set_bg_color(self, color):
        self._bg_color = color
        rgba = f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()/255:.2f})"
        self.setStyleSheet(f"background-color: {rgba}; border-radius: 6px;")

    bg_color = pyqtProperty(QColor, get_bg_color, set_bg_color)

# calculate button hover effect
class CalculateButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bg_color = QColor("#007ACC")
        self.setStyleSheet(f"""
            background-color: {self._bg_color.name()};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px;
            font-size: 20px;
            font-weight: 600;
        """)
        self.anim = QPropertyAnimation(self, b"bg_color")
        self.anim.setDuration(180)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._bg_color)
        self.anim.setEndValue(QColor("#005F99"))
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._bg_color)
        self.anim.setEndValue(QColor("#007ACC"))
        self.anim.start()
        super().leaveEvent(event)

    def get_bg_color(self):
        return self._bg_color

    def set_bg_color(self, color):
        self._bg_color = color
        self.setStyleSheet(f"""
            background-color: {self._bg_color.name()};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px;
            font-size: 20px;
            font-weight: 600;
        """)

    bg_color = pyqtProperty(QColor, get_bg_color, set_bg_color)

# clear history button hover effect
class ClearHistoryButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bg_color = QColor("#d9534f")
        self.setStyleSheet(f"""
            background-color: {self._bg_color.name()};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px;
            font-size: 20px;
            font-weight: 600;
        """)
        self.anim = QPropertyAnimation(self, b"bg_color")
        self.anim.setDuration(180)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._bg_color)
        self.anim.setEndValue(QColor("#b7413e"))
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._bg_color)
        self.anim.setEndValue(QColor("#d9534f"))
        self.anim.start()
        super().leaveEvent(event)

    def get_bg_color(self):
        return self._bg_color

    def set_bg_color(self, color):
        self._bg_color = color
        self.setStyleSheet(f"""
            background-color: {self._bg_color.name()};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px;
            font-weight: 600;
            font-size: 20px;
        """)

    bg_color = pyqtProperty(QColor, get_bg_color, set_bg_color)

# history window
class HistoryDialog(QDialog):
    # basic config
    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.setWindowTitle("History")
        self.setFixedSize(400, 320)
        self.history = history
        flags = self.windowFlags()
        flags &= ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)
        self.initUI()

    def set_small_font(self, widget, size=11):
        font = widget.font()
        font.setPointSize(size)
        widget.setFont(font)

    def initUI(self):
        # history display
        layout = QVBoxLayout()
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.set_small_font(self.text_area)
        self.text_area.setStyleSheet("""
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 8px;
        """)
        self.update_history_text()
        layout.addWidget(self.text_area)

        # clear history button
        self.clear_button = ClearHistoryButton("Clear History", self)
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.clicked.connect(self.clear_history)
        layout.addWidget(self.clear_button)

        self.setLayout(layout)

    # history update
    def update_history_text(self):
        if not self.history:
            self.text_area.setText("There is no history yet.")
        else:
            text = "\n\n".join(self.history)
            self.text_area.setText(text)

    # confirm window
    def clear_history(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm")
        msg_box.setText("Are you sure you want to clear the history?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        msg_box.setIcon(QMessageBox.Question)
        
        font = msg_box.font()
        font.setPointSize(10)
        msg_box.setFont(font)
        
        yes_button = msg_box.button(QMessageBox.Yes)
        no_button = msg_box.button(QMessageBox.No)
        
        small_font = yes_button.font()
        small_font.setPointSize(10)
        yes_button.setFont(small_font)
        no_button.setFont(small_font)

        confirm = msg_box.exec_()

        if confirm == QMessageBox.Yes:
            self.history.clear()
            self.update_history_text()

# main window
class BMICalculator(QMainWindow):
    def __init__(self):
        # basic config
        super().__init__()
        self.setWindowTitle("BMI Calculator")
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "icon.png")
        self.setWindowIcon(QIcon(icon_path))
        self.setFixedSize(600, 600)
        default_font = QFont('Segoe UI', 12)
        QApplication.setFont(default_font)
        self.is_metric = True
        self.history = []
        self.initUI()
        self.center()

    def initUI(self):
        # layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(50, 30, 50, 30)
        self.setStyleSheet("background-color: #fafafa;")

        top_layout = QHBoxLayout()
        top_layout.addStretch()

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "history.png")
        history_icon = QIcon(icon_path)

        self.history_button = HistoryButton(self)
        self.history_button.setIcon(history_icon)
        self.history_button.setIconSize(QtCore.QSize(28, 28))
        self.history_button.setFixedSize(40, 40)
        self.history_button.setFlat(True)
        self.history_button.clicked.connect(self.show_history)

        top_layout.addWidget(self.history_button)
        main_layout.addLayout(top_layout)

        # title
        title_label = QLabel("BMI Calculator")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 48px;
            font-weight: 600;
            color: #333;
            letter-spacing: 2px;
        """)
        main_layout.addWidget(title_label)
        main_layout.addSpacing(40)

        # weight
        self.weight_label = QLabel("Enter your weight (kg):")
        self.weight_label.setStyleSheet("color: #555; font-weight: 600; font-size: 20px;")
        self.weight_input = QLineEdit(self)
        self.weight_input.setPlaceholderText("e.g., 70")
        self.weight_input.setStyleSheet("""
            font-size: 20px;
            padding: 5px;
            border: 1.5px solid #ccc;
            border-radius: 6px;
            background-color: white;
        """)
        main_layout.addWidget(self.weight_label)
        main_layout.addWidget(self.weight_input)

        # height
        self.height_label = QLabel("Enter your height (cm):")
        self.height_label.setStyleSheet("color: #555; font-weight: 600; font-size: 20px;")
        self.height_label.setMinimumHeight(50)
        self.height_input = QLineEdit(self)
        self.height_input.setPlaceholderText("e.g., 175")
        self.height_input.setStyleSheet("""
            font-size: 20px;
            padding: 5px;
            border: 1.5px solid #ccc;
            border-radius: 6px;
            background-color: white;
        """)
        main_layout.addWidget(self.height_label)
        main_layout.addWidget(self.height_input)

        # calculate button
        self.weight_input.returnPressed.connect(self.bmi_calculation)
        self.height_input.returnPressed.connect(self.bmi_calculation)
        main_layout.addSpacing(30)
        self.calculate_button = CalculateButton("Calculate", self)
        self.calculate_button.setCursor(Qt.PointingHandCursor)
        self.calculate_button.clicked.connect(self.bmi_calculation)
        main_layout.addWidget(self.calculate_button)

        # result label
        main_layout.addSpacing(30)
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.result_label.setMinimumHeight(60)
        self.result_label.setStyleSheet("font-size: 20px; font-weight: 600; color: #222;")
        main_layout.addWidget(self.result_label)

        # footer
        links_layout = QHBoxLayout()
        links_layout.setAlignment(Qt.AlignCenter)

        # change conversion button
        change_conversion_button = QLabel(
            '<a href="#" style="color: #007ACC; text-decoration: none; font-weight: 600;">change conversion</a>')
        change_conversion_button.setStyleSheet("margin: 0 8px; font-size: 18px;")
        change_conversion_button.setCursor(Qt.PointingHandCursor)
        change_conversion_button.mousePressEvent = lambda event: self.change_conversion()

        # separator
        self.separator_label = QLabel("|")
        self.separator_label.setStyleSheet("color: #999; font-size: 16px;")

        # author link button
        author_link = QLabel(
            '<a href="https://linktr.ee/nhy6ck" style="color: #007ACC; text-decoration: none; font-weight: 600;">author</a>')
        author_link.setStyleSheet("margin: 0 8px; font-size: 18px;")
        author_link.setOpenExternalLinks(True)

        links_layout.addWidget(change_conversion_button)
        links_layout.addWidget(self.separator_label)
        links_layout.addWidget(author_link)
        main_layout.addLayout(links_layout)

        # widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    # bmi calculation
    def bmi_calculation(self):
        try:
            if self.is_metric:
                # metric units
                weight = float(self.weight_input.text())
                height_cm = float(self.height_input.text())
                if weight <= 0 or height_cm <= 0:
                    self.result_label.setText("Please enter positive numbers.")
                    self.result_label.setStyleSheet("color: red; font-weight: 600; font-size: 20px;")
                    return
                height_m = height_cm / 100.0
                weight_str = f"{weight} kg"
                height_str = f"{height_cm} cm"
            else:
                # imperial units
                weight_lb = float(self.weight_input.text())
                height_ft = float(self.height_input.text())
                if weight_lb <= 0 or height_ft <= 0:
                    self.result_label.setText("Please enter positive numbers.")
                    self.result_label.setStyleSheet("color: red; font-weight: 600; font-size: 20px;")
                    return
                height_m = height_ft * 0.3048
                weight = weight_lb * 0.453592
                weight_str = f"{weight_lb} pounds"
                height_str = f"{height_ft} feet"

            # bmi formula
            bmi = weight / (height_m ** 2)
            classification = self.bmi_classification(bmi)
            result_text = f"BMI: {bmi:.2f} - {classification}"
            self.result_label.setText(result_text)
            self.result_label.setStyleSheet("color: #333; font-weight: 600; font-size: 20px;")

            # saving the calculations
            entry = (f"Weight: {weight_str}\n"
                     f"Height: {height_str}\n"
                     f"{result_text}")
            self.history.append(entry)

            # inputs clearing
            self.weight_input.clear()
            self.height_input.clear()

        except ValueError:
            # error message
            self.result_label.setText("Please enter valid numbers.")
            self.result_label.setStyleSheet("color: red; font-weight: 600; font-size: 20px;")

    # bmi classification
    def bmi_classification(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    # conversion unit change
    def change_conversion(self):
        if self.is_metric:
            # imperial
            self.is_metric = False
            self.weight_label.setText("Enter your weight (pounds):")
            self.height_label.setText("Enter your height (feet):")
            self.weight_input.setPlaceholderText("e.g., 154")
            self.height_input.setPlaceholderText("e.g., 5.8")
        else:
            # metric
            self.is_metric = True
            self.weight_label.setText("Enter your weight (kg):")
            self.height_label.setText("Enter your height (cm):")
            self.weight_input.setPlaceholderText("e.g., 70")
            self.height_input.setPlaceholderText("e.g., 175")

        self.weight_input.clear()
        self.height_input.clear()

    # history display
    def show_history(self):
        dialog = HistoryDialog(self.history, self)
        dialog.exec_()

    # to center the window
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BMICalculator()
    window.show()
    sys.exit(app.exec_())