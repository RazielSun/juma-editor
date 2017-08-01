#!/usr/bin/env python

import os.path
import math
import logging

from juma.core                	import signals

import pyassimp
from pyassimp.postprocess import *
from pyassimp.helper import multiplyTransform, quatToEuler

##----------------------------------------------------------------##
def _getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
class PyAssimpConverter( object ):
	def __init__( self ):
		pass

	##----------------------------------------------------------------##
	def preview(self, objects, options):
		signals.emitNow( 'mesh.assimp_clear' )
		for obj in objects:
			self.convert( obj, options )
		signals.emitNow( 'mesh.assimp_render' )

	##----------------------------------------------------------------##
	def export(self, objects, path, options):
		signals.emitNow( 'mesh.assimp_clear' )
		for obj in objects:
			self.convert( obj, options )
		signals.emitNow( 'mesh.assimp_save', path )

	##----------------------------------------------------------------##
	def convert(self, obj, options):
		processing = (aiProcess_Triangulate|aiProcessPreset_TargetRealtime_MaxQuality|aiProcess_FlipUVs)
		if obj.GetStaticBatch():
			processing = (aiProcess_Triangulate|aiProcessPreset_TargetRealtime_MaxQuality|aiProcess_FlipUVs|aiProcess_PreTransformVertices)

		scene = pyassimp.load(obj.GetPath( True ), processing = processing)

		#the model we load
		print
		print("MODEL:" + str(obj))
		print

		#write some statistics
		print("SCENE:")
		print("  meshes:" + str(len(scene.meshes)))
		print("  materials:" + str(len(scene.materials)))
		print("  textures:" + str(len(scene.textures)))
		print

		materials = []
		print("MATERIALS:")
		for index, material in enumerate(scene.materials):
			print("  MATERIAL (id:" + str(index+1) + ")")
			path = ""
			matName = ""
			for key, value in material.properties.items():
				print("    %s: %s" % (key, value))
				if key == "file":
					path = value
				elif key == "name":
					matName = value
			mat = {
				"id" 	: index+1,
				"file"	: os.path.basename(path),
				"path"	: path,
				"name"	: matName,
			}
			materials.append(mat)
		print
		signals.emitNow( 'mesh.assimp_materials', materials )

		print("TEXTURES:")
		for index, texture in enumerate(scene.textures):
			print("  TEXTURE" + str(index+1))
			print("    width:" + str(texture.width))
			print("    height:" + str(texture.height))
			print("    hint:" + str(texture.achformathint))
			print("    data (size):" + str(len(texture.data)))

		print("MESHES:")
		meshCount = len(scene.meshes)

		for index, mesh in enumerate(scene.meshes):
			if meshCount == 1:
				mesh.name = obj.GetExportName()
			else:
				mesh.name = "{}{}".format(obj.GetExportName(),index+1)

			print("  MESH id: " + str(index+1) + " (" + str(mesh.name) + ")")
			print("    material id: " + str(mesh.materialindex+1))
			print("    vertices: " + str(len(mesh.vertices)))
			print("    normals: " + str(len(mesh.normals)))
			print("    colors: " + str(len(mesh.colors)))
			print("    uv channels: " + str(len(mesh.texturecoords)))
			print("    uv-component-count:" + str(len(mesh.numuvcomponents)))
			print("    faces:" + str(len(mesh.faces)))
			print("    bones:" + str(len(mesh.bones)))
			print

			bonesNames = []
			for bone in mesh.bones: bonesNames.append(bone.name)

			meshDict = {
				'name'          : mesh.name or index,
				'materialID'	: mesh.materialindex+1,
				'vertices'      : mesh.vertices,
				'verticesCount' : len(mesh.vertices),
				'texturecoords' : mesh.texturecoords,
				'uvcounts' 		: len(mesh.texturecoords),
				'faces'         : mesh.faces,
				'facesCount'    : len(mesh.faces),
				'bones'         : mesh.bones,
				'bonesNames'	: bonesNames,
				'normals'       : mesh.normals
			}
			signals.emitNow( 'mesh.assimp_mesh', meshDict, obj, options )

		print
		print("NODES:")
		transforms = []
		self.searchNode(scene.rootnode, transforms)
		size = obj.GetPerPixel()
		for tr in transforms:
			pos = tr['pos']
			for i, v in enumerate(pos):
				pos[i] = v * size

		signals.emitNow( 'mesh.assimp_transforms', obj, transforms )

		# Finally release the model
		pyassimp.release(scene)

	##----------------------------------------------------------------##
	def searchNode(self, node, data, tr = None, level = 0):
		print("  " + "\t" * level + "- " + str(node))

		hasMesh = None
		for mesh in node.meshes:
			hasMesh = mesh.name
			print("  " + "\t" * level + " mesh:" + str(mesh.name))

		ntr = multiplyTransform( node.transformation, tr )

		if hasMesh:
			m = pyassimp.matrix_from_transformation(ntr)
			scl, rot, pos = pyassimp.decompose_matrix(m)
			ra, rb, rc = quatToEuler( rot )
			trDict = {
				'name': hasMesh,
				'pos':[pos.x, pos.y, pos.z],
				'rot':[math.degrees(ra), math.degrees(rb), math.degrees(rc)],
				'scl':[scl.x, scl.y, scl.z],
			}
			data.append( trDict )

		for child in node.children:
			self.searchNode(child, data, ntr, level+1)
