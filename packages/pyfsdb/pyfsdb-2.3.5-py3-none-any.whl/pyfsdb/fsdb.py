#!/usr/bin/python

"""
pyfsdb.Fsdb - class for reading and writing Fsdb files

# creating a Fsdb object attached to a file to read:
f = pyfsdb.Fsdb("data.fsdb")

# Getting column numbers for named columns:
name_col = f.get_column_number('name')
time_col = f.get_column_number('time')

# iterating over a fsdb file:
for data in f:
    print(data[name_col] + ".." + data[time_col])

# iterating over a fsdb file with dictionaries:
# (slower)
f = pyfsdb.Fsdb("data.fsdb", return_type=pyfsdb.RETURN_AS_DICTIONARY)
for data in f:
    print(data['name'] + ".." + data['time'])

# writing FSDB formatted data out
# (note: a single Fsdb object can be set up for both reading and writing)
f = pyfsdb.Fsdb(out_file = "my.fsdb")
f.out_column_names = ['foo','bar','baz']
f.out_separator = "\t"
f.append(["a", "b", "c"])
f.close() # closes and writes trailing comments

# (if the FSDB object is also reading a file, default values
# for out_column_names and out_separator will be taken from the input file).

# Convenience wrappers

# foreach: return a list of the values from the second column
f = pyfsdb.Fsdb("data.fsdb")
results = f.foreach(lambda x: x[2])

# filter: reads the input file, filters it using myfilt, and writes to output
def myfilt(row):
    return [int(row['mycol']) * 2]

f = pyfsdb.Fsdb("data.fsdb", out_file="output.fsdb")
results = f.filter(myfilt)

"""

import sys
import os
import io

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

RETURN_AS_ARRAY = 1
RETURN_AS_DICTIONARY = 2

incoming_type_converters = {
    # python doesn't have different int sizes
    "c": int,
    "C": int,
    "s": int,
    "S": int,
    "i": int,
    "l": int,
    "L": int,
    "q": int,
    "Q": int,
    # python doesn't have different float/double sizes
    "f": float,
    "d": float,
    # we leave strings as strings
    "a": str,
}

outgoing_type_converters = {
    int: "l",
    float: "d",
    str: "a",
}


