"""
    this module contains a variety of handy functions that show up
    at different parts of the analysis
"""
import datetime as dt

def write_to_file( data = None, filename = None, write_mode='a' ) :
    """
    """
    if data is None:
        raise ValueError('Must supply data to write\n.')
    if filename is None:
        raise ValueError('Must supply filename to write\n.')
    if write_mode not in ['a', 'w']:
        raise ValueError('Unrecognized write mode.\n')
    outfile = open( filename, write_mode )
    outfile.write( data )
    outfile.close()

def daterange(start_date, end_date, endpoint=False):
    """
    """
    j0 = 0 if not endpoint else 1
    for n in range(j0 + int((end_date - start_date).days)):
        yield start_date + dt.timedelta(days=n)

def mondays_in_interval( start_date, end_date ):
    mondays = []
    for date in daterange( start_date, end_date ):
        if date.weekday() == 1 :
            mondays.append( np.datetime64(date) )
    return mondays
