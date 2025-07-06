import numpy as np
import sys
import re
import argparse
from collections import defaultdict
import re

# 1996 1997 1999 2004 2005


def parseargs():
    parser = argparse.ArgumentParser('Parse new articles.')
    parser.add_argument('-i', '--input-file', required=True, help='npy data file.')
    parser.add_argument('-t', '--title-list', required=False, help='Only export titles in this list.')
    args = parser.parse_args()
    return args


def main():
    args = parseargs()
    for news in ['blesk', 'mfd']:
        for year in ['1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']:

            file1 = args.title_list + f'{news}_{year}.txt'
            file2 = args.input_file + f'{news}_{year}.txt'

            separator = '--------------'
            last_lines = []
            words = []
            chars = []

            matcher = re.compile('\A[0-9]+. ')

            title_list = []
            if args.title_list:
                try:
                    with open(file1, 'r', encoding='utf8', ) as f:
                        title_list = [line.strip() for line in f if matcher.match(line)]
                except:
                    title_list = [line.strip() for line in open(file1, 'r') if matcher.match(line)]

            title_list = set(title_list)

            dates = defaultdict(int)
            dates_words = defaultdict(int)
            dates_chars = defaultdict(int)

            state = 'preable'
            article_title = None
            article_date = None
            for line in open(file2, 'r', encoding='utf8'):
                line = line.strip()
                if state == 'preable':
                    if separator == line[:len(separator)]:
                        state = 'article_start'
                elif state == 'article_start':
                    if matcher.match(line):
                        article_title = line
                    elif re.match('^[\w ]*\w: ', line):
                        state = 'info'
                elif state == 'info':
                    if 'Datum:' in line:
                        d = line.split()[1]
                        d = ' '.join(d.split('.')[1:][::-1])
                        article_date = d
                    if line == '':
                        state = 'article'
                        last_lines = []
                elif state == 'article':
                    if line[:9] == '{[p class':
                        state = 'preable'
                        if not title_list or article_title in title_list:
                            #print('HAVE', article_title)
                            words.append(np.sum([len(l.split()) for l in last_lines]))
                            chars.append(np.sum([len(l) for l in last_lines]))
                            dates[article_date] += 1
                            dates_words[article_date] += np.sum([len(l.split()) for l in last_lines])
                            dates_chars[article_date] += np.sum([len(l) for l in last_lines])
                        else:
                            pass
                            #print('REJECTED', article_title)
                    else:
                        last_lines.append(line.strip())

            for y in range(1995, 2021):
              for m in range(1, 13):
                date_str = f'{y} {m:02d}'
                if dates[date_str]:
                    print(f'{y}\t{m:02d}\t{dates[date_str]}\t{dates_words[date_str]}\t{dates_chars[date_str]}')


if __name__ == '__main__':
    main()

#print('\t' + '\t'.join([str(w) for w in chars]))


