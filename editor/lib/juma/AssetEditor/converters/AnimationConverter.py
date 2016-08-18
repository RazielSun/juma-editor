#!/usr/bin/env python

import os.path
import math
import logging

from juma.core                	import signals

from fbx import *
import FbxCommon
import fbxsip

##----------------------------------------------------------------##
def _getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
class AnimationConverter( object ):
	def __init__( self ):
		pass

	##----------------------------------------------------------------##
	def convert(self, obj):
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
						
