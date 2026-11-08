import serial
import keyboard

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

    # Pokud už držíme stejnou klávesu,
    # nic neděláme
    if held_key == key:
        return

    # Pustíme předchozí klávesu
    if held_key is not None:
        keyboard.release(held_key)

    # Stiskneme novou klávesu
    keyboard.press(key)

    held_key = key


def release_key():
    global held_key

    if held_key is not None:
        keyboard.release(held_key)
        held_key = None


def tap_key(key):
    # Krátký stisk klávesy
    keyboard.press_and_release(key)


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
        # X je pouze krátký stisk.
        elif command == "M+":
            tap_key("x")

        # =========================
        # M-
        # =========================
        # Z je pouze krátký stisk.
        elif command == "M-":
            tap_key("z")


except KeyboardInterrupt:

    print("\nUkoncuji...")


finally:

    # Před ukončením vždy pustíme
    # případnou drženou klávesu
    release_key()

    ser.close()

    print("COM7 odpojeno")
