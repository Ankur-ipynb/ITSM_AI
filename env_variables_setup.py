import logging
import os
import sys
from requests.auth import HTTPBasicAuth


def initialize_spark():
    logging.info("Python executable: " + sys.executable)
    logging.info("sys.path: " + str(sys.path))

    os.environ['SPARK_HOME'] = 'D:/spark'
    os.environ['HADOOP_HOME'] = 'D:/hadoop'
    os.environ['JAVA_HOME'] = 'D:/java'
    os.environ['PATH'] = os.environ['PATH'] + ';' + 'D:/hadoop/bin'
    logging.info("Environment variables set.")

    winutils_path = 'D:/hadoop/bin/winutils.exe'
    if not os.path.exists(winutils_path):
        logging.error("winutils.exe not found at " + winutils_path)
        raise FileNotFoundError("winutils.exe not found at " + winutils_path)
    logging.info(f"winutils.exe found at {winutils_path}.")


def get_servicenow_auth():
    return HTTPBasicAuth("admin", "X-Xi4Rg9Wnj*")
