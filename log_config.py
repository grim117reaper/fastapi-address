import logging
import uvicorn

FORMAT = "%(levelname)s:%(message)s"
logging.basicConfig(format=FORMAT, level=logging.ERROR)

FORMAT: str = "%(levelprefix)s %(asctime)s | %(message)s"

# code variant:
def init_loggers(logger_name: str = "Address_logging"):
    # formatter
    formatter = uvicorn.logging.DefaultFormatter(FORMAT)
    formatter = uvicorn.logging.DefaultFormatter(FORMAT, datefmt="%Y-%m-%d %H:%M:%S")