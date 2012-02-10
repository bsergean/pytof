#!/usr/bin/env coffee

fs = require ('fs')
path = require ('path')

class Mesh
    constructor: (name) ->
        @name = name
        @verts = []
        @faces = []
        @facesColor = []
        @colors = []
        @defaultColor = [1, 0, 0]
        @defaultColorIdx = 0
        @colors.push @defaultColor

    addVert: (x, y) ->
        @verts.push [x, y]
        @verts.length - 1

    addFace: (v0, v1, v2) ->
        @facesColor.push @defaultColorIdx
        @faces.push [v0, v1, v2]
        @faces.length - 1

    addColor: (r, g, b) ->
        @colors.push [r, g, b]
        @colors.length - 1

    setColor: (f, c) ->
        @facesColor[f] = c

    middle: (v0, v1) ->
        [ (@verts[v0][0] + @verts[v1][0]) / 2,
          (@verts[v0][1] + @verts[v1][1]) / 2 ]
          
    #       v2
    #       t3
    #    v5    v4
    #    t0 t2 t1
    # v0    v3     v1
    subdivideFace: (f) ->
        [v0, v1, v2] = @faces[f]

        [x, y] = @middle(v0, v1)
        v3 = @addVert(x, y)
        [x, y] = @middle(v1, v2)
        v4 = @addVert(x, y)
        [x, y] = @middle(v2, v0)
        v5 = @addVert(x, y)

        @addFace(v0, v3, v5)
        @addFace(v3, v4, v5)
        @addFace(v3, v1, v4)
        @addFace(v5, v4, v2)

        @faces[f] = -1

    subdivide: ->
        for _, i in @faces
            @subdivideFace(i)

        @faces = (f for f in @faces when f != -1)

    randomColors: ->
        @colors = []
        for _, i in @faces
            c = @addColor(Math.random(),
                          Math.random(),
                          Math.random())
            @setColor(i, c)

    pushEdge: (v0, v1, f) ->
        edge = [v0, v1]
        console.log(edge)
        if @edgeFace[edge] == undefined
            @edgeFace[edge] = [f]
        else
            @edgeFace[edge].push(f)

    pushFace: (f0, f1) ->
        if @faceFace[f0] == undefined
            @faceFace[f0] = [f1]
        else
            @faceFace[f0].push(f1)

    connectTable: ->
        console.log("connectTable")
        @edgeFace = {}
        for f, i in @faces
            if f[0] < f[1]
                @pushEdge(f[0], f[1], i)
            else
                @pushEdge(f[1], f[0], i)

            if f[1] < f[2]
                @pushEdge(f[1], f[2], i)
            else
                @pushEdge(f[2], f[1], i)

            if f[2] < f[0]
                @pushEdge(f[2], f[0], i)
            else
                @pushEdge(f[0], f[2], i)

        console.log(Object.keys(@edgeFace).length)
        for e, faces of @edgeFace
            console.log("edge #{ e } ->", faces)

        @faceFace = {}
        for edge, faces of @edgeFace
            if faces.length == 2
                @pushFace(faces[0], faces[1])
                @pushFace(faces[1], faces[0])

        for f, faces of @faceFace
            console.log("face #{ f } ->", faces)

    toDot: (fn) ->
        fd = fs.openSync(absmtl, 'w')
        fs.writeSync(fd, "graph faceFace {\n")
        for f, faces of @faceFace
            for g in faces
                text = "  #{ f } -- #{ color[1] } #{ color[2] }\n\n"
                fs.writeSync(fd, text)
                
            console.log("face #{ f } ->", faces)
            text += "Kd #{ color[0] } #{ color[1] } #{ color[2] }\n\n"
            fs.writeSync(fd, text)
        fs.writeSync(fd, "}\n")
        fs.closeSync(fd)

    print: ->
        console.log "Verts:"
        for vert, i in @verts
            console.log('\t', i, vert[0], vert[1])
        console.log "Faces:"
        for face, i in @faces
            console.log('\t', i,
                        face[0], face[1], face[2])

    toObj: (fn) ->
        # Write material first
        mtl = path.basename(fn, path.extname(fn))
        absmtl = path.join(path.dirname(fn), mtl+'.mtl')
        fd = fs.openSync(absmtl, 'w')
        for color, i in @colors
            text  = "newmtl color#{i}\n"
            text += "Kd #{ color[0] } #{ color[1] } #{ color[2] }\n\n"
            fs.writeSync(fd, text)
        fs.closeSync(fd)
    
        # Then write .obj file
        fd = fs.openSync(fn, 'w')
        fs.writeSync(fd, "mtllib #{ absmtl }\n")

        for vert, i in @verts
            # console.log('v', vert[0], vert[1], 0)
            text = "v #{ vert[0] } #{vert[1]} 0 }\n"
            fs.writeSync(fd, text)

        fs.writeSync(fd, "\n")
        fs.writeSync(fd, "vn 0 0 0.8\n")

        for face, i in @faces
            text = "\ng group#{i}\n"
            fs.writeSync(fd, text)
            text = "usemtl color#{ @facesColor[i] }\n"
            fs.writeSync(fd, text)
            text  = "f #{ 1+face[0] }//1"
            text += "  #{ 1+face[1] }//1"
            text += "  #{ 1+face[2] }//1\n"
            fs.writeSync(fd, text)

        fs.closeSync(fd)

mesh = new Mesh("caca")
v0 = mesh.addVert(0, 0)
v1 = mesh.addVert(1, 0)
v2 = mesh.addVert(0.5, 0.86)
f0 = mesh.addFace(v0, v1, v2)
mesh.subdivide()
#mesh.subdivide()
#mesh.subdivide()
mesh.randomColors()
mesh.toObj("/Users/bsergean/Desktop/189.obj")
mesh.connectTable()
