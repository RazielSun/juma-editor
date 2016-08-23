#!/usr/bin/env python

import os.path
from juma.core                	import app

##----------------------------------------------------------------##
class MeshObject( object ):
	def __init__( self, path ):
		self._per_pixel = 1.0
		self._texture = ""
		self._bake_light = False
		self._diffuse_power = 0.3
		self._ambient_light = (0.7, 0.7, 0.7, 1.0)
		self._light_direction = (0.14, 0.98, 0.14)
		self._static_batch = False
		self._export_name = ""
		self._export_animation_name = "animation.json"
		self._export_mesh = True
		self._export_animation = False
		self._export_transform = False
		self._export_buffers = False

		if isinstance(path, dict):
			self.LoadObject( path )
		else:
			self.SetPath( path )

	def __repr__( self ): return "< {} >   {}".format(self.format, self.name)
	def GetName( self ): return self.name
	def GetFormat( self ): return self.format

	def SetPath( self, path ):
		self.fullpath = app.getRelPath( path )
		fullname = os.path.basename( path )
		array = fullname.split('.')
		self.format = array[-1].upper()
		self.name = array[0].lower()
		self._export_name = array[0]

	def GetPath( self, abs_path = False ):
		if abs_path:
			return app.getAbsPath( self.fullpath )
		return self.fullpath

	def GetPerPixel( self ): return self._per_pixel
	def SetPerPixel( self, per_pixel ): self._per_pixel = per_pixel

	def GetTexture( self, abs_path = False ):
		if abs_path:
			return app.getAbsPath( self._texture )
		return self._texture
	def SetTexture( self, texture ): self._texture = texture

	def GetExportName( self ): return self._export_name
	def SetExportName( self, name ): self._export_name = name

	def GetExportAnimationName( self ): return self._export_animation_name
	def SetExportAnimationName( self, name ): self._export_animation_name = name

	def GetBakeLight( self ): return self._bake_light
	def SetBakeLight( self, bake_light ): self._bake_light = bake_light

	def GetDiffusePower( self ): return self._diffuse_power
	def SetDiffusePower( self, power ): self._diffuse_power = power

	def GetAmbientLight( self ): return self._ambient_light
	def SetAmbientLight( self, light ): self._ambient_light = light

	def GetLightDirection( self ): return self._light_direction
	def SetLightDirection( self, direction ): self._light_direction = direction

	def GetStaticBatch( self ): return self._static_batch
	def SetStaticBatch( self, static_batch ): self._static_batch = static_batch

	def GetExportMesh( self ): return self._export_mesh
	def SetExportMesh( self, export_mesh ): self._export_mesh = export_mesh

	def GetExportAnimation( self ): return self._export_animation
	def SetExportAnimation( self, export_animation ): self._export_animation = export_animation

	def GetExportTransform( self ): return self._export_transform
	def SetExportTransform( self, export_transform ): self._export_transform = export_transform

	def GetExportBuffers( self ): return self._export_buffers
	def SetExportBuffers( self, export_buffers ): self._export_buffers = export_buffers

	def GetSaveObject( self ):
		return dict(
			path = self.GetPath(),
			per_pixel = self.GetPerPixel(),
			texture = self.GetTexture(),
			export_name = self.GetExportName(),
			export_animation_name = self.GetExportAnimationName(),
			bake_light = self.GetBakeLight(),
			diffuse_power = self.GetDiffusePower(),
			ambient_light = self.GetAmbientLight(),
			light_direction = self.GetLightDirection(),
			static_batch = self.GetStaticBatch(),
			export_mesh = self.GetExportMesh(),
			export_animation = self.GetExportAnimation(),
			export_transform = self.GetExportTransform(),
			export_buffers = self.GetExportBuffers()
			)

	def LoadObject( self, data ):
		self.SetPath( data.get('path', "") )
		self.SetPerPixel( data.get('per_pixel', 1.0) )
		self.SetTexture( data.get('texture', "") )
		self.SetExportName( data.get('export_name', "") )
		self.SetExportAnimationName( data.get('export_animation_name', "") )
		self.SetBakeLight( data.get('bake_light', False) )
		self.SetDiffusePower( data.get('diffuse_power', 0.3) )
		self.SetAmbientLight( data.get('ambient_light', (0.7, 0.7, 0.7, 1.0)) )
		self.SetLightDirection( data.get('light_direction', (0.14, 0.98, 0.14)) )
		self.SetStaticBatch( data.get('static_batch', False) )
		self.SetExportMesh( data.get('export_mesh', True) )
		self.SetExportAnimation( data.get('export_animation', False) )
		self.SetExportTransform( data.get('export_transform', False) )
		self.SetExportBuffers( data.get('export_buffers', False) )

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
		if file and os.path.exists(file):
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
