import socket
import time

def sender():
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_address = ('127.0.0.1', 12345)
    sender_socket.settimeout(2) 

    messages = ["Message 1", "Message 2", "Message 3", "END"]
    sequence_number = 0

    for message in messages:
        while True:
            try:
                data = f"{sequence_number}:{message}"
                sender_socket.sendto(data.encode(), receiver_address)
                print(f"Sender: Sent -> {data}")

            
                ack, _ = sender_socket.recvfrom(1024)
                ack = ack.decode()
                print(f"Sender: Received ACK -> {ack}")

                if ack == str(sequence_number):
                    sequence_number = 1 - sequence_number 
                    break 
            except socket.timeout:
                print("Sender: Timeout! Resending...")

    sender_socket.close()

if __name__ == "__main__":
    sender()
