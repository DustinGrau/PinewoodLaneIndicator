import adafruit_dotstar
import array
import board
import time
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction

# Initialize DotStar LED for indicator
dot_led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)

# Configuration and constants
RESET_TIME = 10  # Reset interval after detecting a winner (in seconds)
NUM_READINGS = 16  # Number of readings for averaging
SLEEP_TIME = 1  # Sleep time between readings (in milliseconds)

# Variables for sensor data
readIndex = 0
l1_readings = array.array("f", [0] * NUM_READINGS)
l2_readings = array.array("f", [0] * NUM_READINGS)
l1_total = 0
l1_average = 0
l2_total = 0
l2_average = 0
has_averages = False

# Flags for winner detection
l1_winner = False
l2_winner = False

# Set up lane sensors and indicator LEDs
lane1 = AnalogIn(board.A3)
lane2 = AnalogIn(board.A4)
led1 = DigitalInOut(board.A1)
led1.direction = Direction.OUTPUT
led2 = DigitalInOut(board.A2)
led2.direction = Direction.OUTPUT

def initialize_sensors():
    # Initialize sensors and LEDs, and build up initial averages.
    global has_averages
    dot_led[0] = (60, 40, 0)  # Orange - initialization
    while not has_averages:
        avg_lanes()
        time.sleep(0.01)
    dot_led[0] = (0, 60, 0)  # Green - ready status

def get_input(pin):
    # Read the voltage on the analog pin.
    return round(((pin.value * pin.reference_voltage) / 65536), 1)

def avg_lanes():
    # Calculate moving averages for the lane sensors.
    global l1_total, l2_total, l1_last, l2_last, l1_average, l2_average, readIndex, has_averages

    # Remove the oldest reading from totals
    l1_total -= l1_readings[readIndex]
    l2_total -= l2_readings[readIndex]

    # Get new readings and update arrays
    l1_last = get_input(lane1)
    l2_last = get_input(lane2)
    l1_readings[readIndex] = l1_last
    l2_readings[readIndex] = l2_last

    # Add the new reading to the totals
    l1_total += l1_last
    l2_total += l2_last

    # Move to the next index, wrap if at the end
    readIndex = (readIndex + 1) % NUM_READINGS

    # Calculate the averages
    l1_average = round(l1_total / NUM_READINGS, 1)
    l2_average = round(l2_total / NUM_READINGS, 1)

    # Signal averages are ready after initial build-up
    if not has_averages and readIndex == 0:
        has_averages = True
        print("Average values ready.")

def detect_winner():
    # Check for the winner based on a lane sensor becoming more than 50% obscured.
    global l1_winner, l2_winner
    l1_change = l2_change = 0.0

    # Check for low light or improper setup
    if l1_average < (lane1.reference_voltage * 0.6) or l2_average < (lane2.reference_voltage * 0.6):
        dot_led[0] = (40, 0, 40)  # Purple - low light or setup issue
        return

    # Calculate percent changes in readings
    if l1_average > l1_readings[(readIndex - 1) % NUM_READINGS]:
        l1_change = round(((l1_average - l1_readings[(readIndex - 1) % NUM_READINGS]) / l1_average) * 100, 1)
    if l2_average > l2_readings[(readIndex - 1) % NUM_READINGS]:
        l2_change = round(((l2_average - l2_readings[(readIndex - 1) % NUM_READINGS]) / l2_average) * 100, 1)

    # Debug: Print significant changes
    if l1_change > 20 or l2_change > 20:
        print("Lane1:", l1_average, "v avg,", l1_change, "% | Lane2:", l2_average, "v avg,",l2_change, "%")

    # Determine winner if a change exceeds 50%
    if l1_change > 50 or l2_change > 50:
        l1_winner = l1_change > l2_change
        l2_winner = l2_change > l1_change

def announce_winner():
    # Indicate the winner with LEDs and reset after a timeout.
    global l1_winner, l2_winner
    initial_time = time.monotonic()

    # Set the winning lane LED and display blue on DotStar
    if l1_winner:
        print("Winner: Lane 1!")
        led1.value = True
    if l2_winner:
        print("Winner: Lane 2!")
        led2.value = True

    dot_led[0] = (0, 0, 60)  # Blue - winner indication

    # Hold the winner indication for RESET_TIME, then reset
    while time.monotonic() - initial_time < RESET_TIME:
        avg_lanes()  # Continue gathering sensor data during delay
        time.sleep(0.4)

    # Reset LEDs and winner flags
    l1_winner = l2_winner = False
    led1.value = led2.value = False
    print("Reset completed.")
    dot_led[0] = (0, 60, 0)  # Green - ready status

def main():
    # Main loop to initialize sensors, detect, and announce race winner.
    initialize_sensors()  # Initial setup and averaging

    while True:
        avg_lanes()  # Update averages for both lanes

        if not (l1_winner or l2_winner):  # Only detect if no winner has been set
            detect_winner()

        if l1_winner or l2_winner:  # Announce if a winner is detected
            announce_winner()

        time.sleep(SLEEP_TIME / 1000)  # Small sleep between readings

# Run the main function
main()
