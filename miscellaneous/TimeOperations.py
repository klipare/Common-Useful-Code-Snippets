import decimal
import datetime
import time
import pytz
from pytz import timezone

tz = timezone('Asia/Calcutta')
print("timezone:",tz)
utc = pytz.utc

now = time.time()
print("current time:",now)
utc_dt = utc.localize(datetime.datetime.utcfromtimestamp(now))
localized_dt = utc_dt.astimezone(tz)
print("local time:",localized_dt)

ts_at_fetch_horizon = now - (1 * 3600)
print("start time:",ts_at_fetch_horizon)
st_utc_dt = utc.localize(datetime.datetime.utcfromtimestamp(ts_at_fetch_horizon))
st_localized_dt = st_utc_dt.astimezone(tz)
print("local start time:",st_localized_dt)