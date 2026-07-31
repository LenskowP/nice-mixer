mod app;
use crate::app::App;

mod audio;
mod ui;

fn main() -> anyhow::Result<()> {
    env_logger::init();

    let app = App::new();

    app.run();

    Ok(())
}
