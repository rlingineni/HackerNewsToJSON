# Hacker News to JSON #

Save 'saved stories' from a Hacker News account to a simple JSON format.

The script parses the saved stories page on HN (http://news.ycombinator.com) and, for each link on each page of the saved stories history it outputs an entry to a JSON document with information taken from the Hacker News API. (https://github.com/HackerNews/API)

The script is meant to be launched from the command line.

Originally developed on iPad by Luciano Fiandesio with the awesome Pythonista (http://omz-software.com/pythonista/)
and modified for JSON output by John David Pressman.

## How to use ##

`python hn2json.py [hn user] [hn password] -n [Number of pages to grab] -f [JSON filename]`
