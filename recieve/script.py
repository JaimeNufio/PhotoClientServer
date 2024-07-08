import socket
import struct
import io
import os

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = ('', 1197)  # Empty string '' means to listen on all available interfaces
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print("Waiting for a connection...")

try:
    while True:
        # Wait for a connection
        connection, client_address = server_socket.accept()

        try:
            print(f"Connection from {client_address}")

            # Make a file-like object out of the connection
            connection_file = connection.makefile('rb')

            while True:
                # Read the image size from the connection
                image_len = struct.unpack('<L', connection_file.read(struct.calcsize('<L')))[0]

                # If the length is 0, it indicates the end of transmission
                if not image_len:
                    break

                # Read the image data
                image_data = connection_file.read(image_len)

                # Save the image to a folder
                image_file_name = f"image_{time.time()}.jpg"  # You can generate a unique filename here
                save_path = './' + image_file_name  # Replace with your desired save path
                with open(save_path, 'wb') as image_file:
                    image_file.write(image_data)
                    print(f"Image saved: {image_file_name}")

        finally:
            # Clean up the connection
            connection_file.close()
            connection.close()

finally:
    server_socket.close()

