import moaipy
from moaipy import *



##----------------------------------------------------------------##
## Input DEVICE
##----------------------------------------------------------------##
class MOAIInputDevice(object):
	def __init__( self, name, id ):
		self.id           = id
		self.name         = name or 'device'
		self.sensors      = {}
		self.lastSensorId = 0
		self.registered   = False

	def addSensor(self, name, sensorType='touch'):
		assert not self.registered, 'input device already registered !!'
		assert sensorType in ( 'touch', 'pointer', 'button', 'keyboard', 'joystick', 'wheel'), 'unsupported sensor type'
		assert not self.sensors.has_key(name), 'duplicated sensor name'

		classes={
			# 'touch'    : MOAITouchSensor,
			'pointer'  : MOAIPointerSensor,
			'wheel'    : MOAIWheelSensor,
			'button'   : MOAIButtonSensor,
			'keyboard' : MOAIKeyboardSensor,
			} [sensorType]

		sensor = classes(self, self.lastSensorId, name)
		self.sensors[name] = sensor
		self.lastSensorId += 1

		AKUReserveInputDeviceSensors ( self.id, self.lastSensorId )
		print("AKUReserveInputDeviceSensors : {} {}".format( self.id, self.lastSensorId ))
		for k in self.sensors:
			sensor = self.sensors[k]
			sensor.onRegister()

	def getSensor(self, name):
		return self.sensors.get( name, None )

	def onRegister(self):
		AKUSetInputDevice ( self.id, self.name )
		AKUReserveInputDeviceSensors ( self.id, self.lastSensorId )
		print("AKUSetInputDevice {} {}".format( self.id, self.name ))
		print("AKUReserveInputDeviceSensors {} {}".format( self.id, self.lastSensorId ))
		for k in self.sensors:
			sensor = self.sensors[k]
			sensor.onRegister()



##----------------------------------------------------------------##
## Input SENSOR
##----------------------------------------------------------------##
class MOAIInputSensor(object):
	def __init__(self, device, id, name):
		self.device=device
		self.id=id
		self.name=name

	def onRegister(self):
		pass

##----------------------------------------------------------------##
class MOAITouchSensor(MOAIInputSensor):
	def enqueueEvent(self, touchId, down, x, y):
		AKUEnqueueTouchEvent (
				self.device.id,
				self.id,
				touchId,
				down,
				x,y
			)

	def enqueueEventCancel(self):
		AKUEnqueueTouchEventCancel (
				self.device.id,
				self.id				
			)

	def onRegister(self):
		AKUSetInputDeviceTouch(self.device.id, self.id, self.name)

##----------------------------------------------------------------##
class MOAIPointerSensor(MOAIInputSensor):
	"""docstring for MOAIPointerSensor"""
	def enqueueEvent(self, x, y):
		AKUEnqueuePointerEvent (
				self.device.id,
				self.id,
				x, y
			)

	def onRegister(self):
		AKUSetInputDevicePointer (self.device.id, self.id, self.name)

##----------------------------------------------------------------##
class MOAIWheelSensor(MOAIInputSensor):
	"""docstring for MOAIWheelSensor"""
	def enqueueEvent(self, value):
		AKUEnqueueWheelEvent (
				self.device.id,
				self.id,
				value
			)

	def onRegister(self):
		AKUSetInputDeviceWheel (self.device.id, self.id, self.name)

##----------------------------------------------------------------##
class MOAIButtonSensor(MOAIInputSensor):
	"""docstring for MOAIPointerSensor"""
	def enqueueEvent(self, down):
		AKUEnqueueButtonEvent (
				self.device.id,
				self.id,
				down
			)

	def onRegister(self):
		AKUSetInputDeviceButton (self.device.id, self.id, self.name)

##----------------------------------------------------------------##
class MOAIKeyboardSensor(MOAIInputSensor):
	def enqueueKeyEvent(self, keyId, down):
		AKUEnqueueKeyboardKeyEvent (
				self.device.id, 
				self.id,
				keyId,
				down
			)

	def enqueueCharEvent(self, char):
		AKUEnqueueKeyboardKeyEvent (
				self.device.id, 
				self.id,
				char
			)

	def enqueueTextEvent(self, text):
		AKUEnqueueKeyboardKeyEvent (
				self.device.id, 
				self.id,
				text
			)

	def onRegister(self):
		AKUSetInputDeviceKeyboard (self.device.id, self.id, self.name)