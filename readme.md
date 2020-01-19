# Hacker News to Google Search #

In addition to the original script - added a script to generate a list of links that can be used to search your upvoted articles with Google Custom Search.

Save 'saved stories' from a Hacker News account to a simple JSON format. The script is meant to be launched from the command line.

Originally developed on iPad by Luciano Fiandesio with the awesome [Pythonista] (http://omz-software.com/pythonista/) and modified for JSON output by John David Pressman.

## How to use ##

`python hn2json.py [hn user] [hn password] -n [Number of pages to grab] -f outputs.json`

`node main.js`

You can use the output of `hn-sites.txt` to copy and paste into Google Custom Search.

If you run into rate-limiting - you can pass the id to resume the script from into the `startParsing()` method.