class Fsdb(object):
    """Reads FSDB files from the perl FSDB module.

    (see the fsdb module documentation for full details)
    """

    fileh = None
    _header_line = None
    current_line = None
    filename = None
    _separator = "\t"
    _separator_token = "t"
    _headers = None
    _column_names = {}
    _pass_comments = True
    _mapping = None
    _have_read_header = False

    _out_file = None
    _out_file_handle = None
    _out_header_line = None
    _out_column_names = []
    _out_column_names_set = False
    _out_separator = "\t"
    _out_separator_token = "t"
    _out_command_line = "____BROKEN____"  # ick, magic
    _save_command_history = True
    _handle_compressed = True
    _compression_checked = False
    _commands = False
    _seekable = True

    def __init__(
        self,
        filename=None,
        file_handle=None,
        return_type=RETURN_AS_ARRAY,
        out_file=None,
        out_file_handle=None,
        pass_comments="y",
        out_command_line="____INTERNAL____",
        write_nones_as_blanks=True,
        column_names=None,
        converters=None,
        save_command_history=True,
        out_column_names=None,
        handle_compressed=True,
        no_auto_conversion=False,
    ):
        """Returns a Fsdb class that can be used as an iterator.

        return_type can be pyfsdb.RETURN_AS_ARRAY (default) or
        RETURN_AS_DICTIONARY to return dictionary based rows with
        indexes as columns (this is slower).

        If `pass_comments` is "y" and both an input and output file
        handle are available, any comments read in while reading
        are printed to the output.

        If `save_command_history` is True, then comments will be saved
        to the comments attribute.

        `converters` may be passed in as an array or dict of
        converters to call (such as int, float, etc)

        If `handle_compressed` is True (the default), the class will
        do its best to handle compressed formats: bz2, gzip, and xz (lzma).

        """

        self.return_type = return_type
        self.filename = filename
        self.fileh = file_handle
        self._column_names = column_names
        self._pass_comments = pass_comments
        self._write_nones_as_blanks = write_nones_as_blanks
        self._header_written = False
        self._converters = converters
        self._save_command_history = save_command_history
        self._handle_compressed = handle_compressed
        self._no_auto_conversion = no_auto_conversion

        if out_column_names:
            self._out_column_names = out_column_names
            self._out_column_names_set = True

        if pass_comments not in ["y", "n", "e"]:
            raise ValueError("pass_comments must be y/n/e")

        if out_file:
            self.out_file = out_file
        elif out_file_handle:
            self._out_file_handle = out_file_handle
        self._maybe_open_out()

        if out_command_line == "____INTERNAL____":
            self.out_command_line = " ".join(sys.argv)
        else:
            self.out_command_line = out_command_line

        self._comments = []

    @property
    def file_handle(self):
        "The input file handle being read."
        return self.fileh

    @file_handle.setter
    def file_handle(self, fileh):
        self.fileh = fileh

        return fileh

    @property
    def headers(self):
        "Headers for the file handle being read."
        self.maybe_open_filehandle()
        if not self._headers:
            self.read_header()
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value

    @property
    def header_line(self):
        "The top #fsdb header line in the file being read."
        self.maybe_open_filehandle()
        if not self._header_line:
            self.read_header()
        return self._header_line

    @header_line.setter
    def header_line(self, value):
        self._header_line = value

    @property
    def column_names(self):
        "An array of column names for the file being read"
        self.maybe_open_filehandle()
        if not self._column_names:
            self.read_header()
        return list(self._column_names.keys())

    @column_names.setter
    def column_names(self, values):
        mapping = self.__create_column_name_mapping__(values)
        self._header_line = self.create_header_line(
            columns=values, separator_token=self._separator_token
        )
        self.headers = self._header_line

    @property
    def separator(self):
        """The 'separator_token' is the argument that comes after -F in the
        fsdb header and the separator is it's translation;
        eg, for tab-based separator the separator_token would
        be the 't' character and the separator would be '\t'.

        Changing this will also change the stored separator_token value."""
        self.maybe_open_filehandle()
        if not self._separator:
            self.read_header()
        return self._separator

    @separator.setter
    def separator(self, value):
        self._separator = value
        self._separator_token = self.convert_separator_token(value)
        self._header_line = self.create_header_line(
            columns=self.column_names, separator_token=self._separator_token
        )

    @property
    def separator_token(self):
        """The separator_token character for the file being read or written.

        The 'separator_token' is the argument that comes after -F in the
        fsdb header; eg, for a tab-based separator the separator_token would
        be the 't' character and the separator would be '\t'.

        Changing this will also change the stored separator value."""
        self.maybe_open_filehandle()
        if not self._separator_token:
            self.read_header()
        return self._separator_token

    @separator_token.setter
    def separator_token(self, value):
        self._separator_token = value
        self._separator = self.parse_separator(self.separator_token)
        self._header_line = self.create_header_line(
            columns=self.column_names, separator_token=self._separator_token
        )

    def __create_column_name_mapping__(self, columns):
        """Internal

        Creates a list of columns and numbers for rapid mapping
        at the start to make more rapid lookups later.
        """
        mapping = {"names": {}, "numbers": {}, "header": {"separator": self.separator}}

        for argn, token in enumerate(columns):
            # find out if we have auto-type-converters in the column names
            if not self._no_auto_conversion and token.find(":") != -1:
                if self._converters is None:
                    self._converters = {}
                (token, datatype) = token.split(":")
                if (
                    datatype in incoming_type_converters
                    and token not in self._converters
                ):
                    if isinstance(self._converters, dict):
                        self._converters[token] = incoming_type_converters[datatype]
                    else:
                        self._converters[argn] = incoming_type_converters[datatype]

            mapping["names"][token] = argn
            mapping["numbers"][argn] = token

        self._column_names = mapping["names"]
        self.column_nums = mapping["numbers"]

        if not self._out_column_names_set:
            self._out_column_names = self._column_names.keys()

        self._mapping = mapping
        return mapping

    #
    # output properties
    #
    @property
    def out_file(self):
        """The output file being written to (if one is being written)"""
        return self._out_file

    @out_file.setter
    def out_file(self, value):
        self._out_file = value
        self._out_file_handle = None
        self._maybe_open_out()

    @property
    def out_file_handle(self):
        """The output file being written to (if one is being written)"""
        return self._out_file_handle

    @out_file_handle.setter
    def out_file_handle(self, value):
        self._out_file_handle = value
        self._out_file = None
        self._maybe_open_out()

    def _maybe_open_out(self):
        if not self._out_file_handle and self.out_file:
            self._out_file_handle = open(self.out_file, "w")
        elif self.out_file_handle:
            try:
                self._out_file = self._out_file_handle.name
            except:
                pass

    @property
    def out_separator(self):
        """The separator for the output.

        Changing this will also change the stored
        out_separator_taken value.

        This should not be changed after the header has
        already been written.
        """
        return self._out_separator

    @out_separator.setter
    def out_separator(self, value):
        self._out_separator = value
        self._out_separator_token = self.convert_separator_token(value)
        self._out_header_line = self.create_header_line()

    @property
    def out_separator_token(self):
        """The separator for the output.

        Changing this will also change the stored
        out_separator value.

        This should not be changed after the header has
        already been written.
        """
        return self._out_separator_token

    @out_separator_token.setter
    def out_separator_token(self, value):
        self._out_separator_token = value
        self._out_separator = self.parse_separator(self._out_separator_token)
        self._out_header_line = self.create_header_line()

    @property
    def out_header_line(self):
        "The top #fsdb header line to write to the output."
        self.maybe_open_filehandle()
        self._out_header_line = self.create_header_line()
        return self._out_header_line

    @out_header_line.setter
    def out_header_line(self, value):
        """The output header line to print when writing.

        This must be set prior to writing the first row for it to
        be written"""
        self._out_header_line = value

    @property
    def out_command_line(self):
        """The output trailing command to print as the last line.

        The out_command_line is printed with a '#   | ' prefix
        to preserve the history of the command run.  It defaults
        to " ".join(sys.argv).  Set to None if you wish to surpress
        printing of the line entirely."""
        return self._out_command_line

    @out_command_line.setter
    def out_command_line(self, value):
        self._out_command_line = value

    @property
    def out_column_names(self):
        """An array of column names for the output file being written.

        This must be set prior to writing the first row, and modifies
        the internal output_header_line too."""
        if len(self._out_column_names) == 0:
            self._out_column_names = self.column_names
        return self._out_column_names

    @property
    def comments(self):
        """Returns a list of comments seen in the document"""
        return self._comments

    @property
    def commands(self):
        return self.parse_commands()

    @out_column_names.setter
    def out_column_names(self, values):
        mapping = self.__create_column_name_mapping__(values)

    # support functions

    def create_header_line(self, columns=None, separator_token=None, init_row=None):
        "Returns a header string for the stored column_names and separator/separator_token."
        if not columns:
            columns = self.out_column_names

        if separator_token is None:
            separator_token = self.out_separator_token

        if separator_token is None:
            separator_token = self.separator_token

        # create the header line
        header_line = "#fsdb -F " + separator_token + " "

        if isinstance(init_row, dict):
            init_row = [init_row[x] for x in self.out_column_names]

        # add each column, with an optional map
        for n, column in enumerate(columns):
            header_line += column

            if not self._no_auto_conversion:
                converters = self._converters
                if not converters:
                    converters = {}
                # if converters is a dictionary:
                if (
                    isinstance(converters, dict)
                    and column in converters
                    and converters[column] in outgoing_type_converters
                ):
                    header_line += ":" + outgoing_type_converters[converters[column]]
                elif (
                    isinstance(converters, list)
                    and converters[n] in outgoing_type_converters
                ):
                    header_line += ":" + outgoing_type_converters[converters[n]]
                elif (
                    init_row
                    and len(init_row) > n
                    and type(init_row[n]) in outgoing_type_converters
                ):
                    header_line += ":" + outgoing_type_converters[type(init_row[n])]

            header_line += " "

        header_line = header_line.rstrip() + "\n"
        self._have_read_header = True

        return header_line

    @property
    def converters(self):
        """The list of conversion routines.

        It may be an array, with a converter per column,
        or a dict with a convert per named column.

        This must be set before the file is opened/read.

        Useful converted may include int, float, etc.

        Note: if a converter throws an exception, a value of None will
        be placed into the returned row instead.
        """
        return self._converters

    @converters.setter
    def converters(self, new_converters):
        self._converters = new_converters

    def _convert_converters(self):
        if isinstance(self._converters, dict):
            converters = []
            # convert this to an array based on column names
            for column_name in self.column_names:
                if column_name in self._converters and callable(
                    self._converters[column_name]
                ):
                    converters.append(self._converters[column_name])
                else:
                    converters.append(None)
            self._converters = converters

    def guess_converters(self, example_row):
        """Returns a best-guess effort list of converters after determining
        if floats/ints exist in the dataset"""
        converters = {}
        for column in example_row:
            try:
                int(example_row[column])
                converters[column] = int
            except Exception:
                try:
                    float(example_row[column])
                    converters[column] = float
                except Exception:
                    pass
        return converters

    # column accessor helpers
    def get_column_number(self, column_name):
        "Given a column_name, returns its integer index into an array of values."
        self.maybe_open_filehandle()
        self.read_header()
        return self._column_names[column_name]

    def get_column_numbers(self, column_names):
        "Given a list of column_names, returns a list of integer index into an array of values."
        self.maybe_open_filehandle()
        self.read_header()
        column_numbers = []
        for name in column_names:
            column_numbers.append(self.get_column_number(name))
        return column_numbers

    def get_column_name(self, column_number):
        "Given an integer column number, returns its column name."
        self.maybe_open_filehandle()
        self.read_header()
        return self.column_nums[column_number]

    def set_iterator_function(self):
        "XXX: change this to an property"
        if self.return_type == RETURN_AS_DICTIONARY:
            self.__next__ = self._next_as_dict
        else:
            self.__next__ = self._next_as_array

    def __iter__(self):
        """Returns an iterator object for looping over an fsdb file."""
        if not self.filename and not self.file_handle:
            raise ValueError("No filename or handle currently available for reading")
        # XXX: throw error on -1 parse
        return self

    def maybe_open_filehandle(self, mode="r"):
        "Internal"

        # the simple case:
        if self.file_handle and (
            self._compression_checked or not self._handle_compressed
        ):
            return self.file_handle

        # don't try to do this twice
        self._compression_checked = True

        # the simple case, open it if we don't need to detect compressed
        if not self.file_handle and self.filename and not self._handle_compressed:
            self.file_handle = open(self.filename, mode)
            return self.file_handle

        # wrap this in case anything at all fails:
        try:

            # otherwise we need to check if we're getting compressed data
            filename = self.filename
            if not filename and self.file_handle and self.file_handle.name != "<stdin>":
                filename = self.file_handle.name

            # if we were passed a file but not a file name, open that and check it
            if filename:
                # see if we can determine the file type from the first few bytes
                # https://stackoverflow.com/questions/13044562/python-mechanism-to-identify-compressed-file-type-and-uncompress
                # XXX: there should be a package that does this...

                magic_dict = {
                    bytes([0x1F, 0x8B, 0x08]): "gz",
                    bytes([0x42, 0x5A, 0x68]): "bz2",
                    bytes([0xFD, 0x37, 0x7A, 0x58, 0x5A, 0x00]): "xz",
                }

                max_len = max(len(x) for x in magic_dict)

                with open(filename, "rb") as f:
                    file_start = f.read(max_len)
                    for magic, filetype in magic_dict.items():
                        if file_start.startswith(magic):
                            try:
                                if filetype == "gz":
                                    import gzip

                                    self._seekable = False  # unlikely
                                    self.file_handle = gzip.open(filename, "rt")
                                    return self.file_handle
                                elif filetype == "bz2":
                                    import bz2

                                    self._seekable = False  # unlikely
                                    self.file_handle = bz2.open(filename, "rt")
                                    return self.file_handle
                                elif filetype == "xz":
                                    import lzma

                                    self._seekable = (
                                        False  # say they are when they're not
                                    )
                                    self.file_handle = lzma.open(filename, "rt")
                                    return self.file_handle
                            except Exception:
                                sys.stderr.write(
                                    f"failed to use {filetype} module to decode the input stream"
                                )
                                raise ValueError("cannot decode file")
        except Exception:
            pass

        # fall back to just opening it and hope its raw
        if self.filename:
            self.file_handle = open(self.filename, mode)

        return self.file_handle

    def __next__(self):
        """Returns the next array of data from an fsdb file.
        Returns an array by default, or a dictionary if return_type
        was set to pyfsdb.RETURN_AS_DICTIONARY."""

        fh = self.maybe_open_filehandle()
        if not self._header_line:
            self.read_header()

        self._convert_converters()

        if self.return_type == RETURN_AS_DICTIONARY:
            self.__next__ = self._next_as_dict
        else:
            self.__next__ = self._next_as_array

        if not fh:
            return None

        return self.__next__()

    def _handle_comment(self, line):
        """Handle a comment by printing it, possibly with header init first,
        and then returning the next line in the file"""
        if self._pass_comments != "n" and self._out_file_handle:

            if self.append != self._append_really:
                # we haven't printed anything yet, so we haven't written
                # the fsdb_header yet

                self._write_header_line()

            if self._pass_comments == "y":
                self._out_file_handle.write(line)
            else:
                self._comments.append(line)
        elif self._pass_comments == "y":
            self._comments.append(line)

        return next(self.fileh)

    def _convert_array_values(self, row):
        for (n, converter) in enumerate(self._converters):
            if row[n] == "-" or row[n] == "":
                row[n] = None
            elif converter is not None and row[n] is not None:
                try:
                    row[n] = converter(row[n])
                except Exception:
                    row[n] = None
        return row

    def _next_as_array(self):
        """Return the next object as an array of columns."""

        line = next(self.fileh)
        while line and line[0] == "#":
            line = self._handle_comment(line)

        # return an array of data
        self.current_line = line
        self._current_row = line.rstrip("\n\r").split(self.separator)
        if len(self._current_row) < len(self._column_names):
            n = (len(self._column_names)) - len(self._current_row)
            self._current_row.extend([""] * n)
        if self._converters:
            self._current_row = self._convert_array_values(self._current_row)
        return self._current_row

    def _next_as_dict(self):
        """Return the next object as a dictionary, with column
        names as the indexes.

        Note: This is less efficient than returning data as an
        array using the normal __next__() routine."""

        array = self._next_as_array()

        return_dict = {}
        for index in range(0, len(array)):
            return_dict[self.column_nums[index]] = array[index]

        return return_dict

    # generator type function for returning a row as an array
    def next_as_array(self):
        """Generator function to return a row as an array.

        Using a generator is faster than using the Fsdb object
        as a iterator."""

        fh = self.maybe_open_filehandle()

        try:
            line = next(self.fileh)
            while line:
                while line and line[0] == "#":
                    line = self._handle_comment(line)

                # return an array of data
                self.current_line = line
                self._current_row = line.rstrip("\n\r").split(self.separator)
                yield self._current_row
                line = next(self.fileh)
        except StopIteration as e:
            return

    def next_as_dict(self):
        """Generator function to return an array row.

        Using a generator is faster than using the Fsdb object
        as a iterator."""

        fh = self.maybe_open_filehandle()

        try:
            line = next(self.fileh)
            while line:
                while line and line[0] == "#":
                    line = self._handle_comment(line)

                # return an array of data
                self.current_line = line
                self._current_row = line.rstrip("\n\r").split(self.separator)

                return_dict = {}
                for index in range(0, len(self._current_row)):
                    return_dict[self.column_nums[index]] = self._current_row[index]

                yield return_dict
                line = next(self.fileh)
        except StopIteration as e:
            return

    def parse_separator(self, separator=None):
        """Converts a separator ("t") into a separator_token ("\t")"""
        if separator == "t":
            return "\t"
        elif separator == "S":
            return "  "
        elif separator == "s":
            return " "
        elif separator[0] == "c":
            return separator[1:]
        elif separator[0] == "C":
            return separator[1:]  # won't handle multiples like manual says
        elif separator[0] == "x":
            return chr(int("0x" + separator[1:], 0))
        elif separator[0] == "X":  # won't handle multiples like manual says
            return chr(int("0x" + separator[1:], 0))
        elif separator == "D":
            # python NONE to splits on all white space
            return None

        # unknown
        raise ValueError("Unknown separator value: " + separator)

    def convert_separator_token(self, separator_token=None):
        """Converts a separator ("\t") into a separator_token ("t")"""
        if separator_token == "\t":
            return "t"
        elif separator_token == "  ":
            return "S"
        elif separator_token == " ":
            return "s"
        elif len(separator_token) == 1:
            return "C" + separator_token
        elif separator_token == None:
            # XXX
            separator_token = "D"

        # unknown
        raise ValueError("Unknown separator token value: " + separator_token)

    def read_header(self, line=None):
        """Internal

        Returns a dict of header -> column numbers.

        The header line should be in the form:

            #fsdb -option value column1(separator)column2...

        Returns:
           [0, {
                  names: { colname: colnum, ...},
                  numbers: { colnum: colname, ...}
                  header: { separator: separator_string}
               }]    on success
           [-1, "error description"]         on failure
        """

        if self._have_read_header:
            return [0, self._mapping]
        self._have_read_header = True

        if not line:
            line = next(self.file_handle)
        self._header_line = line
        self._headers = [self._header_line]

        args = line.split()
        if args[0] != "#fsdb":
            raise ValueError("failed to find expected #fsdb header")

        # should we use argparse here?
        argn = 1
        separator = None  # (D)efault is all white space
        while args[argn][0] == "-":
            if args[argn] == "-F":
                argn += 1
                self._separator_token = args[argn]
            else:
                return [-1, "Unown option: " + args[argn]]

            argn += 1

        self._separator = self.parse_separator(self._separator_token)

        # join the remainder of the arguments back together to split
        # by the correct separator

        # XXX: allow other separators in the header
        remainder = " ".join(args[argn:]).rstrip()
        args = remainder.split(" ")

        mapping = self.__create_column_name_mapping__(args)
        self._separator = mapping["header"]["separator"]

        return [0, mapping]

    def row_as_string(self, row=None):
        """Converts an array row to an FSDB output line."""
        if not row:
            row = self._current_row
        return self.separator.join(row) + "\n"

    #
    # Useful higher-level functions
    #

    def get_all(self):
        """Read all the data into memory and return it as an array of rows."""
        all_rows = []
        for row in self:
            all_rows.append(row)
        return all_rows

    def put_all(self, rows):
        "Reads a list of rows and appends them to the FSDB file."
        for row in rows:
            self.append(row)

    def get_pandas(
        self, usecols=None, comment="#", data_has_comment_chars=False, **kwargs
    ):
        """Returns a pandas dataframe for the given data.  Warning: this
        cannot preserve comments in the files; FSDB comments are
        stripped from the output.  Any other args will be passed to
        pandas.read_csv()
        """
        import pandas

        column_names = self.column_names  # forces opening and reading headers

        if data_has_comment_chars:
            # when data has the comment character in the middle,
            # pandas.read_csv fails because it assumes comment
            # characters are line breaks.  We have no choice but to
            # read all the data ourselves (slow).
            slow_data = self.get_all()

            df = pandas.DataFrame(slow_data, columns=column_names)

            for column in column_names:
                try:
                    df[column] = pandas.to_numeric(df[column])
                except:
                    pass

            return df
        else:
            return pandas.read_csv(
                self.file_handle,
                sep="\t",
                comment=comment,
                names=column_names,
                usecols=usecols,
                **kwargs,
            )

    def put_pandas(self, df):
        "saves a pandas dataframe to the output file"
        import pandas

        if not self._out_column_names:
            self.out_column_names = df.columns.values.tolist()
        self._write_header_line()
        df.to_csv(self._out_file_handle, sep="\t", header=False, index=False)

    def comment(self, line):
        """Add a comment to an ouput FSDB file

        Addition and its placement depends on the value of pass_comments"""

        if line[0] != "#":
            line = "# " + line
        if line[-1] != "\n":
            line += "\n"

        # TODO: merge with _handle_comment, which also does a next()
        if self._pass_comments != "n":
            if self._header_written and self._pass_comments == "y":
                self._out_file_handle.write(line)
            else:
                self._comments.append(line)

    def foreach(self, fn, return_results=True, args=[]):
        """Applies a function fn to each row, returning an
        aggregate list of results if desired."""
        results = []
        if return_results:
            for row in self:
                results.append(fn(row, *args))
        else:
            # do this separately for speed purposes
            for row in self:
                fn(row, *args)

        return results

    def filter(self, fn, args=[]):
        """Applies a function to the input stream rows, and saves the output
        results back to the output fsdb handle."""
        for row in self:
            filtered = fn(row, *args)
            if filtered:
                self.append(filtered)

    #
    # writing functions
    #

    def append(self, row=None):
        """Writes a passed in row (or the one previously read) to the output file."""
        self._append_init(row)

    def extend(self, rows=None):
        """Writes multiple rows to the output FSDB"""
        for row in rows:
            self.append(row)

    def _write_header_line(self, init_row=None):
        if not self._out_column_names and not self._header_line:
            return  # we're unable to at this point

        # maybe construct it
        if not self._out_header_line and self._out_column_names:
            self._out_header_line = self.create_header_line(init_row=init_row)

        # write out the correct header
        if self._out_header_line:
            self._out_file_handle.write(self._out_header_line)
        elif self._header_line:
            # assuming copy the original
            self._out_file_handle.write(self._header_line)

        # see if we have any early stored comments
        if self._pass_comments == "y" and self._comments:
            for comment in self._comments:
                self._out_file_handle.write(comment)
            self._comments = []

        # if we write the header line,
        #    it's now ok to set the output function to the right function
        self.append = self._append_really
        self._header_written = True

    def _append_init(self, row=None):
        # internallly, if we haven't written the header out we do that first
        # then switch our operator for speed

        self._write_header_line(row)
        self.append(row)

    def _append_really(self, row=None):
        if not row:
            row = self._current_row
        if isinstance(row, dict):
            row = [row[x] for x in self.out_column_names]
        if self._write_nones_as_blanks:
            for i in range(0, len(row)):
                if row[i] == None:
                    row[i] = ""
        self._out_file_handle.write(self._out_separator.join(map(str, row)) + "\n")

    # backwards compatible ... don't use
    def write_row(self, row=None):
        self.append(row)

    def write_finish(self):
        self.close()

    def import_comments(self, from_fsdb):
        for comment in from_fsdb._comments:
            self._comments.append(comment)

    def get_file_size(self):
        return os.stat(self.fileh.name).st_size

    def read_commands_ahead(self):
        """reads the command list at the bottom of the input stream if the input stream can seek.

        returns a list of commands found in comments in the input stream
        returns None when the input is not seekable"""

        self.maybe_open_filehandle()

        if not self._seekable or not self.file_handle.seekable():
            return None

        guess_length = 512

        # save our spot
        position = self.file_handle.seek(0)

        # get the file size
        try:
            file_size = self.get_file_size()
        except Exception:
            return None
        multiplier = 1

        # move to the bottom minus the guess length
        start_seek = file_size - guess_length
        if start_seek < file_size:
            guess_length = file_size
        self.file_handle.seek(file_size - guess_length)

        # poor man's search from the back
        while True:
            data = self.file_handle.read(guess_length * multiplier)
            first_newline = data.find("\n")

            if first_newline != -1 and (
                first_newline == len(data) - 1 or data[first_newline + 1] == "#"
            ):
                # keep rewinding (x2 since we read x1 in already)
                multiplier += 1

                if file_size - guess_length * multiplier <= 0:
                    return None

                actual = self.file_handle.seek(file_size - guess_length * multiplier)
                continue

            break

        # now extract all the commands from where we've found things
        commands = []
        iowrapper = io.StringIO(data)

        import re

        command_matcher = re.compile("# +\\| (.*)")

        for line in iowrapper:
            result = command_matcher.match(line)
            if result:
                commands.append(result.group(1))

        self.file_handle.seek(position)
        return commands

    def parse_commands(self):
        """parses the list of stored comments for any saved commands

        Note: Assumes saved commands will be prefixed with '#  |' per convention

        Returns a list of strings when commands can be found.

        Returns None when we don't have the information yet, such as when
        we have a non-seekable stream input.
        """

        self.maybe_open_filehandle()

        # we already have some stored
        if self._commands:
            return self._commands

        # see if we can read them from the end of the file
        if not self._comments:
            if self._seekable and self.file_handle.seekable():
                self._commands = self.read_commands_ahead()
                return self._commands
            return None

        import re

        command_matcher = re.compile("# +\\| (.*)")

        # parse them from the comments
        self._commands = []
        for comment in self._comments:
            results = command_matcher.match(comment)
            if results:
                self._commands.append(results.group(1))

        return self._commands

    def close(self, copy_comments_from=None):
        """Writes final processing command comment to the output file and closes it."""
        if self.fileh:
            self.fileh.close()
            self.fileh = None

        if copy_comments_from:
            self.import_comments(copy_comments_from)

        if self._out_file_handle:
            # ignore closing errors
            try:
                if not self._header_written:
                    self._write_header_line()
                if self._save_command_history and self.out_command_line:
                    for comment_line in self._comments:
                        self._out_file_handle.write(comment_line)
                    self._out_file_handle.write("#  | " + self.out_command_line + "\n")
                self._out_file_handle.close()
            except:
                pass
            self._out_file_handle = None

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()
