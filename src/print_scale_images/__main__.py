from src.print_scale_images.config import LoggerConfig
from src.print_scale_images.handlers.main_controller import MainController
from src.utils import configure_logger


def main():
    configure_logger(file_name=LoggerConfig.filename, console=LoggerConfig.console)
    app = MainController()
    app.run()


if __name__ == "__main__":
    main()
