import serial
import keyboard

PORT = "COM7"
BAUDRATE = 115200

ser = serial.Serial(PORT, BAUDRATE, timeout=1)

print("BMW GWS -> KLAVESNICE")
print("COM7 pripojeno")
print("Cekam na povely...")

while True:
    try:
        command = ser.readline().decode("utf-8", errors="ignore").strip()

        if not command:
            continue

        print("GWS:", command)

        # PARK
        if command == "P":
            keyboard.press_and_release("t")

        # REVERSE
        elif command == "R":
            keyboard.press_and_release("o")

        # NEUTRAL
        elif command == "N":
            keyboard.press_and_release("n")

        # DRIVE
        elif command == "D":
            keyboard.press_and_release("y")

        # MANUAL / SPORT
        elif command == "M/S":
            keyboard.press_and_release("u")

        # M+
        elif command == "M+":
            keyboard.press_and_release("x")

        # M-
        elif command == "M-":
            keyboard.press_and_release("z")

    except KeyboardInterrupt:
        break

ser.close()