# Wavin AHC9000 — Quick Start

Your module is already flashed. You only need to connect it to Wi-Fi and add it
to Home Assistant.

<a href="https://github.com/nic6911/ha-Wavin-AHC9000-Zones"><img src="docs/integration-repo-qr.png" width="170" alt="QR code for the Wavin AHC9000 Zones integration"></a>

**You need**

- A 2.4 GHz Wi-Fi network
- Home Assistant 2026.11 or newer with the built-in **Marketplace**
- The AHC controller powered on
- The RS-485 cable connected to the module

> ESP32 does not support 5 GHz Wi-Fi. If your router has separate 2.4 GHz and
> 5 GHz names, use the 2.4 GHz one.

---

## 1. Power the module

Connect the module to the AHC controller and power it on.

Wait **1–2 minutes**. The module will try to connect to Wi-Fi. If it cannot,
it creates a setup hotspot.

## 2. Connect to the setup hotspot

On your phone or laptop, open the Wi-Fi list and connect to:

```text
Wavin Fallback Hotspot
```

No password is needed.

If a setup page does not open automatically, open:

```text
http://192.168.4.1
```

Enter your home Wi-Fi name and password, then save.

The module restarts and joins your Wi-Fi. This can take a minute.

## 3. Add the integration in Home Assistant

1. Go to **Settings → Marketplace**.
2. Select **Add from link**.
3. Enter this repository:

   ```text
   https://github.com/nic6911/ha-Wavin-AHC9000-Zones
   ```

4. If Marketplace asks for a type, choose **Integration**.
5. Open **Wavin AHC9000 Zones** and select **Install**.
6. If Home Assistant asks to restart, restart it.
7. Home Assistant normally finds the module automatically. Select
   **Configure** on the discovered **Wavin AHC9000** card.
8. Confirm the device. You do not need to enter an address.

If no discovery card appears, use **Add integration** → **Wavin AHC9000
Zones** and enter the module address from the label, for example
`wavin-ahc9000.local`, or its IP address from your router. Leave the Noise key
empty.

## 4. Check that the zones appear

You should now see devices named like:

```text
Zone (1+2)
Zone (16)
```

Each zone has a thermostat, temperature, floor temperature, battery, and child
lock.

Open a thermostat and try changing the temperature. The wall thermostat should
follow.

---

## Optional: sync all zones

Open the Wavin device and turn on:

```text
Sync all zones to zone (x)
```

All zones then follow the first active zone's setpoint. Turn it off to make the
zones independent again.

## If something does not work

| Problem | Try |
|---|---|
| The setup hotspot is not visible | Wait another minute, then power-cycle the module |
| The setup page does not open | Open `http://192.168.4.1` manually |
| Cannot connect in Home Assistant | Try the module's IP address instead of `.local` |
| No zones appear | Check the RS-485 A/B wiring and that the AHC is powered |
| Zones appear but do not control | Update the module firmware and the integration together |

Need help? Open an issue:

```text
https://github.com/nic6911/ha-Wavin-AHC9000-Zones/issues
```
