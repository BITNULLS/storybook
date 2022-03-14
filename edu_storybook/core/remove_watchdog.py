"""
remove_watchdog.py
    Simple script for managing the removal of temporary files in a separate 
    process.

Functions:
    remove_watchdog(...)
    future_del_temp(...) - The function you use to mark a file for deletion.
"""

import os
import time 
import sys
import logging
from multiprocessing import Process, Queue
from .config import config

# TODO: fix logging from this script.  The problem is that remove_watchdog() is
#       run in a parallel process, meaning that it's logging is not correctly
#       bubbled up.

def remove_watchdog(remove_queue):
    """
    Removes files that are passed into the queue, after a timeout. The format of
    the remove queue is a list of dicts, with each dict containing "expiration"
    and "filepath". It looks like

    [
        {
            "expiration": 129941234,
            "filepath": "temp/somefile.csv"
        },
        ...
    ]

    Where "expiration" is epoch time of file to be deleted.
    """
    logging.debug('Remove Watchdog is now running')
    sys.stdout.flush()
    while True:
        destruct = remove_queue.get(True)  # wait until remove queue is gotten
        for file in destruct:
            if os.path.isfile(file["filepath"]):
                # wait for a file's expiration time to come about
                while True:
                    if int(time.time()) < file["expiration"]:
                        time.sleep(10)
                        continue
                    else:
                        break
                os.remove(file['filepath'])


remove_queue = Queue()
rmwd = Process(target=remove_watchdog, args=(remove_queue,))


def future_del_temp(filepath: str = '', files: list = []) -> None:
    """
    Marks the temporary files that should be removed later by the Remove 
    Watchdog in the future.

    NOTE: Only filepath or files args should be valued, not both (XOR).

    :param filepath: The path to a file that should be removed.
    :param files: A list of files that should be removed.
    :type filepath: str
    :type files: str
    :returns: None.
    """
    assert not (filepath == '' and len(files) ==
                0), 'filepath and files args cannot both be empty'
    assert not (filepath != '' and len(files) !=
                0), 'filepath and files args cannot both be valued'
    if rmwd.is_alive() == False:
        rmwd.start()
    if len(files) == 0:
        remove_queue.put([
            {
                "filepath": filepath,
                "expiration": int(time.time()) + config['temp_file_expire']
            }
        ])
    elif len(filepath) == 0:
        exp = int(time.time()) + config['temp_file_expire']
        remove_queue.put(
            map(lambda f: {"filepath": f, "expiration": exp}, files))
