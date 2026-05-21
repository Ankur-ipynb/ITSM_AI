import logging
import os
import sys
from requests.auth import HTTPBasicAuth


def initialize_spark():
    logging.info("Python executable: " + sys.executable)
    logging.info("sys.path: " + str(sys.path))

    os.environ['SPARK_HOME'] = '<YOUR SPARK PATH>'
    os.environ['HADOOP_HOME'] = '<YOUR HADOOP PATH>'
    os.environ['JAVA_HOME'] = '<YOUR JAVA PATH>'
    os.environ['PATH'] = os.environ['PATH'] + ';' + '<YOUR HADOOP BIN PATH>'
    logging.info("Environment variables set.")

    winutils_path = 'D:/hadoop/bin/winutils.exe'
    if not os.path.exists(winutils_path):
        logging.error("winutils.exe not found at " + winutils_path)
        raise FileNotFoundError("winutils.exe not found at " + winutils_path)
    logging.info(f"winutils.exe found at {winutils_path}.")


def get_servicenow_auth():
    return HTTPBasicAuth("admin", "<YOUR SERVICE-NOW PDI PASSWORD>")
