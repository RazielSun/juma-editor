#!/usr/bin/env python

import os.path
import time
import math
import logging

from PySide                   	import QtCore, QtGui, QtOpenGL
from PySide.QtCore            	import Qt

from juma.core                	import signals, app, jsonHelper, Field
from AssetEditor             	import AssetEditorModule
from MeshNodes 					import OBJNode
from juma.qt.controls.GenericListWidget import GenericListWidget

import pyassimp
from pyassimp.postprocess import *
from pyassimp.helper import multiplyTransform, quatToEuler

from fbx import *
import FbxCommon
import fbxsip

from juma.qt.controls.PropertyEditor.PropertyEditor import buildFieldEditor

##----------------------------------------------------------------##
def _getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
def _traceClass( clazz ):
	print(" TRACE: " + str(clazz))
	for it in clazz.__dict__.items():
		print(" - " + str(it))

##----------------------------------------------------------------##
class MeshObject( object ):
	def __init__( self, path ):
		self._per_pixel = 1.0
		self._texture = ""
		self._export_name = ""
		self._export_anim = "animation.json"
		self._bake_light = False
		self._diffuse_power = 0.3
		self._ambient_light = (0.7, 0.7, 0.7, 1.0)
		self._light_direction = (0.14, 0.98, 0.14)
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

	def GetExportAnimation( self ): return self._export_anim
	def SetExportAnimation( self, name ): self._export_anim = name

	def GetBakeLight( self ): return self._bake_light
	def SetBakeLight( self, bake_light ): self._bake_light = bake_light

	def GetDiffusePower( self ): return self._diffuse_power
	def SetDiffusePower( self, power ): self._diffuse_power = power

	def GetAmbientLight( self ): return self._ambient_light
	def SetAmbientLight( self, light ): self._ambient_light = light

	def GetLightDirection( self ): return self._light_direction
	def SetLightDirection( self, direction ): self._light_direction = direction

	def GetSaveObject( self ):
		return dict(
			path = self.GetPath(),
			per_pixel = self.GetPerPixel(),
			texture = self.GetTexture(),
			export_name = self.GetExportName(),
			export_anim = self.GetExportAnimation(),
			bake_light = self.GetBakeLight(),
			diffuse_power = self.GetDiffusePower(),
			ambient_light = self.GetAmbientLight(),
			light_direction = self.GetLightDirection()
			)

	def LoadObject( self, data ):
		self.SetPath( data.get('path', "") )
		self._per_pixel = data.get('per_pixel', 1.0)
		self._texture = data.get('texture', "")
		self._export_name = data.get('export_name', "")
		self._export_anim = data.get('export_anim', "")
		self._bake_light = data.get('bake_light', False)
		self._diffuse_power = data.get('diffuse_power', 0.3)
		self._ambient_light = data.get('ambient_light', (0.7, 0.7, 0.7, 1.0))
		self._light_direction = data.get('light_direction', (0.14, 0.98, 0.14))

