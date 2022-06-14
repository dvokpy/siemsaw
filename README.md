# Siemsaw
***
Written solely in Python, Siemsaw is a tool designed to mass query evtx log using chainsaw.

## General Info
***
Siemsaw currently runs on linux and windows exclusively, support for mac will be added in the future. **Chainsaw must be installed prior to running the tool**. Siemsaw currently supports the sigma hunt and regex search function of chainsaw.

## Installation
***
1. Download siemsaw zip file
2. Unpack zip
   1. `unzip <siemsaw_zip_dir> <siemsaw_install_dir>` (linux)
   2. Using 7zip, select the zip file and extract (windows)
3. Change to the the directory with the siemsaw python binary`cd <siemsaw_install_dir`
4. Run siemsaw `(\ or /)siemsaw.py`
5. siemsaw will now generate the config, input chainsaw binary location. The config can be changed if you mess up.

## Usage
***
Once you the config is properly generated you will be able to use the tool. 2 folders will be created, output_dir and evtx_repo. Drop all evtx files in the evtx repo if you don't want to input them manually. All queries results (if there are any) will be placed in the output_dir. For the sigma hunt, selecting to manually input rules can be tedious, if you go to the sigma rule directory under the chainsaw_dir you can just place your own diretory there.

## Technologies
***
- Chainsaw (https://github.com/countercept/chainsaw)
- Python 3.8.10

#### TODO
- [x] Build Siemsaw cmdline
- [x] Integrate windows and linux compatability
- [ ] Flush out robust help pages
- [ ] Add auto chainsaw install
- [ ] Integrate event id querying
- [ ] Add evtx pointing
- [ ] Add output parsing and displaying
- [ ] Add remote evtx gathering
- [ ] Build GUI
- [ ] Build in mac support
