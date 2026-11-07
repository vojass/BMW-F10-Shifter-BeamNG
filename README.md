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

Pokud používáš BeamNG.drive přes NVIDIA GeForce NOW, může být problém s předáváním kláves generovaných programem Python do streamované hry. Proto je vhodné nejdříve otestovat celý systém v běžné aplikaci Windows, například v Poznámkovém bloku. Pokud klávesy fungují v Poznámkovém bloku, ale nefungují v BeamNG.drive přes GeForce
