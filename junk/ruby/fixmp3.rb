require "rubygems"
require "mp3info"
require 'find'

# http://ruby-mp3info.rubyforge.org/

def mp3tag(path)
    Mp3Info.open(path) do |mp3|
        # puts mp3info
        title = mp3.tag.title
        artist = mp3.tag.artist   
        album = mp3.tag.album
        tracknum = mp3.tag.tracknum
        if title.nil? || artist.nil? || album.nil? || tracknum.nil?
            puts "bad tags for \"" + path + "\""
        end
    end
end

#if __FILE__ == $0
mp3tag(ARGV[0])
#end
