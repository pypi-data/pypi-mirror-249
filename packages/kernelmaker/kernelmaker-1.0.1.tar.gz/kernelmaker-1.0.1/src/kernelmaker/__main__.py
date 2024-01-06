from kernelmaker import run

import os
if os.getuid() == 0: raise PermissionError("Cannot be root to run makepkg!")

import argparse
parser = argparse.ArgumentParser(
    prog='kernelmaker.py',
    description=f"Helps manages the creation and updating of custom kernel builds.",
    epilog="Note: This program is also available as a python script binding; simply call kernelmaker.run(...) with your desired arguments.")
meta_parser_group = parser.add_argument_group("Metadata overrides", description="The string used for <new_kernel> will be used as the pkgbase for the new kernel in the makefile provided with "   +
    "base kernel. This program will attempt to automatically merge this value into the PKGBUILD. The same will be done with the description passed into the program with '-d <desc>', which will " +
    " be used as the pkgdesc. The pkgver cannot be changed; it will be inherited from the base kernel.")
conf_parser_group = parser.add_argument_group("Kernel configuration overrides", description="This program allows for automatic merging of config overrides. Any config values you wish to "        +
    "override should be placed in a file with the same syntax as the 'config' file bundled with the kernel. Pass the path to this file into the program with '-c <path>'. If the specified path "  +
    "is a directory, all files within that directory will be parsed and applied. This program also allows for automatic patch application, as well. Directories having their files recursively "   +
    "parsed applies here, too.")
build_parser_group = parser.add_argument_group("Build overrides", description="")
io_parser_group = parser.add_argument_group("Output overrides", description="")
io_subgroup_for_verbosity_flags = io_parser_group.add_mutually_exclusive_group()

parser.add_argument(
    metavar="base_kernel",
    help="The base kernel to build from, e.x. 'linux' or 'linux-hardened'.",
    dest='base_kernel_name')
parser.add_argument(
    metavar="new_kernel",
    help="The new kernel to build, e.x. 'linux-custom'. Will be used as the pkgbase in makepkg.",
    dest='new_kernel_name')
meta_parser_group.add_argument(
    "-d", "--desc", "--pkgdesc", "--description",
    help="The pkgdesc to use in makekpg. Unspecified or blank will default to \"custom <pkgbase> kernel\".",
    required=False,
    dest='description',
    default="")
conf_parser_group.add_argument(
    "-c", "--config-override",
    help="The path to the config overrides file. See footnote [1].",
    required=False,
    dest='config_overwrite_paths',
    action='append')
conf_parser_group.add_argument(
    "-p", "--patch",
    help="The path to a single patch file. This argument can be specified multiple times. If any given path is a directory, all files within it will be read as patch files. See footnote [2].",
    required=False,
    dest='patches_paths',
    action='append')
build_parser_group.add_argument(
    "-o", "--output-dir",
    help="The directory to place the kernel and kernel headers into, once made. Unspecified or blank will default to current working directory.",
    required=False,
    dest='output_folder',
    default='.')
build_parser_group.add_argument(
    "-D", "--make-docs",
    help="If this flag is present, docs and htmldocs generation will NOT be skipped. Recommended action is to skip this generation (omit this flag), since it takes a very long time.",
    required=False,
    dest='should_make_docs',
    action='store_true')
build_parser_group.add_argument(
    "--makepkg-flags",
    help="Flags to use when compiling with makepkg. If -s is not present, it will be added. See makepkg(8).",
    required=False,
    dest='makepkg_flags',
    default='')
build_parser_group.add_argument(
    "--use-modprobed-db",
    help="If this flag is present, `make LSMOD=$HOME/.config/modprobed.db localmodconfig` will be added to PKGBUILD `prepare()`. This is an advanced option, do not include this unless you are sure " +
         "modprobed-db is installed and the local module database is up to date, or else your kernel will not include any of the modules it needs to function. See modprobed-db(8) and the Arch wiki " +
         "page for modprobed-db.",
    required=False,
    dest='should_modprobed_db',
    action='store_true')
io_parser_group.add_argument(
    "-j", "--ncores",
    help="The number of cores to use during makepkg. Must be an integer value. Unspecified or <1 will default to all available cores (from `nproc`).",
    required=False,
    dest='num_cores',
    default=0,
    type=int)
io_parser_group.add_argument(
    "-i", "--interrupt",
    help="If this flag is present, the program will pause after all major events (base kernel download, config overrides applied, PKGBUILD update, " +
            "and just before makepkg) and wait for the user to type 'ready'. In place to allow for manual checking of progress, mostly for testing/debugging.",
    required=False,
    dest='should_interrupt',
    action='store_true')
io_subgroup_for_verbosity_flags.add_argument(
    "-q", "--quiet",
    help="Quiet output. Specify once to remove output from called programs, twice to remove all output except warnings+errors, or three times to remove all output except errors.",
    required=False,
    dest='quiet_amt',
    action='count')
io_subgroup_for_verbosity_flags.add_argument(
    "-v", "--verbose", help="Verbose output. Specify once to show intermediate information, twice to show debug logging. Three occurances implies -i.",
    required=False,
    dest='verbose_amt',
    action='count')

#ifdef TESTING 
# args = parser.parse_args(['linux', 'linux-custom', '-i', '-vvv', '-d', 'testing package description']))
#else 
args = parser.parse_args()
#endif

# simple rearranging a lil bit before passing off the spotlight to run()
args = vars(args)

# count v's
v = args.pop('verbose_amt')
if v is None: v = 0
v = min(max(int(v), 0), 3)

# count q's
q = args.pop('quiet_amt')
if q is None: q = 0
q = min(max(int(q), 0), 3)

# calculate verbosity
args['verbosity'] = v - q
if args['verbosity'] == 3: args['should_interrupt'] = True

# ladies and gentleman, at long last, the Big Event, live and in the flesh. the run function.
run(**args)
