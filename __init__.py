""" The main module for the Stirling Engine.
    
    .. module::    stirling
        :synopsis: Main module for a persistent multiplayer role-playing game
    .. moduleauthor: emsenn <morgan.sennhauser@gmail.com>
    .. versionadded:: 0.1.1

    The main ``stirling`` module sets up a few of the constants that are 
    used across the engine, which are outlined in the table below.  In 
    addition, it also creates the class :class`BaseObj`, which is the core 
    class behind all daemons and entities.

    +-------------+------------------------------------------------------------+
    |   CONSTANT  |                         Value                              |
    +=============+============================================================+
    |     NAME    | The colloquial name for the MUD you are running.           |
    +-------------+------------------------------------------------------------+
    |             | The version of the MUD.  For information on how Stirling   |
    |   VERSION   | handles versioning, read the                               |
    |             | :doc:`developer's docs </dev/conventions/versioning>`      |
    +-------------+------------------------------------------------------------+
    |   HTTP_URI  | The HTTP URI to the documentation of the MUD.              |
    +-------------+------------------------------------------------------------+
    |   SPLASHES  | A list of phrases and words and random information that is |
    |             | shown to users on connect.                                 |
    +-------------+------------------------------------------------------------+
    |   GREETING  | The last text shown to an incoming connection prior to     |
    |             | requesting their username.                                 |
    +-------------+------------------------------------------------------------+
    |             | The host serving daemons bind to.  **Recommended:**        |
    |    HOST     | ``localhost`` for development, ``0.0.0.0`` for             |
    |             | production.                                                |
    +-------------+------------------------------------------------------------+
    |             | The port the                                               |
    |   MUD_PORT  | :class:`MUDServer <stirling.daemons.servers.MUDServer>`    |
    |             | binds to.                                                  |
    +-------------+------------------------------------------------------------+

"""


import logging


NAME        =   'Stirling'
VERSION     =   '0.1.1'

# If you don't want to use random splashes, uncomment this line and comment the 
# others.
# SPLASHES = [ ('Based on Stirling v%s' % VERSION) ]
HTTP_URI    =   'http://github.com/emsenn/stirling/'
SPLASHES = [
    'Oh bfo!',                  'We love panthers!', 
    'PRAISE BEETROOT!',         'It isn\'t work.',
    'Not Canland!',             'Probably illegal!', 
    'Grue-free!',               'Featureless!', 
    'Both fun and Fun!',        'Bane of Productivity!',
    'Way to go, sunshine!',     'Forget about the bunnies!',
    'Hello, Bigfoot.',          'It\'s a bucket of rainbows.',
    'Twenty-seven.',            'Mongoose fedora.',
    'Neptune\'s Net',           'It\'s how they\'ve always been.',
    'Hello My Love <3.',         'I heard a kiss from you.',
    'Symphony for a Feud',      '(::you are the sun::)',
    'Everyday seems so plain.'  'There\'s a cold day coming.',
    'Tonight is the night.',    'Don\'t fear the unknown,',
    'Everything\'s a miracle.', 'Love will set you free.',
    'Who says I can\'t?',       'Let\'s get down and dirty.',
    'If I don\'t do it...',     '...someone else will!',
    'ill b there w8ing 4 u',    'Sugary Philosphy',
    'Something\'s missing.',    'rm -rf /',
    'Death is just a door.',    'I love you more and more and more and more',
    'Next stop: Shangri-La.',   'Rave on, that crazy feeling.',
    'All over now.',            'Love is denser than water.',
    'Original',                 'Sweet confusing moonlight.',
    'Young money, cash money',  'Construct additional pylons.',
    'Bazingle!',                'Go on home, British soldiers, go on home.',
    'be here now',              'Exaaaaactly',
    'FUCKIN\' NIGGERS',         'Go outside, seriously',
    'Fuck money, get bitches',  'Johnny\'s in the basement',
    'I wanna bury you',         'I love you everything burrito',
    'Everybody\'s talkin\'',    'Redododiculous',
    'Be calmed by my saliva',   'I know you wanna slump up on these lumps',
    'This *does* compute',      'Youz ain\'t special',
    'Bunk this flip',           'You gonna do that thing again?',
    'What the what',            'Must this pig walk, forever alone?',
    'monkey watermelon,'         'Everything is chemicals',
    'WHATEVERS 2009!',          'What the cabbage?',
    'All about feeding hobos',  'Would you like to hear what my nuts have to say?',
    'Y\'all whack with poobrain', 'Hah that fly\'s poopin\' on your foot.',
    'Supercaliswagalisticsexyhelladopeness', 'Don\'t stay up too late.',
    'you are a part of all you have met,', 'Don\'t be that guy.',
    'All part of the proverbial "it."', 'Profane',
    'Less frequently useful than a broken clock', '#3cc',
    'showin\' up is the biggest part of showin\' up.',
    ]
GREETING = ('Stirling is a engine for building textual MMORPGs, and is currently '
            'in really really really early development.  So unless you\'re a '
            'developer, there is not much here for you to do.  If you are a '
            'developer, you probably don\'t even read this message anymore, and '
            'won\'t notice that I\'ve changed it for quite some time.  For more '
            'information, check out %s' % HTTP_URI)

# 0.0.0.0 for production, localhost for testing
HOST        =   '0.0.0.0'
MUD_PORT    =   5878
HTTP_PORT   =   5877

class BaseObj(object):
    """ The base object behind all :term:`entities <entity>` and 
        :term:`daemons <daemon>`.
    """
    def __init__(self):
        """ At the moment, all BaseObj defines is four methods to make logging 
            less verbose across the engine.

            .. todo:: Improve :class:`BaseObj`'s logging methods.
        """
        # The reason logger is added to self.__dict__ rather than set by 
        # using self.logger is because of the fact that entities' persistence 
        # requires it. ! DON'T CHANGE THIS UNLESS YOU KNOW WHAT YOU'RE DOING! !
        self.__dict__['logger'] = logging.getLogger(self.__module__)
        return

    def debug(self, message):
        """ Print the debug `message` to console.

            :param  message:        The message to be shown to the console.
            :type   message:        str
        """
        return self.__dict__['logger'].debug(message)

    def info(self, message):
        """ Print the informative `message` to console.

            :param  message:        The message to be shown to the console.
            :type   message:        str
        """
        return self.__dict__['logger'].info(message)

    def warning(self, message):
        """ Print the warning `message` to console.

            :param  message:        The message to be shown to the console.
            :type   message:        str
        """
        return self.__dict__['logger'].warning(message)

    def error(self, message):
        """ Print the error `message` to console.

            :param  message:        The message to be shown to the console.
            :type   message:        str
        """
        return self.__dict__['logger'].error(message)
