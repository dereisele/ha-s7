# Siemens Simatic S7 Component for Home Assistant

This is a **work in progress** Home Assistant integration for light and roller shutter.
The S7 is programmed to reflect the state for each light in a bool in **DB10**.
Then there is a separate bool at address to turn it on and another one to turn it off.

The roller shutter have no state bit, but two command bits to open and close it.

This addon uses [python-snap7](https://github.com/gijzelaerr/python-snap7) to communicate with the S7 PLC

## Example Config

```yaml
light:
  - platform: simatic
    host: 192.168.50.9
    lib: /config/custom_components/simatic/libsnap7.so
    devices:
      - name: "Lampen Buero OG 1"
        state_address:
          byte: 4
          bit: 6
      - name: "Lampen Buero OG 2"
        state_address:
          byte: 4
          bit: 7
```

## Disclaimer

This home assistant is integration is unofficial and has to warranty to work properly or at all.
It may cause damages of the PLC, Home Assistant and attached devices at your own risk.
It is not an official or supported product by Home Assistant or Siemens

Simatic and S7 are brands owned by Siemens.
