##############################################################################
#
# Copyright (c) 1999 Jonothan Farr and contributors
# All rights reserved. Written by Jonothan Farr <jfarr@speakeasy.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission
#
# Disclaimer
#
#   THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#   IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
#   OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#   IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
#   INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
#   NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
#   THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# In accordance with the license provided for by the software upon
# which some of the source code has been derived or used, the following
# acknowledgement is hereby provided:
#
#      "This product includes software developed by Digital Creations
#      for use in the Z Object Publishing Environment
#      (http://www.zope.org/)."
#
##############################################################################
from io import BytesIO
from io import StringIO

from OFS.Image import File
from OFS.Image import Image
from OFS.Image import Pdata
from ZPublisher.HTTPRequest import FileUpload


BUFFER_SIZE = 1 << 16


def _read_data(self, file):
    # We do not want to load the whole file into memory, so just
    # get the file size and return a faked Pdata object.
    if isinstance(file, (bytes, str)):
        size = len(file)
        if size < BUFFER_SIZE:
            return file, size
        # Big string: cut it into smaller chunks
        if isinstance(file, bytes):
            file = BytesIO(file)
        else:
            file = StringIO(file)

    if isinstance(file, FileUpload) and not file:
        raise ValueError('File not specified')

    if hasattr(file, '__class__') and file.__class__ in (Pdata, Sdata):
        size = len(file)
        return file, size

    pos = file.tell()
    file.seek(0, 2)
    size = file.tell()
    file.seek(pos, 0)
    return Sdata(file, size), size


class StreamingFile(File):
    """ Wrapper around OFS.Image.File """
    _read_data = _read_data


class StreamingImage(Image):
    """ Wrapper around OFS.Image.Image """
    _read_data = _read_data


class Sdata(Pdata):
    """ Streaming wrapper for possibly large data """
    # Imitates OFS.Image.Pdata
    # Make it a subclass of Pdata to be conform with ExternalEditor

    _p_changed = 0

    def __init__(self, file, fsize, _offset=0):
        self.file = file
        self.fsize = fsize
        self.offset = _offset

    def __getitem__(self, key):
        size = min(BUFFER_SIZE, len(self))
        if isinstance(key, int):
            if key > size:
                return b''

            self.file.seek(self.offset+key, 0)
            return self.file.read(1)

    @property
    def data(self):
        return self[0:BUFFER_SIZE]

    @property
    def next(self):
        offset = self.offset + BUFFER_SIZE
        if offset < self.fsize:
            return Sdata(self.file, self.fsize, offset)

    def __len__(self):
        return self.fsize - self.offset

    def __bytes__(self):
        self.file.seek(self.offset, 0)
        return self.file.read()
