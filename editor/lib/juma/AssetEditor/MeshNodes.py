#!/usr/bin/env python

import os.path

##----------------------------------------------------------------##
class OBJMaterialLib( object ):
	def __init__( self, path ):
		self.path = os.path.dirname( path )
		self.filename = os.path.basename( path )

		self.commands = {
			'newmtl' : "newMaterial",
			'map_Kd' : "setMap",
		}

		self.name = None
		self.textureName = None

		self.parse()

	def getFullPath( self ):
		return self.getPath( self.filename )

	def getPath( self, file ):
		if file:
			return os.path.join( self.path, file )
		return self.path

	def parse( self ):
		file = self.getFullPath()
		with open(file, "rU") as f:
			for line in f:
				s = [x.strip() for x in line.split()]
				if s and s[0] in self.commands:
					name = self.commands[s[0]]
					method = getattr(self, name)
					method(s)

	def use( self, name ):
		pass

	def newMaterial( self, data ):
		self.name = data[1]

	def setMap( self, data ):
		self.textureName = data[1]

	def GetTexturePath( self ):
		return self.getPath( self.textureName )

	def GetTextureName( self ):
		return self.textureName

##----------------------------------------------------------------##
class OBJNode( object ):
	def __init__( self, path ):
		self.path = os.path.dirname( path )
		self.filename = os.path.basename( path )
		self.name = None

		self.commands = {
			'o' : "setName",
			'v' : "writeVertex",
			'vn' : "writeNormal",
			'vt' : "writeUV",
			'g' : "writeGroup",
			'f' : "writeFace",
			'mtllib' : "loadMaterial",
			'usemtl' : "useMaterial",
		}

		self.vertexes = []
		self.uv = []
		self.normals = []
		self.faces = []
		self.material = None

		self.parse()

	def setName( self, data ):
		self.name = data[1]

	def GetName( self ):
		return self.name

	def getFullPath( self ):
		return self.getPath( self.filename )

	def getPath( self, file ):
		if file:
			return os.path.join( self.path, file )
		return self.path

	def parse( self ):
		file = self.getFullPath()
		with open(file, "rU") as f:
			for line in f:
				s = [x.strip() for x in line.split()]
				if s and s[0] in self.commands:
					name = self.commands[s[0]]
					method = getattr(self, name)
					method(s)

	def writeFace( self, data ):
		face = [tuple(x.split('/')) for x in data[1:]]
		self.faces.append(face)

	def writeGroup( self, data ):
		print("writeGroup", data)

	def writeVertex( self, data ):
		self.vertexes.append( tuple(data[1:]) )

	def writeNormal( self, data ):
		self.normals.append( tuple(data[1:]) )

	def writeUV( self, data ):
		self.uv.append( tuple(data[1:]) )
		# flip v - from Vavius
		# uv = data[1:]
		# uv = [uv[0], str(1.0 - float(uv[1]))]
		# obj['uv'].append(tuple(uv))

	def GetFaceCount( self ):
		return len(self.faces)

	def GetFaceSize( self, faceIndex ):
		return len(self.faces[faceIndex])

	def GetVertexes( self ):
		return self.vertexes

	def GetUV( self ):
		return self.uv

	def GetNormals( self ):
		return self.normals

	def GetFaceVertex( self, faceIndex, index ):
		face = self.faces[faceIndex]
		return face[index]
		# params = face[index]
		# (v, uv, n) = params
		# return [v, uv, n]

	def GetMaterial( self ):
		return self.material

	def loadMaterial( self, data ):
		self.material = OBJMaterialLib( self.getPath(data[1]) )

	def useMaterial( self, data ):
		if self.material:
			self.material.use( data[1] )