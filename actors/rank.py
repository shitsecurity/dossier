#!/usr/bin/env python

from core.actor import Actor, forever, action, unique

from seo import tic, pr, Session

class PageRankActor( Actor ):

    name = 'rank.pr'

    listeners =  [
        'domain.rank',
        'domain.rank.pr',
        'domain.lookup.rank',
    ]

    def __init__( self, *args, **kwargs ):
        super( PageRankActor, self ).__init__( *args, **kwargs )
        self.session = Session()

    @forever
    @action
    @unique
    def act( self, domain ):
        rank = pr( domain, session=self.session )
        self.channels.publish('rank.pr', {'domain': domain, 'rank': rank})

class TICActor( Actor ):

    name = 'rank.tic'

    listeners =  [
        'domain.rank',
        'domain.rank.tic',
        'domain.lookup.rank',
    ]

    def __init__( self, *args, **kwargs ):
        super( TICActor, self ).__init__( *args, **kwargs )
        self.session = Session()

    @forever
    @action
    @unique
    def act( self, domain ):
        rank = tic( domain, session=self.session )
        self.channels.publish('rank.tic', {'domain': domain, 'rank': rank})
