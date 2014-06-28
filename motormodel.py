import numpy as np 
import math
import matplotlib.pyplot as plt
import random as rand

theta1 = math.pi / 2.0
theta2 = 11.0 / 6.0 * math.pi
theta3 = 7.0 / 6.0 * math.pi

r1x = -1.0
r1y = 0.0
r2y = - math.sqrt(3)/2.0
r2x = 1.0
r3x = -0.5
r3y = - math.sqrt(3)




def invTan(a, b, trueAng):
	if trueAng:
		if b > 0:
			if a > 0:
				return math.atan(float(a/b))
			elif a < 0:
				return 2*math.pi - math.atan(float(a/-b))
			else:
				return 0
		elif b < 0:
			if a > 0:
				return math.pi - math.atan(float(a/-b))
			elif a < 0:
				return math.pi + math.atan(float(-a/-b))
			else:
				return math.pi
		else:
			if a > 0:
				return math.pi / 2.0
			elif a < 0:
				return 3 * math.pi / 2.0
			else:
				return 0
	else:
		if b != 0:
			return math.atan(abs(a)/abs(b))
		else:
			return math.pi/2.0
def isneg(a, b=1):
	if a < 0:
		return 1
	elif a == 0:
		return isneg(b)
	else:
		return 0
def ispos(a, b=	-1):
	if a > 0:
		return 1
	elif a == 0:
		return ispos(b)
	else:
		return 0


def plotRobot(theta1, theta2, theta3, r1x, r1y, r2x, r2y, r3x, r3y):
	fig = plt.figure()
	ax = fig.add_subplot(111, aspect='equal', axisbg='w')
	plt.plot([r1x, r1x+math.cos(theta1)],[r1y, r1y+math.sin(theta1)], '^--k', label='Wheel Driven') 
	plt.plot([r2x, r2x+math.cos(theta2)],[r2y, r2y+math.sin(theta2)], '^--k')
	plt.plot([r3x, r3x+math.cos(theta3)],[r3y, r3y+math.sin(theta3)], '^--k')
	plt.plot(0,0, '*k', r1x, r1y, 'or', r2x, r2y, 'ob',r3x, r3y, 'og')

	plt.plot([-1.5, 1.5], [0, 0], '-m')
	plt.plot([-1.5, 0], [0, -math.sqrt(27)/2.0], '-m')
	plt.plot([0, 1.5], [-math.sqrt(27)/2.0, 0], '-m')
	plt.legend()
	plt.show()

def VtoU(theta1, theta2, theta3, r1x, r1y, r2x, r2y, r3x, r3y, Vx, Vy, omega):
	
	A = np.matrix([[math.cos(theta1), 0, 0],
				   [math.sin(theta1), 0, 0],
				   [0, math.cos(theta2), 0],
				   [0, math.sin(theta2), 0],
				   [0, 0, math.cos(theta3)],
				   [0, 0, math.sin(theta3)]])

	M = np.matrix([[math.cos(theta1 - (math.pi/2.0)), 0, 0, -1, 0, r1y],
				   [math.sin(theta1 - (math.pi/2.0)), 0, 0, 0, -1, r1x],
				   [0, math.cos(theta2 - (math.pi/2.0)), 0, -1, 0, r2y],
				   [0, math.sin(theta2 - (math.pi/2.0)), 0, 0, -1, r2x],
				   [0, 0, math.cos(theta3 - (math.pi/2.0)), -1, 0, r3y],
				   [0, 0, math.sin(theta3 - (math.pi/2.0)), 0, -1, r3x]])

	L = np.linalg.inv(M)

	L1 = L[0:3]
	L2 = L[3:6]

	J = np.dot(L1, -A)
	N = np.dot(L2, -A)

	#Jinv = np.linalg.inv(J)
	Ninv = np.linalg.inv(N)

	V = np.matrix([[float(Vx)],
				   [float(Vy)],
				   [float(omega)]])
	U = np.dot(Ninv, V)
	R = np.dot(J, U)


	return U, R


def TESTVtoUwithoutomega(theta1, theta2, theta3, r1x, r1y, r2x, r2y, r3x, r3y, numTests):
	ret = [[False, False, False] for i in range(numTests)]
	alpha = 0
	thetas = [theta1, theta2, theta3]
	for i in range(numTests):
		Vx = rand.randint(-1000, 1000)
		Vy = rand.randint(-1000, 1000)
		omega = 0
		alpha = invTan(Vy,Vx, True)			
		U, R = VtoU(theta1, theta2, theta3, r1x, r1y, r2x, r2y, r3x, r3y, Vx, Vy, omega)
		for j in range(3):
			if not (Vx == 0 and Vy == 0):
				a = (thetas[j] - (math.pi * isneg(float(U[j][0])))) % (2 * math.pi)
				b = (invTan(R[j][0], U[j][0], False)* ispos(R[j][0] * (U[j][0]), R[j][0]))
				c = (invTan(R[j][0], U[j][0], False)* isneg(R[j][0] * (U[j][0]), R[j][0]))
				k = (a - b + c) % (round(2.0*math.pi, 9))
				d = "{0:4f}".format(k)
				e = "{0:4f}".format(alpha)
				#print(k)
				#print(e)
				#print(c, '\n')
				if  d == e:
					ret[i][j] = True
				elif d == '6.2832':
					if e == '0.0000':
						ret[i][j] = True
				else:
					ret[i][j] = (Vx, Vy, d, e)
			else:
				if float(U[j][0]) == 0.0 and float(R[j][0]) == 0.0:
					ret[i][j] = True
				else:
					ret[i][j] = (Vx, Vy)
	return ret


def simulate(theta1, theta2, theta3, r1x, r1y, r2x, r2y, r3x, r3y, Vx, Vy, omega, iterations):
	U, R = VtoU(theta1, theta2, theta3, r1x, r1y, r2x, r2y, r3x, r3y, Vx, Vy, omega)
	increment = 0.001
	dist1to2 = math.sqrt((r2x - r1x)**2 + (r2y-r1y)**2)
	dist1to3 = math.sqrt((r3x - r1x)**2 + (r3y-r1y)**2)
	dist2to3 = math.sqrt((r2x - r3x)**2 + (r2y-r3y)**2)
	current_origin = (0,0)
	U =[U[0][0],U[1][0],U[2][0]]
	
	for i in range(iterations):
		




#plotRobot(theta1, theta2, theta3, r1x, r1y, r2x, r2y, r3x, r3y)
# Vx = input("velocity x: ")
# Vy = input("velocity y: ")
# omega = input("omega: ")
# U, R = VtoU(theta1, theta2, theta3, r1x, r1y, r2x, r2y, r3x, r3y, Vx, Vy, omega)

# print("U: \n", U)
# print("R: \n", R)

test = TESTVtoUwithoutomega(theta1, theta2, theta3, r1x, r1y, r2x, r2y, r3x, r3y, 400000)

for i in test:
	if i != [True, True, True]:
		print(i)