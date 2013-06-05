"""Find duplicate files inside a directory tree."""

from os import walk, remove, stat, sep, path, makedirs
from os.path import join as joinpath
from md5 import md5
import itertools, shutil

def find_uniques( dir1, dir2 ):
    """Find duplicate files in directory tree."""
    filesizes = {}
    # Build up dict with key as filesize and value is list of filenames.
    for path, dirs, files in itertools.chain(walk(dir1), walk(dir2)):
        for filename in files:
            filepath = joinpath( path, filename )
            filesize = stat( filepath ).st_size
            print( "found file '" + filepath + "' with file size '" + str(filesize) + "' bytes" )
            filesizes.setdefault( filesize, [] ).append( filepath )
    unique = set()
    myuniques = []
    # We are only interested in lists with more than one entry.
    for files in [ flist for flist in filesizes.values() if len(flist)>1 ]:
        for filepath in files:
            with open( filepath ) as openfile:
                filehash = md5( openfile.read() ).hexdigest()
            if filehash not in unique:
                unique.add( filehash )
                myuniques.append( filepath )
                print("found an unique file :: '" + str(filepath) + "'" )
    return myuniques
    

def create_filepath_and_directories( dir1, dir2, srcdir, filepath ):
    """Removes the source directorie paths from the filepath"""
    #print("NEW FILEPATH ~~~~~~~  " + str(filepath))
    if dir1 in filepath:
        f = filepath.replace(dir1, '')
    elif dir2 in filepath:
        f = filepath.replace(dir2, '')
    else:
        f = filepath
        
    print("Reduced filepath :: " + str(f))
    
    file = f.split( sep )[ len( f.split( sep ) ) - 1 ]
    print( "file :: " + str( file ) )
    dirs = f.replace( file, "" )
    dirs = srcdir + sep + dirs
    if not path.exists(dirs):
        if ARGS.perfcopy == True:
            print("making directories :::> " + str( dirs ) )
            makedirs( dirs )
    
    return f
    
def create_filepath( fp ):
    if "\\" in fp:
        fps = joinpath( * fp.split("\\") ) 
    elif "/" in fp:
        fps = joinpath( * fp.split("/") ) 
    else:
        fps = fp
    return fps

if __name__ == '__main__':
    from argparse import ArgumentParser
    
    PARSER = ArgumentParser( description='Copies files from 2 seperate directories into 1, ignoring duplicates' )
    PARSER.add_argument( '-perfcopy', action='store_true', help='perform copy of files' )
    PARSER.add_argument( '-dir1', metavar='<path>', default = '', help='Source Directory 1' )
    PARSER.add_argument( '-dir2', metavar='<path>', default = '', help='Source Directory 2' )
    PARSER.add_argument( '-destdir', metavar='<path>', default = '', help='Destination Directory for copy' )
    ARGS = PARSER.parse_args()

    if ARGS.dir1 == '' or ARGS.dir2 == '':
        print("Either dir1 or dir2 was empty")
    else:
        d1 = create_filepath(ARGS.dir1)
        d2 = create_filepath(ARGS.dir2)
        print("performing multi-directory copy....")
        srcdir = ""
        if ARGS.destdir != '':
                srcdir = create_filepath( ARGS.destdir )
                print( "source directory given ::: " + str( srcdir ) )
                if not path.exists(srcdir):
                    print("making destination directory === " + str(srcdir))
                    makedirs(srcdir)
        
        UNQ = find_uniques( d1, d2 )
        print '%d UNIQUE files found.' % len(UNQ)
        
        for f in sorted( UNQ ):
            nf = create_filepath( f )
            print( '\n\r\n\rnext filepath -- ' + str(nf) )
            if srcdir != '':
                newf = create_filepath_and_directories( d1, d2, srcdir, nf)
                newf = joinpath(srcdir, newf)
                if ARGS.perfcopy == True:
                    print("EXECUTING COPY -- " + str(nf) + " to " + str(newf))
                    shutil.copy2(nf, newf)
        print("\n\r\n\r\n\rFINISHED COPYING FILES!!!!!!!!!!!!!!!!!!!")
        print("Total files transfered ::: " + str(len(UNQ)))


