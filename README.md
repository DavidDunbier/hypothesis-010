# hypothesis-010

A tool to generate [Hypothesis](https://hypothesis.readthedocs.io) strategies for generating data
that matches some [010 editor](https://www.sweetscape.com/010editor/)
binary template.

This would extend to include over [170 binary file formats built in](https://www.sweetscape.com/010editor/repository/templates/),
and [many more from the community](https://www.google.com/search?q=github+010+templates).

[Here's the PyPI page](https://pypi.org/project/hypothesis-010/) and
[the GitHub repo](https://github.com/DavidDunbier/hypothesis-010) for the purposes of this COMP4560 project.

## API

`hypothesis-010` has been developed to a proof-of-concept stage over the course of this project. Inspired by
[`FormatFuzzer`](https://uds-se.github.io/FormatFuzzer/) and the wide variety of
useful features already integrated into Hypothesis, hypothesis-010 successfully supports a small subset of the filetypes
listed above.

## Using the tool:
I did most of my work on this tool, including testing and debugging, in the Spyder (4.1.5) IDE provided by Anaconda.
I recommend running my tool with this IDE to see the internal functions and data structures I used, as Spyder provides
an interactive session when running the file.

The only outward facing function is from_template, which takes in two arguments:
 - `filetemplate` = Path to the desired binary file template
 - `gen_as_bytes` = Boolean flag for how the resulting strategy should create it's examples. True generates the strategy to produce bytestrings of the file template, False generates the strategy to produce examples of the file template in python objects. Either strategy can produce valid examples of the filetype in their own format.

Other functions in the file are not intended for user interaction, serving only to help produce the final output of from_template.

It is also possible to run the tool from the command line using the following command:
`python __init__.py filetemplate gen_as_bytes`
But the resulting output in the terminal isn't very useful, showing the strategy generated without any formatting.

The getTemplates file is simply a method of fetching the binary templates listed from the sweetscape repository above, and should also be run by the Spyder IDE if required. I have also included the fetched templates as a part of this repository in the directory "templateRepo", so it shouldn't be necessary to run this file.

I acknowledge that the work for this project does not include the work from the following libraries, all of which are required to use this tool:
 - py010parser
 For the web scraper tool (not required for use of hypothesis-010):
 - beautifulsoup4
 - requests

Required libraries can be installed using: pip install (library_name)

## Supported versions and dependencies

`hypothesis-010` requires Python 3.6 or later, along with the following library dependencies:
 - [py010parser 0.1.18](https://pypi.org/project/py010parser/)
 
The webscraper also implemented as a part of helping me develop this tool requires the following libraries:
 - [requests 2.25.1](https://pypi.org/project/requests/)
 - [beautifulsoup4 4.9.3](https://pypi.org/project/beautifulsoup4/)
