""" The main module for the Stirling Engine.
    
    .. module::    stirling
        :synopsis: Stirling MUD
    .. moduleauthor: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1

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
VERSION     =   '0.1.0'

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
    'Fuck money, get bitches',  'Johnny\'s in the basement']
GREETING = ('Hi there!  You\'ve connected to Stirling, a textual MMORPG '
            'currently in active development.  You\'re probably here because '
            'you\'ve already heard about the project, and are here to help '
            'with testing or development.  If you have arrived here by '
            'accident, I recommend looking at %s before you '
            'register a user.' % HTTP_URI)

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
        # requires it.
        self.__dict__['logger'] = logging.getLogger(self.__module__)
        return

    def debug(self, message):
        """ Print the debug `message` to console.
        """
        return self.__dict__['logger'].debug(message)

    def info(self, message):
        """ Print the informative `message` to console.
        """
        return self.__dict__['logger'].info(message)

    def warning(self, message):
        """ Print the warning `message` to console.
        """
        return self.__dict__['logger'].warning(message)

    def error(self, message):
        """ Print the error `message` to console.
        """
        return self.__dict__['logger'].error(message)
