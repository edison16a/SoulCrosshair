import sys
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

# PyQt5 application
class CrosshairWindow(QLabel):
    def __init__(self):
        super().__init__()
        self.config = {}
        self.load_config()

        # Load and display crosshair
        self.update_crosshair()

        # Set the window properties
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_X11DoNotAcceptFocus, True)

    def load_config(self):
        """Load the configuration file."""
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error loading config.json: {e}")
            sys.exit(1)

    def update_crosshair(self):
        """Update the crosshair based on the configuration."""
        crosshair_file = self.config.get('crosshair', 'crosshair.png')
        scale_factor = self.config.get('scale', 50)

        # Load crosshair image
        pixmap = QPixmap(crosshair_file)
        if pixmap.isNull():
            print(f"Error: Unable to load image {crosshair_file}")
            return

        # Scale the crosshair
        scaled_pixmap = pixmap.scaled(
            pixmap.width() * scale_factor // 100,
            pixmap.height() * scale_factor // 100,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        # Set the scaled image to the QLabel
        self.setPixmap(scaled_pixmap)
        self.setFixedSize(scaled_pixmap.size())

        # Center the crosshair on the screen
        screen_geometry = QApplication.primaryScreen().geometry()
        self.move(
            (screen_geometry.width() - self.width()) // 2,
            (screen_geometry.height() - self.height()) // 2,
        )

# File change handler for Watchdog
class ConfigFileHandler(FileSystemEventHandler):
    def __init__(self, crosshair_window):
        super().__init__()
        self.crosshair_window = crosshair_window

    def on_modified(self, event):
        if event.src_path.endswith('config.json'):
            print("config.json modified. Reloading...")
            self.crosshair_window.load_config()
            self.crosshair_window.update_crosshair()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the crosshair window
    window = CrosshairWindow()
    window.show()

    # Watchdog observer to monitor config.json
    observer = Observer()
    event_handler = ConfigFileHandler(window)
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Exiting...")
        observer.stop()
    observer.join()
