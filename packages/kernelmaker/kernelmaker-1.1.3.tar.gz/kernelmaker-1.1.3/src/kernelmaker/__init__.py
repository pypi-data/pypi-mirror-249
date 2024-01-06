import os
import sys
import select
import subprocess
import time
import shutil
import shlex
import tempfile

from typing import Tuple, Dict, List, Optional, TextIO, Any
from os import PathLike


# io funcs

def __poll_stream(stream: TextIO) -> Optional[str]:
    i,o,e = select.select( [stream], [], [], 0 )
    return stream.readline() if i else None


def __interrupt(msg: Optional[str] = ""):
    """
    Blocks until the user types :const:`'ready'` or issues a :class:`KeyboardInterrupt`.
    """
    t = ""
    if msg: print(msg)
    print("Interrupting for manual inspection")
    while t != "ready":
        try:
            t = input("Type 'ready' when you are ready to continue, or ctrl+c to exit: ")
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            exit(0)


__verbosity_prefixes = ['ERR', 'WRN', 'INF', 'LOG', 'PRC', 'DBG', 'DBG']
def __print(cur_verbosity: int, msg_level: int, *msg: List[str]) -> None:
    if cur_verbosity >= msg_level:
        print('[' + __verbosity_prefixes[msg_level+3] + '] ', *msg, file=sys.stderr if msg_level<=-3 else sys.stdout, flush=True)


def __prompt(s: str, default: bool = None) -> bool:
    """
    Asks the user a y/n question. If :attr:`default` is :const:`None`, continue
    asking until a definite yes or no; if :attr:`default` is not :const:`None`,
    return :attr:`default` if the user does not pick from [yYnN].
    """
    t = ""
    if default is None:
        s += " [y/n] : "
        while len(t) == 0 or t[0] not in "ynYN":
            t = input(s)
        return t[0] in "yY"
    else:
        s += " [Y/n] : " if default else " [y/N] : "
        t = input(s)
        if len(t):
            if   s[0] in "yY": return True
            elif s[0] in "nN": return False
        return default


# lower-level shell wrappers

