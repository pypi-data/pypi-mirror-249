# linkedText

It allows to create a table of contents and link them to the different titles of a Markdown document, without altering the original file and generating a new one.

The idea came up to automate this manual process, it was tedious to write and check that each title has its link and create the table of contents. Now I simply write the content, run the program and I have the finished document.


## Usage

The `LinkedText` class supports both Markdown files (`markdown_file` parameter) and strings in Markdown format (`string` parameter).


* Markdown file

When passing a Markdown file, it will be parsed and processed, generating a new file with the same name as the original and ending with `_finish.md`. The original file is never altered. Writing is automatic.

```python
>>> from linkedtext import LinkedText
>>>
>>> c = LinkedText(markdown_file='my_file.md')
>>> c.process()
```


* Markdown string

When a Markdown string is used, the result will be displayed in the terminal, it can be written to a file, this will be named `linkedtext_finish.md` by default.


```python
>>> from linkedtext import LinkedText
>>>
>>> c = LinkedText(string=string_markdown)
>>> c.process()
>>> c.to_write()
```


## Sample

* String Markdown

```python
string = """
# First

First paragraph.

## Second

Second paragraph.

# Third

Third paragraph.


# Fourth

Fourth paragraph.
"""

from linkedtext import LinkedText

c = LinkedText(string=string)
c.process()
# c.to_write()   # write to the `linkedtext_finish.md` file.
```

* Output

```markdown
1. [First](#first)
    1. [Second](#second)
2. [Third](#third)
3. [Fourth](#fourth)

\pagebreak


<a name="first"></a>

# First

First paragraph.

<a name="second"></a>

## Second

Second paragraph.

<a name="third"></a>

# Third

Third paragraph.


<a name="fourth"></a>

# Fourth

Fourth paragraph.

```


# Tests

```python
python -m unittest
```
