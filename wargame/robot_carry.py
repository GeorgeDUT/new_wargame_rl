"""
this file is env model
"""

from __future__ import division
import sys
import numpy as np
import time

if sys.version_info.major == 2:
    from Tkinter import *
    import Tkinter as tk
else:
    from tkinter import *
    import tkinter as tk

MAP_W = 15
MAP_H = 5
UNIT_PIX = 25


class ARMY(object):
    def __init__(self, x_loc=0, y_loc=0, id=0, blood=10, dirction=(0, 1)):
        self.x = x_loc
        self.y = y_loc
        self.last_x = x_loc
        self.last_y = y_loc
        self.id = id
        self.blood = blood
        self.state = 'live'
        self.init_x = x_loc
        self.init_y = y_loc
        self.init_blood = blood
        # dirction (x,y) x is horizontal axis, y is vertical axis
        # (1,0) is right dirction, (0,1) is down, (-1,0) is left, (0,-1) is up
        self.dirction = dirction

    def move(self, action, ROBOT_MAP):
        def move_up(self):
            return 0, -1

        def move_down(self):
            return 0, 1

        def move_left(self):
            return -1, 0

        def move_right(self):
            return 1, 0

        def move_stay(self):
            return 0, 0

        dic = {'u': move_up(self), 'd': move_down(self), 'l': move_left(self), 'r': move_right(self),
               's': move_stay(self)}
        add_x, add_y = dic[action]
        chang_x = self.x + add_x
        chang_y = self.y + add_y
        # check border
        if chang_x < 0:
            chang_x = 0
            add_x = 0
        if chang_x > ROBOT_MAP.map_w - ROBOT_MAP.map_start_x - 1:
            chang_x = ROBOT_MAP.map_w - ROBOT_MAP.map_start_x - 1
            add_x = 0
        if chang_y < 0:
            chang_y = 0
            add_y = 0
        if chang_y > ROBOT_MAP.map_h - ROBOT_MAP.map_start_y - 1:
            chang_y = ROBOT_MAP.map_h - ROBOT_MAP.map_start_y - 1
            add_y = 0
        if (ROBOT_MAP.env_map[chang_y][chang_x] == 'robot') or (ROBOT_MAP.env_map[chang_y][chang_x] == 'nato'):
            add_y = 0
            add_x = 0
            chang_y = self.y
            chang_x = self.x
        if self.state =='dead':
            add_y = 0
            add_x = 0
            chang_y = self.y
            chang_x = self.x

        self.last_x = self.x
        self.last_y = self.y
        self.x = chang_x
        self.y = chang_y
        return add_x, add_y


class ROBOT(ARMY):
    def __init__(self, x_loc, y_loc, id, blood, dirction):
        super(ROBOT,self).__init__(x_loc,y_loc,id,blood, dirction)
        self.team = 1
        self.class_name = 'robot'
        self.force = 0.1


class NATO(ARMY):
    def __init__(self,x_loc,y_loc,id,blood, dirction):
        super(NATO,self).__init__(x_loc,y_loc,id,blood, dirction)
        self.team = 2
        self.class_name = 'nato'
        self.force = 0.1


'''
class TRUCK(object):
    pass
class WAll(object):
    pass
'''