##----------------------------------------------------------------##
class MeshExporter( AssetEditorModule ):
	"""docstring for MeshExporter"""
	_name = 'mesh_exporter'
	_dependency = [ 'qt', 'moai', 'asset_editor' ]

	def __init__(self):
		super(MeshExporter, self).__init__()
		self.config_name = "mesh_export_config"
		self.export_path = "assets/3ds/"
		self.objects = []
		self.config = {}

	def onLoad(self):
		self.window = self.requestDockWindow(
			'MeshExporter',
			title = 'Mesh Exporter',
			dock  = 'right',
			minSize = (300,200)
			)

		self.toolbar = self.addToolBar( 'mesh_exporter', self.window.addToolBar() )

		self.export_path_edit = epedit= QtGui.QLineEdit( None )
		epedit.textChanged.connect( self.onExportPathChange )

		self.addTool( 'mesh_exporter/add_object', label = 'Add', icon = 'plus_mint' )
		self.addTool( 'mesh_exporter/remove_object', label = 'Remove', icon = 'minus' )
		self.addTool( 'mesh_exporter/preview_render', label = 'Preview' )
		self.addTool( 'mesh_exporter/export', label = 'Export' )
		# self.addTool( 'mesh_exporter/export_all', label = 'ExportAll' )
		self.addTool( 'mesh_exporter/export_animation', label = 'Animation' )
		self.addTool( 'mesh_exporter/export_path_edit', widget = epedit )

		self.mainWidget = wdgt = QtGui.QWidget()
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(wdgt.sizePolicy().hasHeightForWidth())
		wdgt.setSizePolicy(sizePolicy)
		wdgt.setMinimumSize(QtCore.QSize(300, 400))
		wdgt.resize(300, 500)

		self.mainLayout = layout = QtGui.QFormLayout(wdgt)
		layout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
		layout.setRowWrapPolicy(QtGui.QFormLayout.DontWrapRows)
		layout.setContentsMargins(5, 5, 5, 5)

		self.window.addWidget( wdgt, expanding=False )

		self.editors = {}

		self.addField( Field("SetPerPixel", "PerPixelSize", float) )
		self.addField( Field("SetTexture", "Texture", str) )
		self.addField( Field("SetExportName", "ExportName", str) )
		self.addField( Field("SetExportAnimation", "ExportAnim", str) )
		self.addField( Field("SetBakeLight", "BakeLight", bool) )
		self.addField( Field("SetDiffusePower", "DiffusePower", float) )
		self.addField( Field("SetAmbientLight", "AmbientLight", 'color') )
		self.addField( Field("SetLightDirection", "LightDircetion", 'vec3') )

		self.list = self.window.addWidget( 
				MeshExporterListWidget( 
					multiple_selection = False,
					editable           = False,
					drag_mode          = False
				)
			)
		self.list.parentModule = self

		signals.connect( 'project.load', 		self.onProjectLoad )

	def onUnload(self):
		self.saveConfig()

	def addField( self, field ):
		label = field.label
		editor  =  buildFieldEditor( self, field )
		labelWidget  = editor.initLabel( label, self.mainWidget )
		editorWidget = editor.initEditor( self.mainWidget )
		self.mainLayout.addRow ( labelWidget, editorWidget )
		self.editors[label] = editor
		return editor

	def updateList( self ):
		self.list.rebuild()

	def getObjects( self ):
		return self.objects

	def getObjectData( self ):
		data = []
		for obj in self.objects:
			data.append( obj.GetSaveObject() )
		return data

	def openObject( self ):
		fileName, filt = self.getSceneEditor().openFile( "3D Object (*.fbx *.obj)", "Open 3D Object" )
		if fileName:
			self.addObject( fileName )
			self.saveConfig()

	def addObject( self, data ):
		obj = None
		if type(data) is dict:
			obj = MeshObject( data )
		else:
			obj = MeshObject( app.getRelPath(data) )
		self.objects.append(obj)
		self.onAddObject( obj )

	def getObjectIndex( self, obj ):
		index = -1
		for i, o in enumerate(self.objects):
			if o == obj:
				index = i
				break
		return index

	def removeObjects( self ):
		selection = self.list.getSelection()
		for obj in selection:
			index = self.getObjectIndex( obj )
			if index >= 0:
				self.objects.pop( index )
				self.onRemoveObject( obj )
		self.saveConfig()

	def saveConfig( self ):
		self.config["export_path"] = self.export_path
		self.config["data"] = self.getObjectData()

		proj = self.getProject()
		if proj:
			proj.setConfig( self.config_name, self.config )
			proj.saveConfig()

	def loadConfig( self ):
		data = self.config.get( "data", None )
		if data:
			self.objects = []
			for p in data:
				self.addObject( p )
		self.export_path = self.config.get("export_path", "")
		self.export_path_edit.setText( self.export_path )

	def getFullPath( self, path ):
		project = app.getProject()
		if project:
			path = project.getPath(path)
		return path

	##----------------------------------------------------------------##
	def previewRender( self ):
		signals.emitNow( 'mesh.preview' )
		signals.emitNow( 'mesh.assimp_clear' )
		selection = self.list.getSelection()
		for obj in selection:
			self.assimpConvert( obj )
		signals.emitNow( 'mesh.assimp_render' )

	def export( self, olist ):
		signals.emitNow( 'mesh.assimp_clear' )
		for obj in olist:
			self.assimpConvert( obj )
		path = self.getFullPath(self.export_path)
		signals.emitNow( 'mesh.assimp_save', path )

	def exportAnimation( self, olist ):
		for obj in olist:
			self.fbxConvert( obj )

	def exportSelected( self ):
		selection = self.list.getSelection()
		self.export( selection )

	def exportAnimationSelected( self ):
		selection = self.list.getSelection()
		self.exportAnimation( selection )

	def exportAll( self ):
		self.export( self.objects )

	##----------------------------------------------------------------##
	def onMenu(self, node):
		name = node.name

	def onTool( self, tool ):
		name = tool.name

		if name == 'add_object':
			self.openObject()
		elif name == 'remove_object':
			self.removeObjects()

		elif name == 'preview_render':
			self.previewRender()
		elif name == 'export':
			self.exportSelected()
		elif name == 'export_animation':
			self.exportAnimationSelected()
		elif name == 'export_all':
			self.exportAll()

	def onAddObject( self, obj ):
		self.list.addNode( obj )

	def onRemoveObject( self, obj ):
		self.list.removeNode( obj )

	def onProjectLoad( self, project ):
		self.config = project.getConfig( self.config_name, None )
		if self.config is None:
			self.config = {}
			self.saveConfig()
		else:
			self.loadConfig()
		self.updateList()

	def onExportPathChange( self, text ):
		self.export_path = text

	def onPropertyChanged( self, field, value ):
		selection = self.list.getSelection()
		for obj in selection:
			fname = field.model
			func = getattr(obj, fname)
			func( value )

	def onItemSelectionChanged( self ):
		selection = self.list.getSelection()
		for obj in selection:
			self.editors.get("PerPixelSize").set( obj.GetPerPixel() )
			self.editors.get("Texture").set( obj.GetTexture() )
			self.editors.get("ExportName").set( obj.GetExportName() )
			self.editors.get("ExportAnim").set( obj.GetExportAnimation() )
			self.editors.get("BakeLight").set( obj.GetBakeLight() )
			self.editors.get("DiffusePower").set( obj.GetDiffusePower() )
			self.editors.get("AmbientLight").set( obj.GetAmbientLight() )
			self.editors.get("LightDircetion").set( obj.GetLightDirection() )

	##----------------------------------------------------------------##
	def getFBXNode( self, fileName ):
		# Prepare the FBX SDK.
		lSdkManager, lScene = FbxCommon.InitializeSdkObjects()
		# Open FBX file
		lResult = FbxCommon.LoadScene(lSdkManager, lScene, fileName)
		if lResult:
			rootNode = lScene.GetRootNode()
			rootNode.FbxLayerElement = FbxLayerElement
			return rootNode
		# FbxCommon.SaveScene(lSdkManager, lScene, path + '/' + 'output.fbx')

		# Destroy all objects created by the FBX SDK.
		lSdkManager.Destroy()

	def getOBJNode( self, fileName ):
		node = OBJNode( fileName )
		return node

	def recur_node(self,node,data,tr = None,level = 0):
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
			self.recur_node(child,data,ntr,level+1)

	def assimpConvert(self, obj):
	    scene = pyassimp.load(obj.GetPath( True ), processing = (aiProcessPreset_TargetRealtime_MaxQuality|aiProcess_FlipUVs)) 
	    # aiProcess_PreTransformVertices - Static Batching (Material)
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
	            'vertices'      : mesh.vertices,
	            'verticesCount' : len(mesh.vertices),
	            'texturecoords' : mesh.texturecoords,
	            'faces'         : mesh.faces,
	            'facesCount'    : len(mesh.faces),
	            'bones'         : mesh.bones,
	            'bonesNames'	: bonesNames,
	            'normals'       : mesh.normals
	        }
	        signals.emitNow( 'mesh.assimp_mesh', meshDict, obj )

	    print
	    print("NODES:")
	    transforms = []
	    self.recur_node(scene.rootnode, transforms)
	    size = obj.GetPerPixel()
	    for tr in transforms:
	    	pos = tr['pos']
	    	for i, v in enumerate(pos):
	    		pos[i] = v * size
	    signals.emitNow( 'mesh.assimp_transforms', obj.GetExportName(), transforms )

	    print("MATERIALS:")
	    for index, material in enumerate(scene.materials):
	        print("  MATERIAL (id:" + str(index+1) + ")")
	        for key, value in material.properties.items():
	            print("    %s: %s" % (key, value))
	    print
	    
	    print("TEXTURES:")
	    for index, texture in enumerate(scene.textures):
	        print("  TEXTURE" + str(index+1))
	        print("    width:" + str(texture.width))
	        print("    height:" + str(texture.height))
	        print("    hint:" + str(texture.achformathint))
	        print("    data (size):" + str(len(texture.data)))
	    
	    # Finally release the model
	    pyassimp.release(scene)

	def fbxConvert(self, obj):
		if obj.GetFormat() == 'FBX':
			lSdkManager, lScene = FbxCommon.InitializeSdkObjects()
			lResult = FbxCommon.LoadScene(lSdkManager, lScene, obj.GetPath( True ))
			if lResult:
				settings = lScene.GetGlobalSettings()
				self.timeMode = settings.GetTimeMode()
				# _traceClass(FbxGlobalSettings)

				count = lScene.GetSrcObjectCount()
				# print
				# print("ALL SRC OBJECTS: ", count)
				# print
				for i in range(count):
					srcObject = lScene.GetSrcObject(i)
					# print(str(i) + ". object " + str(srcObject))
					if srcObject.ClassId == FbxAnimStack.ClassId:
						self.currentAnimStack = srcObject
					if srcObject.ClassId == FbxAnimEvaluator.ClassId:
						self.currentAnimEvaluator = srcObject
					if srcObject.ClassId == FbxPose.ClassId:
						self.loadPose(srcObject)
						# print(" Anim stack:" + str(srcObject))
						# self.fbxAnimStack(srcObject)

				rootNode = lScene.GetRootNode()
				# self.searchNode(rootNode, animEvaluator, animStack)

				# _traceClass(FbxAnimStack)
				# _traceClass(FbxAnimEvaluator)
				# _traceClass(FbxNode)
				# _traceClass(FbxTime)

				# self.findAnimation(rootNode, self.currentAnimStack)
				
				frames, frameRate = self.getTotalFrames(self.currentAnimStack)
				skeleton = { 'bones' : [], "animations" : { "default" : { 'bones' : {}, 'frameRate' : int(frameRate), 'frames' : int(frames) } } }
				self.searchSkeleton(rootNode, skeleton)

				path = self.getFullPath(self.export_path)
				jsonHelper.saveJSON(skeleton, path + obj.GetExportAnimation())
				
			lSdkManager.Destroy()

	def searchSkeleton(self, node, skeleton, level = 0):
		for i in range(node.GetChildCount()):
			child = node.GetChild(i)
			hasSkelet = child.GetSkeleton()
			if hasSkelet:
				bones = skeleton.get('bones')
				animations = skeleton.get('animations')
				default = animations.get('default')
				bonesAnim = default.get('bones')
				self.addSkeleton(bones, bonesAnim, child)
			else:
				self.searchSkeleton(child, skeleton, level + 1)

	def addSkeleton(self, bones, anims, node):
		evaluator = self.currentAnimEvaluator
		time = FbxTime()
		time.SetTime( 0, 0, 0 )
		matrix = evaluator.GetNodeLocalTransform(node, time)

		name = node.GetName()
		# transform = []
		# for y in range(4):
		# 	transform.append([])
		# 	for x in range(4):
		# 		transform[y].append(matrix.Get(x,y))

		pos = matrix.GetT()
		rot = matrix.GetR()
		scl = matrix.GetS()

		# prer = node.PreRotation.Get()
		# print(" bone "+ str(name) + " PreRotation " + str(prer) + " " + str(prer))

		bone = {
			'name' : name,
			'children' : [],
			'inverseBindPose' : self.bindPoses[name] or [],
			# 'transform' : transform,
			'position' : [pos[0], pos[1], pos[2]],
			'rotation' : [rot[0], rot[1], rot[2]],
			'scale' : [scl[0], scl[1], scl[2]],
		}
		bones.append(bone)

		stack = self.currentAnimStack
		boneAnimation = {}
		self.findCurveNode(node.LclTranslation.GetCurveNode(stack), 'loc', boneAnimation)
		self.findCurveNode(node.LclRotation.GetCurveNode(stack), 'rot', boneAnimation)
		self.findCurveNode(node.LclScaling.GetCurveNode(stack), 'scl', boneAnimation)
		anims[str(name)] = boneAnimation

		for i in range(node.GetChildCount()):
			child = node.GetChild(i)
			self.addSkeleton(bone.get('children'), anims, child)

	def findCurveNode(self, node, name, bone):
		if node:
			for ch in range(node.GetChannelsCount()):
				for c in range(node.GetCurveCount(ch)):

					curve = node.GetCurve(ch,c)
					channel = str(node.GetChannelName(ch))
					animKey = "{}{}".format(name, channel)
					animation = self.getAnimWithKey(bone, animKey)
					if not animation:
						animation = []
						bone[animKey] = animation

					for k in range(curve.KeyGetCount()):
						time = curve.KeyGetTime(k)
						frame = int(self.getFrameFromTime(time))
						value = curve.KeyGetValue(k)
						animation.append( { 'frame' : frame, 'value' : value } )

	def getAnimWithKey(self, bone, key):
		if bone:
			for k in bone:
				if k == key:
					return bone[key]
		return None

	def loadPose( self, pose ):
		bindPoses = {}
		# _traceClass(FbxPose)
		for i in range(pose.GetCount()):
			node = pose.GetNode(i)
			name = pose.GetNodeName(i)
			mtx = pose.GetMatrix(i)
			inv = mtx.Inverse()
			transform = []
			for y in range(4):
				transform.append([])
				for x in range(4):
					transform[y].append(inv.Get(x,y))
			bindPoses[str(name.GetCurrentName())] = transform
			# print(" pose node " + str(node) + " " + str(name.GetCurrentName()) + " " + str(transform))
		self.bindPoses = bindPoses

	def traceCurveNode(self, node, name):
		print(" CURVE NODE:" + str(node) + " " + name.upper())
		if node:
			for ch in range(node.GetChannelsCount()):
				for c in range(node.GetCurveCount(ch)):
					curve = node.GetCurve(ch,c) #FbxAnimCurve
					print("   - curve: " + str(curve) + " channel:" + node.GetChannelName(ch))
					for k in range(curve.KeyGetCount()):
						key = curve.KeyGetValue(k)
						time = curve.KeyGetTime(k)
						self.printTime(time, "   value: " + str(key) + " = ")

	def getTotalFrames(self, stack):
		timeSpan = stack.GetLocalTimeSpan()
		time = timeSpan.GetStop()
		timeMode = self.timeMode or 0
		time.SetGlobalTimeMode(timeMode)
		return time.GetFrameCount(), time.GetFrameRate(timeMode)

	def findAnimation(self, rootNode, stack):
		print
		print("STACK " + str(stack))
		timeSpan = stack.GetLocalTimeSpan()
		start = timeSpan.GetStart()
		stop = timeSpan.GetStop()
		duration = timeSpan.GetDuration()

		self.printTime(start, "START")
		self.printTime(stop, "STOP")
		self.printTime(duration, "DURATION")
	
	def getFrameFromTime( self, time ):
		timeMode = self.timeMode or 0
		time.SetGlobalTimeMode(timeMode)
		return time.GetFrameCount()

	def printTime(self, time, name):
		timeMode = self.timeMode or 0
		time.SetGlobalTimeMode(timeMode)
		print("   "+name+": " +
			# " Get "+str(time.Get())+
			" Time "+str(time.GetTime())+
			# " Second "+str(time.GetSecondCount())+
			" FrameRate "+str(time.GetFrameRate(timeMode))+
			" FrameCount "+str(time.GetFrameCount())
			)

	def searchNode(self, node, evaluator, stack, level = 0):
		print(" " + "\t" * level + " - " + str(node) + " " + str(node.GetName()))

		m = evaluator.GetNodeLocalTransform(node)
		# transform = []
		# for y in range(4):
		# 	transform.append([])
		# 	for x in range(4):
		# 		transform[y].append(m.Get(y,x))
		# print(" " + "\t" * level + "   matrix " + str(transform) )
		# print(" " + "\t" * level + "   T R Q S " + str([m.GetT(), m.GetR(), m.GetQ(), m.GetS()]) )
		# print(" " + "\t" * level + "   translation " + str(node.LclTranslation.GetCurveNode(stack)))
		# print(" " + "\t" * level + "   rotation " + str(node.LclRotation.GetCurveNode(stack)))
		# print(" " + "\t" * level + "   scale " + str(node.LclScaling.GetCurveNode(stack)))

		for a in range(node.GetNodeAttributeCount()):
			attr = node.GetNodeAttributeByIndex(a)
			print(" " + "\t" * level + "   + " + str(attr) + " " + str(attr.GetName()))
		
		for i in range(node.GetChildCount()):
			child = node.GetChild(i)
			self.searchNode(child, evaluator, stack, level + 1)

	def fbxAnimStack( self, stack ):
		for i in range(stack.GetSrcObjectCount()):
			obj = stack.GetSrcObject(i) #FbxAnimLayer
			print("   - layer: " + str(obj))
			for j in range(obj.GetSrcObjectCount()):
				node = obj.GetSrcObject(j) #FbxAnimCurveNode
				print("     - node: " + str(node) + " " + str(node.GetName())) 
				for ch in range(node.GetChannelsCount()):
					for c in range(node.GetCurveCount(ch)):
						curve = node.GetCurve(ch,c) #FbxAnimCurve
						print("       - curve: " + str(curve) + " channel:" + node.GetChannelName(ch))
						for k in range(curve.KeyGetCount()):
							key = curve.KeyGetValue(k)
							time = curve.KeyGetTime(k)
							print("         - " + str(k) + " key: " + str(key) + " time: " + str(time.Get()))
						

##----------------------------------------------------------------##

MeshExporter().register()

##----------------------------------------------------------------##
class MeshExporterListWidget( GenericListWidget ):
	def getNodes( self ):
		return self.parentModule.getObjects()

	def updateItemContent( self, item, node, **options ):
		item.setText( repr(node) )

	def onItemSelectionChanged(self):
		self.parentModule.onItemSelectionChanged()
