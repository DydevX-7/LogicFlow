
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PIL import Image

from ui.branding import create_logo_pixmap


def main():
    app = QApplication([])

    output_directory = Path("assets/icons")
    output_directory.mkdir(parents=True, exist_ok=True)

    png_path = output_directory / "logicflow.png"
    ico_path = output_directory / "logicflow.ico"

    # Generate the existing LogicFlow logo.
    logo = create_logo_pixmap(256)

    if not logo.save(str(png_path), "PNG"):
        raise RuntimeError("Could not generate LogicFlow PNG icon.")

    # Convert it into a Windows-compatible multi-resolution ICO.
    image = Image.open(png_path).convert("RGBA")

    image.save(
        ico_path,
        format="ICO",
        sizes=[
            (16, 16),
            (24, 24),
            (32, 32),
            (48, 48),
            (64, 64),
            (128, 128),
            (256, 256),
        ],
    )

    print(f"PNG icon created: {png_path}")
    print(f"Windows icon created: {ico_path}")

    app.quit()


if __name__ == "__main__":
    main()
