# pythontidy2

[![Travis](https://img.shields.io/badge/pypi-0.1-blue.svg)](https://pypi.python.org/pypi?:action=display&name=pythontidy2) [![PyPI](https://img.shields.io/pypi/l/Django.svg)](#)


### Usage

``` python
python -m pythontidy2 [-t expandtabsize] script.py
```

## Installation

``` python
pip install pythontidy2
```

## Description

Life is short, format the code automatically

(人生苦短，自动排版)

Tidy python scripts

## Effect

Convert Tabs to Spaces(Tabs sized can be decide in argument -t, default is 4)

Delete white spaces at end of line

###Own thoughts about code format, some part are different from PEP8

PEP8: [Whitespace in Expressions and Statements](https://www.python.org/dev/peps/pep-0008/#id23)
Not compliant

Always add 1 white space between operators

Align dict and assignment statments like following

### From:

``` python
list = [1, 2, {
   'Alicedefg': '2341',
   'Beth' : "c",
   'Cecil' : '3258',
}, 4]
```

### To:

``` python
list = [1, 2, {
                'Alicedefg' : '2341',
                'Beth'      : "c",
                'Cecil'     : '3258',
                }, 4]
```

### From:

``` python
doc = ""
long_variable = ((doc+' ') if doc else '')
x = ""
```

### To:

``` python
doc           = ""
long_variable = ((doc + ' ') if doc else '')
x             = ""
```

## Limitation

Only Windows(*CRLF*) Linux/Modern OSX(*LF*) end of line mark supported

Do not support classic Mac end of line mark(*CR*)

Widechar(Asian) in sorce code (as variable or dict Key) not tested

## VIM Integration

Below example binds the tidy fucntion to F7

``` vim
command -range=% -nargs=* TidyPython <line1>,<line2>!python -m pythontidy2
fun DoTidyPython()
    let Pos = line2byte( line( "." ) )
    :TidyPython
    exe "goto " . Pos
endfun
au Filetype python nmap <F7> :call DoTidyPython()<CR>
au Filetype python imap <F7> <ESC>:call DoTidyPython()<CR>
au Filetype python vmap <F7> :TidyPython<CR>
```

## License

**BSD**


>    Copyright (c) 2016, Boying Xu
>    All rights reserved.

>    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

>    1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

>    2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

>    3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

>    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.