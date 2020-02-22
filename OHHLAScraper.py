# OHHLA Scrapper. Written by Andoni M. Garcia. 2014

from pathlib import Path

from argparser import create_arg_parser
from scraper import OHHLAScraper


if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args()

    Path(args.output_directory).mkdir(exist_ok=True)
    scraper = OHHLAScraper(args.output_directory)
    if args.all_artists:
        scraper.scrape_all_artists()
    else:
        scraper.scrape_top_artists()
