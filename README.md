# audio-retargeting

This repository provides an OS X executable named `retarget` which demonstrates the ability to change the length of a piece of music.  (It also contains the Python source, for those who want to delve deeper or run on a different platform; see documentation installation details below)

## Download the `retarget` command:

Download the executable from https://github.com/adobe-research/audio-retargeting/releases/download/v0.2.0/retarget 

## `retarget` Usage:

The general form of the command is:

```
$ retarget [options] INPUT.wav

```

Its default behavior (without any options) is to produce a version of the input music, retargeted to 60 seconds long.  For an input name mytrack.wav, the output by default will be named mytrack-60.wav

Note that the first time you run this program for a given input file, it will take some time to analyze the song -- but it will cache the analysis.  Subsequent runs for the same input file will be very fast, even with different retargeting options.

The program has two main capabilities:

* **_Always:_ Retarget to a new length.**  You can choose the length in seconds via the `--length` option, e.g.

        $ retarget --length 120 mytrack.wav

  By default the output music will start and end with the start and end of the input music (and the middle will be trimmed or extended as needed).  The `--no-start` and `--no-end` options allow the program to start or end in the middle of the music so it will need to make fewer changes to meet the target length.

* **_Optionally:_ Place interesting musical "changes" at specific times.**  You can use the `--change` option to specify a time in seconds at which the program should place a musical change.  E.g.

        $ retarget --length 120 --change 32 mytrack.wav
        
  You can specify the `--change` argument more than once but it may have trouble meeting the requirements if you give too many.  Note also that if you specify change times, that implies `--no-start` and `--no-end`.
  
For a complete list of options, run `retarget --help`


-------
## Python Source Installation and Use

For those who want to run `retarget` on a platform other than OS X or want to delve deeper into the Python code...


This repository contains:

* `radiotool` -- The [ucbvislab/radiotool](https://github.com/ucbvislab/radiotool) library. 
  > `radiotool` is included here as a [git subrepo](https://github.com/ingydotnet/git-subrepo).  This means that a copy of the source is available here and can be worked on locally.  (But if you want to pull a newer version from [ucbvislab/radiotool](https://github.com/ucbvislab/radiotool) or submit changes to it, you'll need to install the [git-subrepo](https://github.com/ingydotnet/git-subrepo) commands.)

* `retarget.py` -- A simple CLI front-end to the retargeting features of `radiotool`.  This is the script that gets compiled (using [pyinstaller](https://github.com/pyinstaller/pyinstaller)) to produce the standalone `retarget` command.  See Usage instructions above for how to run it, once you have installed the necessary environment as described below.

## Installation


### Prerequisites: 

* *Developers tools:*  You need to have a working development environment.  On OS X this could mean running `xcode-select --install`

* *Package manager:* On OS X it's good to use [homebrew](http://brew.sh) to simplify installing various dependencies.  In a `bash` or `zsh` shell:

		$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

  [homebrew](http://brew.sh) can then also check that your development environment is OK is in order:

      $ brew doctor

* *Python:* You need to have a working installation of python 2.7.*, including `pip`.  On OS X, the system python does not include `pip` by default and will likely require you to `sudo` to install the necessary components. It's highly recommended that you use `brew` to install python 2.7.9 (which includes `pip`) into `/usr/local/bin`:

		$ brew install python


### Installing radiotool and retarget.py:

If you are familiar with [virtualenv](http://virtualenv.readthedocs.org) or [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org) you could create an empty virtualenv to install this all in.

This repo includes an installation script that, if all goes well, will take care of everything for you:

	$ python install.py

(If all *doesn't* go wel, an installation log will be left in `install.log`)

This can take a while to download and compile the various modules.  It's OK to run the script multiple times, it won't try to re-install things that are already installed.  When all is installed, the output should look something like:

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


### (Optional) Creating the standalone `retarget` executable

You can use [pyinstaller](https://github.com/pyinstaller/pyinstaller) to create the standalone `retarget` command which you can give to others who work on the same platform as you, and which they then can run without needing to install anything.

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
			
(You may see errors `RuntimeError: The WebAgg backend requires Tornado.` and/or `UserWarning: error getting fonts from fc-list`.  These can be safely ignored.)

The resulting executable is`dist/retarget`.  It has all the necessary libraries and python environment encapsulated in it -- so it can be run by anyone with a similar platform to the one you build it on, without needing to perform any of the installation steps listed above.

    	$ dist/retarget --help
	    ...
    	$ cp dist/retarget /wherever/you/want/it/to/live

