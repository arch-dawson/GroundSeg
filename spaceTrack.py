import spacetrack.operators as op
from spacetrack import SpaceTrackClient
import argparse
import sys

# Space Track allows no more than 20 requests per minute
# On Windows, run 'py -3 ./spacetrack.py -id 41474'
# Change id above to different NORAD IDs if necessary

# Add path to TLEs folder 

def main(noradID, path):

    st = SpaceTrackClient('dawson.beatty@gmail.com', 'COSGCGroundSegment')

    try:
        st.authenticate() # Will raise an error if incorrect login
    except:
        print('Incorrect Login.')
        sys.exit(0)

    data = st.tle_latest(iter_lines=True, norad_cat_id=noradID, limit=1, format='3le')
    # Change format to whatever is easiest
    
    line1 = next(data) # 0 MINXSS
    line2 = next(data) # 1 blah blah
    line3 = next(data) # 2 blah blah
    
    outFile = path + line1.split()[1] + '.txt'

    # Need to split up the generator to get the name for above. 
    with open(outFile, 'w+') as f:
        f.write(line1)
        f.write(line2)
        f.write(line3) 
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Requests most recent 3LE data from spacetrack.org')
    parser.add_argument('-id', action="store", dest="noradID", type=str, default=41474) #41474 is MINX
    parser.add_argument('-path',action="store",type=str,default='')
    args = parser.parse_args()

    main(args.noradID, args.path)
