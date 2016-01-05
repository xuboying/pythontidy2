
# Usage

`python -m pythontidy2 [-t expandtabsize] script.py `

# Description

Tidy python scripts

Not compliant to PEP8

# Effect

From:

    list = [1, 2, {
       'Alicedefg': '2341',
       'Beth' : "c",
       'Cecil' : '3258',
    }, 4]

To:

    list = [1, 2, {
                    'Alicedefg' : '2341',
                    'Beth'      : "c",
                    'Cecil'     : '3258',
                    }, 4]

From:

    doc = ""
    long_variable = ((doc+'\n') if doc else '')
    x = ""

To:

    doc           = ""
    long_variable = ((doc + '\n') if doc else '')
    x             = ""

# License

BSD