import unittest
import particlefilter as pf
import random
import numpy as np
import math
import scipy.stats as ss

class TestResample(unittest.TestCase):

	def test_zeroWeights(self):
		w = [1, 0, 0, 0, 0]
		p = pf.generateRandomParticles(5)
		resampled = pf.resample(w, p)
		for i in resampled:
			print(i)
			self.assertEqual(i, p[0])

	def test_randomPercent(self):
		num = 4
		randPercent = [random.random()]
		b = (1.0 - randPercent[0]) / (num-1)
		restofparticles = [b for i in range(num)]
		w = randPercent + restofparticles
		p = pf.generateRandomParticles(num)
		count = 0
		N = 1000
		for i in range(N):
			resampled = pf.resample(w, p)
			count += resampled.count(p[0])
		percent = count / (N * num)
		self.assertWithinx(percent, randPercent[0], 0.02)

	def assertWithinx(self, a, b, x):
		return self.assertTrue(a + x > b and a - x < b)

class TestWeights(unittest.TestCase):

	def test_zeroPos(self):
		num = 10
		robot = pf.Robot()
		robot.setPose(0.0001,0.001,1,1,1,1)
		p = [robot for i in range(num)]
		measurement = robot.senseUltrasonic()
		weight = pf.weight(p, measurement)
		self.assertEqual([float('%.8f' % i) for i in weight], [(1.0/num) for i in range(num)])
	
	def test_sum(self):
		num = 10
		p = pf.generateRandomParticles(num)
		measurement = p[np.random.randint(0, len(p)-1)].senseNoiseUltrasonic()
		weight = pf.weight(p, measurement)
		cumsum = np.array(weight).cumsum()[num-1]
		self.assertWithinx(cumsum, 1.0, 0.000000001)

	def test_weighting(self):
		num = 5
		r = pf.Robot()
		p = pf.generateRandomParticles(num) + [r]
		for i in p:
			print(i)
		measurement = r.senseNoiseUltrasonic()
		weight = pf.weight(p, measurement)
		print(weight)
		self.assertAismaxinList(weight[5], weight)


	def assertWithinx(self, a, b, x):
		return self.assertTrue(a + x > b and a - x < b)
	def assertAismaxinList(self, a, list):
		max = np.max(np.array(list))
		print(max)
		print(a)
		return self.assertTrue(max == a)


