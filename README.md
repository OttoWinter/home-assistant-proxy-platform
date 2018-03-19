# Home Assistant Proxy Platform

This custom platform currently allows any switch-like entity to be converted to a light.

With this configuration entry:

```yaml
# Example configuration.yaml entry
light:
  - platform: proxy
    name: Kitchen Lights
    entity_id: switch.kitchen_lights_as_switch
```

you can for example proxy the `switch.kitchen_lights_as_switch` to be `light.kitchen_lights`.

### Configuration variables:

- **name**: *(Optional)* The name of the new light.
- **entity_id**: *(Optional)* The entity id of the switch that should be copied.

### Installation

This is a [custom component](https://home-assistant.io/developers/creating_components/), to install it simply copy the [`proxy.py`](proxy.py) file to `<config_dir>/custom_components/light/proxy.py`.

(If several users want this and I have some time, I might do the same for other entity mappings.)
