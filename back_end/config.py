# --------------------------------- #
#  Back-end REST API Configuration  #
# --------------------------------- #

# Singleton JSON_filewriter instances
from pathlib import Path

from back_end.JSON_statefiles.filewriter_menu import Filewriter_menu
from back_end.JSON_statefiles.filewriter_orders import Filewriter_orders
from back_end.JSON_backup.filewriter_finished_orders import Filewriter_finished_orders
from back_end.JSON_statefiles.sequence_manager import Sequence_manager

FILEMANAGER_ORDERS: Filewriter_orders = Filewriter_orders(Path.cwd() / "back_end" / "JSON_statefiles" / "orders.json")
FILEMANAGER_MENU: Filewriter_menu = Filewriter_menu(Path.cwd() / "back_end" / "JSON_statefiles" / "menu.json")
FILEMANAGER_FINISHED_ORDERS: Filewriter_finished_orders = Filewriter_finished_orders(Path.cwd() / "back_end" / "JSON_backup" / "finished_orders.json")
FILEMANAGER_SEQUENCE: Sequence_manager = Sequence_manager(Path.cwd() / "back_end" / "JSON_statefiles" / "metadata.json")

# Logger configuration
import logging
logging.basicConfig(
    level=logging.DEBUG,
    filename='back_end/back_end.log',
    filemode='a',
    format="[%(asctime)s] - %(filename)s - %(levelname)s:\t%(message)s"
)
LOGGER = logging.getLogger("back_end_REST_API")

# Global variable to store the current mode (development or production)
MODE: str = None