import math
import random
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss

class Utils:
		def logofnormpdf(x, mu, sigma):
		return (-0.5 * (x - mu)**2 / sigma**2) - math.log(sigma * math.sqrt(2*math.pi))

class Field:
	def __init__(self):
		self.x = 100 ##width of the field in cm
		self.y = 200 ##length of the field in cm

class Robot:
	def __init__(self):
		self.field = Field()
		self.fieldwidth = self.field.x
		self.fieldheight = self.field.y
		self.pose = {'x':random.random() * self.fieldwidth, 'y': random.random() * self.fieldheight, 'velox':1, 'veloy':0, 'angpos':math.pi/180, 'angvelo':0.5}
		self.lengthnoise = 2
		self.movenoise = 0.5
		self.angnoise = 0.01 * math.pi
		self.maxvelo = 10
		self.ballEstimate = None

	def setPose(self, x, y, velox, veloy, angpos, angvelo):
		self.pose['x'] = x
		self.pose['y'] = y
		self.pose['velox'] = velox
		self.pose['veloy'] = veloy
		self.pose['angpos'] = angpos
		self.pose['angvelo'] = angvelo
	def senseUltrasonic(self):
		measurement = []
		theta = self.pose['angpos']
		for i in range(4):
			quadrant = math.ceil((theta / (math.pi / 2.0)))
			wall = (int(((self.fieldheight - self.pose['y']) * math.tan(theta)) >= self.pose['x']) * int(quadrant == 1)) + \
				   (int(((self.pose['y'])/math.tan(theta - (math.pi/2.0)))>= self.pose['x']) * int(quadrant == 2)) + \
				   (int(((self.pose['y']) * math.tan(theta - math.pi)) >= (self.fieldwidth - self.pose['x'])) * int(quadrant == 3)) + \
				   (int(((self.fieldheight - self.pose['y']) / math.tan(theta - (math.pi*3.0/2.0)))>= self.fieldwidth - self.pose['x']) * int(quadrant == 4))

			dist = ((((self.pose['x'] / math.cos((math.pi / 2.0) - theta)) * int(wall == 1)) +  (((self.fieldheight-self.pose['y']) / math.cos(theta)) * int(wall == 0))) * int(quadrant == 1)) + \
				   ((((self.pose['x'] / math.cos(theta - (math.pi / 2.0))) * int(wall == 1)) +  (((self.pose['y']) / math.cos(math.pi - theta)) * int(wall == 0))) * int(quadrant == 2)) + \
				   (((((self.fieldwidth - self.pose['x']) / math.cos((3 * math.pi / 2.0) - theta)) * int(wall == 1)) +  ((self.pose['y'] / math.cos(theta)) * int(wall == 0))) * int(quadrant == 3)) + \
				   (((((self.fieldwidth - self.pose['x']) / math.cos(theta - (3 * math.pi / 2.0))) * int(wall == 1)) +  (((self.fieldheight-self.pose['y']) / math.cos((2 * math.pi) - theta)) * int(wall == 0))) * int(quadrant == 4))
			theta += (math.pi / 2.0)
			theta = theta % (2 * math.pi)
			measurement.append(abs(dist))
		return measurement
	def senseNoiseUltrasonic(self):
		measurement = []
		for i in self.senseUltrasonic():
			measurement.append(self.addNoise(i, self.lengthnoise))
		return measurement

	def logprob_measurement(self, measurement):
		sense = self.senseUltrasonic()
		probs = np.array([Utils.logofnormpdf(measurement[i], sense[i], self.lengthnoise) for i in range(4)])
		return np.sum(probs)

	def move(self, t):
		self.pose['x'] += self.addNoise(t * self.pose['velox'], self.movenoise)
		if self.pose['x'] < 0:
			self.pose['x'] = 0
		if self.pose['x'] > self.fieldwidth:
			self.pose['x'] = self.fieldwidth
		self.pose['y'] += self.addNoise(t * self.pose['veloy'], self.movenoise)
		if self.pose['y'] < 0:
			self.pose['y'] = 0
		if self.pose['y'] > self.fieldheight:
			self.pose['y'] = self.fieldheight
		self.pose['angpos'] = self.addNoise(t * self.pose['angvelo'] + self.pose['angpos'], self.angnoise) % (2* math.pi)
		return self
	def addNoise(self, a, noise):
		n = np.random.normal(a, noise, 1)[0]
		return n

	def addNoiseToPose(self):
		r = Robot()
		r.setPose(self.pose['x'], self.pose['y'], self.pose['velox'], self.pose['veloy'], self.pose['angpos'], self.pose['angvelo'])
		r.pose['x'] = self.addNoise(self.pose['x'], self.lengthnoise)
		r.pose['y'] = self.addNoise(self.pose['y'], self.lengthnoise) 
		r.pose['angpos'] = self.addNoise(self.pose['angpos'], self.angnoise) % (2 * math.pi)
		if r.pose['x'] > r.fieldwidth:
			r.pose['x'] = r.fieldwidth
		if r.pose['x'] < 0:
			r.pose['x'] = 0
		if r.pose['y'] > r.fieldheight:
			r.pose['y'] = r.fieldheight
		if r.pose['y'] < 0:
			r.pose['y'] = 0
		return r

	def setPose(self, x, y, velox, veloy, angpos, angvelo):
		self.pose['x'] = x
		self.pose['y'] = y
		self.pose['velox'] = velox
		self.pose['veloy'] = veloy
		self.pose['angpos'] = angpos
		self.pose['angvelo'] = angvelo



	def __repr__(self):
		return str(self.pose)

