import sqlite3
import argparse
import csv
import configparser


def load_config(filename='config.ini'):
    conf = configparser.ConfigParser()
    conf.read(filename)
    return conf


config = load_config()
DATABASE = config['Settings']['database']


def search_export(filename):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT number, content FROM quotes ORDER BY number ASC')
    results = cursor.fetchall()
    conn.close()

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Number', 'Content'])
        csvwriter.writerows(results)

    print(f"Quotes exported to {filename}")


def search_num(number):
    conn = sqlite3.connect(DATABASE)
    cur: sqlite3.Cursor = conn.cursor()
    cur.execute('SELECT content FROM quotes WHERE number = ?', (number,))
    result = cur.fetchone()
    conn.close()
    if result:
        print(f"Quote {number}: {result[0]}")
    else:
        print(f"No quote found with number {number}.")


def search_con(content):
    conn = sqlite3.connect(DATABASE)
    cur: sqlite3.Cursor = conn.cursor()
    cur.execute('SELECT number, content FROM quotes WHERE content LIKE ?', (f'%{content}%',))
    results = cur.fetchall()
    conn.close()
    if results:
        for number, content in results:
            print(f"Quote {number}: {content}")
    else:
        print(f"No quotes contain '{content}'.")


def search_stats():
    conn = sqlite3.connect(DATABASE)
    cur: sqlite3.Cursor = conn.cursor()
    cur.execute('SELECT COUNT(*), MAX(number) FROM quotes')
    count, max_number = cur.fetchone()
    conn.close()
    print(f"Total quotes: {count}")
    print(f"Highest logged quote: {max_number}")
    print(f"Estimated completion: {round((count/max_number)*100)}%")


def search_all():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT number, content FROM quotes ORDER BY number ASC')
    results = cursor.fetchall()
    conn.close()
    if results:
        for number, content in results:
            print(f"Quote {number}: {content}")
    else:
        print("No quotes found.")


def search_missing():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT number FROM quotes ORDER BY number ASC')
    results = cursor.fetchall()

    conn.close()

    if results:
        numbers = [row[0] for row in results]

        missing_num = []
        for i in range(numbers[0], numbers[-1] + 1):
            if i not in numbers:
                missing_num.append(i)

        if missing_num:
            print("Missing quotes:")
            for num in missing_num:
                print(num)
            print("")
            print(f"{len(missing_num)} missing quotes in total")
        else:
            print("No missing quotes!")
    else:
        print("No quotes in database")


def main():
    parser = argparse.ArgumentParser(description='Search for quotes in the database')
    parser.add_argument('-n', '--number', type=int, help='Search for quote by number')
    parser.add_argument('-c', '--content', type=str, help='Search for quote by content')
    parser.add_argument('-s', '--stats', action='store_true', help='Show statistics on collected quotes')
    parser.add_argument('-a', '--all', action='store_true', help='Print all quotes in order')
    parser.add_argument('-e', '--export', type=str, help='Export all quotes to a CSV file')
    parser.add_argument('-m', '--missing', action='store_true', help='Find missing quotes')
    args = parser.parse_args()

    print("Version 1.6.2\n")
    if args.stats:
        search_stats()
    elif args.all:
        search_all()
    elif args.number is not None:
        search_num(args.number)
    elif args.content is not None:
        search_con(args.content)
    elif args.export:
        search_export(args.export)
    elif args.missing:
        search_missing()
    else:
        print("Please provide a search parameter: -n <number> or -c <content>")
        print("Use -h for a list of available commands")


if __name__ == "__main__":
    main()
