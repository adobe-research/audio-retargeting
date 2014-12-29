# retarget-py

A simple CLI front-end to the retargeting features of--and installation instructions for--the [ucbvislab/radiotool](https://github.com/ucbvislab/radiotool) library.

The CLI is a command named `retarget.py` or `retarget` (depending on how it's installed, see below).  For example, to retarget a song to be 30 seconds long, use:

```
$ retarget -l 30 mysong.wav
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
$ retarget --help
```

## Installation

Prerequisites: 

* *Developers tools:*  You need to have a working development environment.  On OS X this could mean running `xcode-select --install`

* *Package manager:* On OS X it's good to use [homebrew](http://brew.sh) to simplify installing various dependencies.  In a `bash` or `zsh` shell:

      $ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

  [homebrew](http://brew.sh) can then check that your development environment is OK is in order:

      $ brew doctor


* *Python:* You need to have a working installation of python 2.7.*.  On OS X, the system python should work, but you may want to install `/usr/local/bin/python` using [homebrew](http://brew.sh), to get the latest and to avoid needing to `sudo` in order to install the necessary python packages.

      $ brew install python


### Installing radiotool

1. [radiotool](https://github.com/ucbvislab/radiotool) requires that your system have [libsndfile](http://www.mega-nerd.com/libsndfile/) and [libsamplerate](http://www.mega-nerd.com/SRC/) installed.  On OS X, the easest way to install them is using [homebrew](http://brew.sh):

        $ brew install libsndfile libsamplerate
    
1. To be able to install [radiotool](https://github.com/ucbvislab/radiotool) you first need to install various other python libraries explicitly:

		$ pip install cython numpy scipy matplotlib 
  		
    Many of these dependencies would be handled automatically, but it's a good idea to do this separately in case anythong goes wrong.   For me all the above currently installs without a hitch on OS X 10.10.1, but YMMV.
    
    In particular, installing [scipy](http://www.scipy.org) is slow sometimes problematic.  If you have trouble, maybe one of these discussions might help:
    
    * [how-to-install-scipy-with-pip-on-mac-mountain-lion-os-x-v10-8](http://stackoverflow.com/questions/12092306/how-to-install-scipy-with-pip-on-mac-mountain-lion-os-x-v10-8)
    * [numpy_ox_x_10_9.sh](https://gist.github.com/goldsmith/7262122)
    * [cannot-pip-install-numpy-on-os-x-yosemite](http://stackoverflow.com/questions/26653768/cannot-pip-install-numpy-on-os-x-yosemite)
    
    See also the official installation instructions at [scipy.org/install](http://www.scipy.org/install.html)
    
1. Once the above are installed, a few more to be installed next (these can't be done as a single step with the above because of dependencies in their setup definitions):
    
    	$ pip install scikits.audiolab scikits.samplerate librosa
    	
   These should all install without any trouble.
       
1. The latest version of [radiotool](https://github.com/ucbvislab/radiotool) is not currently available in `pip` so you must install from the source:

    	$ git clone https://github.com/ucbvislab/radiotool.git
	    $ cd radiotool
        $ python setup.py install

   This should be quick and easy.


### Installing retarget.py

Once you've installed radiotool as per the above instructions, installing `retarget.py` should be easy:

    	$ git clone https://github.com/ronen/retarget-py.git
	    $ cd retarget-py
        $ python setup.py install
        
This will install `retarget.py` into your path.  This is a python script that depends on the succesfull installation of radiotool and its dependencies.

### (Optional) Creating a standalone `retarget` executable

Once you've installed `radiotool` and `retarget.py`, you can use [pyinstaller](https://github.com/pyinstaller/pyinstaller) to create a command that you can give to others, which they then can run without needing to install anything.

Unfortunately `radiotool` uses some libraries that tickle a bug in the current official release (2.1) of `pyinstaller`.  This has been fixed for future releases, but for now you need to install the latest version of pyinstaller from the source:

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

