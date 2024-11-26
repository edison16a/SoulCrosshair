import sys
import json
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
import os

class CrosshairWindow(QLabel):
    def __init__(self):
        super().__init__()
        self.config = {}
        self.last_modified_time = 0  # Track last modification time
        self.load_config()

        # Load and display crosshair
        self.update_crosshair()

        # Set the window properties
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_X11DoNotAcceptFocus, True)

        # Set up a timer to periodically check the configuration file
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_config)
        self.timer.start(1000)  # Check every 1000 milliseconds (1 second)

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

    def check_config(self):
        """Check if the configuration file has changed and reload if necessary."""
        try:
            # Get the modification time of the config file
            current_modified_time = os.path.getmtime('config.json')
            if current_modified_time != self.last_modified_time:
                self.last_modified_time = current_modified_time
                print("config.json modified. Reloading...")
                self.load_config()
                self.update_crosshair()
        except FileNotFoundError:
            print("Error: config.json not found.")
        except Exception as e:
            print(f"Error checking config.json: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the crosshair window
    window = CrosshairWindow()
    window.show()

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Exiting...")
