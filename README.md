# BMW F10 GWS → Arduino Nano → MCP2515 → BeamNG.drive

## 🇨🇿 ČESKY

Tento projekt umožňuje připojit řadicí páku BMW F10 GWS k počítači pomocí Arduino Nano a MCP2515 a používat ji v BeamNG.drive jako klasické ovládání klávesnicí. Projekt čte komunikaci z BMW GWS přes CAN-BUS, rozpoznává polohu páky P, R, N, D, M/S, M+ a M− a následně přes Python převádí tyto příkazy na klávesy ve Windows. Není potřeba žádný joystick emulator.

Po stažení projektu z GitHubu jako ZIP je nutné ZIP soubor nejdříve úplně rozbalit do normální složky v počítači. Arduino soubor `BMW_F10_GWS.ino` neotevírej přímo ze ZIP archivu. Po rozbalení otevři složku projektu, potom složku `Arduino` a otevři soubor `BMW_F10_GWS.ino` v Arduino IDE. Pokud se Arduino IDE zeptá, zda chceš otevřít nebo vytvořit sketch ve stejnojmenné složce, potvrď **OK**.

Pro projekt lze použít běžné Arduino Nano, včetně kompatibilních kopií a klonů. Arduino Nano je připojeno k počítači pouze přes USB a je napájeno z USB. BMW GWS musí mít vlastní samostatné napájení 12 V s minimálním proudem 2 A. Napájení 12 V se rozdělí na pin 1 GWS (+12 V) a pin 2 GWS (+12 V Wake-up). GND ze zdroje se rozdělí na pin 5 GWS a GND Arduina. GND MCP2515 musí být také propojeno s GND Arduina. GWS a Arduino mohou mít oddělené napájecí zdroje, ale musí mít společnou zem. Napětí 12 V z GWS nikdy nepřipojuj na 5V nebo VIN Arduina.

Konektor BMW F10 GWS je při pohledu shora, když je řadicí páka před tebou, zapojen zleva doprava takto: pin 1 = +12 V, pin 2 = +12 V Wake-up, pin 3 = CAN-L, pin 4 = CAN-H a pin 5 = GND.

MCP2515 se připojuje k Arduino Nano přes SPI. D13 je SCK, D12 je SO/MISO, D11 je SI/MOSI, D10 je CS a D2 je INT. VCC MCP2515 připoj na 5 V Arduina a GND MCP2515 na GND Arduina. Na MCP2515 musí být zapojený také jumper J1.

BMW GWS používá CAN-BUS rychlost 500 kbps. MCP2515 modul může mít krystal 8 MHz nebo 16 MHz. Pokud máš 8MHz MCP2515, ponech v Arduino kódu `MCP_8MHZ`. Pokud máš 16MHz MCP2515, změň v řádku `CAN0.begin(...)` hodnotu `MCP_8MHZ` na `MCP_16MHZ`. Příklad pro 8 MHz je `CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ)`.

V Arduino IDE otevři soubor `Arduino/BMW_F10_GWS.ino`, vyber správnou desku Arduino Nano a správný COM port. U některých Arduino Nano klonů je potřeba v nastavení procesoru vybrat `ATmega328P (Old Bootloader)`. Potom nahraj program do Arduina.

Po nahrání programu připoj Arduino Nano přes USB k počítači. COM port zjistíš ve Správci zařízení Windows v části Porty (COM a LPT). V souboru `beamng_gws.py` potom uprav řádek `PORT = "COM7"` podle svého COM portu, například `PORT = "COM8"`.

Pro Python je potřeba mít nainstalovaný Python. Závislosti projektu jsou uvedené v souboru `requirements.txt`. Ve složce projektu spusť příkaz `py -m pip install -r requirements.txt`. Pokud příkaz `py` nefunguje, můžeš použít `python -m pip install -r requirements.txt`.

Po instalaci můžeš spustit `beamng_gws.py` dvojklikem. Program se připojí k Arduinu přes nastavený COM port a bude čekat na příkazy z BMW GWS. Před použitím v BeamNG.drive doporučujeme program otestovat například v Poznámkovém bloku. Pokud při pohybu řadicí páky program vypisuje příkazy a v Poznámkovém bloku se zadávají správné klávesy, komunikace funguje.

Mapování ovládání je následující: P posílá klávesu T, R posílá O, N posílá N, D posílá Y, M/S posílá U, M+ posílá X a M− posílá Z.

Projekt používá CAN ID `0x197` pro informace o poloze řadicí páky a CAN ID `0x3FD` pro komunikaci displeje GWS. Hodnoty poloh páky jsou R = `0x2F`, N = `0x1F` nebo `0x3F`, D = `0x4F`, M/S střed = `0x7F`, M− = `0x5F`, M+ = `0x6F`, P stisknuto = `0xD5` a P uvolněno = `0xC0`. Displej používá P = `0x20`, R = `0x40`, N = `0x60` a D = `0x81`. CRC používá polynom `0x1D`, počáteční hodnotu `0x00` a XOR `0x70`.

Ve Windows se používá Python knihovna `keyboard` pro odesílání kláves. Program proto nepotřebuje joystick emulator ani další virtuální ovladač. BeamNG.drive potom používá běžné klávesové ovládání.

Pokud používáš BeamNG.drive přes NVIDIA GeForce NOW, může být problém s předáváním kláves generovaných programem Python do streamované hry. Proto je vhodné nejdříve otestovat celý systém v běžné aplikaci Windows, například v Poznámkovém bloku. Pokud klávesy fungují v Poznámkovém bloku, ale nefungují v BeamNG.drive přes GeForce NOW, problém pravděpodobně nesouvisí s Arduino GWS převodníkem.