class Ball:
	def __init__(self):
		self.pose = {'x': 0, 'y': 0, 'velox': 0, 'veloy': 0}
		self.field = Field()
		self.fieldwidth = self.field.x
		self.fieldheight = self.field.y
		self.robot = Robot()
		self.measurenoise = 1
		self.movenoise = 1

	def senseInfrared(self):
		pass
		#### this is the hard bit

	def prob_measurement(self, measurement):
		sense = self.senseInfrared()
		return np.sum(np.array([Utils.logofnormpdf(measurement[i], sense[i], self.measurenoise) for i in range(16)]))



	def setPose(self, x, y, velox, veloy):
		self.pose['x'] = x
		self.pose['y'] = y
		self.pose['velox'] = velox
		self.pose['veloy'] = veloy

def weight(p, measurement):
	w = np.array([i.logprob_measurement(measurement) for i in p])
	w -= np.max(w)
	w = np.exp(w)
	w /= np.sum(w)
	return w

def resample(w, p): ## normalised weight list w, partile list p
	sumw = np.array(w).cumsum()
	ret = []
	N = len(p)
	for i in range(N):
		index = 0
		a = random.random()
		while a > sumw[index]:
			index += 1
		#if i ==1:
			#print("w/o", p[min(index, N-1)])
			#print("w", p[min(index, N-1)].addNoiseToPose())
		ret.append(p[min(index, N-1)].addNoiseToPose())
		#ret.append(p[min(index, N-1)])		
	return ret

def filter(p, iterations, robot, measurement): 
	for i in range(iterations):
		w = weight(p, measurement)
		p = resample(w, p)
	return p

def moveParticles(p, t):
	p = [i.move(t) for i in p]
	return p
def filterwithmove(p, iterations, robot, t):
		for i in range(iterations):
			if i != 0:
				p = moveParticles(p, t)
				robot = robot.move(t)
			measurement = robot.senseNoiseUltrasonic()
			p = filter(p, 30, robot, measurement)
		return p
def generateRandomParticles(num):
	p = []
	for i in range(num):
		r = Robot()
		r.setPose(np.random.randint(0, r.fieldwidth), np.random.randint(0, r.fieldheight), np.random.randint(0, r.maxvelo), np.random.randint(0, r.maxvelo), np.random.random() * 2 * math.pi, np.random.randint(0, r.maxvelo) )
		p.append(r)
	return p
def plotParticles(p, robot):
	x = np.array([i.pose['x'] for i in p])
	y = np.array([i.pose['y'] for i in p])
	angpos = np.array([i.pose['angpos'] for i in p])
	fig = plt.figure()
	ax1 = plt.subplot2grid((12,6), (0,0), colspan= 6, rowspan=3)
	plt.hist(x, axes=ax1)
	ax2 = plt.subplot2grid((12,6), (4, 0), colspan= 6, rowspan=3)
	plt.hist(y, axes=ax2)
	ax3 = plt.subplot2grid((12,6), (8, 0), colspan = 6, rowspan = 3)
	plt.hist(angpos, axes = ax3, bins = 20)
	plt.show()

def evaluate(p, measurement):
	sum = 0
	count = 0
	print(measurement)
	for i in measurement:
		for j in p:
			sum += abs(j.senseUltrasonic()[measurement.index(i)] - i)
			count += 1
	print(sum / count)

def meanPart(p):
	x = np.average(np.array([i.pose['x'] for i in p]))
	y = np.average(np.array([i.pose['y'] for i in p]))
	velox = np.average(np.array([i.pose['velox'] for i in p]))
	veloy = np.average(np.array([i.pose['veloy'] for i in p]))
	angpos = np.median(np.array([i.pose['angpos'] for i in p]))
	angvelo = np.average(np.array([i.pose['angvelo'] for i in p]))
	r = Robot()
	r.setPose(x, y, velox, veloy, angpos, angvelo)
	return r

if __name__ == '__main__':
	# w = [0.64, 0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.04]
	# p = generateRandomParticles(10)
	# for i in p:
	# 	print(i)
	# p = resample(w, p)
	# for i in p:
	# 	print(i)

	N = 20 # number of particles
	I = 10# number of iterations 
	r = Robot()
	measurement = r.senseNoiseUltrasonic()
	randomparts = generateRandomParticles(N)
	#p = filter(randomparts, I, r, measurement)
	p = filterwithmove(randomparts, I, r, 0.3)
	# print("p")

	# for i in p:
	# 	print(i.senseUltrasonic())
	# 	print(i)

	print("robot: ", r)

	mean = meanPart(p)
	print("average particle: ", mean)

	print("particle measurement: ", mean.senseUltrasonic())
	print("robot measurement: ", r.senseUltrasonic())

	plotParticles(p, r)




