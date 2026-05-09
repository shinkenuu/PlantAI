# Increase when facing errors AND the L Led (pin 13) blinks once then fades
RESET_DELAY = 1

# Change these according to your Arduino setup
PORT = "/dev/ttyACM0"
BAUD_RATE = 115200
TIMEOUT = 5  # Increase empirically when DEBUG tells there is no bytes waiting for either Tx and Rx
LAST_PIN_INDEX = 69  # Mega's highest pin address
