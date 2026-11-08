import serial
import keyboard
import time

PORT = "COM7"
BAUDRATE = 115200

ser = serial.Serial(PORT, BAUDRATE, timeout=1)

print("BMW GWS -> BEAMNG")
print("COM7 pripojeno")
print("Cekam na povely...")

# Aktuálně držená klávesa
held_key = None


def hold_key(key):
    global held_key

    # Vždy nejdříve pustíme aktuální klávesu.
    # Díky tomu lze stejný příkaz poslat znovu.
    if held_key is not None:
        keyboard.release(held_key)
        time.sleep(0.03)

    # Znovu stiskneme požadovanou klávesu
    keyboard.press(key)

    held_key = key


def release_key():
    global held_key

    if held_key is not None:
        keyboard.release(held_key)
        held_key = None


def tap_key(key):
    # Krátký samostatný stisk
    keyboard.press(key)
    time.sleep(0.03)
    keyboard.release(key)


try:

    while True:

        command = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if not command:
            continue

        print("GWS:", command)

        # =========================
        # PARK
        # =========================
        if command == "P":
            hold_key("t")

        # =========================
        # REVERSE
        # =========================
        elif command == "R":
            hold_key("o")

        # =========================
        # NEUTRAL
        # =========================
        elif command == "N":
            hold_key("n")

        # =========================
        # DRIVE
        # =========================
        elif command == "D":
            hold_key("y")

        # =========================
        # MANUAL / SPORT
        # =========================
        # U musí být drženo.
        elif command == "M/S":
            hold_key("u")

        # =========================
        # M+
        # =========================
        # Každý M+ = nový stisk X
        elif command == "M+":
            tap_key("x")

        # =========================
        # M-
        # =========================
        # Každý M- = nový stisk Z
        elif command == "M-":
            tap_key("z")


except KeyboardInterrupt:

    print("\nUkoncuji...")


finally:

    release_key()

    ser.close()

    print("COM7 odpojeno")
