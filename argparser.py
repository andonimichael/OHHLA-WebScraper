from argparse import ArgumentParser


def create_arg_parser():
    """ Creates an argument parser that handles an output directory name. """

    cmd_line_parser = ArgumentParser()
    cmd_line_parser.add_argument('-o',
                                 '--output',
                                 dest='output_directory',
                                 help='The output directory',
                                 default='lyrics')
    return cmd_line_parser
