# KernelMaker
Automate building and updating your custom kernel with ease. KernelMaker can automatically detect and fix common errors, like unknown pgp keys or `pkgbase` in a URL.

*It's already not that hard but I'm lazy and don't want to manually sift through files every time, so I wrote this. :3*

# Installing

```bash
python3 -m pip install kernelmaker
python3 -m kernelmaker --help
```

Easy.

# Usage

My workflow using this tool is the following:
1. There exists a folder, `~/build`, that contains config overrides and patches:
```
build
├── configs
│   ├── vivepro2-configs
│   ├── apparmor-enable
│   └── perf-configs
└── patches
    └── OpenRGB.patch
```
2. Any time I feel like updating to the latest kernel, I run `kernelmaker`:
```bash
cd ~/build
python3 -m kernelmaker                         \
    linux-hardened linux-custom                \
    -d "Custom kernel based on linux-hardened" \
    -c configs -p patches                      \
    --use-modprobed-db --makepkg-flags="-sCfL"
```
3. After that finishes I just install the new kernels:
```
pacman -U linux-custom-*
# in case this is a new kernel, repopulate grub.cfg
grub-mkconfig -o /boot/grub/grub.cfg
```

In actuality I have this all in a shell script, but, y'know.

# Just wanna do it yourself, for curiosity or paranoia's sake?

The script really is quite simple, most of the lines of code are value type checks and the like. If you already know what you want, go ahead and do it yourself:

If you don't much care to keep the build files around after generating your new custom kernel, you can make a temporary directory in RAM (`/tmp`) to make things faster:
```
tmpdir = $(mktemp -d)
cd tmpdir
```
Note that `/tmp` is cleared when you shut down or reboot, so any customization will be lost.

(Alternatively, just use the folder of your choice, and it'll be saved just fine.)

### Downloading the kernel build files

You'll need to have the `extra/devtools` package installed to use pkgctl and make.

First, The base kernel config files can be downloaded:

```bash
# change 'linux' to the kernel of your choice, e.x. linux-hardened or linux-zen
pkgctl repo clone --protocol=https linux
cd linux
```

This should result in a directory tree like the following (the top-level directory has the name of the base kernel):
```
linux
├── config
├── keys
│   └── pgp
│       ├── 647F28654894E3BD457199BE38DBBDC86092693E.asc
│       ├── 83BC8889351B5DEBBB68416EB8AC08600F108CDF.asc
│       └── ABAF11C65A2970B130ABE3C479BE3E4300411886.asc
└── PKGBUILD
```

Don't worry about the `keys` folder. The two files to edit are `PKGBUILD` and `config`.

### Setting new kernel name and description

The file that configures the metadata of the package is the `PKGBUILD` file.

The `PKGBUILD` file will have lines near the top that should look something like:
```makefile
pkgbase=linux      # <-- EDIT THIS ONE
pkgver=6.6.9.arch1
pkgrel=1
pkgdesc='Linux'    # <-- AND THIS ONE
```
Note the two lines with comments, `pkgbase` and `pkgdesc`. You can, **and should,** edit them. (If you know what you're doing, go ham. Edit what you want.)

Note that the pacman package name and kernel name (in e.x. neofetch) will be whatever is in `pkgbase`. This is why you should change these values -- if you make a fancy shiny new kernel, but don't change the name from `linux`, it'll be replaced as soon as there's a new kernel release by the base kernel. All your changes and custom configuration will be lost.

### Disabling docs
A large chunk of the compilation time will be just generating documentation. It's pretty safe to skip these.

Further down in the `PKGBUILD` file you'll probably find the following:
```makefile
build() {
  cd $_srcname
  make all
  make htmldocs  # <-- COMMENT THIS LINE
}
```
Same applies here:
```makefile
pkgname=(
  "$pkgbase"
  "$pkgbase-headers"
  "$pkgbase-docs"     # <-- COMMENT THIS LINE
)
```

### Main config
The main config file (named, well, `config`) is where the kernel configuration parameters are. Most values are a simple `y` or `n`, or `m` to install it as a module, or a special `is not set` with that line commented. Some are a little more, but those are mostly names, descriptions, lists of modules, etc. Nothing too exquisite.

A sample from the linux-6.6.9 kernel, more specifically the kernel hz regulators:
```conf
# CONFIG_HZ_100 is not set
# CONFIG_HZ_250 is not set
CONFIG_HZ_300=y
# CONFIG_HZ_1000 is not set
CONFIG_HZ=300
CONFIG_SCHED_HRTICK=y
```

If you're curious about what the current kernel is using as `config`, `zcat` it to a file or file viewer, or `zgrep` the key you're looking for:
```bash
zcat /proc/config.gz | most
zgrep "CONFIG_SCHED_HRTICK" /proc/config.gz
```
This DOES have to be `zcat` and `zgrep`, not just regular `cat` or `grep`, because it's a gzip-compressed file. You could also cat it into gunzip and cat/grep that, but you do you.

### Patch files

Sometimes it may be useful to apply a patch file, like in the case of the [OpenRGB .patch file](https://github.com/CalcProgrammer1/OpenRGB/blob/master/OpenRGB.patch) for certain motherboards. This is as simple as placing them in the base kernel directory, and makepkg will detect and apply them:

```
linux
├── config
├── keys
│   └── ...
├── OpenRGB.patch
└── PKGBUILD
```

### Compilation and installation

Once all your changes are made, patches in place, etc etc, run `updpkgsums` and `makepkg`.

NOTE THAT YOU SHOULD NOT BE THE ROOT USER TO COMPILE THE KERNEL. DOING SO WILL CAUSE `makepkg` TO ERROR AND THINGS MIGHT BREAK.

Note that `updpkgsums` will download the base kernel source code; what you downloaded before, with `pkgctl`, was just the configuration files.
```bash
updpkgsums
```

I usually use the following makepkg flags, although `-s` will do just fine. If you wish to use all available cores to compile with, use `-j ${nproc}` as your makeflags; otherwise, put the number of cores you want to use. If you don't want to know how long the compilation took, just remove the `time env` part of the second line.
```bash
export MAKEFLAGS="-j 8"
time env makepkg -sCcfL
```

To install the packages once they're built, install them with pacman (might need to use `sudo` for this):
```bash
pacman -U <KERNEL_NAME>-*
# ex: pacman -U linux-custom-*
```
**Make sure both the kernel AND headers packages get installed. Just the headers means you won't be using the custom kernel, and just the kernel means you won't be able to compile any packages for your kernel.**

If pacman doesn't automatically do it, you'll need to refresh your bootloader with the new kernels to use them, e.x. for `grub`, run:
```bash
grub-mkconfig -o /boot/grub/grub.cfg
```
...to re-detect the new kernels in `/boot` and add them as entries.
