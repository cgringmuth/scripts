#!/usr/bin/env python

'''
Created on Dec 10, 2013

@author: Christoph Hoffmann
'''

import argparse
from os.path import expanduser
import os
import subprocess

# versioning follows the semantic versioning http://semver.org/
__version__ = (0,0,1)
__description__ = """Synchronize the a folder specified by src to a destination
specified by dst. If src is not provided, the framework assumes the current 
home folder to be the source.
"""

__exclude_lst = []
__exclude_lst.append("Dropbox/")
__exclude_lst.append("Downloads/")
__exclude_lst.append("Music/")
__exclude_lst.append("tmp/")
__exclude_lst.append("test/")
__exclude_lst.append("bin/")

__exclude_lst.append(".*")     # ignore all hidden files/folders

# __exclude_lst.append(".thumbnails")
# __exclude_lst.append(".cache")
# __exclude_lst.append(".mozilla")

__include_lst = []
__include_lst.append('.vimrc')
__include_lst.append('.profile')
__include_lst.append('.bashrc')

_home_folder = expanduser("~")
_home_folder += os.sep

def parse_args():
    parser = argparse.ArgumentParser(description=__description__)
    
    parser.add_argument(
        "-v", 
        "--verbose", 
        help="increase output verbosity.", 
        action="store_true"
    )
    
    src_help_str = """the folder which should be synced. Normally this is the 
home folder of the system (defined by ~)"""
    parser.add_argument(
        "--src", 
        default=_home_folder,
        help=src_help_str
    )
    
    dst_help_str = """the destination folder to which everything will be 
synchronized"""
    parser.add_argument(
        "--dst",
        required=True, 
        help=dst_help_str
    )
    
    args = parser.parse_args()
    
    return args


def get_exclude_list():
    return ["--exclude="+ent for ent in __exclude_lst]


def get_include_list():
    return ["--include="+ent for ent in __include_lst]


def sync(args):
    src = args.src
    dst = args.dst
    arg_lst = []
    
    # using rsync: http://www.dedoimedo.com/computers/rsync-guide.html or 
    arg_lst.append("rsync")     # http://rsync.samba.org/
    arg_lst.append("-a")    # archive options. same as -rlptgoD
    arg_lst.append("-v")    # verbose output
    arg_lst.append("-s")    # do not allow remote shell to interpret characters
    arg_lst.append("-h")    # summary in a human-readable format
    
    arg_lst.extend(get_exclude_list())
    arg_lst.extend(get_include_list())
    
#     arg_lst.append("--delete")     # delete file(s) which have been removed from source
    
    arg_lst.append(src)
    arg_lst.append(dst)
    
    subprocess.call(arg_lst)


def main():
    args= parse_args()

    answ = raw_input("sync {} to {} [y/N]: ".format(args.src, args.dst))
    if answ.lower() in ('yes', 'y'):
        print '... start syncing'
        sync(args)

if __name__ == '__main__':
    main()
