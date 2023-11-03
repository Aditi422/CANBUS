import threading
import queue
import time

# Define message priorities
LOW_PRIORITY = 2
MEDIUM_PRIORITY = 1
HIGH_PRIORITY = 0

# Define a message queue for message storage
message_queue = queue.PriorityQueue()

# Function to send a message to the queue
def send_message(message, priority):
    message_queue.put((priority, message))

# Function to simulate message handling
def message_handler():
    while True:
        try:
            priority, message = message_queue.get(timeout=1)  # Timeout to allow for message handling
            if priority == HIGH_PRIORITY:
                print(f"Handling HIGH PRIORITY message: {message}")
            elif priority == MEDIUM_PRIORITY:
                print(f"Handling MEDIUM PRIORITY message: {message}")
            elif priority == LOW_PRIORITY:
                print(f"Handling LOW PRIORITY message: {message}")
            message_queue.task_done()
        except queue.Empty:
            pass

# Create threads for message handling
handler_thread = threading.Thread(target=message_handler)
handler_thread.daemon = True  # Allow the program to exit when all threads are done
handler_thread.start()

# Simulate sending messages with different priorities
for i in range(1, 11):
    if i % 3 == 0:
        send_message(f"Emergency message {i}", HIGH_PRIORITY)
    elif i % 2 == 0:
        send_message(f"Medium priority message {i}", MEDIUM_PRIORITY)
    else:
        send_message(f"Low priority message {i}", LOW_PRIORITY)
    time.sleep(1)  # Simulate message generation delay

# Wait for all messages to be processed
message_queue.join()

