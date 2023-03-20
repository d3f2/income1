Getting started:

If no virtual environment already:
`python3 -m venv .venv`
Activate it:
`source .venv/bin/activate`
Install Python Packages:
`pip install -r requirements.txt`

Code Review:

- Please comment on my use of modules... I have used Make and Read but i'm not sure this is the best way. How would you do it?
- Please comment on code re-use... Are there places where I use constants where I should use vars?
- Please comment on my use of MultiIndex... is it correct that every non-numeric column should be an index? For example, I made FormatType a column not an index because it's not really part of the data, it is used for formatting the line in the table, should it be an index? I'm using MultiIndex for speed are there any other cases where it's better to use Column than index?
- Should the code conform to PEP?

Notes:

- I haven't used try/catch anywhere because in general I have followed [this advice](https://stackoverflow.com/questions/32394582/wrap-every-method-in-try-catch-or-specific-part-of-code): "The basic rule of thumb for catching exceptions is to catch exceptions if and only if you have a meaningful way of handling them. Don't catch an exception if you're only going to log the exception and throw it up the stack. It serves no meaning and clutters code. Do catch an exception when you are expecting a failure in a specific part of your code, and if you have a fallback for it." There is nowhere really in my code that I need to meaningfully catch an exception. I could argue maybe I need to do it on csv read/write but I would only exit the program, I wouldn't meaningfully handle the error.

Todo:

- Output table to a .txt file, formatting each line by FormatType (Journal or Subtotal or Total), potentially with ASCII.
- I include the logging library but don't really use it so I should use it.
- Testing for each method.
