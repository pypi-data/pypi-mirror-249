# Readable Format

This module contains a function that helps format an input number into a readable number string.

For example:

print(form(1000000000).form())

Would print the following:

'1B'

and:

print(form('1B').form())

Would print the following:

1000000000
