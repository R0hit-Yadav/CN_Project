import tkinter as tk
from tkinter import messagebox
import time
import random
from threading import Thread, Event


class StopAndWaitGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stop-and-Wait Protocol Simulation")

        # Control variables
        self.paused = Event()
        self.stopped = Event()
        self.paused.set()  # Initially, not paused

        self.retransmissions = 0  # Counter for retransmissions

        # Create GUI components
        self.sender_label = tk.Label(root, text="Sender", font=("Arial", 16))
        self.sender_label.grid(row=0, column=0, padx=20, pady=20)

        self.receiver_label = tk.Label(root, text="Receiver", font=("Arial", 16))
        self.receiver_label.grid(row=0, column=2, padx=20, pady=20)

        self.packet_box = tk.Text(root, width=30, height=10, state="disabled")
        self.packet_box.grid(row=1, column=0, padx=10, pady=10)

        self.status_box = tk.Text(root, width=30, height=10, state="disabled")
        self.status_box.grid(row=1, column=2, padx=10, pady=10)

        self.stats_box = tk.Text(root, width=30, height=5, state="disabled")
        self.stats_box.grid(row=2, column=1, padx=10, pady=10)

        self.start_button = tk.Button(root, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=3, column=0, pady=10)

        self.pause_button = tk.Button(root, text="Pause Simulation", command=self.toggle_pause)
        self.pause_button.grid(row=3, column=1, pady=10)

        self.stop_button = tk.Button(root, text="Stop Simulation", command=self.stop_simulation)
        self.stop_button.grid(row=3, column=2, pady=10)

    def log_message(self, box, message):
        """Logs a message to the specified text box."""
        box.config(state="normal")
        box.insert(tk.END, message + "\n")
        box.see(tk.END)
        box.config(state="disabled")

    def update_stats(self):
        """Update retransmission stats."""
        self.stats_box.config(state="normal")
        self.stats_box.delete(1.0, tk.END)
        self.stats_box.insert(tk.END, f"Retransmissions: {self.retransmissions}\n")
        self.stats_box.config(state="disabled")

    def sender(self):
        packets = ["Packet1", "Packet2", "Packet3"]
        timeout = 3  # Timeout in seconds

        for packet in packets:
            sent = False
            while not sent:
                self.paused.wait()  # Pause if needed
                if self.stopped.is_set():
                    self.log_message(self.packet_box, "Simulation stopped.")
                    return

                self.log_message(self.packet_box, f"Sending: {packet}")
                time.sleep(1)  # Simulate transmission time

                # Simulate acknowledgment with a random chance of failure
                if random.choice([True, False]):
                    self.log_message(self.status_box, f"ACK received for {packet}")
                    sent = True
                else:
                    self.log_message(self.status_box, f"ACK not received, retransmitting {packet}")
                    self.retransmissions += 1
                    self.update_stats()
                    time.sleep(timeout)

    def receiver(self):
        received_packets = []

        while len(received_packets) < 3:
            self.paused.wait()  # Pause if needed
            if self.stopped.is_set():
                self.log_message(self.status_box, "Simulation stopped.")
                return

            # Simulate packet receipt with a random chance of loss
            if random.choice([True, False]):
                packet = f"Packet{len(received_packets) + 1}"
                self.log_message(self.status_box, f"Receiver: Received {packet}")
                received_packets.append(packet)
            else:
                self.log_message(self.status_box, "Receiver: Packet lost in transmission")
            time.sleep(2)  # Simulate processing time

        self.log_message(self.status_box, "Receiver: All packets received")

    def start_simulation(self):
        """Starts the sender and receiver simulation in separate threads."""
        self.stopped.clear()
        self.paused.set()
        Thread(target=self.sender).start()
        Thread(target=self.receiver).start()

    def toggle_pause(self):
        """Pauses or resumes the simulation."""
        if self.paused.is_set():
            self.paused.clear()
            self.pause_button.config(text="Resume Simulation")
        else:
            self.paused.set()
            self.pause_button.config(text="Pause Simulation")

    def stop_simulation(self):
        """Stops the simulation."""
        if messagebox.askyesno("Stop Simulation", "Are you sure you want to stop the simulation?"):
            self.stopped.set()
            self.paused.set()
            self.log_message(self.packet_box, "Simulation stopped.")
            self.log_message(self.status_box, "Simulation stopped.")
            self.update_stats()


if __name__ == "__main__":
    root = tk.Tk()
    app = StopAndWaitGUI(root)
    root.mainloop()