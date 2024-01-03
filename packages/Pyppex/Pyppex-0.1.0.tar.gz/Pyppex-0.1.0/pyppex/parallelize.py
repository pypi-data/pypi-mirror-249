import multiprocessing as mp
import numpy as np
import psutil, traceback
from tqdm import tqdm
from typing import Iterable, Callable, Optional, Generator
from pyppex import modstring

class Parallelize:
    """
    A class that allows for parallel processing of a function using multiple processes.

    Libraries:
    ----------
        - multiprocessing: https://docs.python.org/3/library/mp.html

    Args:
    -----
        - `function` (callable): The function to be executed in parallel.
        - `item` (iterable): The iterable containing the arguments to the function.
        - `num_processes` (int or None): The number of processes to use. If None, the number of processes used will be determined by the available CPU cores and the limit_percent parameter.
        - `limit_percent` (float, optional): The percentage at which a CPU core is considered "in use" and will not be used for parallel execution. Defaults to 50.0.
        - `verbose` (bool): prompt useful information about RAM and CPU memory usage.
    """


    def __init__(self, function:Callable, item:Iterable, num_processes:Optional[int]=None, limit_percent:float=50.0, verbose:bool=True):
        self.parent_process = mp.parent_process()
        self.limit_percent = limit_percent
        self.function = function
        self.processes = self.__processes_warning(num_processes)
        self.processes_ids = None
        self.__verbose = verbose
        self.__manager = mp.Manager()
        self.__item = self.__share_item(self.__manager, item)
        self.__pool = mp.Pool(processes=self.processes)

        if self.__verbose:
            print(
                f'''Virtual RAM memory statistics:
        - In use: {modstring(psutil.virtual_memory().percent, mod="green")} %
        - Available: {modstring(psutil.virtual_memory().available/10**9, mod="green")} GB
        - Shared: {modstring(psutil.virtual_memory().shared/10**6, mod="green")} MB
                '''
            )


    def __processes_warning(self, num_p:Optional[int]=None) -> int:
        """
        Determines the number of processes to use for parallel execution.

        Args:
        -----
            - `num_p` (int or None): The desired number of processes. If None, the number of processes used will be determined by the available CPU cores and the limit_percent parameter.

        Returns:
        --------
            - `int`: The number of processes to use for parallel execution.

        Raises:
        -------
            - `ValueError`: If the specified number of processes is greater than the number of available CPU cores.
        """
        try:
            percent = psutil.cpu_percent(interval=1, percpu=True)

            if num_p == None:
                return len(list(filter(lambda x: True if x<=self.limit_percent else False ,percent)))
            
            elif num_p > mp.cpu_count():
                raise ValueError
            
            else:
                return num_p
            
        except ValueError:
            print(f'There are {modstring(mp.cpu_count(), mod="green")} Logical CPU cores available')
        except Exception:
            print(f'{modstring(traceback.format_exc(), mod="red")}')
        

    def __share_item(self, manager:object, item:Iterable) -> Iterable:
        """
        Converts the input iterable into a shared object that can be used by the multiprocessing.Pool object.

        Args:
        -----
            - `manager` (multiprocessing.Manager): A multiprocessing.Manager object.
            - `item` (iterable): The iterable containing the arguments to the function.

        Returns:
        --------
            - `iterable`: A shared object that can be used by the multiprocessing.Pool object.

        Raises:
        -------
            - `ValueError`: If the input iterable is not a dict, list, array, int, or float.
        """
        try:
            if type(item) == dict:
                shared_item = manager.dict(item)
            elif type(item) == list:
                shared_item = manager.list(item)
            elif type(item) == np.array:
                shared_item = manager.Array('d', item)
            elif type(item) in [int, float]:
                shared_item = manager.Value(item)
            else:
                raise ValueError
            
            return shared_item
        
        except ValueError:
            print('Assign to the argument "item" one of the listed objects: dict, list, np.array, int, or float')
    

    def compute(self, chunksize:int=1, progressbar_desc:Optional[str]=None) -> Generator:
        """
        The compute method applies a function to an iterable object in parallel using the multiprocessing module yielding the results in order as soon
        as they are computed.
        In order to work multiprocessing, add the code after a if __name__=='__main__': block.

        Args:
        -----
            - `chunksize` (int): The size of the chunks to divide the iterable object into. Default is 1.
            - `progressbar_desc` (str or None): Description to set to the progress bar from tqdm.
        
        Returns:
        --------
            - `generator`: yields each result in order when it's execution is finished.
        
        Example:
        --------
            >>> from pyppex import Parallelize
            >>> def run(e):
            ...     time.sleep(5)
            ...     return e
            >>> if __name__=='__main__':
            ...     parallel = Parallelize(function=run, item=list(range(10)))
            ...     results = parallel.compute()
            ...     print(*results)
            0 1 2 3 4 5 6 7 8 9
        """
        try:
            for result in tqdm(
                self.__pool.imap(func=self.function, iterable=self.__item, chunksize=chunksize),
                total=len(self.__item),
                desc=progressbar_desc
            ):
                yield result

            self.processes_ids = [p.pid for p in mp.active_children() if p.name!='SyncManager-1']
            self.__pool.close()
            self.__pool.join()

        except Exception:
            print(f'{modstring(traceback.format_exc(), mod="red")}')

        if self.__verbose:
            print(f'Number of child processes used: {modstring(len(self.processes_ids), mod="yellow")}')