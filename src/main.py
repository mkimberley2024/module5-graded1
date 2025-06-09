# main.py
import logging
from db_operations import DBOperations
from db_initialise import initialise_database
from greet import Greet
from menu import Menu
import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("squeezyjet.log"),
        handler  # Use the colorlog handler here
    ]
)

db_filename = "FlightDB.db"

def main():
    initialise_database(db_filename)

    
    greeter = Greet()
    greeter.greet()  

    menu = Menu(db_filename)
    menu.handle_main_menu()
    logging.info("Application started successfully.")    


if __name__ == "__main__":
    main()