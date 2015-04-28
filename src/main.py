import argparse
import pandas as pd
import shutil, os
import time

def die():
    print """Usage: python main.py --gmbrc /home/USER/.config/gmusicbrowser/gmbrc --lastdb /PATH/TO/scrobbles.tsv"""
    exit(1)

def backup_gmbrc(gmbrc):
    shutil.copy2(gmbrc, os.path.join('.', gmbrc + 'backup' + str(int(time.time()))))

def find_data_start(gmbrc):
    h = open('gmbrc_header', 'w')
    with open(gmbrc) as gmb:
        for i, line in enumerate(gmb):
            if line.rstrip() == '[Songs]':
                gmb.close()
                h.write(line)
                h.close()
                return i+1
            else:
                h.write(line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gmbrc', help='gmusicbrowser database file where your music libary is stored')
    parser.add_argument('--lastdb', help='scrobbles.tsv file exported from your last.fm account')

    args = parser.parse_args()
    gmbrc = args.gmbrc
    lastdb = args.lastdb

    if not gmbrc or not lastdb:
        die()

    backup_gmbrc(gmbrc)

    gmb_header_end = find_data_start(gmbrc)
    gmb_library = pd.read_csv(gmbrc, sep='\t', header=1, skiprows=gmb_header_end, index_col=0)
    last_data = pd.read_csv(lastdb, sep='\t')
    last_data['playcount'] = 0

    last_grouped = last_data['playcount'].\
        groupby([last_data['uncorrected artist name'],
                 last_data['album name'],
                 last_data['uncorrected track name']]).count()


    hits = 0
    for id in last_grouped.index:
        mask = (gmb_library['artist'].str.lower() == id[0].lower()) & (gmb_library['album'].str.lower() == id[1].lower()) & (gmb_library['title'].str.lower() == id[2].lower())

        if not gmb_library[mask].empty:
            value = gmb_library.loc[mask, 'playcount']
            if value.iloc[0] < last_grouped.ix[id]:
                gmb_library.loc[mask, 'playcount'] = last_grouped.ix[id]
            hits += last_grouped.ix[id]
        else:
            print "fail:", id

    print "matched ", hits, " scrobbles in your gmb library with last.fm export data (consisting of ", len(last_data.index), " scrobbles)"

    gmb_library.to_csv('gmbrc_dump', sep='\t', float_format='%.0f', index_label=False)
    os.remove(gmbrc)

    destination = open(gmbrc, 'wb')
    shutil.copyfileobj(open('gmbrc_header', 'rb'), destination)
    shutil.copyfileobj(open('gmbrc_dump', 'rb'), destination)

    os.remove('gmbrc_header')
    os.remove('gmbrc_dump')

if __name__ == '__main__':
    main()