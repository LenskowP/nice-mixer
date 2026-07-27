# Nice Mixer

![Mixer Image](https://github.com/LenskowP/nice-mixer/blob/master/preview/mixer-1.png)


A lightweight mixer for managing **PipeWire virtual audio buses** on Linux.

Nice Mixer provides a simple interface for controlling the volume and mute state of permanent PipeWire virtual sinks. Rather than acting as another routing engine, it serves as a control surface for an existing PipeWire routing setup.

Functionality may be extended in the future to include the creation, deletion and linking of virtual audio sources.

## Features

- Simple GTK4 interface
- Per-bus volume control
- Designed for permanent PipeWire virtual sinks
- Lightweight backend using `wpctl`
- Basic customization using CSS

## Planned Features

- Mute controls
- Output device switching
- Per-application routing
- Persistent application routing profiles
- Persistent volume profiles
- Stream and monitor presets
- Peak/VU meters
- Keyboard shortcuts
- System tray support
- MIDI controller support
- Native PipeWire API backend (replacing `wpctl`)

## Why?

I require a simple application that focuses on controlling a set of virtual audio buses.

## Requirements

- Linux
- PipeWire
- WirePlumber
- Python 3.12+
- GTK4

## Installation

1. Clone the repository:

```bash
git clone https://github.com/LenskowP/nice-mixer.git
cd nice-mixer
```

2. Install the required packages (Ubuntu / Linux Mint):

```bash
sudo apt install python3-gi libwireplumber-0.5-dev gir1.2-gtk-4.0
```

3. Ensure PipeWire and WirePlumber are installed and running.


4. Configure devices in config.toml:

The name property of each node should be set to the `node.name` of the target sink. The nice_name property is the title that is displayed beneath the mixer/slider.

Example ("my_sink" is `node.id` and "Huge Sink" is my chosen mixer display name):

```toml
[devices]
master_node = { name = "my_sink", nice_name = "Huge Sink" }
```

## Running

```bash
python3 main.py
```

## Customization

CSS theme files are stored under the `themes` directory. In the config.toml file, change `theme` under the customization header, to your theme's file name without the extension.

e.g. Default theme is 'dark.css' which is set in the config.toml as `dark`.

Customization is limited to Gtk elements for now until I add the class names to the objects.

## Roadmap

- [x] Basic GTK4 interface
- [X] Volume sliders
- [X] Configuration file support
- [X] Volume control
- [ ] Native PipeWire API integration
- [ ] Mute controls
- [ ] Automatic bus discovery
- [ ] Output device switching
- [ ] Per-application routing
- [ ] Persistent application routing
- [ ] Profiles and presets
- [ ] VU meters


## Development
Will fill out once I figure out how to make a release for this and replace the Installation section.

## Contributing

Contributions, feature requests, and bug reports are welcome. If you have ideas for improving Nice Mixer, feel free to open an issue or submit a pull request.

## License

This project is licensed under the GNU General Public License.
