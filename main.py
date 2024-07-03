import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.vector import Vector
import math
import random
class Paddle(Widget):
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.vx,ball.vy
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.vx=vel[0]
            ball.vy=vel[1]

class PongBall(Widget):
    vx=NumericProperty(4)
    vy=NumericProperty(4)
    def Move(self,*args):
        self.pos[0]=self.pos[0] + self.vx
        self.pos[1]=self.pos[1] + self.vy

class PongGame(Widget):
    ball=ObjectProperty()
    player1=ObjectProperty()
    player2=ObjectProperty()
    score1=NumericProperty(0)
    score2=NumericProperty(0)
    def Serve(self):
        phi=random.random()*math.pi
        self.ball.center=self.center
        self.ball.vx=4*math.sin(phi)
        self.ball.vy=6*math.cos(phi)
    def Update(self,*args):
        #move the ball
        self.ball.Move()
        #bouncing off the top and the bottom
        if self.ball.top>=self.top or self.ball.y<=self.y:
            self.ball.vy*=-1

        #bouncing off left and right
        #if self.ball.right>=self.right or self.ball.x<=self.x:
        #    self.ball.vx*=-1
        if self.ball.x>=self.right:
            self.Serve()
            self.score1+=1
        if self.ball.right<self.x:
            self.Serve()
            self.score2+=1
        #bouncing off player paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

    def on_touch_move(self,touch):
        if touch.x<self.width*1/3:
            self.player1.center_y=touch.y
        elif touch.x>self.width*2/3:
            self.player2.center_y=touch.y

class PongApp(App):
    def build(self):
        g=PongGame()
        g.Serve()
        Clock.schedule_interval(g.Update,1/60)
        return g

if __name__=="__main__":
    PongApp().run()