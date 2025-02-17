import argparse
import csv
import logging
import datetime

def parseargs():
    parser = argparse.ArgumentParser('Parse new articles.')
    parser.add_argument('-i', '--input-file', required=True, help='Csv file.')
    parser.add_argument('-o', '--output-path', required=True, help='Output path.')
    args = parser.parse_args()
    return args

#Kód článku;Datum publikování;Název;Autor;Strana;Plné znění;Sentiment;Důležitá zpráva;AVE;Rubrika;Obrázek
#2024B296A24D;20.12.2024;Chcípneš jako pes! ;Natália Kudrnová;24;"Poslední vzkaz dcery u soudu:
#Rozsudek v monstrprocesu s Francouzem Pelicotem, který nechával znásilňovat svou omámenou ženu

def main():
    args = parseargs()

    with open(args.input_file, 'r', newline='', encoding='utf8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            # Datum publikování
            # Název
            # Plné znění
            published_date = row["Datum publikování"]
            title = row["Název"]
            full_text = row["Plné znění"]

            # parse the data
            published_date = datetime.datetime.strptime(published_date, '%d.%m.%Y')
            year = published_date.year
            output_file = f'{args.output_path}_{year}.txt'
            with open(output_file, 'a', encoding='utf8') as f:
                f.write(f'{title}\n')
                f.write(f'{full_text}\n')
                f.write('\n')
                f.write('\n')

if __name__ == '__main__':
    main()



