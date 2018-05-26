import io
import struct
from PIL import Image
import cv2 as cv
import numpy as np
import socket

from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage

class StreamServer(QThread):
    changePixmap = pyqtSignal(np.ndarray)
    sendImage = pyqtSignal(np.ndarray)

    def __init__(self, host, port):
        super().__init__()
        print("Stream_server_Start")
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        

    def run(self):
        try:
            self.server_socket.listen(1)
            self.connection = self.server_socket.accept()[0].makefile('rb')

            while True:
                # Read the length of the image as a 32-bit unsigned int. If the
                # length is zero, quit the loop
                image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break
                # Construct a stream to hold the image data and read the image
                # data from the connection
                image_stream = io.BytesIO()
                image_stream.write(self.connection.read(image_len))
                # Rewind the stream, open it as an image with PIL and do some
                # processing on it
                image_stream.seek(0)
                image = Image.open(image_stream)
                image.verify()

                data = np.fromstring(image_stream.getvalue(), dtype=np.uint8)

                cv_image = cv.imdecode(data, 1)
                cv_image = cv.cvtColor(cv_image, cv.COLOR_BGR2RGB)

                self.sendImage.emit(cv_image)
                self.changePixmap.emit(cv_image)


        finally:
            self.connection.close()
            self.server_socket.close()

    def __del__(self):
        print("server is close")
        self.wait()

