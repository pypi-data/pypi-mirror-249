import argparse
import os

arg_parser = argparse.ArgumentParser(description=__doc__)
# arg_parser.add_argument("--subdir-target", action="store", dest="subdir_target")
arg_parser.add_argument(
    "-c",
    "--configure",
    action="store_true",
    dest="configure",
    help="Trigger cmake to configure the generated CMakeLists.txt.",
)
args, unknown_args = arg_parser.parse_known_args()
