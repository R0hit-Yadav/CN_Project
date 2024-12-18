import socket
import random 

def receiver():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_socket.bind(('127.0.0.1', 12345))

    expected_sequence_number = 0

    while True:
        data, sender_address = receiver_socket.recvfrom(1024)
        data = data.decode()
        sequence_number, message = data.split(":", 1)

        print(f"Receiver: Received -> {data}")

        if random.random() > 0.8:  # 20% chance to drop ACK
            print(f"Receiver: Dropping ACK for sequence number {sequence_number}")
            continue

    
        if int(sequence_number) == expected_sequence_number:
            print(f"Receiver: Processing -> {message}")
            receiver_socket.sendto(str(expected_sequence_number).encode(), sender_address)
            expected_sequence_number = 1 - expected_sequence_number 
        else:
            print("Receiver: Out-of-order packet. Resending last ACK.")
            receiver_socket.sendto(str(1 - expected_sequence_number).encode(), sender_address)

        if message == "END":
            print("Receiver: End of communication.")
            break

    receiver_socket.close()

if __name__ == "__main__":
    receiver()
