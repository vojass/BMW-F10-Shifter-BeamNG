# BMW F10 GWS → Arduino Nano → MCP2515 → BeamNG.drive

## ČESKY

Tento projekt umožňuje připojit BMW F10 GWS řadičku k Arduinu přes CAN-BUS pomocí modulu MCP2515 a následně posílat její povely do počítače jako klávesy pro BeamNG.drive. Není potřeba žádný joystick emulator. Lze použít prakticky jakékoli běžné Arduino, včetně kompatibilních klonů, pokud má potřebné SPI piny. V tomto projektu je použito Arduino Nano.

BMW GWS musí být napájena **samostatným 12V zdrojem s proudovou kapacitou minimálně 2 A**. Arduino Nano se napájí pouze přes USB z počítače. 12 V ze zdroje GWS se nepřipojuje do Arduina.

Při pohledu na konektor GWS shora, když je řadička před tebou, jsou piny zleva doprava: pin 1 = +12 V, pin 2 = +12 V Wake-up, pin 3 = CAN-L, pin 4 = CAN-H a pin 5 = GND. Kladný vodič +12 V ze zdroje se rozdělí na dvě větve: jedna vede na pin 1 GWS (+12 V) a druhá na pin 2 GWS (+12 V Wake-up). GND ze zdroje se rozdělí na dvě větve: jedna vede na pin 5 GWS (GND) a druhá vede na libovolný GND pin Arduina. Arduino je tedy napájené pouze z USB, zatímco GWS má vlastní 12V zdroj. GWS a Arduino nemusí mít stejný zdroj napájení, ale jejich GND musí být propojené. MCP2515 GND musí být také propojena s GND Arduina. **+12 V nikdy nepřipojuj na 5 V nebo VIN Arduina.**

MCP2515 je připojen k Arduinu přes SPI. Použité zapojení je D13 → SCK, D12 → SO/MISO, D11 → SI/MOSI, D10 → CS, D2 → INT, 5V → VCC a GND → GND. CAN-H a CAN-L z MCP2515 se připojují na CAN-H a CAN-L BMW GWS. GND MCP2515 musí být propojena s GND Arduina.

Na MCP2515 musí být také propojený jumper **J1**. J1 slouží k aktivaci zakončení CAN sběrnice a v tomto zapojení musí být nasazený/propojený. Pokud J1 není propojený, CAN komunikace nemusí fungovat správně.

CAN komunikace používá rychlost **500 kbit/s**. MCP2515 modul může mít krystal 8 MHz nebo 16 MHz. V aktuálním programu je nastavena varianta 8 MHz pomocí `MCP_8MHZ`. Pokud má tvůj MCP2515 16MHz krystal, změň v programu `MCP_8MHZ` na `MCP_16MHZ` v řádku `CAN0.begin(...)`. Pokud máš 8MHz modul, není potřeba tuto část měnit.

Pokud používáš jiné piny než v tomto projektu, můžeš je změnit na začátku programu pomocí `CAN_CS` a `CAN_INT`. Standardní zapojení tohoto projektu používá CS na D10 a INT na D2.

Pro nahrání programu do Arduina otevři `Arduino/BMW_F10_GWS.ino` v Arduino IDE, vyber správnou desku a COM port a program nahraj. U některých Arduino Nano klonů může být potřeba v Arduino IDE v nastavení procesoru vybrat `ATmega328P (Old Bootloader)`. Pokud nahrávání funguje s běžným `ATmega328P`, není potřeba Old Bootloader používat.

Po připojení Arduina k počítači se v systému objeví COM port. Číslo portu zjistíš ve Správci zařízení v části `Porty (COM a LPT)`. V souboru `beamng_gws.py` musí být nastaven stejný port. Aktuálně je nastaveno `PORT = "COM7"`, takže pokud máš například COM8, změň hodnotu na `PORT = "COM8"`.

Python program používá knihovny `pyserial` a `keyboard`. Python musí být nainstalovaný v počítači. Knihovny lze nainstalovat příkazem `pip install pyserial keyboard`. Pokud příkaz `pip` nefunguje, použij `py -m pip install pyserial keyboard`.

### Jak spustit převodník

