import re
from django.conf import settings
from pygments import highlight
from pygments.lexers import *
from pygments.formatters import HtmlFormatter

"""
# Get a list of all lexer, and then remove all lexer which have '-' or '+'
# or 'with' in the name. Those are too specific and never used. This produces a
# tuple list of [(lexer, Lexer Display Name) ...] lexers.
from pygments.lexers import get_all_lexers
ALL_LEXER = set([(i[1][0], i[0]) for i in get_all_lexers()])
LEXER_LIST = [l for l in ALL_LEXER if not (
       '-' in l[0]
    or '+' in l[0]
    or '+' in l[1]
    or 'with' in l[1].lower()
    or ' ' in l[1]
    or l[0] in IGNORE_LEXER
)]
LEXER_LIST = sorted(LEXER_LIST)
"""

# The list of lexers. Its not worth to autogenerate this. See above how to
# retrieve this.
LEXER_LIST = getattr(settings, 'DPASTE_LEXER_LIST', (
    ('text', 'Text'),
    ('text', '----------'),
    ('apacheconf', 'ApacheConf'),
    ('applescript', 'AppleScript'),
    ('as', 'ActionScript'),
    ('bash', 'Bash'),
    ('bbcode', 'BBCode'),
    ('c', 'C'),
    ('clojure', 'Clojure'),
    ('cobol', 'COBOL'),
    ('css', 'CSS'),
    ('cuda', 'CUDA'),
    ('dart', 'Dart'),
    ('delphi', 'Delphi'),
    ('diff', 'Diff'),
    ('django', 'Django'),
    ('erlang', 'Erlang'),
    ('fortran', 'Fortran'),
    ('go', 'Go'),
    ('groovy', 'Groovy'),
    ('haml', 'Haml'),
    ('haskell', 'Haskell'),
    ('html', 'HTML'),
    ('http', 'HTTP'),
    ('ini', 'INI'),
    ('java', 'Java'),
    ('js', 'JavaScript'),
    ('json', 'JSON'),
    ('lua', 'Lua'),
    ('make', 'Makefile'),
    ('mako', 'Mako'),
    ('mason', 'Mason'),
    ('matlab', 'Matlab'),
    ('modula2', 'Modula'),
    ('monkey', 'Monkey'),
    ('mysql', 'MySQL'),
    ('numpy', 'NumPy'),
    ('ocaml', 'OCaml'),
    ('perl', 'Perl'),
    ('php', 'PHP'),
    ('postscript', 'PostScript'),
    ('powershell', 'PowerShell'),
    ('prolog', 'Prolog'),
    ('properties', 'Properties'),
    ('puppet', 'Puppet'),
    ('python', 'Python'),
    ('rb', 'Ruby'),
    ('rst', 'reStructuredText'),
    ('rust', 'Rust'),
    ('sass', 'Sass'),
    ('scala', 'Scala'),
    ('scheme', 'Scheme'),
    ('scilab', 'Scilab'),
    ('scss', 'SCSS'),
    ('smalltalk', 'Smalltalk'),
    ('smarty', 'Smarty'),
    ('sql', 'SQL'),
    ('tcl', 'Tcl'),
    ('tcsh', 'Tcsh'),
    ('tex', 'TeX'),
    ('text', 'Text'),
    ('vb.net', 'VB.net'),
    ('vim', 'VimL'),
    ('xml', 'XML'),
    ('xquery', 'XQuery'),
    ('xslt', 'XSLT'),
    ('yaml', 'YAML'),
))

LEXER_KEYS = dict(LEXER_LIST).keys()

# The default lexer is python
LEXER_DEFAULT = getattr(settings, 'DPASTE_LEXER_DEFAULT', 'python')

# Lexers which have wordwrap enabled by default
LEXER_WORDWRAP = getattr(settings, 'DPASTE_LEXER_WORDWRAP', ('text', 'rst'))


class NakedHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile):
        return self._wrap_code(source)

    def _wrap_code(self, source):
        for i, t in source:
            yield i, t

SPACE_START = re.compile(r'^(\s+)', re.UNICODE | re.MULTILINE)

def SPACE_REPL(match):
    length = match.end() - match.start()
    print length
    return u'&nbsp;' * length

def pygmentize(code_string, lexer_name=LEXER_DEFAULT, nbsp=False):
    try:
        lexer = lexer_name and get_lexer_by_name(lexer_name) \
                            or PythonLexer()
    except Exception as e:
        if settings.DEBUG:
            raise Exception(e)
        lexer = PythonLexer()
    code = highlight(code_string, lexer, NakedHtmlFormatter())
    if nbsp:
        code = SPACE_START.sub(SPACE_REPL, code)
    return code
