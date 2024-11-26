import sys
import json
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QSlider, QPushButton, QFileDialog, QWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QDesktopServices
import subprocess

CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"crosshair": "crosshair.png", "scale": 50}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

class SettingsMenu(QMainWindow):
    def __init__(self):
        super().__init__(None, Qt.FramelessWindowHint)
        self.setWindowTitle("Soul Crosshair")
        self.setFixedSize(400, 480)
        self.config = load_config()
        self.drag_pos = None

        self.setStyleSheet("""
            QMainWindow { background-color: #101010; }
            QLabel { color: #ffffff; font-family: 'Consolas'; font-size: 14px; }
            QLabel#logo { color: #34ebb4; font-family: 'Consolas'; font-size: 24px; font-weight: bold; padding: 10px; }
            QPushButton { 
                background-color: #2c2c2c; 
                color: #ffffff; 
                font-family: 'Consolas'; 
                font-size: 16px; 
                font-weight: normal; 
                padding: 8px; 
                border: 2px solid transparent; 
                border-radius: 5px; 
            }
            QPushButton:hover { background-color: #3e3e3e; }
            QPushButton:focus { outline: none; }
            QLabel#bold-text { font-weight: bold; color: #ffffff; }
            QSlider::groove:horizontal { background: #1e1e1e; height: 4px; border-radius: 2px; }
            QSlider::handle:horizontal { background: #34ebb4; width: 12px; height: 12px; margin: -4px 0; border-radius: 6px; }
        """)


        self.init_ui()

    def init_ui(self):
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Title
        title_label = QLabel("Soul Crosshair", self)
        title_label.setObjectName("logo")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Crosshair file picker
        file_label = QLabel(f"Crosshair File: {os.path.basename(self.config['crosshair'])}", self)
        file_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(file_label)

        file_button = QPushButton("Change Crosshair File", self)
        file_button.clicked.connect(lambda: self.change_file(file_label))
        main_layout.addWidget(file_button)

        # Scale slider
        scale_label = QLabel(f"Scale: {self.config['scale']}%", self)
        scale_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(scale_label)

        scale_slider = QSlider(Qt.Horizontal, self)
        scale_slider.setMinimum(1)
        scale_slider.setMaximum(1000)
        scale_slider.setValue(self.config['scale'])
        scale_slider.valueChanged.connect(lambda: self.update_scale(scale_slider.value(), scale_label))
        main_layout.addWidget(scale_slider)

        # Create Crosshair Button
        create_button = QPushButton("Open Crosshair Creator", self)
        create_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://crosshair.themeta.gg/")))
        main_layout.addWidget(create_button)

        instructions_label = QLabel(self)
        instructions_label.setText(
            "How To Use Custom Crosshair Creator:\n"
            "1. Create or find Crosshair\n"
            "2. Download as png/jpg\n"
            "3. Put it in this folder in crosshairs\n"
            "4. Select it in the menu\n"
            "5. To End Crosshair Terminate Python"
        )
        instructions_label.setWordWrap(True)
        instructions_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(instructions_label)

        run_button = QPushButton("Show/Start Crosshair", self)
        run_button.clicked.connect(self.run_crosshair)
        main_layout.addWidget(run_button)

        # Save and Close Buttons
        button_layout = QVBoxLayout()


        close_button = QPushButton("Close Menu", self)
        close_button.clicked.connect(lambda: (self.close_crosshair(), self.close()))
        button_layout.addWidget(close_button)

        main_layout.addLayout(button_layout)

    def change_file(self, label):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Crosshair File", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.config['crosshair'] = file_path
            label.setText(f"Crosshair File: {os.path.basename(file_path)}")
            save_config(self.config)  # Automatically save the configuration


    def update_scale(self, value, label):
        self.config['scale'] = value
        label.setText(f"Scale: {value}%")
        save_config(self.config)  # Automatically save the configuration

    def save_config(self):
        save_config(self.config)

    def run_crosshair(self):
        """Launch crosshair.py as a separate process."""
        try:
            subprocess.Popen(["python", "crosshair.py"])  # Adjust to "python" if using Windows or another Python version
        except Exception as e:
            print(f"Error running crosshair.py: {e}")

    def mousePressEvent(self, event):
        self.drag_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()
            event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    menu = SettingsMenu()
    menu.show()
    sys.exit(app.exec_())
