# BMW F10 GWS → Arduino Nano → MCP2515 → BeamNG.drive

## 🇨🇿 ČESKY

### 1. Co je potřeba

Pro použití projektu potřebuješ Arduino Nano, MCP2515 CAN modul, BMW F10 GWS řadičku, 12V zdroj pro GWS s proudovou kapacitou minimálně 2 A, USB kabel pro Arduino a počítač s Windows.

Arduino Nano je napájené pouze z USB. BMW GWS musí mít vlastní 12V zdroj.

### 2. Stažení projektu

Na GitHubu klikni na **Code → Download ZIP** a stáhni celý projekt do počítače.

ZIP rozbal například na plochu. Ve složce projektu by měl být soubor `beamng_gws.py`, složka `Arduino`, soubor `requirements.txt` a další soubory projektu.

### 3. Instalace Pythonu

Pokud ještě nemáš Python, stáhni a nainstaluj Python z oficiálních stránek Pythonu.

Během instalace je důležité zaškrtnout možnost **Add Python.exe to PATH**.

Po dokončení instalace můžeš pokračovat dalším krokem.

### 4. Instalace potřebných knihoven

Ve složce projektu se nachází soubor `requirements.txt`. Ten obsahuje knihovny potřebné pro Python převodník.

Otevři složku projektu v Průzkumníku Windows. Klikni do adresního řádku nahoře, napiš `cmd` a stiskni Enter.

Do otevřeného okna napiš:

```text
py -m pip install -r requirements.txt
```

Pokud příkaz `py` nefunguje, použij:

```text
python -m pip install -r requirements.txt
```

Po dokončení instalace jsou potřebné knihovny nainstalované.

### 5. Zapojení BMW GWS

BMW GWS musí být napájena **samostatným 12V zdrojem s proudovou kapacitou minimálně 2 A**.

Při pohledu na konektor GWS shora, když je řadička před tebou, jsou piny zleva doprava:

```text
Pin 1 = +12 V
Pin 2 = +12 V Wake-up
Pin 3 = CAN-L
Pin 4 = CAN-H
Pin 5 = GND
```

+12 V ze zdroje se rozdělí na dvě větve. Jedna vede na pin 1 GWS a druhá na pin 2 GWS.

GND ze zdroje se rozdělí na dvě větve. Jedna vede na pin 5 GWS a druhá na libovolný GND pin Arduina.

Arduino Nano je napájené pouze přes USB.

**12 V ze zdroje GWS nikdy nepřipojuj na 5 V nebo VIN Arduina.**

GWS a Arduino mohou mít oddělené napájení. Musí však mít společnou GND.

### 6. Zapojení MCP2515

MCP2515 připoj k Arduinu následovně:

```text
Arduino Nano    MCP2515

D13             SCK
D12             SO / MISO
D11             SI / MOSI
D10             CS
D2              INT
5V              VCC
GND             GND
```

CAN-H z MCP2515 připoj na CAN-H GWS.

CAN-L z MCP2515 připoj na CAN-L GWS.

Na MCP2515 musí být v tomto zapojení nasazený/propojený jumper **J1**.

### 7. Nastavení 8MHz / 16MHz MCP2515

MCP2515 může mít 8MHz nebo 16MHz krystal.

Pokud máš **8MHz MCP2515**, v Arduino programu nech:

```cpp
MCP_8MHZ
```

Pokud máš **16MHz MCP2515**, změň:

```cpp
MCP_8MHZ
```

na:

```cpp
MCP_16MHZ
```

v řádku `CAN0.begin(...)`.

Projekt používá CAN rychlost **500 kbit/s**.

### 8. Nahrání programu do Arduina

Otevři Arduino IDE a načti soubor:

```text
Arduino/BMW_F10_GWS.ino
```

Vyber správnou desku Arduino Nano a COM port.

U některých Arduino Nano klonů může být potřeba vybrat:

```text
ATmega328P (Old Bootloader)
```

Pokud běžný `ATmega328P` funguje, není potřeba Old Bootloader používat.

Nahraj program do Arduina.

Po úspěšném nahrání můžeš Arduino připojit k zapojenému MCP2515 a GWS.

### 9. Nastavení COM portu

Připoj Arduino Nano k počítači přes USB.

Otevři **Správce zařízení → Porty (COM a LPT)**.

Najdi Arduino a zjisti jeho COM port.

Například:

```text
COM7
```

Otevři soubor:

```text
beamng_gws.py
```

Najdi řádek:

```python
PORT = "COM7"
```

Pokud má Arduino například COM8, změň ho na:

```python
PORT = "COM8"
```

### 10. Spuštění převodníku

Po instalaci Pythonu a knihoven není potřeba pokaždé používat CMD.

Stačí ve složce projektu **dvakrát kliknout na `beamng_gws.py`**.

Spustí se Python převodník mezi BMW GWS a klávesnicí
