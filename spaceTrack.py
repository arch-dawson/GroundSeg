import spacetrack.operators as op
from spacetrack import SpaceTrackClient

# Space Track allows no more than 20 requests per minute

import sys

outFile = 'latestTLE.txt'

noradID = 41474 # MINX

st = SpaceTrackClient('dawson.beatty@gmail.com', 'COSGCGroundSegment')

try:
    st.authenticate() # Will raise an error if incorrect login
except:
    print('Incorrect Login.')
    sys.exit(0)

data = st.tle_latest(iter_lines=True, norad_cat_id=noradID, limit=1, format='tle')
# Change format to whatever is easiest

with open(outFile, 'w+') as f:
    for line in data:
        f.write(line)
