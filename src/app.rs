use gtk4 as gtk;
use gtk::prelude::*;
use gtk::{Application, ApplicationWindow};

pub struct App {
    gtk: Application,
}

impl App {
    pub fn new() -> Self {
        let gtk = Application::builder()
        .application_id("space.lenskowp.NiceMixer")
        .build();

        gtk.connect_activate(|app| {
            let window = ApplicationWindow::builder()
                .application(app)
                .default_width(700)
                .default_height(400)
                .title("Nice Mixer")
                .build();

            window.present();
        });

        Self { gtk }
    }

    pub fn run(self) {
        self.gtk.run();
    }
}