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
#  The thread pool lib supports a timeout mechanism when executing the commands.
#  Specify the timeout value in seconds when creating the thread pool. If the
#  execution time of the command exceeds the timeout value, a timout exception
#  will occur and the command will be retried. The number of retries can also be
#  specified when creating the thread pool. If the command wasn't successful after
#  the specified number of retries, the command will be considered as failed.
#  In this case, a message '##FAILURE##' will be put into the output queue and
#  the item will be put back into the input queue.
#  if the command was successful, the result of the command will be put into the
#  output queue.
# =============================================================================


# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
import atexit
import ctypes
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
    def callable(self, outputQueue, item) -> int:
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

        Returns
        -------
        int
            The return code of the task.
            Return 0 if successful, otherwise any other value.
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
        timeout (int, optional): The timeout in seconds for the input queue.
            If not provided, a default timeout of 5 seconds will be used.
        numOfRetries (int, optional): The number of retries for the input queue.
            If not provided, a default number of 3 retries will be used.
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
    timeout = 5
    numOfRetries = 3
    callable = None

    # -------------------------------------------------------------
    # INIT METHOD DEFINITION
    # -------------------------------------------------------------
    def __init__(
        self,
        numOfThreads=5,
        inputQueue=None,
        outputQueue=None,
        callable=None,
        timeout=5,
        numOfRetries=3,
    ):
        self.inputQueue = inputQueue if inputQueue is not None else queue.Queue()
        self.outputQueue = outputQueue if outputQueue is not None else queue.Queue()
        self.callable = callable if callable is not None else ThreadPoolFunction()
        self.numOfThreads = numOfThreads if numOfThreads is not None else 5
        self.timeout = timeout if timeout is not None else 5
        self.numOfRetries = numOfRetries if numOfRetries is not None else 3
        # create worker threads
        for i in range(numOfThreads):
            self.startThread(
                self.callback, i, self.inputQueue, self.outputQueue, self.callable
            )
        # register atexit function
        atexit.register(self.stopThreads)

    # -------------------------------------------------------------
    # START THREADS METHOD DEFINITION
    # -------------------------------------------------------------
    def startThread(self, callback, threadNum, inputQueue, outputQueue, callable):
        thread = threading.Thread(
            target=callback,
            args=(threadNum, inputQueue, outputQueue, callable),
            daemon=True,
        )
        thread.start()
        self.threadList.append(thread)

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
                inputQueue.task_done()
            else:
                numOfRetries = self.numOfRetries
                # start retry mechanism
                while numOfRetries > 0:
                    # reset result
                    result = 0
                    # create timer thread
                    timer = self.startTimerThread(threadNum)
                    # call the callable function
                    try:
                        # execute callable
                        result = callable.callable(outputQueue, item)
                    except Exception as e:
                        print(f"##TIMEOUT## - {item} - retry {numOfRetries}")
                        result = 1
                    finally:
                        # stop timer thread
                        self.stopTimerThread(timer)
                    # check results
                    if result != 0:
                        numOfRetries -= 1
                # check if we were successfull
                if result != 0:
                    print(f"##FAILURE## - {item}")
                    outputQueue.put(("##FAILURE##", item))
                # signal that this task is done
                # this is done in every case, if successful or not
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

    # -------------------------------------------------------------
    # START TIMER THREAD METHOD DEFINITION
    # -------------------------------------------------------------
    def startTimerThread(self, threadNum):
        timer = threading.Timer(
            interval=self.timeout,
            function=self.timeoutThread,
            args=[threadNum, threading.get_ident()],
        )
        # start timer thread
        timer.start()
        return timer

    # -------------------------------------------------------------
    # STOP TIMER THREAD METHOD DEFINITION
    # -------------------------------------------------------------
    def stopTimerThread(self, timer):
        timer.cancel()

    # -------------------------------------------------------------
    # TIMEOUT THREAD METHOD DEFINITION
    # -------------------------------------------------------------
    def timeoutThread(self, threadNum, threadId):
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(threadId), ctypes.py_object(RuntimeError)
        )
