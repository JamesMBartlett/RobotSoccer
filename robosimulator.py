import random
import math
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np
'''
Created on 24/06/2013

@author: james
'''
sensorxdirectivity = [1.0,0.98,0.95,0.9,0.85,0.75,0.7,0.62,0.55,0.525]
sensorydirectivity = [0.98,1,0.95,0.8,0.7,0.6,0.5,0.4,0.2]
field_width = 182 #cm X
field_length = 243 #cm Y
max_velocity = 185 #revs/per10sec
sigma = 3.0

        
def plotscattergraph(coords, ball, robot, weights = None):
    plt.clf()
    N = len(coords)
    if weights is None:
        weights = np.tile(1.0, N)
    x = np.array([])
    y = np.array([])
    for i in range(N):
        reps = max(1,5 * N * weights[i]/sum(weights))
        x = np.concatenate((x, np.tile(coords[i].xcoord, reps)))
        y = np.concatenate((y,np.tile(coords[i].ycoord, reps)))
    plt.plot(x+np.random.normal(size=len(x))*0.5, y+np.random.normal(size=len(x))*0.5, "b.",
             ball.xcoord, ball.ycoord, "ro",
             robot.xcoord, robot.ycoord, "g+")
    plt.axis([0,field_width,0,field_length])
   # plt.show()
def plothist(sensor_readings):
    plt.hist(sensor_readings)
    plt.show() 
class Robot:
    def __init__(self):
        self.xcoord = random.random() * field_width
        self.ycoord = random.random() * field_length
        self.velox = random.random() * max_velocity
        self.veloy = random.random() * max_velocity
        self.direct = random.random() * 360
        self.angular_velo = random.random()
        self.sensor1_cirang = 0
        self.sensor1_yang = -10
        self.sensorheight = 50
        self.sigma = 0.05
    def set(self,x,y,v1,v2,h,av):
        self.xcoord = x
        self.ycoord = y
        self.velox = v1
        self.veloy = v2
        self.direct = h
        self.angular_velo = av
    def take_measurements(self, Ball, noise = None):
        if noise is None:
            noise = np.random.lognormal(sigma = self.sigma)
        sensor_reading = self.sensor_readings(Ball)
        sensor_reading *= noise
        sensor_reading = min(sensor_reading, 1023)    
        return sensor_reading
    def measurement_prob(self, measurement, Ball):
        sensor_reading = self.sensor_readings(Ball)
        if sensor_reading != 0:
            measurement = measurement / sensor_reading
        else:
            return 0
        return scipy.stats.lognorm.pdf(measurement,self.sigma)
    def sensor_readings(self, Ball):
        sensor1_inposition = False
        x_distance_to_ball = Ball.xcoord-self.xcoord
        y_distance_to_ball = Ball.ycoord-self.ycoord
        direct_of_ball = (math.atan2(x_distance_to_ball,y_distance_to_ball) * 180 / math.pi) + self.direct
        if direct_of_ball > 360:
            direct_of_ball -= 360
        if direct_of_ball < 0:
            direct_of_ball *= -1
        if direct_of_ball - self.sensor1_cirang <= 45 and direct_of_ball - self.sensor1_cirang >= -45:
            sensor1_inposition = True
        if sensor1_inposition:
            sensor_reading = 500.0 / (x_distance_to_ball**2 + y_distance_to_ball**2)
            sensor_reading *= sensorxdirectivity[int((direct_of_ball-self.sensor1_cirang)//5)]**2
            #sensor_reading *= sensorydirectivity[int((((math.atan(self.sensorheight/y_distance_to_ball) * 180) / math.pi)+self.sensor1_yang)//10)]
            sensor_reading *= 1023
            #sensor_reading = min(sensor_reading, 1023)
            return sensor_reading
        else:
            return 0
            
    def __repr__(self):
        return "[Coordinates: (%s, %s), Velocity: (%s, %s), Heading: %s, Angular Velocity: %s, Direction of ball: %s]" % (self.xcoord,self.ycoord,self.velox,self.veloy,self.direct,self.angular_velo, self.direct_of_ball)
    def move_goal(self,bx,by,g,d):
        deltaxbig = g - bx
        deltaybig = by
        prop = d / math.sqrt((deltaxbig**2) + deltaybig**2)
        deltaxsmall = deltaxbig * prop
        deltaysmall = deltaybig * prop
        x = bx + deltaxsmall
        y = by - deltaysmall
        return int(x),int(y)  
class BallPose:
    def __init__(self):
        self.xcoord = random.random() * field_width
        self.ycoord = random.random() * field_length
        self.velox = random.random() * max_velocity
        self.veloy = random.random() * max_velocity
    def __repr__(self):
        return "[Ball Coordinates: (%s , %s), Ball Velocity: (%s , %s)]" % (self.xcoord,self.ycoord,self.velox,self.veloy)    
    def set(self,x,y,v1,v2):
        self.xcoord = x
        self.ycoord = y
        self.velox = v1
        self.veloy = v2
        if self.xcoord > field_width:
            self.xcoord = field_width
        if self.xcoord < 0 :
            self.xcoord = 0
        if self.ycoord > field_length:
            self.ycoord = field_length
        if self.ycoord < 0 :
            self.ycoord = 0
    def make_key(self):
        return '(%s,%s,%s,%s)' % (self.xcoord,self.ycoord,self.velox,self.veloy)

def eval(b, p):
    ave = np.sum(np.array([[p[i].xcoord, p[i].ycoord] for i in range(len(p))]),axis=0)/float(len(p))
    return math.sqrt((ave[0]-b.xcoord)**2 + (ave[1]-b.ycoord)**2)

    sum = 0.0;
    
    for i in range(len(p)):
        dx = p[i].xcoord - b.xcoord
        dy = p[i].ycoord - b.ycoord
        err = math.sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))   


