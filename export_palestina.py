import argparse
import csv
import logging
import datetime
import os
from tqdm import tqdm
from collections import defaultdict

def parseargs():
    parser = argparse.ArgumentParser('Parse new articles.')
    parser.add_argument('-i', '--input-file', required=True, help='Csv file.')
    parser.add_argument('-o', '--output-path', required=True, help='Output path.')
    args = parser.parse_args()
    return args

#Kód článku;Datum publikování;Název;Autor;Plné znění;Sentiment;Originální internetový zdroj;Rubrika


def main():
    args = parseargs()

    os.makedirs(args.output_path, exist_ok=True)


    with open(args.input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        articles = [row for row in reader]
        title_counts = defaultdict(int)
        for row in articles:
            print(row["Datum publikování"])
            row["Datum publikování"] = datetime.datetime.strptime(row["Datum publikování"].split()[0], '%d.%m.%Y')
            title_counts[row["Název"]] += 1


        articles = sorted(articles, key=lambda x: title_counts[x["Název"]], reverse=True)

        for row in articles:
            if title_counts[row["Název"]] > 1:
                logging.warning(f'Multiple: {row["Název"]} {title_counts[row["Název"]]}')

            date_string = row["Datum publikování"].strftime('%Y-%m-%d')
            output_name = f'{date_string}_{row["ID"]}.txt'
            with open(os.path.join(args.output_path, output_name), 'w', encoding='utf8') as f:
                f.write(f'{row["Název"]}\n\n')
                f.write(f'{row["Plné znění"]}\n')


if __name__ == '__main__':
    main()



