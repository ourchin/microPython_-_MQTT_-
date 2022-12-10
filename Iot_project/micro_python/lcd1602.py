################################################################################
#                           叁议电子
#                        www.ppptalk.com
# 版本：      pyboard改进版(V1.0)
# 文件名：    lcd1602.py
# 说明：      lcd1602液晶显示模块
# 淘宝店地址： https://shop115025335.taobao.com
# 免责声明：  该程序仅用于学习与交流
# (c) PPPTalk  All Rights Reserved
################################################################################


import pyb
from pyb import Pin
import time


class LCD1602():
    def __init__(self,   rs_pin, rw_pin, en_pin, d0_pin, d1_pin,
                 d2_pin, d3_pin, d4_pin, d5_pin, d6_pin, d7_pin):

        self.rs = Pin(rs_pin,Pin.OUT_PP)
        self.rw = Pin(rw_pin,Pin.OUT_PP)
        self.en = Pin(en_pin,Pin.OUT_PP)
        self.d0 = Pin(d0_pin,Pin.OUT_PP)
        self.d1 = Pin(d1_pin,Pin.OUT_PP)
        self.d2 = Pin(d2_pin,Pin.OUT_PP)
        self.d3 = Pin(d3_pin,Pin.OUT_PP)
        self.d4 = Pin(d4_pin,Pin.OUT_PP)
        self.d5 = Pin(d5_pin,Pin.OUT_PP)
        self.d6 = Pin(d6_pin,Pin.OUT_PP)
        self.d7 = Pin(d7_pin, Pin.OPEN_DRAIN, Pin.PULL_UP)


    def Busy_Check(self):
        self.d7(1)
        while 1:
            self.rs(0)
            self.rw(1)
            self.en(0)
            self.en(1)
            time.sleep_us(2)

            if self.d7.value()==0:
                time.sleep_us(1)
                self.en(0)
                break
            time.sleep_us(1)
            self.en(0)
            time.sleep_us(1)


    def Write_Cmd(self,cmdWrite):
        self.Busy_Check()
        self.rs(0)
        self.rw(0)
        self.en(0)
        self.d0(cmdWrite&0x01)
        self.d1(cmdWrite&0x02)
        self.d2(cmdWrite&0x04)
        self.d3(cmdWrite&0x08)
        self.d4(cmdWrite&0x10)
        self.d5(cmdWrite&0x20)
        self.d6(cmdWrite&0x40)
        self.d7(cmdWrite&0x80)
        time.sleep_us(1)
        self.en(1)
        time.sleep_us(1)
        self.en(0)
        time.sleep_us(2)


    def Init(self):
        time.sleep_ms(15)
        self.Write_Cmd(0x38)
        time.sleep_ms(5)
        self.Write_Cmd(0x38)
        self.Write_Cmd(0x08)
        self.Write_Cmd(0x01)
        self.Write_Cmd(0x06)
        self.Write_Cmd(0x0c)

    def Show_String(self,row,col,str):
        if row == 1:
            self.Write_Cmd(0x00+0x80+col-1)
            for letter in str:
                self.Write_Data(ord(letter))
        if row == 2:
            self.Write_Cmd(0x40+0x80+col-1)
            for letter in str:
                self.Write_Data(ord(letter))

    def Custom_Char(self, row,col, pos,customValueTable ):
        for i in range(8):
            self.Write_Cmd(0x40+pos*8+i)
            self.Write_Data(customValueTable[i])
        if row==1:
            self.Write_Cmd(0x00+0x80+col-1)
            self.Write_Data(0x00+pos)
        else:
            self.Write_Cmd(0x40+0x80+col-1)
            self.Write_Data(0x00+pos)

    def Write_Data(self,dataWrite):
        self.Busy_Check()
        self.rs(1)
        self.rw(0)
        self.en(0)
        self.d0(dataWrite&0x01)
        self.d1(dataWrite&0x02)
        self.d2(dataWrite&0x04)
        self.d3(dataWrite&0x08)
        self.d4(dataWrite&0x10)
        self.d5(dataWrite&0x20)
        self.d6(dataWrite&0x40)
        self.d7(dataWrite&0x80)
        time.sleep_us(1)
        self.en(1)
        time.sleep_us(1)
        self.en(0)
        time.sleep_us(2)


