# x = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120]
# y = [10,22,35,35,35,35,42,46,87,90,90,90,90,150,200,200,205,206,210,210,210,210,210,250,275]
# z = [0]
# for i in range(1,len(y)):
#    z.append((y[i]-y[i-1])/5.0)
# print len(x)
# print len(z)
#
# import matplotlib.pyplot as plt
#
# plt.plot(x, z, color='green')
# plt.xlabel('Time (from beginning to now)')
# plt.ylabel('Total Number of Keys Pressed')
# plt.title('Student Activity\nAli Emre Oz - 213950785')
# plt.grid(True)
# plt.show()





import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
canvas = fig.canvas


class MyApp(App):
    def build(self):
        box = BoxLayout()
        self.i = 0
        self.line = [self.i]
        box.add_widget(canvas)
        plt.show()
        Clock.schedule_interval(self.update, 1)
        return box

    def update(self, *args):
        plt.plot(self.line, self.line)
        self.i += 1
        self.line.append(self.i)
        canvas.draw_idle()


MyApp().run()