Pro běžné používání není potřeba pokaždé otevírat CMD ani zadávat žádné příkazy. Po nastavení Pythonu a instalaci potřebných knihoven stačí najít soubor `beamng_gws.py` v projektu a **dvakrát na něj kliknout**. Tím se spustí převodník mezi BMW GWS a klávesnicí počítače. Otevře se okno programu, které zůstane spuštěné a bude čekat na povely z řadičky. Během používání musí toto okno zůstat otevřené. Pokud se okno zavře, převodník přestane fungovat. Po skončení používání lze okno jednoduše zavřít.

Pokud Windows při dvojkliku soubor `beamng_gws.py` otevře v editoru místo spuštění, je potřeba mít správně nainstalovaný Python a asociaci souborů `.py` s Pythonem. Alternativně lze soubor otevřít pravým tlačítkem a zvolit spuštění pomocí Pythonu.

Po spuštění převodníku se program připojí k Arduinu přes USB a čeká na příkazy z GWS. Před použitím v BeamNG.drive je vhodné program nejdříve otestovat v Poznámkovém bloku. Pokud při pohybu řadičky program vypisuje správné příkazy a v Poznámkovém bloku se správně generují klávesy, komunikace mezi GWS, Arduino, MCP2515 a Pythonem funguje.

Aktuální mapování je P = T, R = O, N = N, D = Y, M/S = U, M+ = X a M− = Z. V tomto projektu znamená M+ pohyb řadičky směrem k řidiči a M− pohyb řadičky směrem od řidiče. Python tyto příkazy převádí na klávesové vstupy systému Windows.

BMW GWS používá CAN ID `0x197` pro informace o poloze řadičky a CAN ID `0x3FD` pro informace displeje. Program také používá CRC8 s polynomem `0x1D`, počáteční hodnotou `0x00` a finálním XOR `0x70`. CAN ID `0x3FD` je odesíláno průběžně bez čekání, aby zůstala komunikace s displejem aktivní.

Struktura projektu je jednoduchá. Soubor `Arduino/BMW_F10_GWS.ino` obsahuje program pro Arduino a MCP2515. Soubor `beamng_gws.py` obsahuje Python program, který převádí příkazy z Arduina na klávesy Windows. Soubor `README.md` obsahuje návod k zapojení a použití projektu.

Pokud používáš NVIDIA GeForce NOW, může být problém s předáváním programově generovaných kláves do streamované hry. Proto je důležité nejdříve ověřit funkčnost v běžné aplikaci, například v Poznámkovém bloku. Pokud klávesy fungují v Poznámkovém bloku, ale nefungují v BeamNG.drive přes GeForce NOW, problém pravděpodobně není v Arduinu, GWS ani Python programu, ale v tom, jak GeForce NOW přijímá vstupy.

Projekt je určený pro experimentování s BMW GWS, CAN-BUS, Arduino, MCP2515 a ovládáním BeamNG.drive. Před připojením vždy zkontroluj polaritu napájení a zapojení CAN vodičů. BMW GWS musí být napájena vhodným **12V zdrojem s proudovou kapacitou minimálně 2 A**.

## ENGLISH

This project allows you to connect a BMW F10 GWS shifter to an Arduino through CAN-BUS using an MCP2515 module and then send the shifter commands to a PC as keyboard inputs for BeamNG.drive. No joystick emulator is required. Almost any normal Arduino can be used, including compatible Arduino clones, as long as it has the required SPI pins. This project uses an Arduino Nano.

The BMW GWS must be powered by a **separate 12V power supply with a minimum current capacity of 2 A**. The Arduino Nano is powered only through USB from the computer. The 12V GWS power supply must not be connected directly to the Arduino.

When looking at the GWS connector from above with the shifter in front of you, the pins are, from left to right: pin 1 = +12 V, pin 2 = +12 V Wake-up, pin 3 = CAN-L, pin 4 = CAN-H and pin 5 = GND. The +12 V wire from the power supply is split into two branches: one branch goes to GWS pin 1 (+12 V) and the other branch goes to GWS pin 2 (+12 V Wake-up). The GND wire from the power supply is split into two branches: one branch goes to GWS pin 5 (GND) and the other branch goes to any GND pin on the Arduino. The Arduino is therefore powered only from USB while the GWS has its own 12V power supply. The GWS and Arduino do not need to use the same power supply, but their GND connections must be connected together. MCP2515 GND must also be connected to Arduino GND. **Never connect +12 V to the Arduino 5 V or VIN.**

