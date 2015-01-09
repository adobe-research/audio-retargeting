# audio-retargeting

This repository contains:

* `radiotool` -- The [ucbvislab/radiotool](https://github.com/ucbvislab/radiotool) library. 
  > `radiotool` is included here as a [git subrepo](https://github.com/ingydotnet/git-subrepo).  This means that a copy of the source is available here and can be worked on locally.  (But if you want to pull a newer version from [ucbvislab/radiotool](https://github.com/ucbvislab/radiotool) or submit changes to it, you'll need to install the [git-subrepo](https://github.com/ingydotnet/git-subrepo) commands.)

* `retarget.py` -- A simple CLI front-end to the retargeting features of `radiotool`


---

## retarget.py

The CLI is a command named `retarget.py` or `retarget` (if you want to build it, see below).  For example, to retarget a song to be 30 seconds long, use:

```
$ retarget.py -l 30 mysong.wav
input:	mysong.wav
output:	mysong-30.wav
length:	30
change_points:
start:	True
end:	True
cache:	/Users/ronen/Library/Caches/retarget
Retargeting...
Wrote mysong-30.wav
```
	
This script uses [radiotool](https://github.com/ucbvislab/radiotool)'s caching mechanism: The first time you run it for a given input file will take some time to analyze the song and will cache the .  Subsequent runs with different options for the same input will be very fast.

For complete usage instructions, run:

```
$ retarget.py --help
```

---

## Installation

### Prerequisites: 

* *Developers tools:*  You need to have a working development environment.  On OS X this could mean running `xcode-select --install`

* *Package manager:* On OS X it's good to use [homebrew](http://brew.sh) to simplify installing various dependencies.  In a `bash` or `zsh` shell:

		$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

  [homebrew](http://brew.sh) can then also check that your development environment is OK is in order:

      $ brew doctor

* *Python:* You need to have a working installation of python 2.7.*.  On OS X, the system python should work, but you may want to install `/usr/local/bin/python` using [homebrew](http://brew.sh), to get the latest and to avoid needing to `sudo` in order to install the necessary python packages.

		$ brew install python


### Installing radiotool and retarget.py:

Just run the install script:

	$ python install.py

This can take a while to download and compile the various modules.  It's OK to run the script multiple times.  When all is installed, the output should look something like:

```
$ python install.py
*** External libraries ***
libsndfile          OK  [1 of 2]
libsamplerate       OK  [2 of 2]

*** External python modules ***
cython              0.21.1    [1 of 7]
numpy               1.9.1     [2 of 7]
scipy               0.14.0    [3 of 7]
matplotlib          1.4.2     [4 of 7]
scikits.audiolab    0.11.0    [5 of 7]
scikits.samplerate  0.3.3     [6 of 7]
librosa             0.3.1     [7 of 7]

*** radiotool ****
radiotool 0.4.3

*** retarget.py ***
Installed /usr/local/bin/retarget.py
```

This both installs `retarget.py` as a global executable, and installs `radiotool` as a global python module that you can use in other projects.  (However, retarget.py imports radiotool from the local subrepo, so you can make changes in the subrepo and test them locally without needing to install.)

#### Notes:

* If [libsndfile](http://www.mega-nerd.com/libsndfile/) or [libsamplerate](http://www.mega-nerd.com/SRC/) aren't already installed, the script will attempt to install them using `brew`.  If you don't have `brew`, you can install them manually.

* `radiotool` and `retarget.py` require the latest versions of the external modules as listed in the above output.  But this script doesn't check python module versions; if any version of a python module (including `radiotool`) is already installed, this script won't try to override it with a newer version.  So if you already have older versions installed and need to update them, you'll need to do that manually (using `pip install --upgrade`)

* Installing [scipy](http://www.scipy.org) is sometimes problematic.  It may require having a fortran compiler that's compatible with the compiler which build python.  If you have trouble, maybe one of these discussions might help:
    
    * [how-to-install-scipy-with-pip-on-mac-mountain-lion-os-x-v10-8](http://stackoverflow.com/questions/12092306/how-to-install-scipy-with-pip-on-mac-mountain-lion-os-x-v10-8)
    * [numpy_ox_x_10_9.sh](https://gist.github.com/goldsmith/7262122)
    * [cannot-pip-install-numpy-on-os-x-yosemite](http://stackoverflow.com/questions/26653768/cannot-pip-install-numpy-on-os-x-yosemite)
    
    See also the official installation instructions at [scipy.org/install](http://www.scipy.org/install.html)
    
* Radiotool gets installed from the local subrepo source rather than using `pip`, so any changes you make locally will get installed.


### (Optional) Creating a standalone `retarget` executable

You can use [pyinstaller](https://github.com/pyinstaller/pyinstaller) to create a command that you can give to others, which they then can run without needing to install anything.

Unfortunately `radiotool` uses some libraries that tickle a bug in the current official release (2.1) of `pyinstaller`.  This has been fixed for future releases, but for now you need to install the latest version of pyinstaller from the source:

		$ cd /some/other/work/directory
    	$ git clone https://github.com/pyinstaller/pyinstaller.git
	    $ cd pyinstaller
        $ python setup.py install

You can then run pyinstaller, with some necessary magic options for it to succesfully do the build.

		$ cd retarget.py
		$ pyinstaller \
			--onefile \
			--hidden-import=scipy.special._ufuncs_cxx \
			--hidden-import=sklearn.utils.sparsetools._graph_validation \
			--hidden-import=sklearn.utils.sparsetools._graph_tools \
			--hidden-import=sklearn.utils.lgamma \
			--hidden-import=sklearn.utils.weight_vector \
			--hidden-import=sklearn.neighbors.typedefs \
			--strip \
			--log-level=ERROR \
			retarget.py
			
(You may see `RuntimeError: The WebAgg backend requires Tornado.` and `UserWarning: error getting fonts from fc-list`.  These can be safely ignored.)

The resulting executable is`dist/retarget`.  It can be run by anyone with a similar platform to the one you build it on, without needing to perform any of the installation steps listed above.

    	$ dist/retarget --help
	    ...
    	$ cp dist/retarget /some/shared/bin/directory

