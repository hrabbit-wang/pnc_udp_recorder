from udp_recorder import UdpRecorder
from threading import Thread
import sys
import time
from PyQt5.QtWidgets import (QPushButton, QApplication,
     QVBoxLayout, QDialog, QLabel, QFileDialog)

class Form(QDialog):
    def __init__(self, parent, udp_rec):
        super(Form, self).__init__(parent)
        self.udp_rec = udp_rec
        # Create widgets
        self.dir_button = QPushButton("Save Dir")
        self.label = QLabel("./")
        self.trig_button = QPushButton("Trigger Recording")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.dir_button)
        layout.addWidget(self.label)
        layout.addWidget(self.trig_button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.trig_button.clicked.connect(self.trigger_event)
        self.dir_button.clicked.connect(self.select_dir)

    # trigger
    def trigger_event(self):
        time_t = int(time.time())
        self.udp_rec.trigger_evt(time_t)

    # save dir
    def select_dir(self):
      dir_str = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
      self.label.setText(dir_str)
      self.udp_rec.set_save_dir(dir_str)


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    # start the bk udp recording thread
    udp_rec = UdpRecorder("192.168.1.187", 6002)
    rec_thread = Thread(target=udp_rec.receive, args=())
    rec_thread.start()
    # Create and show the form
    form = Form(None, udp_rec)
    form.show()
    ret = app.exec()
    udp_rec.exit()
    rec_thread.join()
    print("closed")
    # Run the main Qt loop
    sys.exit(ret)
