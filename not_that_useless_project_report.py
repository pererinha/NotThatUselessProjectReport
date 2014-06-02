import sublime, sublime_plugin
import os
import sys
import codecs
import threading

# window.run_command('not_that_useless_project_report')

class NotThatUselessProjectReportCommand(sublime_plugin.WindowCommand):

    def __init__(self, window):
        sublime_plugin.WindowCommand.__init__(self, window)

    def run(self):
        miner = Miner(self.window.folders())
        miner.start()
        self.handle_key_miner(miner)

    def handle_key_miner(self, thread, i=0, direction=1):
        view = self.window.active_view()
        if thread.is_alive():
            if (view):
                before = i % 8
                after = (7) - before
                if not after:
                    direction = -1
                if not before:
                    direction = 1
                i += direction
                view.set_status('miner', 'Mining your code [%s=%s]' % (' ' * before, ' ' * after))
            sublime.set_timeout(lambda: self.handle_key_miner(thread, i, direction), 100)
            return
        if (view):
            view.erase_status('miner')
        results = thread.result
        self.report(results)

    def report (self, results):
        write = Writer()
        report = write.tablefy(results)
        self.window.new_file()
        self.window.active_view().run_command('insert_snippet', {'contents': report})

class Writer:

    def highest(self, results):
      highest = 12 # 'Blank lines' lengh
      for key in results:
        if key.__len__() > highest:
          highest = key.__len__()
      highest += 2
      return highest

    def tablefy(self, results):
        report = ''
        total_files = 0
        total_lines = 0
        blank_lines = 0
        blank_types = 0

        highest = self.highest(results)
        divider = ((self.col(('-'*highest) + '-', highest,''))*4) + self.col_end()

        report += self.nl()
        report += self.title('Project report')
        report += self.nl()

        report += self.subtitle('Summary')

        report += divider
        report += self.col('Type', highest)
        report += self.col('Files', highest)
        report += self.col('Lines', highest)
        report += self.col('Blank lines', highest)
        report += self.col_end()
        report += divider

        for key in sorted(results):
          files = results[key]['files']
          lines = results[key]['lines']
          blank = results[key]['blank']
          type = key[1:].upper()

          report += self.col(type, highest)
          report += self.col(str(files), highest)
          report += self.col(str(lines), highest)
          report += self.col(str(blank), highest)
          report += self.col_end()

          total_lines += lines
          blank_lines += blank
          total_files += files
          blank_types += 1

        report += divider

        report += self.nl()
        report += self.subtitle('Totals')

        report += divider
        report += self.col('Types', highest)
        report += self.col('Files', highest)
        report += self.col('Lines', highest)
        report += self.col('Blank lines', highest)
        report += self.col_end()
        report += divider

        report += self.col(str(blank_types), highest)
        report += self.col(str(total_files), highest)
        report += self.col(str(total_lines), highest)
        report += self.col(str(blank_lines), highest)
        report += self.col_end()
        report += divider

        if total_lines == 0:
          return 'Oops, it seems you don\'t have a folder open :( '

        return report

    def title(self, title):
      string = title + self.nl()
      string += ('='*title.__len__()) + self.nl()
      return string

    def subtitle(self, subtitle):
      string = subtitle + self.nl()
      string += ('-'*subtitle.__len__()) + self.nl()
      return string

    def nl(self):
      return '\n'

    def col(self, text, pad, spacer=' '):
      return '|' + spacer + text.ljust(pad)

    def col_end(self):
      return '|\n'

    def tab(self):
      return '\t'

class Miner(threading.Thread):

    def __init__(self, path):
        self.path = path
        self.result = dict()
        threading.Thread.__init__(self)

    def run(self):
        self.result = self.mine()

    def mine(self):
      result = dict()
      directories = self.path
      for directory in directories:
        for path, subdirs, files in os.walk(directory):
          for name in files:
            filename = os.path.join(path, name)
            if self.should_go(filename):
              extension = os.path.splitext(filename)[1];
              lines = self.count_lines(filename)
              if extension in result:
                result[extension]['files'] += 1
                result[extension]['lines'] += lines['lines']
                result[extension]['blank'] += lines['blank']
              else:
                result[extension] = dict()
                result[extension]['files'] = 1
                result[extension]['lines'] = lines['lines']
                result[extension]['blank'] = lines['blank']
      return result

    def should_go( self, filename ):
      should_go = True
      ignore_patterns = ['/.']
      should_go = True
      for pattern in ignore_patterns:
        if pattern in filename:
          should_go = False
      if should_go and os.path.exists(filename) and not is_binary( filename ) and not os.path.islink( filename ):
        return True
      else:
        return False

    def count_lines(self, filename):
      lines = dict()
      lines[ 'lines' ] = 0
      lines[ 'blank' ] = 0
      try:
        with codecs.open(filename, "r", encoding="utf-8") as f:
          for line in f:
            lines[ 'lines' ] += 1
            if line in ['\n', '\r\n']:
              lines[ 'blank' ] += 1
      except (IOError,UnicodeDecodeError,SyntaxError):
        coooool = True
      else:
        bad_bad_guy = True
      finally:
        return lines
"""
Libs
"""

"""
binaryornot.check
-----------------
__author__ = 'Audrey Roy'
__email__ = 'audreyr@gmail.com'
__version__ = '0.2.0'

Main code for checking if a file is binary or text.
"""


def is_binary(filename):
    """
    :param filename: File to check.
    :returns: True if it's a binary file, otherwise False.
    """
    chunk = get_starting_chunk(filename)
    return is_binary_string(chunk)


"""
binaryornot.helpers
-------------------

Helper utilities used by BinaryOrNot.
"""
def print_as_hex(s):
    """
    Print a string as hex bytes.
    """

    print(":".join("{0:x}".format(ord(c)) for c in s))


def get_starting_chunk(filename):
    """
    :param filename: File to open and get the first little chunk of.
    :returns: Starting chunk of bytes.
    """
    # Ensure we open the file in binary mode
    with open(filename, 'rb') as f:
        chunk = f.read(1024)
        return chunk


def is_binary_string(bytes_to_check):
    """
    :param bytes: A chunk of bytes to check.
    :returns: True if appears to be a binary, otherwise False.
    """
    # Uses a simplified version of the Perl detection algorithm,
    # based roughly on Eli Bendersky's translation to Python:
    # http://eli.thegreenplace.net/2011/10/19/perls-guess-if-file-is-text-or-binary-implemented-in-python/

    # This is biased slightly more in favour of deeming files as text
    # files than the Perl algorithm, since all ASCII compatible character
    # sets are accepted as text, not just utf-8

    # Empty files are considered text files
    if not bytes_to_check:
        return False

    # Check for NUL bytes first
    if b'\x00' in bytes_to_check:
        return True

    # Now check for a high percentage of ASCII control characters
    printable_extended_ascii = b'\n\r\t\f\b'
    if bytes is str:
        # Python 2 means we need to invoke chr() explicitly
        printable_extended_ascii += b''.join(map(chr, range(32, 256)))
    else:
        # Python 3 means bytes accepts integer input directly
        printable_extended_ascii += bytes(range(32, 256))

    # Binary if control chars are > 30% of the string
    control_chars = bytes_to_check.translate(None, printable_extended_ascii)
    nontext_ratio = float(len(control_chars)) / float(len(bytes_to_check))
    return nontext_ratio > 0.3
