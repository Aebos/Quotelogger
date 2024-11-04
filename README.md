<h1 align="center">
  <img src="https://github.com/user-attachments/assets/727ac73f-7bfe-4802-acc4-f6802347cc2c" alt="Quotelogger!">

</h1>

**Quotelogger** is a simple python program to passively log user quotes from Twitch bots such as StreamElements

- Passively logs quotes from IRC with no authentication necessary
- Easy configuration
- Quotes saved in SQLite3
- No external Python depencies!

Extended by **qsearch**, which helps you manage the database by:
- Searching quotes by content or number
- Exporting the database to a CSV-file
- Finding missing quotes
- Estimating completion

## Installation
Installation can be done either by cloning the repository or downloading one of the released zip or tar.gz packages.

Unpack the included files in a suitable folder.  Database will be initialized when the program is run for the first time.

## Configuration
Quotelogger requires 4 values in it's config.ini file

This is the default config.ini
```
[Settings]

# Filename for quote database (eg. quotes.db)
database = quotes.db

# Channel name (eg. twitch)
channel = twitch

# Quote bot name (eg. StreamElements)
quotebotname = streamelements

# Template for parsing messages
template = @<usr>, #<num>: <quote>
```
Things you need to change are the channel name and quotebotname if the chosen channel has a custom name for StreamElements (or is using a different bot altogether)

For bots other than StreamElements, you'll need to customize the template to suit the output of the bot. This feature may change in the future.

## Running
Open up the your folder in the terminal and run:
```
python qlogger.py
```
Depending on your operating system, you might need to use python3 or py instead.

Press Ctrl + C to quit, as usual.

To use qsearch, run:
```
python qsearch.py - ARGUMENTS
```
Possible arguments for qsearch listed here:
| Short | Long | Explanation |
| ------------ | ------------ | ------------ |
| -h | --help | Show help message |
| -n | --number | Search quotes by number |
| -c | --content | Search quotes by content |
| -s | --stats | Show statistics on saved quotes |
| -a | --all | Show all saved quotes in order |
| -e | --export | Export all saved quotes to a CSV-file (Remember to include filename e.g Example.csv) |
| -m | --missing | Show which quotes are missing |

## Notes
Very rarely the program stops logging new quotes, this issue is still under investigation and hard to replicate.
For now, if you plan running this unsupervised I recommend restarting periodically.

Beautiful logo created with [Neo Cowsay](https://github.com/Code-Hex/Neo-cowsay)