class ROBOT_MAP(tk.Tk, object):
    def __init__(self, ROBOT_NUM = 10, NATO_NUM = 10,draw_pic=True):
        if draw_pic:
            super(ROBOT_MAP, self).__init__()
            self.title('robot carry')
            self.geometry('{0}x{1}'.format(MAP_W * UNIT_PIX, MAP_H * UNIT_PIX))
        else:
            pass
        self.draw_pic = draw_pic
        self.robot_num = ROBOT_NUM
        self.nato_num = NATO_NUM
        self.map_start_x = 10
        self.map_start_y = 0
        self.map_w = MAP_W
        self.map_h = MAP_H
        self.env_map = []
        self.robot=[]
        self.nato=[]
        self.action_space = ['u','d','l','r','s']
        self.action_num = len(self.action_space)
        # robot_loc[i][0] is i robot's x,robot_loc[i][1] is i robot's y,
        self.robot_loc = np.zeros(shape=(ROBOT_NUM,2))
        self.nato_loc = np.zeros(shape=(NATO_NUM,2))
        if self.draw_pic:
            self.display_window()
            self._build_map()
        else:
            self._build_map_server()

    def display_window(self):
        fram1=Frame()
        line = tk.Canvas(self, bg='black', height=MAP_H*UNIT_PIX, width=2)
        line.place(x=(self.map_start_x-1)*UNIT_PIX,y=self.map_start_y)
        display = Label(fram1, text='information', bg='white', width=13, height=2, font=("Arial", 16))
        display.pack(side=TOP)
        a='agent 1'
        agent_inf = Label(fram1, text=a, bg='red', width=13, height=2, font=("Arial", 16))
        agent_inf.pack(side=TOP)
        fram1.place(x=0,y=0)

    def _build_map(self):
        self.map = tk.Canvas(self, bg='white', height=MAP_H * UNIT_PIX, width=(MAP_W-self.map_start_x) * UNIT_PIX)
        self.map.place(x=self.map_start_x*UNIT_PIX,y=self.map_start_y)
        # gird
        for c in range(0, (MAP_W-self.map_start_x) * UNIT_PIX, UNIT_PIX):
            x0, y0, x1, y1 = c, 0, c, MAP_H * UNIT_PIX
            self.map.create_line(x0, y0, x1, y1)
        for r in range(0, MAP_H * UNIT_PIX, UNIT_PIX):
            x0, y0, x1, y1 = 0, r, MAP_W * UNIT_PIX, r
            self.map.create_line(x0, y0, x1, y1)
        # init env_map,env_map[]='robot',robot;env_map[]='nato',nato;env_map[]=
        for i in range(self.map_h):
            a=[]
            for j in range(self.map_w-self.map_start_x):
                a.append('null')
            self.env_map.append(a)

    def _build_map_server(self):
        for i in range(self.map_h):
            a=[]
            for j in range(self.map_w-self.map_start_x):
                a.append('null')
            self.env_map.append(a)

    def regist(self, aclass):
        if aclass.state == 'live':
            a = aclass.last_x
            b = aclass.last_y
            a_ = aclass.x
            b_ = aclass.y
            class_name = aclass.class_name
            self.env_map[b][a] = 'null'
            self.env_map[b_][a_] = class_name
            if aclass.class_name == 'robot':
                self.robot_loc[aclass.id][0] = aclass.x
                self.robot_loc[aclass.id][1] = aclass.y
            elif aclass.class_name == 'nato':
                self.nato_loc[aclass.id][0] = aclass.x
                self.nato_loc[aclass.id][1] = aclass.y
        elif aclass.state == 'dead':
            pass

    def init_robot_tk(self, ROBOT,n):
        for i in range(n):
            self.robot.append(self.map.create_rectangle(ROBOT[i].x * UNIT_PIX,
                    ROBOT[i].y * UNIT_PIX, (ROBOT[i].x+ 1) * UNIT_PIX,
                    (ROBOT[i].y+1) * UNIT_PIX, fill='red'))
            self.regist(ROBOT[i])

    def init_robot_server(self,ROBOT,n):
        for i in range(n):
            self.regist(ROBOT[i])

    def init_robot(self,ROBOT,n):
        if self.draw_pic:
            self.init_robot_tk(ROBOT,n)
        else:
            self.init_robot_server(ROBOT,n)

    def init_nato_tk(self,NATO,n):
        for i in range(n):
            self.nato.append(self.map.create_rectangle(NATO[i].x * UNIT_PIX,
                    NATO[i].y * UNIT_PIX, (NATO[i].x+1) * UNIT_PIX,
                    (NATO[i].y + 1) * UNIT_PIX, fill='black'))
            self.regist(NATO[i])

    def init_nato_server(self,NATO,n):
        for i in range(n):
            self.regist(NATO[i])

    def init_nato(self, NATO, n):
        if self.draw_pic:
            self.init_nato_tk(NATO,n)
        else:
            self.init_nato_server(NATO,n)

    def flash_tk(self,num,action,aclass):
        # move robot
        if aclass[0].class_name == 'robot':
            for i in range(num):
                add_x = action[i][0]
                add_y = action[i][1]
                self.map.move(self.robot[i], UNIT_PIX * add_x, UNIT_PIX * add_y)
                #self.regist(aclass[i])
        # move noto
        elif aclass[0].class_name == 'nato':
            for i in range(num):
                add_x = action[i][0]
                add_y = action[i][1]
                self.map.move(self.nato[i], UNIT_PIX * add_x, UNIT_PIX * add_y)
                #self.regist(aclass[i])
        self.update()

    def flash_server(self,num,action,aclass):
        pass

    def flash(self,num,action,aclass):
        if self.draw_pic:
            self.flash_tk(num, action, aclass)
        else:
            self.flash_server(num, action, aclass)

    def check_surround(self,name,id):
        if name == 'robot':
            pass
        elif name == 'nato':
            find = 0
            x = self.nato_loc[id][0]
            y = self.nato_loc[id][1]
            add_space = np.zeros(shape=(4, 2))
            add_space[0][0] = 0
            add_space[0][1] = -1
            add_space[1][0] = 0
            add_space[1][1] = 1
            add_space[2][0] = -1
            add_space[2][1] = 0
            add_space[3][0] = 1
            add_space[3][1] = 0
            if x == 0:
                add_space[2][0] = 0
                add_space[2][1] = 0
                find = find + 1
            if y == 0:
                add_space[0][0] = 0
                add_space[0][1] = 0
                find = find + 1
            if x == self.map_w - self.map_start_x - 1:
                add_space[3][0] = 0
                add_space[3][1] = 0
                find = find + 1
            if y == self.map_h - self.map_start_y - 1:
                add_space[1][1] = 0
                add_space[1][0] = 0
                find = find + 1
            for j in range(4):
                column = int(self.nato_loc[id][0] + add_space[j][0])
                line = int(self.nato_loc[id][1] + add_space[j][1])
                if self.env_map[line][column] == 'robot':
                    find = find + 1
            if find == 4:
                return True
            else:
                return False

    # TODO fight check
    '''
    def check_fight(self,robot,nato):
        for i in range(self.robot_num):
            x = self.robot_loc[i][0]
            y = self.robot_loc[i][1]
            add_space =np.zeros(shape=(4,2))
            add_space[0][0] = 0
            add_space[0][1] = -1
            add_space[1][0] = 0
            add_space[1][1] = 1
            add_space[2][0] = -1
            add_space[2][1] = 0
            add_space[3][0] = 1
            add_space[3][1] = 0
            if x == 0:
                add_space[2][0] = 0
                add_space[2][1] = 0
            if y == 0:
                add_space[0][0] = 0
                add_space[0][1] = 0
            if x == self.map_w-self.map_start_x-1:
                add_space[3][0] = 0
                add_space[3][1] = 0
            if y == self.map_h-self.map_start_y-1:
                add_space[1][1] = 0
                add_space[1][0] = 0
            for j in range(4):
                column = x + add_space[j][0]
                line = y + add_space[j][1]
                if self.env_map[line][column] == 'nato':
                    robot[i].state = 'war'
                    for k in range(self.nato_num):
                        if nato[k].x == column and nato[k].y == line:
                            nato[k].state = 'war'
    '''

    def restart_tk(self,robot,nato):
        # change robot
        for i in range(self.robot_num):
            add_x = robot[i].init_x - robot[i].x
            add_y = robot[i].init_y - robot[i].y
            robot[i].last_x = robot[i].x
            robot[i].last_y = robot[i].y
            self.map.move(self.robot[i], UNIT_PIX * add_x, UNIT_PIX * add_y)
            robot[i].x = robot[i].init_x
            robot[i].y = robot[i].init_y
            robot[i].blood = robot[i].init_blood
            self.regist(robot[i])
            robot[i].last_x = robot[i].x
            robot[i].last_y = robot[i].y
        # change nato
        for i in range(self.nato_num):
            add_x = nato[i].init_x - nato[i].x
            add_y = nato[i].init_y - nato[i].y
            self.map.move(self.nato[i], UNIT_PIX * add_x, UNIT_PIX * add_y)
            nato[i].last_x = nato[i].x
            nato[i].last_y = nato[i].y
            nato[i].x = nato[i].init_x
            nato[i].y = nato[i].init_y
            nato[i].blood = nato[i].init_blood
            self.regist(nato[i])
            nato[i].last_x = nato[i].x
            nato[i].last_y = nato[i].y
        # ensure all robot or nato are registered on env_map
        for i in range(self.robot_num):
            self.env_map[robot[i].y][robot[i].x] = robot[i].class_name
        for i in range(self.nato_num):
            self.env_map[nato[i].y][nato[i].x] = nato[i].class_name
        self.update()

    def restart_server(self,robot,nato):
        # change robot
        for i in range(self.robot_num):
            add_x = robot[i].init_x - robot[i].x
            add_y = robot[i].init_y - robot[i].y
            robot[i].last_x = robot[i].x
            robot[i].last_y = robot[i].y
            robot[i].x = robot[i].init_x
            robot[i].y = robot[i].init_y
            robot[i].blood = robot[i].init_blood
            self.regist(robot[i])
            robot[i].last_x = robot[i].x
            robot[i].last_y = robot[i].y
        # change nato
        for i in range(self.nato_num):
            add_x = nato[i].init_x - nato[i].x
            add_y = nato[i].init_y - nato[i].y
            nato[i].last_x = nato[i].x
            nato[i].last_y = nato[i].y
            nato[i].x = nato[i].init_x
            nato[i].y = nato[i].init_y
            nato[i].blood = nato[i].init_blood
            self.regist(nato[i])
            nato[i].last_x = nato[i].x
            nato[i].last_y = nato[i].y
        # ensure all robot or nato are registered on env_map
        for i in range(self.robot_num):
            self.env_map[robot[i].y][robot[i].x] = robot[i].class_name
        for i in range(self.nato_num):
            self.env_map[nato[i].y][nato[i].x] = nato[i].class_name

    def restart(self,robot,nato):
        for i in range(self.robot_num):
            robot[i].state='live'
        for i in range(self.nato_num):
            nato[i].state='live'
        if self.draw_pic:
            self.restart_tk(robot,nato)
        else:
            self.restart_server(robot,nato)

    def remove_agent(self,agent,agent_id):
        if agent.class_name == 'robot':
            pass
        elif agent.class_name == 'nato':
            agent.state='dead'
            self.env_map[agent.y][agent.x]='null'
