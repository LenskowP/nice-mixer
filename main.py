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
        master_bus = self.config["devices"]["master_bus"]
        stream_bus = self.config["devices"]["stream_bus"]

        mix_sliders = [master_bus, stream_bus]

        mix_slider_group = self.create_slider_group(box, "Mix", mix_sliders)

        box.append(mix_slider_group)

        # Outputs
        
        out_sliders = self.config["devices"]["out_buses"]

        out_slider_group = self.create_slider_group(box, "Outputs", out_sliders)

        box.append(out_slider_group)

        # Inputs

        in_sliders = self.config["devices"]["in_buses"]

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
            slider = self.create_slider(box, entry["name"], entry["node_id"])
            
            slider_box.append(slider)

        box.append(slider_box)

        return box
    

    def create_slider(self, box, name, node_id) -> Gtk.Box:
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

        slider = Slider(box, name, node_id)

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

        label = Gtk.Label(label=name)
        label.add_css_class("slider")

        box.append(label)

        return box
        
class Slider():
    name = ""
    node_id = ""

    volume_value = 0
    monitor_value = 0.0
    
    visual_slider = None
    visual_level = None

    def __init__(self, box, name, node_id):
        self.name = name
        self.node_id = node_id
        
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

        self._connect_signals()
        

    def _connect_signals(self):
        #self.visual_slider.value-changed.connect(self.set_volume)
        pass

    
    def set_volume(self, value):
        if (self.volume_value == value):
            return
        
        self.volume_value = value * 100

        self.apply_volume_change()

    def apply_volume_change(self):
        subprocess.run([
            "wpctl",
            "set-volume",
            str(self.node_id),
            str(self.volume_value / 100)
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
