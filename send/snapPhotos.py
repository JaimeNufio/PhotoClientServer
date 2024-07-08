import io
import socket
import struct
import time
import picamera

# Connect a client socket to my_server:8000 (change my_server to the IP address of your receiving computer)
client_socket = socket.socket()
client_socket.connect(('192.168.1.158', 1197))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)  # Adjust resolution as needed
        camera.framerate = 30  # Adjust framerate as needed
        time.sleep(2)  # Let camera warm up

        # Capture images continuously
        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            # Rewind the stream and send image data over the wire
            stream.seek(0)
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            stream.seek(0)
            stream.truncate()

            # Add a delay between captures to control frame rate
            time.sleep(0.1)  # Adjust delay to achieve desired frame rate

finally:
    connection.close()
    client_socket.close()

