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
            
            painter = QPainter(self)
            painter.begin(self)
            painter.drawImage(0,-100,self.GO)
            painter.drawImage(100,350,self.tryAgain)
            painter.end()
        
    def timing (self):
        try:    
            #print("painting")
            self.CheckGoalCollision()
            self.CollisionCheck()
            self.Move()
            self.repaint()
            self.justMoved = False
        finally:
            if(self.GameOver == False):
                QTimer.singleShot(120, self.timing)
                
            
            
    
    def Move(self):
        
        for i in range (self.bodyCount, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
   

        if (self.left) :
            self.x[0] = self.x[0] - 10
                

        if (self.right) :
            self.x[0] = self.x[0] + 10
    

        if (self.up) :
            self.y[0] = self.y[0] - 10
    

        if (self.down) :
            self.y[0] = self.y[0] + 10
    
    
    
    def keyPressEvent(self, event):
        
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
            
        if (event.key() == Qt.Key_Return and self.GameOver == True):
            self.GameOver = False
            self.left = False
            self.right = False
            self.up = False
            self.down = True
            self.bodyCount = 4
            for i in range(2500):
                self.x[i] = 0
                self.y[i] = 0
            for i in range(self.bodyCount):
                self.x[i] = 20
                self.y[i] = 70 - i*10
                
            self.timing()
        
    
    def CheckGoalCollision (self):
        
        if(self.x[0] == self.goal_x and self.y[0] == self.goal_y):
            self.bodyCount = self.bodyCount + 1
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
