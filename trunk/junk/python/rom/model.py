from elixir import *

metadata.bind = "sqlite:///rokulibrary_test.sqlite"

class Song(Entity):
    name = Field(Unicode(200))
    album = ManyToOne('Album')
    
    def __repr__(self):
        return '<Song "%s">' % (self.name)

class Album(Entity):
    name = Field(Unicode(200))
    artist = ManyToOne('Artist')
    songs = OneToMany('Song')
    
    def __repr__(self):
        return '<Album "%s">' % (self.name)

class Artist(Entity):
    name = Field(Unicode(200))
    albums = OneToMany('Album')
    
    def __repr__(self):
        return '<Artist "%s">' % (self.name)


if __name__ == '__main__':
    metadata.bind.echo = False

    # Test load from db
    Load = True
    if Load:
        setup_all(True)
        print Artist.query.all()

    else:
        setup_all(True)
        print Artist.query.all()
        a = Artist(name = 'Dyonisos')
        album = Album(name = 'Haiku', artist = a)

        session.flush()
        print Artist.query.all()
    
