# ---------------------------------- #
#  Front-end REST API Configuration  #
# ---------------------------------- #

# Logger configuration
import logging
logging.basicConfig(
    level=logging.DEBUG,
    filename='front_end/front_end.log',
    filemode='a',
    format="[%(asctime)s] - %(filename)s - %(levelname)s:\t%(message)s"
)
LOGGER = logging.getLogger("front_end_REST_API")

USERS: set[str] = set()  # Set to store usernames