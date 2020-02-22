# OHHLA Scrapper. Written by Andoni M. Garcia. 2014

from pathlib import Path

from argparser import create_arg_parser
from scraper import scrape_OHHLA

OHHLA_URL = "http://ohhla.com/"
ALL_ARTIST_SITES = ["http://ohhla.com/all.html",
                    "http://ohhla.com/all_two.html",
                    "http://ohhla.com/all_three.html",
                    "http://ohhla.com/all_four.html",
                    "http://ohhla.com/all_five.html"]

if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args()

    Path(args.output_directory).mkdir(exist_ok=True)
    scrape_OHHLA(OHHLA_URL, ALL_ARTIST_SITES, args.output_directory)
