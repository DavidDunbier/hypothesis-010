# hypothesis-010

A tool to generate [Hypothesis](https://hypothesis.readthedocs.io) strategies for generating data
that matches some [010 editor](https://www.sweetscape.com/010editor/)
binary template.

This would include over [170 binary file formats built in](https://www.sweetscape.com/010editor/repository/templates/),
and [many more from the community](https://www.google.com/search?q=github+010+templates).

[Here's the PyPI page](https://pypi.org/project/hypothesis-010/) and
[the GitHub repo](https://github.com/DavidDunbier/hypothesis-010) for the purposes of this COMP4560 project.

## API

`hypothesis-010` has been developed to a proof-of-concept stage over the course of this project. Inspired by
[`FormatFuzzer`](https://uds-se.github.io/FormatFuzzer/) and the wide variety of
useful features already integrated into Hypothesis, hypothesis-010 successfully supports a small subset of the filetypes
listed above. 

## Supported versions

`hypothesis-010` requires Python 3.6 or later, along with the following library dependencies:
 - [py010parser 0.1.18](https://pypi.org/project/py010parser/)
 
The webscraper also implemented as a part of helping me develop this tool requires the following libraries:
 - [requests 2.25.1](https://pypi.org/project/requests/)
 - [beautifulsoup4 4.9.3](https://pypi.org/project/beautifulsoup4/)

## Changelog

Commit history can be found [here](https://github.com/DavidDunbier/hypothesis-010/blob/master/CHANGELOG.md).
