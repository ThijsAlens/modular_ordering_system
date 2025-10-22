# --------------------------------- #
#  Back-end REST API Configuration  #
# --------------------------------- #

# Singlton JSON_filewriter instances
from back_end.JSON_filewriter.JSON_filewriter import JSON_Filewriter
from pathlib import Path
from back_end.JSON_statefiles.filewriter_orders import Filewriter_orders
from back_end.JSON_statefiles.filewriter_pending_tickets import Filewriter_pending_tickets

FILEWRITERS = {
    "JSON_statefiles/orders.json": Filewriter_orders(Path.cwd() / "back_end" / "JSON_statefiles" / "orders.json"),
    "JSON_statefiles/pending_tickets.json": Filewriter_pending_tickets(Path.cwd() / "back_end" / "JSON_statefiles" / "pending_tickets.json"),
    "JSON_backup/finished_orders.json": JSON_Filewriter(Path.cwd() / "back_end" / "JSON_backup" / "finished_orders.json"),
}

# Logger configuration
import logging
logging.basicConfig(
    level=logging.DEBUG,
    filename='back_end/back_end.log',
    filemode='a',
    format="[%(asctime)s] - %(filename)s - %(levelname)s:\t%(message)s"
)
LOGGER = logging.getLogger("back_end_REST_API")

