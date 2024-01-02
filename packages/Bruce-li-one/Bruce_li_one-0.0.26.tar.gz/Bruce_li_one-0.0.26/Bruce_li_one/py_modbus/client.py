#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time :2023/2/6 
# @Author :wsli
# @File : client.py
# @Software: PyCharm


from modbus_tk import modbus_rtu
import modbus_tk.defines as cst
import serial
from pyModbusTCP.client import ModbusClient
from modbus_tk import modbus_rtu_over_tcp

class Bruce_modbus_serial_com():
    def __init__(self,port:str="com1",
                 baudrate:int=9600,
                 bytesize:int=8,
                 parity:str="N",
                 stopbits:int=1):
        """

        :param port:com口
        :param baudrate:波特率
        :param bytesize:几位数据 默认为8
        :param parity:  奇偶校验
        :param stopbits: 停止位
        """
        self.master = modbus_rtu.RtuMaster(serial.Serial(port=port,
                                                    baudrate=baudrate,
                                                    bytesize=bytesize,
                                                    parity=parity,
                                                    stopbits=stopbits))
        self.master.set_timeout(5.0)
        self.master.set_verbose(True)

    def read_h03(self,slave:int, starting_address:int,quantity_of_x:int):
        """
        读线圈
        :param slave:站号
        :param starting_address:地址
        quantity_of_x:长度
        :return:
        """
        data=self.master.execute(slave, cst.READ_HOLDING_REGISTERS, starting_address, quantity_of_x)
        return data


class Bruce_modbus_tcp(ModbusClient):
    def __init__(self,host:str="localhost",port:int=502):
        ModbusClient.__init__(self,host,port)

    def read_holding_registers3(self,address:int,reg_len:int):
        """
        address register address (0 to 65535)
        功能码3 读取单个保持寄存器
        长度 reg_len
        :return:
        """
        regs_ist1 = self.read_holding_registers(reg_addr=address, reg_nb=reg_len)
        return regs_ist1

    def write_single_register6(self, address: int, reg_val: int):
        """
        功能码6 写单个寄存器
        address register address (0 to 65535)
        长度 reg_len
        :return:
        """
        try:
            self.write_single_register(reg_addr=address, reg_value=reg_val)
            return True
        except Exception as e:
            return False
    def write_multiple_registers16(self,address:int,reg_list_val:list):
        """
        功能码16 写多个寄存器的值(顺序的才可以写多个)
        :return:
        """
        try:
            self.write_multiple_registers(regs_addr=address,regs_value=reg_list_val)
            return True
        except Exception as e:
            return False


class Bruce_modbus_rtu_over_tcp():
    def __init__(self,ip:str,port:int=502):
        self.IP=ip
        self.PORT=port
        self.master=self.do_conect()

    @property
    def is_open(self):
        return self.master._is_opened

    def do_conect(self):
        master = modbus_rtu_over_tcp.RtuOverTcpMaster(host=self.IP, port=self.PORT)
        return master

    def read_input_registers4(self,Slave_ID:int=1,Address:int=0,Quantity:int=1)->tuple:
        result = self.master.execute(Slave_ID, cst.READ_INPUT_REGISTERS, Address, Quantity)
        return result

    def read_write_definition(self,Slave_ID: int,Function:str, Address: int, Quantity: int)->tuple:
        function_code=""
        if Function=="1":
            function_code=cst.READ_COILS
        elif Function=="2":
            function_code=cst.READ_DISCRETE_INPUTS
        elif Function=="3":
            function_code=cst.READ_HOLDING_REGISTERS
        elif Function=="4":
            function_code=cst.READ_INPUT_REGISTERS
        elif Function=="5":
            function_code=cst.WRITE_SINGLE_COIL
        elif Function=="6":
            function_code=cst.WRITE_SINGLE_REGISTER
        elif Function=="15":
            function_code=cst.WRITE_MULTIPLE_COILS
        elif Function=="16":
            function_code=cst.WRITE_MULTIPLE_REGISTERS
        else:
            return "Function_code_error"
        result = self.master.execute(Slave_ID, function_code, Address, Quantity)
        return result
    def read_write_function_code(self)->dict:
        dict1={
            "READ_COILS" : "1",
            "READ_DISCRETE_INPUTS" : "2",
            "READ_HOLDING_REGISTERS" : "3",
            "READ_INPUT_REGISTERS" : "4",
            "WRITE_SINGLE_COIL" : "5",
            "WRITE_SINGLE_REGISTER" : "6",
            "WRITE_MULTIPLE_COILS" : "15",
            "WRITE_MULTIPLE_REGISTERS" : "16"
        }
        return dict1