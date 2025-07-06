import numpy as np
import argparse
import glob
import os
from collections import defaultdict
from scipy import stats
from  defaultlist import defaultlist


def parseargs():
    parser = argparse.ArgumentParser('Parse new articles.')
    parser.add_argument('-p', '--input-path', default="c:\\projects\\katka\\2023-01-13_merge\\",  help='Path with csv files.')
    parser.add_argument('--prefix', default='mfd')
    parser.add_argument('-c', '--column', default=2, type=int)
    args = parser.parse_args()
    return args


def main():
    args = parseargs()

    relFreqDict = defaultdict(defaultlist)
    ARFDict = defaultdict(defaultlist)
    countDict = defaultdict(float)
    years = ['95', '96', '97', '98', '99', '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19']
    for i, year in enumerate(years):
        file = os.path.join(args.input_path, f'{args.prefix}{year}.csv')
        with open(file, 'r', encoding='utf8') as f:
            for line in f.readlines()[3:]:
                word, count, relFreq, ARF = line.strip().split(',')
                relFreqDict[word][i] = float(relFreq)
                ARFDict[word][i] = float(ARF)
                countDict[word] += float(count)

    results = []
    for word in relFreqDict:
        if countDict[word] > 50:
            y = [v if v is not None else 0 for v in relFreqDict[word]]
            x = [i for i, v in enumerate(relFreqDict[word])]
            if len(x) < 3:
                continue
            #print(1, x)
            #print(2, y)
            regression = stats.linregress(x, y)
            results.append((word, regression, np.mean(y)))
            #print(3, word, countDict[word], regression.slope, regression.rvalue, regression.pvalue, regression.stderr, regression.intercept_stderr)

    results = sorted(results, key=lambda x: -abs(x[1].slope / x[2]) )
    for word in results:

        res = [word[0], countDict[word[0]], word[2], word[1].slope, word[1].slope / word[2], word[1].intercept, word[1].rvalue, word[1].pvalue, word[1].stderr, word[1].intercept_stderr]
        res = '\t'.join([str(x) for x in res])
        print(res)













if __name__ == '__main__':
    main()

