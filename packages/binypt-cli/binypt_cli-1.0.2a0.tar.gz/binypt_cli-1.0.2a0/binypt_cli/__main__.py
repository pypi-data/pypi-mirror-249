import os
import re
import sys
import argparse

from binypt import Binypt
from binypt import metadata


def output_path_is_valid(output_path: str):
    if os.path.exists(output_path):
        raise ValueError(f"`{output_path}` is an existing file!")
    elif re.search("(csv)|(xlsx)|(pickle)$", output_path) is None:
        raise TypeError("Output file format is not valid!")
    else:
        return output_path


def configure_parser(parser):
    parser.add_argument(
        "-p",
        "--trading-pair",
        required=True,
        dest="trading_pair",
        type=metadata.trading_pair_exists,
        help="Trading pair symbol (e.g., BTCUSDT).",
    )

    parser.add_argument(
        "-i",
        "--interval",
        required=True,
        dest="interval",
        type=metadata.interval_exists,
        help="Candlestick interval (e.g., 1h, 1d, 1w).",
    )

    parser.add_argument(
        "-od",
        "--open-date",
        required=True,
        dest="open_date",
        type=metadata.date_is_correct_format,
        help="Start date for data collection (YYYY-MM-DD/HH:mm:ss).",
    )

    parser.add_argument(
        "-cd",
        "--close-date",
        required=True,
        dest="close_date",
        type=metadata.date_is_correct_format,
        help="End date for data collection (YYYY-MM-DD/HH:mm:ss).",
    )

    parser.add_argument(
        "-o",
        "--output-path",
        default="binypt_data.csv",
        dest="output_path",
        type=output_path_is_valid,
        help="""
        Path to the output file for data storage.
        Possible formats: .csv, .xlsx, .pickle""",
    )

    parser.add_argument(
        "-hr",
        "--add-hr-time",
        action="store_true",
        default=False,
        dest="human_readable_time_status",
        help="Include human-readable time format in the output data.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        dest="show_log",
        help="Enable verbose logging for debugging purposes.",
    )


def run():
    parser = argparse.ArgumentParser(
        prog="biynpt",
        description="""
        Binypt is a command line utility to download a range
        of chart data from Binance""",
    )
    configure_parser(parser)

    parsed_arguments = vars(parser.parse_args(sys.argv[1:]))

    binypt = Binypt()
    binypt.set_arguments(
        trading_pair=parsed_arguments["trading_pair"],
        interval=parsed_arguments["interval"],
        open_date=parsed_arguments["open_date"],
        close_date=parsed_arguments["close_date"],
    )
    show_log = parsed_arguments["show_log"]
    binypt.set_verbosity(
        show_bar=not show_log,
        show_log=show_log
    )
    binypt.retrieve_data()
    if parsed_arguments["human_readable_time_status"]:
        binypt.add_human_readable_time()
    binypt.export(parsed_arguments["output_path"])
