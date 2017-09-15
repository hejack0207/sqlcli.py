#!/usr/bin/env python
'''
    A substitute of Ora** SQL client that doesn't s*x
    Author: Alejandro E. Brito Monedero
'''

import readline
import sys
import os
import atexit

from db_op import Database
from auto_complete import DBcompleter
from process_line import Processor
import click

def print_usage():
    '''Prints command usage. =( I can't use argparse'''

    # I miss argparse
    print >> sys.stderr, ('''Usage: %s <oracle connection string (DSN)> 
        like "<user>/<password>@<db_host>:<db_port>/<database>"''' %
    sys.argv[0])


def io_loop(processor):
    '''Prompt reading loop'''

    prompt = 'pysqlcli> '
    while True:
        try:
            line = raw_input(prompt)
            processor.process_line(line)
        except(EOFError, KeyboardInterrupt):
            # Old schoold exception handling, dated python =(
            # cosmetic ending
            processor.close()
            print
            break


@click.command()
@click.option('--host',help="host name or ip")
@click.option('--port',default=1521,help="service port number")
@click.option('--sid',default='orcl',help="sid or service name")
@click.option('--user',help="user name")
@click.option('--password',help="password to login")
def _main(host,port,sid,user,password):
    '''Main function'''

    #if len(sys.argv) != 2:
    #    print_usage()
    #    sys.exit(1)
    #dsn = sys.argv[1]
    dsn = "%s/%s@%s:%s/%s" % (user,password,host,port,sid)
    print "dsn:"+dsn
    database = Database(dsn)
    # Enables tab completion and the history magic
    readline.parse_and_bind("tab: complete")
    # load the history file if it exists
    histfile = os.path.join(os.path.expanduser("~"), ".pysqlcli_history")
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass
    # register the function to save the history at exit. THX python examples
    atexit.register(readline.write_history_file, histfile)
    processor = Processor(database)
    db_completer = DBcompleter(database, processor.get_commands())
    readline.set_completer(db_completer.complete)
    io_loop(processor)
    database.close()


if __name__ == '__main__':
    _main()