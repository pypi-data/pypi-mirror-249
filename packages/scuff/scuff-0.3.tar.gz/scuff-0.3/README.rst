######
Scuff
######

*A human-readable data serialization language written in Python.*


Introduction
=============

**Scuff** is a language for data serialization: a way to store and read data
between formats.

One likely use for **Scuff** is application configuration files.


Installation
=============

To install **Scuff** and its tools for Python from the Python Package Index,
run the following in the command line:

.. code:: shell

    $ python -m pip install scuff


Grammar
========

Assigning Variables
--------------------

Variables are assigned with a *key* and a *value*.
Key names must be valid identifiers, meaning they must contain no spaces or
symbols except underscore (``_``).
Values can be assigned to variables with or without an equals sign (``=``):

.. code:: py

    my_favorite_number = 42
    my_favorite_color "Magenta"
    is_but_a_flesh_wound yes

When left without a value, variables will evaluate to ``null``/``None``:

.. code:: py

    set_to_null =
    also_null
    but_this_has_a_value 15


Data Types
-----------

- Numbers
    Numbers can be positive integers or floats::

        1 1.2 1_000 0.123 .123_4

- Booleans
    The boolean values ``True`` and ``False`` are given using these variants::

        True true yes
        False false no

- Strings
    Single-line strings can be enclosed by single quotes (``'``), double
    quotes (``"``) or backticks (`````), and multiline strings are enclosed by
    three of any of those:

    .. code:: py

        foo "abc"
        bar 'def'
        baz '''Hi,
                did you know
                    you're cute?
                        '''


..
    Strings placed right next to each other are concatenated:

    .. code:: py
        
        first = "ABC"
        second = "DEF"
        first_plus_second = "ABC"  "DEF"
        concatenated = "ABCDEF"
                    
- Lists
    Lists are enclosed by square brackets (``[]``).
    Elements inside lists are separated by spaces, commas or line breaks:

    .. code:: py

        groceries [
            "bread",
            "milk" "eggs"
            "spam"
        ]

- Mappings
    Mappings are groups of key-value pairs enclosed by curly braces (``{}``).
    Values may be any expression, even other mappings:

    .. code:: py

        me {
            name "Samantha"
            age 24
            job "Developer"
            favorite_things {
                editor "Vim"
                languages ["Python", "Rust"]
            }
        }

    Mappings may also take the form of dotted attribute lookups:

    .. code:: py

        outer.middle.inner yes  # == {'outer': {'middle': {'inner': True}}}

- Comments
    Single-line comments are made using the ``#`` symbol:

    .. code:: py

        option = "The parser reads this."
        # But this is a comment.
            #And so is this.
        option2 = "# But not this; It's inside a string."
        # The parser ignores everything between ``#`` and the end of the line.
         #   ignore = "Comment out any lines of code you want to skip."


Usage
======
Once you install **Scuff**, you can then import ``scuff`` as a Python module
and use its tools:

.. code:: py

    >>> import scuff
    >>> scuff.convert_file('file.conf')
    ...