The MCP2515 is connected to the Arduino through SPI. The wiring used in this project is D13 → SCK, D12 → SO/MISO, D11 → SI/MOSI, D10 → CS, D2 → INT, 5V → VCC and GND → GND. MCP2515 CAN-H and CAN-L are connected to the BMW GWS CAN-H and CAN-L. MCP2515 GND must be connected to Arduino GND.

The **J1 jumper** on the MCP2515 must also be connected. J1 enables the CAN bus termination and must be installed/connected in this setup. If J1 is not connected, CAN communication may not work correctly.

CAN communication uses **500 kbit/s**. The MCP2515 module can have either an 8 MHz or 16 MHz crystal. The current Arduino program is configured for an 8 MHz module using `MCP_8MHZ`. If your MCP2515 has a 16 MHz crystal, change `MCP_8MHZ` to `MCP_16MHZ` in the `CAN0.begin(...)` line. If your module is 8 MHz, no change is required.

If you use different Arduino pins, you can change them at the beginning of the program using `CAN_CS` and `CAN_INT`. The default wiring in this project uses CS on D10 and INT on D2.

To upload the Arduino program, open `Arduino/BMW_F10_GWS.ino` in Arduino IDE, select the correct board and COM port, and upload the program. Some Arduino Nano clones may require `ATmega328P (Old Bootloader)` in the processor settings. If normal `ATmega328P` works, there is no need to use the old bootloader.

After connecting the Arduino to the PC, Windows will assign it a COM port. You can find it in Device Manager under `Ports (COM & LPT)`. The same port must be selected in `beamng_gws.py`. The current setting is `PORT = "COM7"`, so if your Arduino appears as COM8, change it to `PORT = "COM8"`.

The Python program uses the `pyserial` and `keyboard` libraries. Python must be installed on the PC. Install the required libraries with `pip install pyserial keyboard`. If `pip` does not work, use `py -m pip install pyserial keyboard`.

### How to start the converter

For normal use, you do not need to open CMD or type any commands every time. After Python and the required libraries have been installed, simply find the `beamng_gws.py` file in the project and **double-click it**. This starts the converter between the BMW GWS and the computer keyboard. A program window will open and remain running while it waits for commands from the shifter. This window must remain open while using the shifter. If the window is closed, the converter stops working. When you are finished, simply close the program window.

If Windows opens `beamng_gws.py` in a text editor instead of running it, Python must be installed correctly and `.py` files must be associated with Python. Alternatively, you can right-click the file and choose to open it with Python.

After starting the converter, the program connects to the Arduino through USB and waits for commands from the GWS. Before using it with BeamNG.drive, it is recommended to test the program in Notepad. If the program prints the correct commands and the correct keyboard inputs are generated in Notepad, communication between the GWS, Arduino, MCP2515 and Python is working.

The current keyboard mapping is P = T, R = O, N = N, D = Y, M/S = U, M+ = X and M− = Z. In this project, M+ means moving the shifter toward the driver and M− means moving it away from the driver. Python converts these commands into Windows keyboard inputs.

The BMW GWS uses CAN ID `0x197` for shifter position information and CAN ID `0x3FD` for display information. The program also uses CRC8 with polynomial `0x1D`, initial value `0x00` and final XOR `0x70`. CAN ID `0x3FD` is transmitted continuously without a delay to keep the display communication active.

The project structure is simple. `Arduino/BMW_F10_GWS.ino` contains the Arduino and MCP2515 program. `beamng_gws.py` contains the Python program that converts Arduino commands into Windows keyboard inputs. `README.md` contains the wiring and setup documentation.

If you use NVIDIA GeForce NOW, there may be a problem with forwarding programmatically generated keyboard inputs to the streamed game. Therefore, always test the system in a normal Windows application such as Notepad first. If the keyboard inputs work in Notepad but do not work in BeamNG.drive through GeForce NOW, the problem is likely related to how GeForce NOW receives input rather than the Arduino, GWS or Python program.

This project is intended for experimenting with BMW GWS, CAN-BUS, Arduino, MCP2515 and BeamNG.drive control. Always check the power polarity and CAN wiring before connecting the hardware. The BMW GWS must be powered by a suitable **12V power supply with a minimum current capacity of 2 A**.