Struktura projektu je `Arduino/BMW_F10_GWS.ino`, `beamng_gws.py`, `requirements.txt`, `INSTALL.md` a `README.md`.

Projekt je určen pro BMW F10 GWS, Arduino Nano, MCP2515 a BeamNG.drive. Použití je na vlastní odpovědnost a při zapojování BMW GWS je nutné dodržet správné napájení a zapojení CAN-BUS.

## 🇬🇧 ENGLISH

This project allows you to connect a BMW F10 GWS gear selector to a PC using an Arduino Nano and MCP2515 and use it in BeamNG.drive as normal keyboard control. The project reads communication from the BMW GWS over CAN-BUS, detects the P, R, N, D, M/S, M+ and M− positions and then uses Python to convert these commands into keyboard inputs in Windows. No joystick emulator is required.

After downloading the project from GitHub as a ZIP file, you must completely extract the ZIP archive into a normal folder on your computer first. Do not open the `BMW_F10_GWS.ino` file directly from inside the ZIP archive. After extracting the project, open the project folder, then open the `Arduino` folder and open `BMW_F10_GWS.ino` in Arduino IDE. If Arduino IDE asks whether you want to open or create the sketch in the same-named folder, click **OK**.

You can use a normal Arduino Nano, including compatible copies and clones. The Arduino Nano is connected to the computer only through USB and is powered from USB. The BMW GWS must have its own separate 12 V power supply with a minimum current of 2 A. The 12 V supply is split between GWS pin 1 (+12 V) and GWS pin 2 (+12 V Wake-up). The power supply GND is split between GWS pin 5 and Arduino GND. MCP2515 GND must also be connected to Arduino GND. The GWS and Arduino can use separate power supplies, but they must share a common ground. Never connect the GWS 12 V supply to the Arduino 5V or VIN pin.

When looking at the BMW F10 GWS connector from above with the shifter in front of you, the pins are arranged from left to right as follows: pin 1 = +12 V, pin 2 = +12 V Wake-up, pin 3 = CAN-L, pin 4 = CAN-H and pin 5 = GND.

The MCP2515 is connected to the Arduino Nano using SPI. D13 is SCK, D12 is SO/MISO, D11 is SI/MOSI, D10 is CS and D2 is INT. Connect MCP2515 VCC to Arduino 5 V and MCP2515 GND to Arduino GND. The J1 jumper on the MCP2515 must also be installed.

The BMW GWS uses a CAN-BUS speed of 500 kbps. The MCP2515 module can have either an 8 MHz or 16 MHz crystal. If you have an 8 MHz MCP2515, keep `MCP_8MHZ` in the Arduino code. If you have a 16 MHz MCP2515, change `MCP_8MHZ` to `MCP_16MHZ` in the `CAN0.begin(...)` line. For 8 MHz the line is `CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ)`.

Open `Arduino/BMW_F10_GWS.ino` in Arduino IDE, select the correct Arduino Nano board and the correct COM port. Some Arduino Nano clones require `ATmega328P (Old Bootloader)` to be selected under the processor settings. Then upload the program to the Arduino.

After uploading the program, connect the Arduino Nano to the computer using USB. You can find the COM port in Windows Device Manager under Ports (COM & LPT). In `beamng_gws.py`, change the line `PORT = "COM7"` to match your COM port, for example `PORT = "COM8"`.

Python must be installed on the computer. The project dependencies are listed in `requirements.txt`. Open a terminal in the project folder and run `py -m pip install -r requirements.txt`. If the `py` command does not work, use `python -m pip install -r requirements.txt`.

After installation, you can start `beamng_gws.py` by double-clicking it. The program will connect to the Arduino through the configured COM port and wait for commands from the BMW GWS. Before using it in BeamNG.drive, it is recommended to test the system in a normal Windows application such as Notepad. If the program prints the commands and the correct keyboard keys appear in Notepad when moving the shifter, the communication is working.

The keyboard mapping is as follows: P sends T, R sends O, N sends N, D sends Y, M/S sends U, M+ sends X and M− sends Z.

The project uses CAN ID `0x197` for gear selector position information and CAN ID `0x3FD` for GWS display communication. The selector values are R = `0x2F`, N = `0x1F` or `0x3F`, D = `0x4F`, M/S center = `0x7F`, M− = `0x5F`, M+ = `0x6F`, P pressed = `0xD5` and P released = `0xC0`. The display uses P = `0x20`, R = `0x40`, N = `0x60` and D = `0x81`. The CRC uses polynomial `0x1D`, initial value `0x00` and XOR `0x70`.

Windows uses the Python `keyboard` library to send keyboard inputs. Therefore, no joystick emulator or additional virtual controller is required. BeamNG.drive can then use the normal keyboard controls.

If you are using BeamNG.drive through NVIDIA GeForce NOW, there may be an issue with passing keyboard inputs generated by the Python program into the streamed game. It is therefore recommended to test the complete system in a normal Windows application such as Notepad first. If the keyboard inputs work in Notepad but do not work in BeamNG.drive through GeForce NOW, the problem is likely related to GeForce NOW rather than the Arduino GWS converter.

The project structure is `Arduino/BMW_F10_GWS.ino`, `beamng_gws.py`, `requirements.txt`, `INSTALL.md` and `README.md`.

This project is designed for the BMW F10 GWS, Arduino Nano, MCP2515 and BeamNG.drive. Use it at your own risk and always make sure the BMW GWS power supply and CAN-BUS wiring are connected correctly.