def __pkgctl(cv: int, pkgctl_executable: str, base_kernel_name: str) -> int:
    # assemble pkgctl command
    cmd = [pkgctl_executable, 'repo', 'clone', '--protocol=https', base_kernel_name]
    __print(cv, 2, "... running command:", shlex.join(cmd))
    p = subprocess.Popen(cmd, text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # tick io streams and look for error message
    while p.poll() is None:
        # try read stdout?
        if dat:=__poll_stream(p.stdout):
            __print(cv, 1, dat[:-1])  # last character is newline
        # try write stdin?
        if dat:=__poll_stream(sys.stdin):
            p.stdin.write(dat)
            p.stdin.flush()
    # handle returncodes
    if p.returncode == 255:
        __print(cv, -3, f"ERROR: Auth failed (most likely, base kernel '{base_kernel_name}' was not found and/or not publicly available)")
    return p.returncode


def __gpg(cv: int, key: str) -> bool:
    __print(cv, 2, f"... running command: gpg --recv-keys '{key}'")
    p = subprocess.Popen(["gpg", "--recv-keys", key], text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # tick io streams and look for error message
    while p.poll() is None:
        # try read stdout?
        if dat:=__poll_stream(p.stdout):
            #TODO check for and correct more errors
            __print(cv, 1, dat[:-1])  # last character is newline
        # try write stdin?
        if dat:=__poll_stream(sys.stdin):
            p.stdin.write(dat)
            p.stdin.flush()
    return p.returncode == 0


def __updpkgsums(cv: int, _isredo=False) -> Tuple[int, str]:
    __print(cv, 2, "... running command: updpkgsums")
    unk_keys = []
    p = subprocess.Popen(["updpkgsums"], text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # tick io streams and look for error message
    while p.poll() is None:
        # try read stdout?
        if dat:=__poll_stream(p.stdout):
            __print(cv, 1, dat[:-1])  # last character is newline
            #TODO check for and correct more errors
            if "unknown public key" in dat:
                unk_keys.append( dat.split()[-1][:-1] )
        # try write stdin?
        if dat:=__poll_stream(sys.stdin):
            p.stdin.write(dat)
            p.stdin.flush()
    if p.returncode != 0:
        if _isredo:
            __print(cv, -3, "ERROR: updpkgsums failed to run, already attempted fix, to no avail.")
            return p.returncode
        # unknown key! attempt to add it to the keyring and reattempt
        if len(unk_keys):
            __print(cv, -2, f"ERROR: updpkgsums did not recognize keys: {unk_keys}, attempting fetch...")
            good = True
            for k in unk_keys:
                if __gpg(cv, k):
                    __print(cv, -2, f"Successfully added key {k}")
                else:
                    good = False
                    __print(cv, -3, f"Failed to import key {k}")
                    break
            if good: return __updpkgsums(cv, _isredo=True)
        __print(cv, -3, f"ERROR: updpkgsums did not run correctly")
    return p.returncode

def __makepkg(cv:int, makepkg_flags: str, num_cores: Optional[int] = None, _isredo_unkkey=False) -> int:
    # assemble makepkg command
    if not num_cores: num_cores = os.cpu_count() # try using os module hook?
    if not num_cores: num_cores = "${nproc}"     # os call failed. fine. just fill with nproc call
    cmd = ['/bin/bash', '-c', f'export MAKEFLAGS="-j {num_cores}"; time env makepkg {makepkg_flags}']
    __print(cv, 2, "... running command:", shlex.join(cmd))
    p = subprocess.Popen(cmd, text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # tick io streams and look for error message
    unk_keys = []
    while p.poll() is None:
        # try read stdout?
        if dat:=__poll_stream(p.stdout):
            __print(cv, 1, dat[:-1])  # last character is newline
            #TODO check for and correct more errors
            if "unknown public key" in dat:
                unk_keys.append( dat.split()[-1][:-1] )
        # try write stdin?
        if dat:=__poll_stream(sys.stdin):
            p.stdin.write(dat)
            p.stdin.flush()
    # handle returncodes
    if p.returncode != 0:
        if _isredo_unkkey:
            __print(cv, -3, "ERROR: makepkg failed to run, already attempted fix, to no avail.")
            return p.returncode
        # unknown key! attempt to add it to the keyring and reattempt
        if len(unk_keys):
            __print(cv, -2, f"ERROR: makepkg did not recognize keys: {unk_keys}, attempting fetch...")
            good = True
            for k in unk_keys:
                if __gpg(cv, k):
                    __print(cv, -2, f"Successfully added key {k}")
                else:
                    good = False
                    __print(cv, -3, f"Failed to import key {k}")
                    break
            if good: return __makepkg(cv, makepkg_flags, _isredo_unkkey=True)
        __print(cv, -3, f"ERROR: makepkg did not run correctly")
    return p.returncode


# individual runners

def __run_pkgctl(cv: int, base_kernel_name: str, pkgctl_executable: str = None):
    # unspecified executable? for shame. no matter -- find a new one.
    if pkgctl_executable is None:
        __print(cv, 2, "No pkgctl executable path specified; finding one...")
        pkgctl_executable = shutil.which("pkgctl")
    # still not found? the gall! throw this fine gentleperson an exception.
    if pkgctl_executable is None:
        raise OSError("Command pkgctl not found! Please install the extra/devtools package", 2)
    # user passed an invalid file? how dareth thou!
    if not os.path.isfile(pkgctl_executable):
        raise OSError(f"pkgctl executable path '{pkgctl_executable} does not exist or is not a file")
    # great ok cool nice epic awesome :+1: pkgctl found. try download new kernel?
    __print(cv, 2, f"Using pkgctl executable path '{pkgctl_executable}'")
    retcode = __pkgctl(cv, pkgctl_executable, base_kernel_name)
    if retcode != 0:
        raise OSError(f"Something went wrong trying to clone repo!")


def __read_config(cv: int, path: PathLike) -> Dict[str, str]:
    out: Dict[str, str] = {}
    with open(path, 'r') as file:
        for linenum, line in enumerate(file.readlines()):
            line = line.strip()  # clear any trailing whitespace
            if line == '': continue  # skip blanks
            if line.startswith('#'):
                if not line.endswith("is not set"): continue  # skip comments
                key = line.split()[1]
                val = None
            else:
                if line.count('=') == 0:
                    __print(cv, -2, f"config_read: skipping line {linenum+1}, no val given")
                    continue
                key,val = line.split('=', 1)
            if key in out:
                __print(cv, -2, f"config_read: skipping duplicate key {key} on line {linenum+1}")
                continue
            out[key] = val
    return out


def __run_configmerge(cv: int, out_path: PathLike, in_path: PathLike, changes_paths: List[PathLike], check_against_current: Optional[bool] = False):
    # read current running config
    os.system("zcat /proc/config.gz > cur_config")
    __print(cv, 3, f"grabbed current config from /proc/config.gz to {os.curdir}/cur_config")
    current = __read_config(cv, "cur_config")
    __print(cv, 2, 'Loaded current config')
    # load base config -- shipped with kernel
    __print(cv, 3, f"grabbing unmodified config {in_path}...")
    config = __read_config(cv, in_path)
    __print(cv, 2, "Loaded unmodified config")
    # load all given configs
    changes = {}
    for path in changes_paths:
        __print(cv, 3, f"grabbing config changes file {path}...")
        c = __read_config(cv, path)
        __print(cv, 2, f"Loaded changes file {path}")
        for k,v in c.items(): changes[k] = v
        __print(cv, 3, f"...and successfully merged it with the current running changes dict.")
    # write changes
    __print(cv, 0, f"Loaded {len(changes_paths)} config override files, and accumulated {len(changes)} overrides.")
    with open(out_path, 'w') as file:
        for key,val in config.items():
            oldval = val  # keep copy of original
            if key in changes:
                # change found. overwrite
                val = changes.pop(key)
                current.pop(key, None) # remove from current if present
                if oldval == val:
                    __print(cv, -2, f"config_merge: key '{key}' is specified for change to '{val}', but value is already '{val}'. no change")
                else:
                    __print(cv, 2, f"config_merge: changed key '{key}' from '{oldval}' to '{val}'")
            elif check_against_current:
                # no change found. check for conflicts with current
                if key not in current:
                    __print(cv, 2, f"config_merge: new kernel config has key '{key}' that is not in current config (has val '{val}')")
                else:
                    curval = current.pop(key)
                    if val != curval:
                        __print(cv, -2, f"config_merge: key '{key}' changed, currently using '{curval}', vanilla config uses '{val}'")
                        if cv > -2 and __prompt("use current val instead of vanilla?", default=False): val = curval
            # write to outfile
            if val is None: file.write(f"# {key} is not set\n")
            else: file.write(f"{key}={val}\n")
    __print(cv, 2, f"Successfully wrote merged config, to {out_path}")
    # check for unused current
    for key,val in current.items():
        if val is None: val = "not set"
        else: val = f"'{val}'"
        __print(cv, 2, f"config_merge: key '{key}' removed in new config (current running config has this as '{val}')")
    # check for unused changes
    for key,val in changes.items():
        if val is None: val = "not set"
        else: val = f"'{val}'"
        __print(cv, -2, f"config_merge: overwrite key '{key}' not found in new config (has val '{val}' in overwrite files)")


def __run_change_pkgmeta(cv: int, base_kernel_name: str, new_pkgbase: str, new_pkgdesc: str):
    did_set = { "pkgbase": False, "pkgdesc": False }
    to_set = { "pkgbase": new_pkgbase, "pkgdesc": "'"+new_pkgdesc+"'" }
    # read file
    in_url_section = False  # used for detecting special case -- "${pkgbase}" in url (wont work, duh!)
    with open("PKGBUILD", 'r') as file:
        buf = file.readlines()
    if len(buf) == 0: raise OSError(f"PKGBUILD is empty!")
    __print(cv, 3, f"read PKGBUILD successfully")
    # change lines
    for i,line in enumerate(buf):
        for k,v in to_set.items():
            if   line.startswith("source="): in_url_section = True
            elif line.startswith(")") and in_url_section: in_url_section = False
            elif line.startswith(k):
                # match found. test if already found, otherwise, set to new val
                if not did_set[k]:
                    did_set[k] = True
                    __print(cv, 2, f"... set {k}={v}")
                    buf[i] = f"{k}={v}\n"
                else:
                    __print(cv, -2, f"... found multiple lines defining {k}! only changing first instance.")
            # the aforementioned special case. $pkgbuild in a url.
            elif in_url_section:
                if 'pkgbase' in line:
                    __print(cv, 2, f"... fixed '$pkgbase' appearing in url")
                    buf[i] = buf[i].replace('$pkgbase', base_kernel_name).replace('${pkgbase}', base_kernel_name)
    __print(cv, 3, f"applied PKGBUILD metadata changes in buffer")
    # write file
    with open("PKGBUILD", 'w') as file:
        file.writelines(buf)
    # warn of not sets
    for k,v in did_set.items():
        if not v:
            __print(cv, -2, f"Couldn't apply PKGBUILD metadata key {k} (tried to set to '{to_set[k]}')")


def __run_disable_docs(cv: int):
    # read file
    with open("PKGBUILD", 'r') as file:
        inbuf = file.readlines()
    if len(inbuf) == 0: raise OSError(f"PKGBUILD is empty!")
    __print(cv, 3, f"read PKGBUILD successfully")
    # lines to remove
    badlines = [
        "make htmldocs",     # from linux
        '"$pkgbase-docs"',   # from linux
        "make htmldocs &",   # from linux-hardened
        "local pid_docs=$!", # from linux-hardened
        'wait "${pid_docs}"' # from linux-hardened
    ]
    __print(cv, 3, f"commenting evil lines :", badlines)
    # change lines
    commented_something = False
    outbuf = []
    for i,line in enumerate(inbuf):
        cleaned_line = line.strip().lstrip()
        if cleaned_line in badlines:
            commented_something = True
            __print(cv, 2, f"... found and commented bad line {i} \"{cleaned_line}\"")
            if line.startswith(' '): line = '#' + line[1:]
            else: line = '# ' + line
        outbuf.append(line)
    # write file
    with open("PKGBUILD", 'w') as file:
        file.writelines(outbuf)
    # warn if didn't find anything
    if not commented_something:
        __print(cv, -2, f"didn't find any doc-making lines!")


def __run_modprobed_db(cv: int):
    # read file
    with open("PKGBUILD", 'r') as file:
        inbuf = file.readlines()
    if len(inbuf) == 0: raise OSError(f"PKGBUILD is empty!")
    __print(cv, 3, f"read PKGBUILD successfully")
    # change lines
    found = False
    outbuf = []
    for i,line in enumerate(inbuf):
        cleaned_line = line.strip().lstrip()
        if cleaned_line == "make -s kernelrelease > version":
            found = True
            outbuf.append('  make LSMOD="$HOME/.config/modprobed.db" localmodconfig\n')
            __print(cv, 2, f"... embedded modprobed-db")
        outbuf.append(line)
    # write file
    with open("PKGBUILD", 'w') as file:
        file.writelines(outbuf)
    # error if didn't find anything
    if not found:
        __print(cv, -3, f"couldn't embed modprobed-db!")
        raise Exception("Couldn't embed modprobed-db in PKGBUILD")


def __run_copy_patches(cv: int, paths: List[PathLike]):
    for path in paths:
        __print(cv, -3, f"Trying to copy patch file '{path}'...")
        try:
            _,filename = os.path.split(path)
            oldfilename = filename
            renamed = False
            while os.path.exists(filename):
                renamed = True
                filename = "copy-" + filename
            if renamed: __print(cv, 2, f"Patch named {oldfilename} already exists... renamed to {filename}")

            shutil.copyfile()
        except Exception as e:
            __print(cv, 2, f"Couldn't copy {path}, with error: ", e)
        else:
            __print(cv, 2, f"Copied path {path} successfully")


def __run_updpkgsums(cv: int):
    # check for root -- breaks makepkg
    if os.getuid() == 0: raise PermissionError("Cannot be root to run updpkgsums! All other users will lose access")
    __print(cv, 2, "root check passed. executing updpkgsums...")
    retcode = __updpkgsums(cv)
    if retcode != 0:
        raise OSError(f"Something went wrong running updpkgsums!")


def __run_makepkg(cv: int, makepkg_flags: Optional[str] = '', num_cores: Optional[int] = None):
    # check for root -- breaks makepkg
    if os.getuid() == 0: raise PermissionError("Cannot be root to run makepkg! All other users will lose access")
    __print(cv, 2, "root check passed. executing makepkg...")
    retcode = __makepkg(cv, makepkg_flags, num_cores)
    if retcode != 0:
        raise OSError(f"Something went wrong running makepkg!")


# util functions

def __flatten_dir(path: str, _depth: int = 0) -> list:
    # recursion limit
    _depth += 1
    if _depth > 10: raise RecursionError(f"Can't walk path {path}, subdirectory recursion limit(=10) met")
    # check if user-passed path is valid
    if not os.path.exists(path): return []
    out = []
    # is a dir, walk through and recurse
    if os.path.isdir(path):
        for f in os.listdir(path):
            out.extend(__flatten_dir(path+'/'+f, _depth=_depth))
    # not a dir, just return this
    elif os.path.isfile(path):
        out.append( os.path.abspath(path) )
    else:
        raise OSError("Path ")
    return out


def run(
    base_kernel_name:                   str,
    new_kernel_name:                    str,
    description:                        Optional[str]             = None,
    makepkg_flags:                      Optional[str]             = '',
    output_folder:                      Optional[PathLike]        = '.',
    config_overwrite_paths:             Optional[List[PathLike]]  = [],
    patches_paths:                      Optional[List[PathLike]]  = [],
    num_cores:                          Optional[int]             = 0,
    verbosity:                          Optional[int]             = 1,
    should_make_docs:                   Optional[bool]            = False,
    should_modprobed_db:                Optional[bool]            = False,
    should_interrupt:                   Optional[bool]            = False,
    check_base_config_against_current:  Optional[bool]            = False
) -> int:
    """ Runs the module based on the given settings. """

    # recover from NoneType args
    if not description:            description = ''
    if not makepkg_flags:          makepkg_flags = ''
    if not output_folder:          output_folder = '.'
    if not config_overwrite_paths: config_overwrite_paths = []
    if not patches_paths:          patches_paths = []
    if not num_cores:              num_cores = 0
    if not verbosity:              verbosity = 0

    # resolve all paths before chdir -- sum([[a,b,c], [x,y,z], ...], []) flattens the list to [a,b,c,x,y,z,...]
    config_overwrite_paths = sum([__flatten_dir(c) for c in config_overwrite_paths],[])
    patches_paths =          sum([__flatten_dir(p) for p in patches_paths],[])
    output_folder = os.path.abspath(output_folder)

    # check args
    verbosity = min(max(int(verbosity), -3), 3)
    if not makepkg_flags.startswith('-'): makepkg_flags = '-' + makepkg_flags
    if not 's' in makepkg_flags: makepkg_flags += 's'
    if not base_kernel_name: raise ValueError("Base kernel name cannot be empty")
    if not new_kernel_name: raise ValueError("New kernel name cannot be empty")
    if not description: description = f"custom {base_kernel_name} kernel"

    # show args
    __print(verbosity, 3, "")
    __print(verbosity, 3, "====================")
    __print(verbosity, 3, "")
    __print(verbosity, 3, f"Using base_kernel_name '{base_kernel_name}'")
    __print(verbosity, 3, f"Using new_kernel_name '{new_kernel_name}'")
    __print(verbosity, 3, f"Using description '{description}'")
    __print(verbosity, 3, f"Using makepkg_flags '{makepkg_flags}'")
    __print(verbosity, 3, f"Using {num_cores} cores" if num_cores else "Using all available cores")
    __print(verbosity, 0, "Using verbosity =", verbosity)
    __print(verbosity, 3, f"Using should_make_docs =", "YES" if should_make_docs else "NO")
    __print(verbosity, 3, f"Using should_modprobed_db =", "YES" if should_modprobed_db else "NO")
    __print(verbosity, 3, f"Using should_interrupt =", "YES" if should_interrupt else "NO")
    __print(verbosity, 3, f"Using check_base_config_against_current =", "YES" if check_base_config_against_current else "NO")
    __print(verbosity, 3, f"Using output_folder '{output_folder}'")
    if len(config_overwrite_paths) == 0:  __print(verbosity, 3, f"Using no config overrides")
    else:                                 __print(verbosity, 3, f"Using {len(config_overwrite_paths)} config override files:", '\n - '.join(['']+config_overwrite_paths))
    if len(patches_paths) == 0:  __print(verbosity, 3, f"Using no patch files")
    else:                        __print(verbosity, 3, f"Using {len(patches_paths)} patch files:", '\n - '.join(['']+patches_paths))
    __print(verbosity, 3, "")
    __print(verbosity, 3, "====================")
    __print(verbosity, 3, "")

    # warn about non-vanilla
    if base_kernel_name != "linux" and not verbosity == 3:
        __print(verbosity, -2, "WARNING: This tool is only verified to work on kernels using the vanilla 'linux'")
        __print(verbosity, -2, "kernel as a base. This script may not work, may skip something, or may crash")
        __print(verbosity, -2, "entirely. Your usage may vary. It is HIGHLY recommended to use the -i flag to")
        __print(verbosity, -2, "make sure the script will interrupt before committing to a write, to allow you")
        __print(verbosity, -2, "to manually inspect the config and PKGBUILD files.")
        if should_interrupt:
            if not __prompt("Continue?", default=True): exit(0)

    # enter tmpdir
    with tempfile.TemporaryDirectory() as tmpdir:
        __print(verbosity, 0, f"Running under tmpdir {tmpdir}")
        os.chdir(tmpdir)
        
        __print(verbosity, 0, f"Downloading kernel base '{base_kernel_name}'... ")
        __run_pkgctl(verbosity, base_kernel_name, pkgctl_executable=None)
        __print(verbosity, 2, f"Renaming kernel folder from '{base_kernel_name}' to '{new_kernel_name}'... ")
        os.rename(base_kernel_name, new_kernel_name)
        if should_interrupt: __interrupt("pkgctl ran successfully")
        
        __print(verbosity, 0, "Applying config overrides...")
        if l:=len(config_overwrite_paths):
            os.rename(f"{new_kernel_name}/config", "unmod_config")
            __print(verbosity, 2, f"... Unmodified config moved to {os.curdir}/unmod_config")
            __run_configmerge(verbosity, f"{new_kernel_name}/config", "unmod_config", config_overwrite_paths, check_base_config_against_current)
        else:
            __print(verbosity, 3, "... No config overrides to apply.")
        if should_interrupt: __interrupt("Config changes applied")
        
        __print(verbosity, 0, "Changing package metadata in PKGBUILD...")
        os.chdir(new_kernel_name)
        __run_change_pkgmeta(verbosity, base_kernel_name, new_kernel_name, description)
        if not should_make_docs:
            __print(verbosity, 0, "Removing docs from PKGBUILD...")
            __run_disable_docs(verbosity)
        if should_modprobed_db:
            __print(verbosity, 0, "Adding modprobed-db line...")
            __run_modprobed_db(verbosity)
        if should_interrupt: __interrupt("PKGBUILD changes applied")
        
        __print(verbosity, 0, "Copying .patch files to working directory...")
        __run_copy_patches
        if should_interrupt: __interrupt("Patches copied")
        
        __print(verbosity, 0, "Running updpkgsums... (this will download the base kernel)")
        __run_updpkgsums(verbosity)
        if should_interrupt: __interrupt("Base kernel downloaded. Interrupting just before makepkg runs.")

        __print(verbosity, 0, "Running makepkg...")
        __run_makepkg(verbosity, makepkg_flags, num_cores)
        __print(verbosity, 2, f"Moving packages to specified directory '{output_folder}'...")
        # this uses os.system so that we can use * (wildcard) to catch both packages (kernel and headers) regardless of version
        os.system(f'mv "{new_kernel_name}"* "{output_folder}"')
        if should_interrupt: __interrupt("Done, exiting after this")
        
        __print(verbosity, 0, "\n==========\n COMPILED \n==========\n")
        __print(verbosity, 0, f"To install, cd into the output directory ({output_folder}) and run pacman -U\n")
        __print(verbosity, 0, f"Exiting and cleaning up tmpdir {tmpdir}")


# run() is called from __main__.py, with args from argparse
# optionally, pass them in programmatically
