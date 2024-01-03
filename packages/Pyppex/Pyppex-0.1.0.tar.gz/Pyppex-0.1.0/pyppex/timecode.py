import time

def timecode(seconds:float) -> str:
    '''
    Converts the given duration in seconds to a formatted time string.

    Args:
    -----
        - `seconds` (float): Duration in seconds.

    Returns:
    --------
        - `str`: Formatted time string in the format "HH:MM:SS.MS magnitude", representing hours, minutes,
                seconds, and milliseconds.

    Example:
    --------
        >>> to_time(59.54)
        '00:00:59.540 seconds'
        >>> to_time(79.0)
        '00:01:19.000 minutes'
    '''
    def x(t:int) -> str:
        '''Formatting for hours, minutes and seconds.'''
        return '0'+str(t) if t<10 else str(t)
    
    def y(t:float) -> str:
        '''Formatting for miliseconds.'''
        t = int((t*1000)%1000)
        return (3-len(str(t)))*'0' + str(t)
    
    dt = time.gmtime(seconds)
    t_dict = {'hours':dt.tm_hour, 'minutes':dt.tm_min, 'seconds':dt.tm_sec, 'miliseconds':int((seconds*1000)%1000)}

    try:
        return f'{x(dt.tm_hour)}:{x(dt.tm_min)}:{x(dt.tm_sec)}.{y(seconds)} {[k for k,v in t_dict.items() if v!=0][0]}'
    except: # When seconds==0
        return f'{x(dt.tm_hour)}:{x(dt.tm_min)}:{x(dt.tm_sec)}.{y(seconds)}'