class TestRobot(unittest.TestCase):

	def test_setPose(self):
		x = random.random() * 100
		y = random.random() * 200
		velox = random.random() * 10
		veloy = random.random() * 10
		angpos = random.random() * 2 * math.pi
		angvelo = random.random() * 10
		robot = pf.Robot()
		robot.setPose(x, y, velox, veloy, angpos, angvelo)
		self.assertEqual(robot.pose['x'], x)
		self.assertEqual(robot.pose['y'], y)
		self.assertEqual(robot.pose['velox'], velox)
		self.assertEqual(robot.pose['veloy'], veloy)
		self.assertEqual(robot.pose['angpos'], angpos)
		self.assertEqual(robot.pose['angvelo'], angvelo)

	def test_senseUltrasonic_1(self):
		robot = pf.Robot()
		measurement = robot.senseUltrasonic()
		self.assertEqual(measurement, [70.71067811865474 for i in range(4)])

	def test_senseUltrasonic_Quad1(self):
		robot = pf.Robot()
		x = random.random() * robot.fieldwidth
		y = random.random() * robot.fieldheight
		angpos = random.random() * math.pi * 0.5
		robot.setPose(x, y, 0, 0, angpos, 0)
		measurement = robot.senseUltrasonic()
		check = 0
		if math.tan(angpos) * (robot.fieldheight - y) <= x:
			check = (robot.fieldheight - y) / math.cos(angpos)
		else:
			check = x / math.cos(math.pi * 0.5 - angpos)
		self.assertEqual(measurement[0], check)
	def test_senseUltrasonic_Quad2(self):
		robot = pf.Robot()
		x = random.random() * robot.fieldwidth
		y = random.random() * robot.fieldheight
		angpos = random.random() * math.pi * 0.5 + math.pi * 0.5
		robot.setPose(x, y, 0, 0, angpos, 0)
		measurement = robot.senseUltrasonic()
		check = 0
		if y / math.tan(angpos - math.pi * 0.5) <= x:
			check = y / math.sin(angpos - math.pi * 0.5)
		else:
			check = x / math.cos(angpos - math.pi * 0.5)
		self.assertEqual(measurement[0], check)
	def test_senseUltrasonic_Quad3(self):
		robot = pf.Robot()
		x = random.random() * robot.fieldwidth
		y = random.random() * robot.fieldheight
		angpos = random.random() * math.pi * 0.5 + 2 * math.pi * 0.5
		robot.setPose(x, y, 0, 0, angpos, 0)
		measurement = robot.senseUltrasonic()
		check = 0
		if y * math.tan(angpos - 2 * math.pi * 0.5) <= robot.fieldwidth - x:
			check = y / math.cos(angpos - 2 * math.pi * 0.5)
		else:
			check = (robot.fieldwidth - x) / math.cos(3 * math.pi * 0.5 - angpos)
		self.assertWithinx(measurement[0], check, 0.000000001)
	def test_senseUltrasonic_Quad4(self):
		robot = pf.Robot()
		x = random.random() * robot.fieldwidth
		y = random.random() * robot.fieldheight
		angpos = random.random() * math.pi * 0.5 + 3 * math.pi * 0.5
		robot.setPose(x, y, 0, 0, angpos, 0)
		measurement = robot.senseUltrasonic()
		check = 0
		if (robot.fieldheight - y) / math.tan(angpos - 3 * math.pi * 0.5) <= robot.fieldwidth - x:
			check = (robot.fieldheight - y) / math.sin(angpos - 3 * math.pi * 0.5)
		else:
			check = (robot.fieldwidth - x) / math.cos(angpos - 3 * math.pi * 0.5)
		self.assertWithinx(measurement[0], check, 0.000000001)

	def test_probMeasurement(self):
		robot = pf.Robot()
		x = random.random() * robot.fieldwidth
		y = random.random() * robot.fieldheight
		angpos = random.random() * math.pi * 2
		robot.setPose(x, y, 0, 0, angpos, 0)
		measurement = robot.senseUltrasonic()
		noise = robot.lengthnoise
		check = np.average(np.array([robot.logofnormpdf(measurement[i], measurement[i], noise) for i in range(4)]))
		self.assertEqual(robot.prob_measurement(measurement), check)


	def test_logofPdf(self):
		robot = pf.Robot()
		x = 2
		mu = 0
		sigma = 3
		check = math.log(ss.norm.pdf(x, mu, sigma))
		self.assertEqual(robot.logofnormpdf(x, mu, sigma), check)


	def assertWithinx(self, a, b, x):
		return self.assertTrue(a + x > b and a - x < b)

	def test_Random(self):
		r = pf.Robot()
		r.setPose(5, 0, 0, 0, 0.25 * math.pi, 0)
		measurement = r.senseUltrasonic()
		print(measurement)
		print(pf.Robot().prob_measurement(measurement))

	def test_genRandomParticles(self):
		num = 50
		p = pf.generateRandomParticles(num)
		minx = p[0].fieldwidth
		miny = p[0].fieldheight
		maxx = 0
		maxy = 0
		for i in p:
			if i.pose['x'] < minx:
				minx = i.pose['x']
			if i.pose['y'] < miny:
				miny = i.pose['y']
			if i.pose['x'] > maxx:
				maxx = i.pose['x']
			if i.pose['y'] > maxy:
				maxy = i.pose['y']
		print("\n", "particles generated between: ", minx, "and ", maxx, " in the x dimension")
		print("particles generated between: ", miny, "and ", maxy, " in the y dimension")

if __name__ == '__main__':
	unittest.main()