def main():    
    Ball = BallPose()
    ballx = 50
    bally = 100
    Ball.set(ballx, bally, 0, 0)
    
    robotx = 50
    roboty = 50
    myrobot = Robot()
    myrobot.set(robotx,roboty,0,0,0,0)
    finished = False
    N = 1000
    threshold = 1
    T = 100 
    
    p = []
    for i in range(N):
        b = BallPose() 
        p.append(b)
    print ("(x,y) in range: [%f..%f], [%f..%f]" % (min([i.xcoord for i in p]), max([i.xcoord for i in p]), min([i.ycoord for i in p]), max([i.ycoord for i in p])))
    
    print(eval(Ball,p))
    plotscattergraph(p,Ball,myrobot)
    plt.savefig('img/pfilter1000-100-0.png', bbox_inches='tight')
    for t in range(T):
        w = np.zeros(N)
        for i in range(N):
            temprobot = Robot()
            temprobot.set(robotx,roboty,0,0,0,0)
            Z = temprobot.take_measurements(p[i])
            while Z == 0:
                Z = temprobot.take_measurements(p[i])
                p[i] = BallPose()
            w[i] = temprobot.measurement_prob(Z, Ball)    
    
        p2 = []
        index = int(random.random() * N)
        beta = 0.0
        mw = max(w)
        #print w
        while len(p2) < N:
            beta += random.random() * 2.0 * mw
            while beta > w[index]:
                beta -= w[index]
                index = (index + 1) % N
            p2.append(p[index])
            
        ##MOVEMENT       
        reoccurences = {}
        key_to_object = {}
        to_add = []
        for i in p2:
            count = p2.count(i)
            reoccurences[i.make_key()] = count
            key_to_object[i.make_key()] = i
        changed_p2 = p2
        for i in reoccurences:
            if reoccurences[i] > threshold:
                for j in range(reoccurences[i]):
                    changed_p2.remove(key_to_object[i])
                for k in range(reoccurences[i]):
                    new_particle = BallPose()
                    new_particle.set(random.gauss(key_to_object[i].xcoord,sigma),random.gauss(key_to_object[i].ycoord,sigma),0,0)
                    to_add.append(new_particle)
        for i in to_add:
            changed_p2.append(i)
        if changed_p2 != p2:
            p = changed_p2            
        else:
            p = p2
    
        if (t % 1) == 0:
            plotscattergraph(p,Ball,myrobot, w)
            plt.savefig('img/pfilter1000-100-%d'%(t+1), bbox_inches='tight')
    print(eval(Ball,p))

    #print p
def test_sensor_readings():
    myrobot = Robot()
    myrobot.set(field_width / 2, field_length / 2, 0,0,0,0)
    delta = 1
    Ball = BallPose()
    X = np.arange(0,field_width,delta)
    Y = np.arange(0,field_length,delta)
    def z_funct(X,Y):
        Ball.set(X,Y,0,0)
        return myrobot.take_measurements(Ball,1)
    lengthX = len(X)
    lengthY = len(Y)
    Z = np.zeros((lengthY,lengthX))
    for i in range(lengthX):
        for j in range(lengthY):
            Z[j,i] = z_funct(X[i],Y[j])
             
    plt.contour(X,Y,Z)
    plt.colorbar()  
    plt.show()
    
    
    #------------------------------------------------------ sensor_readings = []
    #------------------------------------------------------- for i in range(50):
        #--------------- sensor_readings.append(myrobot.take_measurements(Ball))
        #---------------------------------------------- print sensor_readings[i]
    #------------------------------------------------- plothist(sensor_readings)
#------------------------------------------------------------------------------ 
    #--------------------------------------------- Ball.set(ballx, bally+20,0,0)
    #------------------------------------------------------ sensor_readings = []
    #------------------------------------------------------- for i in range(50):
        #--------------- sensor_readings.append(myrobot.take_measurements(Ball))
        #---------------------------------------------- print sensor_readings[i]
    #------------------------------------------------- plothist(sensor_readings)
#------------------------------------------------------------------------------ 
    #--------------------------------------------- Ball.set(ballx, bally+40,0,0)
    #------------------------------------------------------ sensor_readings = []
    #------------------------------------------------------- for i in range(50):
        #--------------- sensor_readings.append(myrobot.take_measurements(Ball))
        #---------------------------------------------- print sensor_readings[i]
    #------------------------------------------------- plothist(sensor_readings)
#------------------------------------------------------------------------------ 
    #--------------------------------------------- Ball.set(ballx, bally+60,0,0)
    #------------------------------------------------------ sensor_readings = []
    #------------------------------------------------------- for i in range(50):
        #--------------- sensor_readings.append(myrobot.take_measurements(Ball))
        #---------------------------------------------- print sensor_readings[i]
    #------------------------------------------------- plothist(sensor_readings)

repeat = 1
if __name__ == '__main__':
    for i in range(repeat):
        #test_sensor_readings()
        main()
    