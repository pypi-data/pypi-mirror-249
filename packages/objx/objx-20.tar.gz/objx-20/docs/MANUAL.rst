NAME

::

    LIBOP - original programmer.

SYNOPSIS

::

    op <cmd> [key=val] 
    op <cmd> [key==val]
    op [-c] [-v] [-d]


DESCRIPTION

::



    LIBOP is a python3 library implementing the 'op' package. It
    provides all the tools to program a bot, such as disk perisistence
    for configuration files, event handler to handle the client/server
    connection, code to introspect modules for commands, deferred
    exception handling to not crash on an error, a parser to parse
    commandline options and values, etc.

    LIBOP provides a demo bot, it can connect to IRC, fetch and
    display RSS feeds, take todo notes, keep a shopping list
    and log text. You can also copy/paste the service file and run
    it under systemd for 24/7 presence in a IRC channel.

    LIBOP is a contribution back to society and is Public Domain.


INSTALL


::

    $ pipx install libbot


USAGE

::

    without any argument the program does nothing

    $ op
    $

    see list of commands

    $ op cmd
    cmd,err,mod,req,thr,ver

    list of modules

    $ op mod
    cmd,err,fnd,irc,log,mod,req,rss,tdo,thr

    use mod=<name1,name2> to load additional
    modules

    $ op cfg mod=irc

    start a console

    $ op -c mod=irc,rss
    >

    use -v for verbose

    $ op -cv mod=irc
    OP started CV started Sat Dec 2 17:53:24 2023
    >

    start daemon

    $ op -d mod=irc,rss
    $ 


CONFIGURATION


::

    irc

    $ op cfg server=<server>
    $ op cfg channel=<channel>
    $ op cfg nick=<nick>

    sasl

    $ op pwd <nsvnick> <nspass>
    $ op cfg password=<frompwd>

    rss

    $ op rss <url>
    $ op dpl <url> <item1,item2>
    $ op rem <url>
    $ op nme <url< <name>


COMMANDS


::

    cmd - commands
    cfg - irc configuration
    dlt - remove a user
    dpl - sets display items
    fnd - find objects 
    log - log some text
    met - add a user
    mre - displays cached output
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    req - reconsider
    rss - add a feed
    thr - show the running threads


SYSTEMD


::

    save the following it in /etc/systems/system/libop.service and
    replace "<user>" with the user running pipx


    [Unit]
    Description=original programmer
    Requires=network.target
    After=network.target

    [Service]
    Type=simple
    User=<user>
    Group=<user>
    WorkingDirectory=/home/<user>/.op
    ExecStart=/home/<user>/.local/pipx/venvs/libop/bin/op -d mod=irc,rss
    RemainAfterExit=yes

    [Install]
    WantedBy=multi-user.target


    then run this

    $ mkdir ~/.op
    $ sudo systemctl enable libop --now

    default channel/server is #op on localhost


FILES

::

    ~/.op
    ~/.local/bin/op
    ~/.local/pipx/venvs/libop/


AUTHOR


::

    botlib <libbotx@gmail.com>


COPYRIGHT


::

    LIBOP is Public Domain.
