from argparse import ArgumentParser


def create_arg_parser():
    """ Creates an argument parser that handles an output directory name and a toggle on which artists to parse. """

    cmd_line_parser = ArgumentParser()
    cmd_line_parser.add_argument('-o',
                                 '--output',
                                 dest='output_directory',
                                 help='The output directory',
                                 default='lyrics')
    cmd_line_parser.add_argument('-a',
                                 '--all',
                                 dest='all_artists',
                                 action='store_true',
                                 help='Flag to enable parsing all artists instead of top artists.')
    return cmd_line_parser
