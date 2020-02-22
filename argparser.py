from argparse import ArgumentParser


def create_arg_parser():
    """ Creates an argument parser that handles output file names. """

    cmd_line_parser = ArgumentParser()
    cmd_line_parser.add_argument('-o',
                                 '--output',
                                 dest='output_file',
                                 help='The output file',
                                 default='lyrics.txt')
    return cmd_line_parser
