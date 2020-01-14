from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import random
import math
from PyQt5.QtCore import QDir


class Snake(QWidget) :
    
    def __init__(self):
        
        super(Snake, self).__init__()
        #initialize the widget and title it Snake
        #self.window = QWidget()
        #self.window.setFixedHeight(500)
        #self.window.setFixedWidth(500)
        #self.window.resize(500,500)
        #self.window.setWindowTitle('Snake')
        self.setFixedHeight(500)
        self.setFixedWidth(500)
        
        #Set background to black color
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        
        #show the widget
        #self.window.show()
        
        #initialize needed variables for logic
        #directions to know direction to move on
        self.left = False
        self.right = False
        self.up = False
        self.down = True
        #bool to determine if the game was lost or not
        self.GameOver = False
        #creating image objects with their corresponding png images
        pathD = QDir.currentPath() + "/GreenD.png"
        self.head = QImage()
        self.head.load(pathD)
        
        pathL = QDir.currentPath() + "/GreenL.png"
        self.body = QImage()
        self.body.load(pathL)
        
        path = QDir.currentPath() + "/goal.png"
        self.goal = QImage()
        self.goal.load(path)
        
        pathG = QDir.currentPath() + "/GameOver.png"
        pathT = QDir.currentPath() + "/TryAgain.png"
        self.GO = QImage()
        self.GO.load(pathG)
        self.tryAgain = QImage()
        self.tryAgain.load(pathT)
        #timer to move the game progression after x msec
        self.timer = QTimer()
        
        #keeps count how many goals were eaten by player
        self.bodyCount = 4
        self.x = []
        self.y = []
        #first random position of goal
        self.goal_x = (math.floor(random.randint(1,499)/10))*10
        self.goal_y = (math.floor(random.randint(1,499)/10))*10
       
        self.justMoved = False
        
        self.longest_x = 0
        self.longest_y = 0
        self.moving_x = 0
        self.moving_y = 0
        self.iterations = 1
        #average of longest paths from different iterations of the game
        self.average_x = 0
        self.average_y = 0
        self.averagebody = 0
        
        #variables generically modified
        self.stepsx = 6
        self.stepsy = 6
        self.rand = self.bodyCount
        self.caught = False
        
        if(self.goal.isNull == True):
            print("true")
            print(path)
            
        
        #if the player fills all holes, then he will have at most 2500 blocks
        for i in range(2500):
            self.x.append(0)
            self.y.append(0)
        
        #initialize position of player
        for i in range(self.bodyCount):
            self.x[i] = 20
            self.y[i] = 70 - i*10
            
        self.timing()
        
        
        
    def paintEvent(self, event):
    
        self.Draw()
        
    def Draw(self):
        
        if(self.GameOver == False):
            painter = QPainter(self)
            painter.begin(self)
            painter.drawImage(self.goal_x,self.goal_y,self.goal)
            painter.end()
            
            
            for i in range(self.bodyCount):
                painter.begin(self)
                if(i == 0):
                    painter.drawImage(self.x[i],self.y[i],self.head)
                    painter.end()
                else:
                    painter.drawImage(self.x[i],self.y[i],self.body)
                    painter.end()
    
            
        else:
        
            #print("done")
            painter = QPainter(self)
            painter.begin(self)
            painter.drawImage(0,-100,self.GO)
            painter.drawImage(100,350,self.tryAgain)
            for i in range(self.bodyCount):
                painter.begin(self)
                if(i == 0):
                    painter.drawImage(self.x[i],self.y[i],self.head)
                    painter.end()
                else:
                    painter.drawImage(self.x[i],self.y[i],self.body)
                    painter.end()
            
            painter.end()
        
    def timing (self):
        
        it = 0
        delay = 40
        try:    
            #print("painting")
            self.AI()
            self.Move()
            self.CheckGoalCollision()
            self.CollisionCheck()
            self.repaint()
            self.justMoved = False
        finally:
            if(self.GameOver == False):
                QTimer.singleShot(delay, self.timing)
            elif(self.GameOver == True and self.iterations <= it):
                
                self.GameOver = False
                self.left = False
                self.right = False
                self.up = False
                self.down = True
                self.bodyCount = 4
                self.goal_x = (math.floor(random.randint(1,499)/10))*10
                self.goal_y = (math.floor(random.randint(1,499)/10))*10
                self.longest_x = 0
                self.longest_y = 0
                self.moving_x = 0
                self.moving_y = 0
                self.iterations = self.iterations + 1
                for i in range(2500):
                    self.x[i] = 0
                    self.y[i] = 0
                    for i in range(self.bodyCount):
                        self.x[i] = 20
                        self.y[i] = 70 - i*10
                
                self.timing()
                
            elif(self.iterations > it):
                #bare in mind that the averages calculated don't get reset, pressing enter will run it #iterations again 
                #while keeping the averages (since this is what i want)
                self.iterations = 1
                avgx = self.average_x*(self.iterations - 1)
                avgy = self.average_y*(self.iterations - 1)
                avgbody = self.averagebody*(self.iterations -1)
                HtoT = math.sqrt(math.pow(self.x[0] - self.x[self.bodyCount],2) + math.pow(self.y[0] - self.y[self.bodyCount],2))
                self.average_x = (avgx + self.longest_x)/self.iterations
                self.average_y = (avgy + self.longest_y)/self.iterations
                self.averagebody = (avgbody + self.bodyCount)/self.iterations
                self.iterations = self.iterations + 1
            
                print("(Gen" + str(self.iterations) + ") " + "average longest x: " + str(math.floor(self.average_x)) + ", average longest y: " + 
                      str(math.floor(self.average_y)) + ", average body: " + str(math.floor(self.averagebody)))
                print("Head to Tail distance: " + str(HtoT))
                
            
            
    
    def Move(self):
        
        
        for i in range (self.bodyCount, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
   

        if (self.left) :
            self.x[0] = self.x[0] - 10
            self.moving_x = self.moving_x + 1
            self.moving_y = 0
            if(self.moving_x > self.longest_x):
                self.longest_x = self.moving_x
            
                

        if (self.right) :
            self.x[0] = self.x[0] + 10
            self.moving_x = self.moving_x + 1
            self.moving_y = 0
            if(self.moving_x > self.longest_x):
                self.longest_x = self.moving_x

        if (self.up) :
            self.y[0] = self.y[0] - 10
            self.moving_y = self.moving_y + 1
            self.moving_x = 0
            if(self.moving_y > self.longest_y):
                self.longest_y = self.moving_y

        if (self.down) :
            self.y[0] = self.y[0] + 10
            self.moving_y = self.moving_y + 1
            self.moving_x = 0
            if(self.moving_y > self.longest_y):
                self.longest_y = self.moving_y
   
    
    
   

       
    
    def keyPressEvent(self, event):
        
        #The below is used to make a real person control the snake
        '''
        if (event.key() == Qt.Key_Right and self.left == False and self.justMoved == False):
            self.right = True
            self.up = False
            self.down = False
            self.justMoved = True
            
        if (event.key() == Qt.Key_Left and self.right == False and self.justMoved == False):
            self.left = True
            self.up = False
            self.down = False
            self.justMoved = True
            
        if (event.key() == Qt.Key_Up and self.down == False and self.justMoved == False):
            self.up = True
            self.left = False
            self.right = False
            self.justMoved = True
            
        if (event.key() == Qt.Key_Down and self.up == False and self.justMoved == False):
            self.down = True
            self.left = False
            self.right = False
            self.justMoved = True
            
        '''
        
        if (event.key() == Qt.Key_Return and self.GameOver == True):
            self.GameOver = False
            self.left = False
            self.right = False
            self.up = False
            self.down = True
            self.bodyCount = 4
            self.goal_x = (math.floor(random.randint(1,499)/10))*10
            self.goal_y = (math.floor(random.randint(1,499)/10))*10
            self.longest_x = 0
            self.longest_y = 0
            self.moving_x = 0
            self.moving_y = 0
            for i in range(2500):
                self.x[i] = 0
                self.y[i] = 0
            for i in range(self.bodyCount):
                self.x[i] = 20
                self.y[i] = 70 - i*10
                
            self.timing()
        
    
        #the following will be used to make an AI control the snake
    
    def AI (self):
        
        distx = self.x[0] - self.goal_x
        disty = self.y[0] - self.goal_y
        noleft = False
        noright = False
        noUp = False
        noDown = False
        
        
        nothingChanged = True
        
        #checks if snake body or edge limits is in the 4 directions
        for i in range(1,self.bodyCount,1):
            
            if((self.x[0] - 10 == self.x[i] and self.y[0] == self.y[i]) or self.x[0] - 10 < 0):
                    noleft = True
            
            if((self.x[0] + 10 == self.x[i] and self.y[0] == self.y[i]) or self.x[0] + 10 > 500):
                   noright = True
                
            if((self.x[0] == self.x[i] and self.y[0] - 10 == self.y[i]) or self.y[0] - 10 < 0):
                    noUp = True
                
            if((self.x[0] == self.x[i] and self.y[0] + 10 == self.y[i]) or self.y[0] + 10 > 500):
                    noDown = True
            
            
            
        
        #Tried making the snake have to spread itself "stepsx" so that it doesnt create loops
        #tried also making it have to a sqaure to avoid small loops
        #Failed to achieve results
        '''
        
        if(self.moving_x <= self.stepsx):
            #print("here1")
            if(noright == False or noleft == False):
                noUp = True
                noDown = True
            
        elif(self.moving_y <= self.stepsy):
            #print("here2")
            if(noUp == False and noDown == False):
                noright = True
                noleft = True
            
            '''
            
        #Tried letting the snake move randomly after catching the goal 
        #this didn't really help much
        '''
        if(self.rand == 0 and self.caught == True):
                self.rand = self.bodyCount
                self.caught = False
                
        if(self.rand != 0 and self.caught == False):
            
            self.rand = self.rand - 1      
            
           
            
            if(noleft == False):
                noUp = True
                noDown = True
                noright = True
            elif(noright == False):
                noUp = True
                noDown = True
                noleft = True
            elif(noUp == False):
                noDown = True
                noright = True
                noleft = True
            elif(noDown == False):
                noUp = True
                noright = True
                noleft = True
                
        '''
        
        if (abs(distx) >= abs(disty)):
            
            if(distx > 0):
                
                if(self.right == False and noleft == False):
                
                    self.left = True
                    self.up = False
                    self.down = False
                    self.justMoved = True
                    nothingChanged = False
                else:
                    
                    if(disty >= 0 and noUp == False and self.down == False):
                        nothingChanged = False
                        self.up = True
                        self.left = False
                        self.right = False
                        self.justMoved = True
            
                    else:
                
                        if(noDown == False and self.up == False):
                            self.down = True
                            self.left = False
                            self.right = False
                            self.justMoved = True
                            nothingChanged = False
                        elif(noUp == False and self.down == False):
                            nothingChanged = False
                            self.up = True
                            self.left = False
                            self.right = False
                            self.justMoved = True
                        elif (noright == False and self.left == False):
                            self.right = True
                            self.up = False
                            self.down = False
                            self.justMoved = True
                            nothingChanged = False
                        
                      
            else:
                
                if(self.left == False and noright == False):
                    self.right = True
                    self.up = False
                    self.down = False
                    self.justMoved = True
                    nothingChanged = False
                
                else:
                    
                    if(disty >= 0 and noUp == False and self.down == False):
                        nothingChanged = False
                        self.up = True
                        self.left = False
                        self.right = False
                        self.justMoved = True
            
                    else:
                
                        if(noDown == False and self.up == False):
                            self.down = True
                            self.left = False
                            self.right = False
                            self.justMoved = True
                            nothingChanged = False
                        elif(noUp == False and self.down == False):
                            nothingChanged = False
                            self.up = True
                            self.left = False
                            self.right = False
                            self.justMoved = True
                        elif(self.right == False and noleft == False):
                            self.left = True
                            self.up = False
                            self.down = False
                            self.justMoved = True
                            nothingChanged = False
                    
        else:
        
            if(disty > 0):
                
                if(self.down == False and noUp == False):
                    nothingChanged = False
                    self.up = True
                    self.left = False
                    self.right = False
                    self.justMoved = True
                
                else:
                    
                    if(distx >= 0 and noleft == False and self.right == False):
                        nothingChanged = False
                        self.left = True
                        self.up = False
                        self.down = False
                        self.justMoved = True
                        
                    else:
                        
                        if(noright == False and self.right == False):
                            nothingChanged = False
                            self.right = True
                            self.up = False
                            self.down = False
                            self.justMoved = True
                            
                        elif(noleft == False and self.right == False):
                            self.left = True
                            self.up = False
                            self.down = False
                            self.justMoved = True
                            nothingChanged = False
                        elif(self.up == False and noDown == False):
                            nothingChanged = False
                            self.down = True
                            self.left = False
                            self.right = False
                            self.justMoved = True
                    
                    
                     
            
            else:
                
                if(self.up == False and noDown == False):
                    nothingChanged = False
                    self.down = True
                    self.left = False
                    self.right = False
                    self.justMoved = True
                    
                else:
                    
                    if(distx >= 0 and noleft == False and self.right == False):
                        nothingChanged = False
                        self.left = True
                        self.up = False
                        self.down = False
                        self.justMoved = True
                        
                    else:
                        if(noright == False and self.left == False):
                            nothingChanged = False
                            self.right = True
                            self.up = False
                            self.down = False
                            self.justMoved = True
                        elif(noleft == False and self.right == False):
                            self.left = True
                            self.up = False
                            self.down = False
                            self.justMoved = True
                            nothingChanged = False
                        elif(noUp == False and self.down == False):
                            nothingChanged = False
                            self.up = True
                            self.left = False
                            self.right = False
                            self.justMoved = True
                            
                    
                    
        #if (nothingChanged == True):
            
            
            #print("nothing changed")
            #print("goal x: " + str(self.goal_x) + " : goal y:" + str(self.goal_y))
            #print("longest x: " + str(self.longest_x) + ", longest y: " + str(self.longest_y))
            #print("moving x: " + str(self.moving_x) + ", moving y: " + str(self.moving_y))
            #for i in range (self.bodyCount):
                #print("At " + str(i) + " :" + str(self.x[i]) + ", " + str(self.y[i]))                    
                
                
                        
                    
                
        
        
        
        
    def CheckGoalCollision (self):
        
        if(self.x[0] == self.goal_x and self.y[0] == self.goal_y):
            self.bodyCount = self.bodyCount + 1
            self.caught = True
            self.newGoal()
        
    def newGoal (self):
        NotOn = False
        
        while (NotOn == False):
            NotOn = True
            self.goal_x = (math.floor(random.randint(1,499)/10))*10
            self.goal_y = (math.floor(random.randint(1,499)/10))*10
            
            for i in range(self.bodyCount):
                if(self.x[i] == self.goal_x and self.y[i] == self.goal_y):
                    NotOn = False
                    break
            
    
    def CollisionCheck (self):
        
        for i in range(1,self.bodyCount,1):
            if(self.x[i] == self.x[0] and self.y[i] == self.y[0]):
                self.GameOver = True
                break
        #These r used to stop from going out of screen
        
        if(self.y[0] > 500):
            self.GameOver = True
        
        if(self.y[0] < 0):
            self.GameOver = True
            
        if(self.x[0] > 500):
            self.GameOver = True
        
        if(self.x[0] < 0):
            self.GameOver = True
       

   # def TryAgain (self):
        
        
        
        
        
if __name__ == '__main__':
    
    
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    Game = Snake()
    Game.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
