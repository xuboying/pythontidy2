# pythontidy2 

### Usage

``` python
python -m pythontidy2 [-t expandtabsize] script.py
```

### Installation

``` python
pip install pythontidy2
```

### Description

Tidy python scripts

Not compliant to PEP8

### Effect

From:

``` python
list = [1, 2, {
   'Alicedefg': '2341',
   'Beth' : "c",
   'Cecil' : '3258',
}, 4]
```

To:

``` python
list = [1, 2, {
                'Alicedefg' : '2341',
                'Beth'      : "c",
                'Cecil'     : '3258',
                }, 4]
```

From:

``` python
doc = ""
long_variable = ((doc+'\n') if doc else '')
x = ""
```

To:

``` python
doc           = ""
long_variable = ((doc + '\n') if doc else '')
x             = ""
```

### License

BSD