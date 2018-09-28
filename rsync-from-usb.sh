#!/bin/sh
SOURCE_DIR=/cygdrive/d/veracode-load/
DEST_DIR=/cygdrive/c/proj/veracode-load/

rsync -avz --exclude-from=./exclude_rsync --log-file=./rsync.log $SOURCE_DIR $DEST_DIR
cat ./rsync.log
rm -f ./rsync.log
