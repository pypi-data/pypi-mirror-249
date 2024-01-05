# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : eod2pd
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  a simple thread pool library to execute commands in a multithreaded environment
#
# =============================================================================


# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
import atexit
import queue
import threading

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
#  CLASS DEFINITIONS
# -------------------------------------------------------------
class ThreadPoolFunction:
    def callable(self, outputQueue, item):
        """
        This function will be called from the thread pool in order to execute
        a specific command. The command is provided in the command parameter
        and is application specific. After processing the command, the result
        of the command can be put into the outputQueue.

        Parameters
        ----------
        outputQueue : queue.Queue
            The queue to put the result of the task.
        item : object
            The data item for the task.

        """
        pass


class ThreadPool:
    """
    A thread pool implementation for executing tasks concurrently.

    This class manages a pool of threads that can execute tasks in parallel.
    It provides a convenient way to distribute work across multiple threads
    and process the results asynchronously.

    Attributes:
        threadPool (list): A list of threads in the thread pool.
        inputQueue (Queue): The input queue for receiving tasks.
        outputQueue (Queue): The output queue for storing results.

    Args:
        numOfThreads (int): The number of threads in the thread pool.
        inputQueue (Queue, optional): The input queue to use. If not provided,
            a new queue will be created.
        outputQueue (Queue, optional): The output queue to use. If not provided,
            a new queue will be created.
        callable (ThreadPoolFunction, optional): The callable object that will
            be invoked to process tasks. If not provided, a default
            ThreadPoolFunction object will be used.

    Methods:
        stopThreads: Stops all the threads in the thread pool.
        callback: The callback function that is executed by each thread.

    """

    # -------------------------------------------------------------
    # VARIABLE DEFINTIONS
    # -------------------------------------------------------------
    threadList = []
    inputQueue = None
    outputQueue = None

    # -------------------------------------------------------------
    # INIT METHOD DEFINITION
    # -------------------------------------------------------------
    def __init__(
        self,
        numOfThreads=5,
        inputQueue=None,
        outputQueue=None,
        callable=ThreadPoolFunction(),
    ):
        if inputQueue is None:
            inputQueue = queue.Queue()
        if outputQueue is None:
            outputQueue = queue.Queue()
        self.inputQueue = inputQueue
        self.outputQueue = outputQueue
        # create threads
        for i in range(numOfThreads):
            thread = threading.Thread(
                target=self.callback,
                args=(i, self.inputQueue, self.outputQueue, callable),
                daemon=True,
            )
            thread.start()
            self.threadList.append(thread)
        # register atexit function
        atexit.register(self.stopThreads)

    # -------------------------------------------------------------
    # STOP THREADS METHOD DEFINITION
    # -------------------------------------------------------------
    def stopThreads(self):
        for _ in range(len(self.threadList)):
            self.inputQueue.put("##STOP##")

    # -------------------------------------------------------------
    # CALLBACK METHOD DEFINITION
    # -------------------------------------------------------------
    def callback(self, threadNum, inputQueue, outputQueue, callable):
        # set done flag
        done = False
        # endless loop until stop command
        while not done:
            item = inputQueue.get()
            if item == "##STOP##":
                done = True
            else:
                # call callable
                callable.callable(outputQueue, item)
                # signal that this task is done
                inputQueue.task_done()

    # -------------------------------------------------------------
    # GET INPUT QUEUE METHOD DEFINITION
    # -------------------------------------------------------------
    def getInputQueue(self):
        return self.inputQueue

    # -------------------------------------------------------------
    # GET OUTPUT QUEUE METHOD DEFINITION
    # -------------------------------------------------------------
    def getOutputQueue(self):
        return self.outputQueue
