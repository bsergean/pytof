#!/usr/bin/env coffee

fs = require 'fs'

helloWorld = ->
    for i in [0..5]
        console.log "Hello world"

ls = (dir) ->
    for fn in fs.readdirSync dir
        console.log fn

args = process.argv

helloWorld()
ls('..')

console.log args
