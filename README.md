# Wavin AHC9000 Zones

Home Assistant integration for a Wavin AHC 9000 / Jablotron AC-116 heating
controller running the ModBridge `wavinahc9000v4` ESPHome firmware.

It creates one Home Assistant device per heating zone, with a thermostat,
temperature, floor temperature, battery, and child lock. AHC zone changes are
picked up automatically.

[![Open in Marketplace](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=nic6911&repository=ha-Wavin-AHC9000-Zones&category=integration)

<a href="https://github.com/nic6911/ha-Wavin-AHC9000-Zones"><img src="docs/integration-repo-qr.png" width="180" alt="QR code for this integration repository"></a>

---

## ESP32 Modbus Module Rev2

If you use the **ESP32 Modbus Module Rev2** from uStepper, flash the ready-made
AHC9000 automatic-zone configuration instead of building the YAML by hand:

**[ahc9000_v4_auto.yaml](https://github.com/nic6911/ESP32_Modbus_Module/blob/main/esphome_example_code/rev2/ahc9000_v4_auto.yaml)**

It is already configured for the Rev2 board: UART TX `GPIO21`, RX `GPIO20`,
flow control `GPIO3`, and `38400` baud. It also enables automatic zone
discovery and the services required by this integration.

Flash the YAML with ESPHome, then install this integration as described
[below](#2-install-this-integration). The underlying ESPHome component and all
YAML options are documented here:

**[Wavin AHC9000 V4 component setup](https://github.com/nic6911/esphome_components/blob/main/components/wavinahc9000v4/README.md)**

For wiring and the module's RJ45/RS-485 connection, see the
**[ESP32 Modbus Module README](https://github.com/nic6911/ESP32_Modbus_Module#connecting-the-module)**.

---

## Start here

You need two things: the ESP32 firmware and this integration.

### 1. Flash the ESP32

Use the ready-made ESPHome configuration:

**[Wavin AHC9000 V4 quick start](https://github.com/nic6911/esphome_components/blob/main/components/wavinahc9000v4/README.md)**

The short version:

1. Open ESPHome.
2. Create a new device and paste `example_auto.yaml`.
3. Set your Wi-Fi name/password and the correct UART pins for your board.
4. Install it to the ESP32.
5. Wait until the ESPHome device is online.

The firmware automatically finds the AHC zones. You do not need to edit one
climate entity per channel.

### 2. Install this integration

1. Go to **Settings → Marketplace**.
2. Select **Add from link**.
3. Enter this repository:

   `https://github.com/nic6911/ha-Wavin-AHC9000-Zones`

4. If Marketplace asks for a type, choose **Integration**.
5. Open **Wavin AHC9000 Zones** and select **Install**.
6. If Home Assistant asks to restart, restart it.

If the Marketplace link above works for you, it can do steps 1–5.

### 3. Add the device in Home Assistant

Home Assistant normally finds the module automatically after it is online.

1. Wait for a discovered **Wavin AHC9000** card, then select **Configure**.
2. Confirm the device. You do not need to enter an IP address.
3. If discovery does not appear, go to **Settings → Devices & services →
   Add integration**, search for **Wavin AHC9000 Zones**, and enter the ESP32
   address as a fallback. Leave the Noise key empty unless you enabled ESPHome
   API encryption.

The zones appear as devices named like `Zone (1+2)` or `Zone (16)`.

That is it. No MQTT broker is needed.

---

## What you get

- One Home Assistant device per zone
- Climate entity with heat/off and setpoint control
- Current temperature, floor temperature, and battery sensors
- Child lock switch
- ESP32 Wi-Fi RSSI sensor
- Optional **Sync all zones to zone (x)** switch

Zone setpoints follow the physical wall thermostat. The ESP32 only writes a
setpoint when you change it from Home Assistant.

## Sync all zones

The sync switch copies the first available zone's setpoint to every other zone
and keeps them together while enabled. Turn it off to make zones independent
again.

If you rename the master zone device in Home Assistant, the sync switch text
follows that name.

## Troubleshooting

| Problem | Try |
|---|---|
| Cannot connect | Check the ESP32 IP address and that port `6053` is reachable |
| No zones appear | Confirm the firmware uses `auto_zones: true` and has the `topology` text sensor |
| Zones appear but controls fail | Update the firmware and integration together |
| Device is offline | Check Wi-Fi, ESPHome logs, and the RSSI sensor |
| Old zones remain | Reload the integration or restart Home Assistant |

## Compatibility

- Home Assistant 2026.11 or newer
- `wavinahc9000v4` firmware with topology JSON version `1`
- ESPHome native API on TCP port `6053`

## Manual installation

Copy `custom_components/wavin_ahc9000` into your Home Assistant
`custom_components` directory, restart Home Assistant, and add the integration.

## Advanced firmware options

For manual per-channel YAML, external room sensors, floor-probe climates, and
other advanced options, see the firmware repository:

**[wavinahc9000v4 documentation](https://github.com/nic6911/esphome_components/tree/main/components/wavinahc9000v4)**
