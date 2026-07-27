# Nice Mixer

A lightweight mixer for managing **PipeWire virtual audio buses** on Linux.

Nice Mixer provides a simple interface for controlling the volume and mute state of permanent PipeWire virtual sinks. Rather than acting as another routing engine, it serves as a control surface for an existing PipeWire routing setup.

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
- OBS integration
- Native PipeWire API backend (replacing `wpctl`)

## Why?

I require a simple application focused on controlling a set of virtual audio buses.

Nice Mixer aims to fill that gap by providing a clean mixer interface for a predefined PipeWire workflow.

## Requirements

- Linux
- PipeWire
- WirePlumber
- Python 3.12+
- GTK4

## Installation

Clone the repository:

```bash
git clone https://github.com/LenskowP/nice-mixer.git
cd nice-mixer
```

Install the required packages (Ubuntu / Linux Mint):

```bash
sudo apt install python3-gi libwireplumber-0.5-dev gir1.2-gtk-4.0
```

Ensure PipeWire and WirePlumber are installed and running.

## Running

```bash
python3 main.py
```

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


## Contributing

Contributions, feature requests, and bug reports are welcome. If you have ideas for improving Nice Mixer, feel free to open an issue or submit a pull request.

## License

This project is licensed under the GNU General Public License.
