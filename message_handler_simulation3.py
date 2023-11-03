import can
import threading
import time
import random
import matplotlib.pyplot as plt

# Create a CAN bus
bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

# Define message IDs
EMERGENCY_MESSAGE_ID = 0x100
ENGINE_HEAT_MESSAGE_ID = 0x200

# Lists to store data for visualization
time_points = []
temperature_data = []
emergency_data = []

# Enable Matplotlib interactive mode
plt.ion()

# Function to clear data
def clear_data():
    global time_points, temperature_data, emergency_data
    time_points = []
    temperature_data = []
    emergency_data = []

# Function to send messages from Node 1 (Engine Heat Monitor)
def engine_heat_monitor():
    while True:
        heat_data = random.uniform(80, 100)  # Simulate temperature data between 80°C and 100°C
        msg = can.Message(arbitration_id=ENGINE_HEAT_MESSAGE_ID, data=[int(heat_data)])
        bus.send(msg)

        # Record data for visualization
        current_time = time.time()
        time_points.append(current_time)
        temperature_data.append(heat_data)

        time.sleep(1)

# Function to send messages from Node 2 (Obstacle Finder)
def obstacle_finder():
    while True:
        # Simulate an "emergency situation" by sending an "emergency" message occasionally
        if random.random() < 0.1:
            msg = can.Message(arbitration_id=EMERGENCY_MESSAGE_ID, data=[1])
            bus.send(msg)

            # Record emergency data for visualization
            current_time = time.time()
            emergency_data.append((current_time, 1))

        time.sleep(0.5)

# Function to handle received messages in Node 3 (Main Control)
def main_control():
    while True:
        message = bus.recv()

        if message.arbitration_id == EMERGENCY_MESSAGE_ID:
            print("Main Control: Received an emergency message.")
            print("Main Control: Handling the emergency situation.")
            # Handle the emergency situation here
        elif message.arbitration_id == ENGINE_HEAT_MESSAGE_ID:
            temperature = message.data[0]
            print(f"Main Control: Received engine temperature data: {temperature} °C")
            # Handle regular engine heat data here

# Start the threads for each node
engine_heat_thread = threading.Thread(target=engine_heat_monitor)
obstacle_finder_thread = threading.Thread(target=obstacle_finder)
main_control_thread = threading.Thread(target=main_control)

engine_heat_thread.start()
obstacle_finder_thread.start()
main_control_thread.start()

# Clear data at the beginning of each run
clear_data()

# Visualization
def plot_data():
    plt.figure(figsize=(10, 6))
    plt.title("Engine Temperature and Emergency Situations Over Time")

    # Plot temperature data
    plt.plot(time_points, temperature_data, label="Engine Temperature (°C)")

    # Plot emergency situations as vertical lines
    for time_point, _ in emergency_data:
        plt.axvline(x=time_point, color='r', linestyle='--', label="Emergency Situation")

    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True)
    plt.pause(0.01)  # Add a pause to allow interactive updates

# Start the data visualization thread
visualization_thread = threading.Thread(target=plot_data)
visualization_thread.start()

# Controlled "emergency situation" simulation
def simulate_emergency():
    time.sleep(10)  # Simulate an emergency situation after 10 seconds
    msg = can.Message(arbitration_id=EMERGENCY_MESSAGE_ID, data=[1])
    bus.send(msg)
    print("Simulated Emergency: An emergency situation has occurred.")

# Start the controlled "emergency situation" simulation
emergency_simulation_thread = threading.Thread(target=simulate_emergency)
emergency_simulation_thread.start()

# Keep the script running
while True:
    pass

