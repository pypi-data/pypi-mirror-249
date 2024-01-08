#%% imports
from jgtfxc import get_price_history
import jgtfxc as jfx
from datetime import datetime
import JGTPDS as pds
#%% Define the parameters
instrument = "EUR/USD"
timeframe = "H4"
#datefrom = datetime(2021, 1, 1)
datefrom = None
dateto = datetime(2021, 12, 31)
quotes_count_spec = 400
quiet = True

#%% PDS

pds.stayConnectedSetter(True)
df=pds.getPH(instrument, timeframe, datefrom, dateto, quotes_count_spec, quiet)
pds.disconnect()

#%% Call the function
jfx.stayConnected = True
jfx.connect()
jfx.get_price_history(instrument, timeframe, datefrom, dateto, quotes_count_spec, quiet)
jfx.disconnect()

# %%
