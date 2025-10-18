# --------------------------------- #
#  Back-end REST API Configuration  #
# --------------------------------- #

# Singlton JSON_filewriter instances


# Logger configuration
import logging
logging.basicConfig(
    level=logging.DEBUG,
    filename='back_end/back_end.log',
    filemode='a',
    format="[%(asctime)s] - %(filename)s - %(levelname)s:\t%(message)s"
)
LOGGER = logging.getLogger("back_end_REST_API")

