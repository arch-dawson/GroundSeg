import spacetrack.operators as op
from spacetrack import SpaceTrackClient
import argparse
import sys

# Space Track allows no more than 20 requests per minute
# On Windows, run 'py -3 ./spacetrack.py -id 41474'
# Change id above to different NORAD IDs if necessary

def main(noradID):
    outFile = str(noradID) + '_3LE.txt'

    st = SpaceTrackClient('dawson.beatty@gmail.com', 'COSGCGroundSegment')

    try:
        st.authenticate() # Will raise an error if incorrect login
    except:
        print('Incorrect Login.')
        sys.exit(0)

    data = st.tle_latest(iter_lines=True, norad_cat_id=noradID, limit=1, format='3le')
    # Change format to whatever is easiest

    with open(outFile, 'w+') as f:
        for line in data:
            f.write(line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Requests most recent 3LE data from spacetrack.org')
    parser.add_argument('-id', action="store", dest="noradID", type=str, default=41474) #41474 is MINX
    args = parser.parse_args()

    main(args.noradID)
