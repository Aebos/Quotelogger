import socket
import sqlite3
import configparser
import os
import sys
import re

SERVER = 'irc.chat.twitch.tv'
PORT = 6667


def load_config(filename='config.ini'):
    if not os.path.exists(filename):
        print(f"Error: '{filename}' not found.")
        print(f"{filename} must contain 'database', 'channel' and 'quotebotname'")
        sys.exit(1)

    conf = configparser.ConfigParser()
    conf.read(filename)
    return conf


def convert_to_regex(template):

    conversion_table = {
        '<usr>': r'(?:\S+)',
        '<num>': r'(?P<num>\d+)',
        '<quote>': r'(?P<quote>.+)'
    }

    regtemplate = re.escape(template)
    for placeholder, pattern in conversion_table.items():
        regtemplate = regtemplate.replace(re.escape(placeholder), pattern)

    return f'^{regtemplate}$'


config = load_config()
NICK = 'justinfan12345'
CHANNEL = '#' + config['Settings']['channel']
QUOTEBOT = config['Settings']['quotebotname']
DATABASE = config['Settings']['database']
TEMPLATE = convert_to_regex(config['Settings']['template'])

conn = sqlite3.connect(DATABASE)
cur: sqlite3.Cursor = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INTEGER UNIQUE,
    content TEXT
)
''')

conn.commit()


def read_chat():
    irc = socket.socket()
    irc.connect((SERVER, PORT))
    irc.settimeout(0.5)

    irc.send(f"PASS oauth:anonymous\r\n".encode('utf-8'))
    irc.send(f"NICK {NICK}\r\n".encode('utf-8'))
    irc.send(f"JOIN {CHANNEL}\r\n".encode('utf-8'))

    while True:
        try:
            response = irc.recv(2048).decode('utf-8')
            if response.startswith('PING'):
                irc.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
            else:
                checksave(response.strip())
        except socket.timeout:
            continue
        except KeyboardInterrupt:
            print("Exiting...")
            break

    irc.close()
    conn.close()


def checksave(resp):
    name = resp.split('!')[0]
    if name[1:] == QUOTEBOT:
        content = resp.split(':', 2)[-1]
        match = re.match(TEMPLATE, content)

        if match:
            parts = match.groupdict()
            number = parts.get('num')
            quote = parts.get('quote')

            cur.execute('''
            INSERT OR IGNORE INTO quotes (number, content) VALUES (?, ?)
            ''', (number, quote))
            conn.commit()
            print("Logged quote #" + str(number) + " successfully!")


def main():
    print("Started QuoteLogger V.1.6")
    try:
        read_chat()
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
