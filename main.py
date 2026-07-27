import re
import subprocess
import tomllib
import gi
gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Gdk


class Mixer(Gtk.Application):
    window = None
    
    config = {}

    master_slider = None
    stream_slider = None

    in_sliders = []
    out_sliders = []

    def __init__(self):
        super().__init__(
            application_id="com.lenskowp.NiceMixer"
        )


    def do_activate(self):        
        # LOAD THEME
        self.apply_css()


        # LOAD CONFIG
        with open("config.toml", "rb") as f:
            self.config = tomllib.load(f)


        # CREATE APP WINDOW
        self.window = Gtk.ApplicationWindow(
            application=self,
            title="Nice Mixer"
        )
        self.window.set_default_size(700, 400)
        self.window.set_resizable(True)


        ## CREATE MAIN CONTAINER
        box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10
        )
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)
        box.set_vexpand(True)
        box.set_hexpand(True)

        box.add_css_class("main")


        ## CREATE SLIDER GROUPS
        
        # Mix
        master_node = self.config["devices"]["master_node"]
        stream_node = self.config["devices"]["stream_node"]

        mix_sliders = [master_node, stream_node]

        mix_slider_group = self.create_slider_group(box, "Mix", mix_sliders)

        box.append(mix_slider_group)

        # Outputs
        
        out_sliders = self.config["devices"]["out_nodes"]

        out_slider_group = self.create_slider_group(box, "Outputs", out_sliders)

        box.append(out_slider_group)

        # Inputs

        in_sliders = self.config["devices"]["in_nodes"]

        in_slider_group = self.create_slider_group(box, "Inputs", in_sliders)

        box.append(in_slider_group)
        
        self.window.set_child(box)
        self.window.present()


    def apply_css(self):
        # 1. Create a CSS Provider
        provider = Gtk.CssProvider()

        with open("themes/dark.css", "r") as f:
            css = f.read()
        
        provider.load_from_data(css)

        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(
            display,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


    def create_slider_group(self, box, name, data) -> Gtk.Box:
        # Create container
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        # Can we do the above in CSS?
        box.add_css_class("slider_group")

        # Create Label
        label = Gtk.Label(label=name)
        label.add_css_class("slider_group")

        box.append(label)
        
        # Create slider container
        slider_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10
        )
        slider_box.set_margin_top(5)
        slider_box.set_margin_bottom(5)
        slider_box.set_margin_start(5)
        slider_box.set_margin_end(5)
        # Can we do the above in CSS?
        slider_box.add_css_class("slider_group")

        # Create sliders
        for entry in data:
            slider = self.create_slider(box, entry["name"], entry["nice_name"])
            
            slider_box.append(slider)

        box.append(slider_box)

        return box
    

    def create_slider(self, box, name, nice_name) -> Gtk.Box:
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        box.set_vexpand(True)

        box.add_css_class("slider")

        slider = Slider(box, name, nice_name)

        match name:
            case "Master":
                self.master_slider = slider
            case "Stream":
                self.stream_slider = slider
            case "Mic":
                self.in_sliders.append(slider)
            case _:
                self.out_sliders.append(slider)


        box.append(slider.visual_slider)

        label = Gtk.Label(label=nice_name)
        label.add_css_class("slider")

        box.append(label)

        return box
        
class Slider():
    name = ""
    node_name = ""
    node_id = ""

    volume_value = 0        # 0 - 100
    monitor_value = 0.0     # 0 - 100
    
    visual_slider = None
    visual_level = None

    def __init__(self, box, name, nice_name):
        self.name = nice_name
        self.node_name = name

        id = self._get_node_id(self.node_name)

        if id == "":
            exit()

        self.node_id = id
        
        self.visual_slider = Gtk.Scale.new_with_range(
                Gtk.Orientation.VERTICAL,
                0,
                100,
                1
            )
        self.visual_slider.set_draw_value(True)
        self.visual_slider.set_format_value_func(None, "%")
        self.visual_slider.set_value_pos(Gtk.PositionType.BOTTOM)

        self.visual_slider.set_vexpand(True)
        self.visual_slider.set_hexpand(True)

        self.visual_slider.set_inverted(True)

        self.visual_slider.set_margin_top(20)
        self.visual_slider.set_margin_bottom(20)

        self.visual_slider.add_css_class("slider")

        new_value = self.get_system_volume() * 100

        if (new_value >= 0):
            self.visual_slider.set_value(new_value)
        
        print("Setting slider " + self.node_id + ":'" + self.name + "' to " + str(new_value) + " volume.")

        self._connect_signals()
        

    def _connect_signals(self):
        self.visual_slider.connect("value-changed", self.set_volume)

    def _get_node_id(self, name) -> str:
        result= subprocess.run(
            ["wpctl", "status", "-n"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return ""

        pattern = rf"(?:.*?)\s*\*?\s*(\d+)\.\s*{re.escape(name)}"

        match = re.search(pattern, result.stdout)

        
        if match:
            print("Found " + match.group(1))
            return match.group(1)
        else:
            print("Failed to find node: " + name)
            return ""
    
    def set_volume(self, slider):
        value = slider.get_value()

        if (self.volume_value == value):
            return
        
        self.volume_value = value

        self.set_system_volume(value / 100)

    def set_system_volume(self, value):
        subprocess.run([
            "wpctl",
            "set-volume",
            str(self.node_id),
            str(value)
        ])
    
    def get_system_volume(self) -> float:
        result = subprocess.run(
            ["wpctl", "get-volume", str(self.node_id)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return -1.0

        parts = result.stdout.split()

        if len(parts) < 2:
            return -1.0

        try:
            return float(parts[1])
        except ValueError:
            return -1.0

    def volume_changed(self, slider, node_id):
        volume = slider.get_value() / 100


app = Mixer()
app.run()
