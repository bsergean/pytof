#!/usr/bin/env ruby
#[1, 2, 3].each do |elem|
#    unless elem == 1
#        msg  = elem
#        msg << "youpla"
#        puts msg
#    end
#end
#

# number = gets.chomp
# number.to_i 
#
# IO.popen("date") { |f| puts f.gets }

fn = '/usr/share/dict/words'
out = `cat #{fn} | wc -l`
puts out

File::open('foo.txt', 'w') do |f|
    Dir.new('.').each do |item| 
        f.puts item
    end
end

require 'find'
Find.find(ENV['HOME']) do |f|
    puts f
end

'foobar'.each do |elem|
    puts elem
end

number = 12
a = <<EOF
Ceci est un nombre: #{number}
EOF

puts a

#require 'net/http'
#Net::HTTP.start( 'www.ruby-lang.org', 80 ) do |http|
#    print( http.get( '/en/LICENSE.txt' ).body )
#end
