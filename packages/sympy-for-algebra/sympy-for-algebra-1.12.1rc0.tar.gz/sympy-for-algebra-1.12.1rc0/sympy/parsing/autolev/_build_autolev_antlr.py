import os
import subprocess
import glob

from sympy.utilities.misc import debug

here = os.path.dirname(__file__)
grammar_file = os.path.abspath(os.path.join(here, "Autolev.g4"))
dir_autolev_antlr = os.path.join(here, "_antlr")

header = '''\
# *** GENERATED BY `setup.py antlr`, DO NOT EDIT BY HAND ***
#
# Generated with antlr4
#    antlr4 is licensed under the BSD-3-Clause License
#    https://github.com/antlr/antlr4/blob/master/LICENSE.txt
'''


def check_antlr_version():
    debug("Checking antlr4 version...")

    try:
        debug(subprocess.check_output(["antlr4"])
              .decode('utf-8').split("\n")[0])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        debug("The 'antlr4' command line tool is not installed, "
              "or not on your PATH.\n"
              "> Please refer to the README.md file for more information.")
        return False


def build_parser(output_dir=dir_autolev_antlr):
    check_antlr_version()

    debug("Updating ANTLR-generated code in {}".format(output_dir))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, "__init__.py"), "w+") as fp:
        fp.write(header)

    args = [
        "antlr4",
        grammar_file,
        "-o", output_dir,
        "-no-visitor",
    ]

    debug("Running code generation...\n\t$ {}".format(" ".join(args)))
    subprocess.check_output(args, cwd=output_dir)

    debug("Applying headers, removing unnecessary files and renaming...")
    # Handle case insensitive file systems. If the files are already
    # generated, they will be written to autolev* but Autolev*.* won't match them.
    for path in (glob.glob(os.path.join(output_dir, "Autolev*.*")) or
        glob.glob(os.path.join(output_dir, "autolev*.*"))):

        # Remove files ending in .interp or .tokens as they are not needed.
        if not path.endswith(".py"):
            os.unlink(path)
            continue

        new_path = os.path.join(output_dir, os.path.basename(path).lower())
        with open(path, 'r') as f:
            lines = [line.rstrip().replace('AutolevParser import', 'autolevparser import') +'\n'
                     for line in f.readlines()]

        os.unlink(path)

        with open(new_path, "w") as out_file:
            offset = 0
            while lines[offset].startswith('#'):
                offset += 1
            out_file.write(header)
            out_file.writelines(lines[offset:])

        debug("\t{}".format(new_path))

    return True


if __name__ == "__main__":
    build_parser()
