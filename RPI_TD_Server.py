#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import cherrypy
import datetime
import sys
from Traffic_detection_server import *
import traceback
import string
import os
import time
import socket
#import json
#import psycopg2

#conf = json.load(open("Bahnhofstr14.json"))

# define variables
current_chart_data = [["Time", "Sys_1", "Sys_2", "Sys_3", "Total"]]
power_chart_data = [["Time", "Sys_1", "Sys_2", "Sys_3", "Total", "Demand"]]
voltage_chart_data = [["Time", "Sys_1", "Sys_2", "Sys_3"]]
delta_voltage_chart_data = [["Time", "Sys_1", "Sys_2", "Sys_3"]]
soc_chart_data = [["Time", "Sys_1", "Sys_2", "Sys_3"]]
chart_display_range = 10

dynamic_data = []
static_data_val = []
dynamic_data_val = []


# class for initialization of the webserver
class Cherrypy_Init:

    def __init__(self, address, port):
        #----------------------------------------------------
        current_directory = os.path.abspath("")
        self.app_config = {}
        self.app_config['/'] = {}
        self.app_config['/']['tools.sessions.on'] = True
        self.app_config['/css'] = {}
        self.app_config['/css']['tools.staticdir.on'] = True
        self.app_config['/css']['tools.staticdir.dir'] = current_directory + "\\Webpage\\assets\\css\\"
        self.app_config['/java'] = {}
        self.app_config['/java']['tools.staticdir.on'] = True
        self.app_config['/java']['tools.staticdir.dir'] = current_directory + "\\Webpage\\assets\\java\\"
        self.app_config['/images'] = {}
        self.app_config['/images']['tools.staticdir.on'] = True
        self.app_config['/images']['tools.staticdir.dir'] = current_directory + "\\Webpage\\assets\\images\\"
        self.app_config['/css2'] = {}
        self.app_config['/css2']['tools.staticdir.on'] = True
        self.app_config['/css2']['tools.staticdir.dir'] = current_directory + "\\Webpage\\assets\\css"
        self.app_config['/fonts'] = {}
        self.app_config['/fonts']['tools.staticdir.on'] = True
        self.app_config['/fonts']['tools.staticdir.dir'] = current_directory + "\\Webpage\\assets\\fonts"
        self.app_config['/js'] = {}
        self.app_config['/js']['tools.staticdir.on'] = True
        self.app_config['/js']['tools.staticdir.dir'] = current_directory + "\\Webpage\\assets\\js"
        self.app_config['/sass'] = {}
        self.app_config['/sass']['tools.staticdir.on'] = True
        self.app_config['/sass']['tools.staticdir.dir'] = current_directory + "\\Webpage\\assets\\sass"

        self.global_config = {}
        self.global_config['log.screen'] = True
        self.global_config['server.socket_host'] = address
        self.global_config['server.socket_port'] = port
        self.global_config['engine.autoreload.on'] = True

        #self.global_config['engine.SIGHUP'] = None
        #self.global_config['engine.SIGTERM'] = None
        #self.global_config['engine.SIGINT'] = None

    def exit(self):
        cherrypy.engine.exit()
        print "  - HTTP Server : exit()"

    def start(self):
        try:
            root = Cherrypy_Web(self)
            cherrypy.config.update(self.global_config)
            cherrypy.tree.mount(root, config=self.app_config)
            cherrypy.engine.start()
            return root

        except:
            print traceback.format_exc()
            return None

# class for cyclic operation of the webserver
class Cherrypy_Web:

    def __init__(self,obj):
        self.CSS = "css/style.css"
        self.ICO = "images/favicon.ico"
        self.JAVA = "java/java.js"
        self.CHARTS = "java/charts.js"
        self.UpdateCycle_fast = conf["WS_UpdateCycleFast"]
        self.UpdateCycle_slow = conf["WS_UpdateCycleSlow"]
        self.BAT = []

    @cherrypy.expose
    def ExampleCall(self,param=""):

        if param == "CheckCOMPorts":
            if Battery_Cluster_Manager.get_available_serial_ports() == [","]:
                param = "No COM ports found"
            else:
                param = str (main.get_available_serial_ports())

        if param == "ConnectSpecifiedBatterySystems":
            result = Battery_Cluster_Manager.connect_specified_battery_systems()
            param = str(result)

        elif param == "print_battery_systems_data":
            param = str(Battery_Cluster_Manager.print_battery_systems_data())

        return param

    @cherrypy.expose
    def Request(self):
        #param = "images/ServerConnection_unknown.png"
        #if connect_database()[0] == True:
        #    param = "images/ServerConnection_on.png"
        #else:
        #print Traffic.TrafficCounter
        param = [Traffic.TrafficCounter, Traffic.DetectionStatus, Traffic.direction]
        print param
        return param

   # @cherrypy.expose
    #def Read_Dynamic_Data(self):
        #param = [True, [('Sys_01', datetime.datetime(2017, 11, 10, 13, 22, 5, 678000), datetime.datetime(2017, 11, 10, 13, 20, 38, 23000), '313238373331470D0026003D', '0', True, 0.0, 364.75, 3.8, 3.8, 39.0854, 20.0, 30.0, -273.15, -273.15, -15.0, 15.0, 340.0, 389.5, '00000000', '00000000', '00000000', '0000', '140A', '140A', 0, 0.0, 0L, 0L, 21.1111, 'FF', 'FF', 'FF', 'FF', 0, 'FF', 'FF', '000000C2', 0.0, 0, datetime.datetime(1, 1, 1, 0, 0), 0.0, 350.0, 0.0, 'FF', '0', 'FFFF', 0.0, datetime.datetime(1, 1, 1, 0, 0), 'SMA', 0L, 0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 30.0, 20.0, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8), ('Sys_02', datetime.datetime(2017, 11, 10, 13, 22, 5, 741000), datetime.datetime(2017, 11, 10, 13, 20, 38, 23000), '31383239333651070042005B', '1', True, 0.0, 364.75, 3.8, 3.8, 39.0854, 20.0, 30.0, -273.15, -273.15, -15.0, 15.0, 340.0, 389.5, '00000000', '00000000', '00000000', '0000', '1801', '1801', 0, 0.0, 0L, 0L, 21.1111, 'FF', 'FF', 'FF', 'FF', 0, 'FF', 'FF', '000000C2', 0.0, 0, datetime.datetime(1, 1, 1, 0, 0), 0.0, 350.0, 0.0, 'FF', '0', 'FFFF', 0.0, datetime.datetime(1, 1, 1, 0, 0), 'SMA', 0L, 0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 30.0, 20.0, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8), ('Sys_03', datetime.datetime(2017, 11, 10, 13, 22, 5, 289000), datetime.datetime(2017, 11, 10, 13, 20, 38, 23000), '31383239333651070043004F', '2', True, 0.0, 364.75, 3.8, 3.8, 39.0854, 20.0, 30.0, -273.15, -273.15, -15.0, 15.0, 340.0, 389.5, '00000000', '00000000', '00000000', '0000', '2730', '2730', 0, 0.0, 0L, 0L, 21.1111, 'FF', 'FF', 'FF', 'FF', 0, 'FF', 'FF', '000000C2', 0.0, 0, datetime.datetime(1, 1, 1, 0, 0), 0.0, 350.0, 0.0, 'FF', '0', 'FFFF', 0.0, datetime.datetime(1, 1, 1, 0, 0), 'SMA', 0L, 0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 30.0, 20.0, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8)]]]
       # print param
      #  return param

    @cherrypy.expose
    def RequestText(self):
        param = "Database connection not initialized"
        if connect_database()[0] == True:
            param = "Database connected"
        else:
            param = "Database not connected"
        return param

    @cherrypy.expose
    def RequestSystem(self):

        SQL_Data = get_dynamic_system_data()

        return str(SQL_Data)

    @cherrypy.expose
    def RequestBatt(self):

        SQL_Data = get_dynamic_battery_system_data()

        return str(SQL_Data)

    @cherrypy.expose
    def RequestBattPicture(self):

        # define variables
        global database_connection
        dynamic_data_val = []
        array2 = [["system_name", "system_active"]]

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
        cursor = database_connection.cursor()

        cursor.execute("SELECT system_name, system_active FROM battery_system_static_data ORDER BY system_name ASC")
        dynamic_data_val.extend(cursor.fetchall())

        cursor.close()

        for data in dynamic_data_val:
            array = []
            for i in range(len(data)):
                array.append(data[i])
            array2.append(array)

        for data in array2[1:]:
            if data[1] is True:
                data[1] = "images/battery-green-512x512.png"
            else:
                data[1] = "images/battery-grey-512x512.png"

        return str(array2)

    @cherrypy.expose
    def RequestChart(self):

        x = random.random() * 100
        y = random.random() * 100
        z = random.random() * 100

        SQL_Data = Fill_SQL_Data_Array()

        # todo-michael: statische Anpassung, damit was zappelt. Muss im produktivumfeld ersetzt werden
        #SQL_Data[1][2] = x
        #SQL_Data[2][2] = y
        #SQL_Data[3][2] = z
        # print "SQLDATA ***************************"
        # print SQL_Data
        return str(SQL_Data)

    @cherrypy.expose
    def RequestChart2(self):

        # define variables
        global database_connection
        dynamic_data_val = []
        array2 = [["system_name", "inverter_grid_current", "inverter_grid_power"]]

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
        cursor = database_connection.cursor()

        cursor.execute(
            "SELECT system_name, inverter_grid_current, inverter_grid_power FROM battery_system_dynamic_data ORDER BY system_name ASC")
        dynamic_data_val.extend(cursor.fetchall())

        cursor.close()

        for data in dynamic_data_val:
            array = []
            for i in range(len(data)):
                array.append(str(data[i]))
            array2.append(array)

        # Strom bissl zappenl lassen
        array2[1][1] = round(random.random() * 100, 2)
        array2[2][1] = round(random.random() * 100, 2)
        array2[3][1] = round(random.random() * 100, 2)

        # Leistung bissl zappenl lassen
        array2[1][2] = int(random.random() * 1000)
        array2[2][2] = int(random.random() * 1000)
        array2[3][2] = int(random.random() * 1000)

        return str(array2)

    @cherrypy.expose
    def RequestErrorMessages(self):

        # define variables
        global database_connection
        error_data_val = []
        array2 = [["error_id", "error_code", "error_message", "error_data", "error_data_detailed", "error_time", "battery_system_name"]]

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
        cursor = database_connection.cursor()

        cursor.execute("SELECT * FROM application_errors ORDER BY error_id DESC LIMIT 10")
        error_data_val.extend(cursor.fetchall())

        for data in error_data_val:
            array = []
            for i in range(len(data)):
                array.append(str(data[i]))

            array2.append(array)
        return str(array2)

    @cherrypy.expose
    def DrawChart(self):

        # define variables
        global database_connection, soc_chart_data, chart_display_range
        dynamic_data_val = []

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
        cursor = database_connection.cursor()

        cursor.execute(
            "SELECT system_name, battery_state_of_charge FROM battery_system_dynamic_data ORDER BY system_name ASC")
        dynamic_data_val.extend(cursor.fetchall())

        cursor.close()

        array = [time.clock()]
        for data in dynamic_data_val:
            array.append(data[1])

        #array.append(array[1] + array[2] + array[3])
        soc_chart_data.append(array)

        if len(soc_chart_data) > (chart_display_range * 60 / (self.UpdateCycle_slow / 1000)):
            soc_chart_data.pop(1)

        return str(soc_chart_data)

        '''
        global chart_display_range
        
        Dynamic_Performance_Display_array=[['Month', 'System 1', 'System 2', 'System 3', 'Average SoC', 'Daily Max', 'Daily Min'], \
            ['CW1'	,  time.clock()		,      70 ,        50,             72,        100,      50		], \
            ['CW2'		,  time.clock()		,      80 ,        60,             75,        100,      60		], \
            ['CW3'		,  time.clock()		,      90 ,        70,             78,        100,      90		], \
            ['CW4'		,  time.clock()		,     100 ,        80,             80,        100,      80		], \
            ['CW5'		,  time.clock()		,      80 ,        90,             75,        100,      80		]]
        
        x = random.random() * 100
        y = random.random() * 100
        z = random.random() * 100
        SQL_Data = Fill_SQL_Data_Array2()
        soc_chart_data.append(SQL_Data)
        #[['system_name', 'battery_state_of_charge'], ['Sys_02', 39.0854], ['Sys_03', 39.0854], ['Sys_01', 39.0854]]
        #origworking = [['Time', 'System 1', 'System 2', 'System 3'], [1.230621808587443e-06, 57.52867986307473, 69.76101177301662, 36.593256478965216]]

        if len(soc_chart_data) > (chart_display_range * 60 / (self.UpdateCycle_slow / 1000)):
            soc_chart_data.pop(1)

        return str(soc_chart_data)
        '''

    @cherrypy.expose
    def DrawChart2(self):

        # define variables
        global database_connection, current_chart_data, chart_display_range
        dynamic_data_val = []

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
        cursor = database_connection.cursor()

        cursor.execute(
            "SELECT system_name, inverter_grid_current FROM battery_system_dynamic_data ORDER BY system_name ASC")
        dynamic_data_val.extend(cursor.fetchall())

        cursor.close()

        array = [time.clock()]
        for data in dynamic_data_val:
            array.append(data[1])

        array.append(array[1]+array[2]+array[3])
        current_chart_data.append(array)

        if len(current_chart_data) > (chart_display_range * 60 / (self.UpdateCycle_slow / 1000)):
            current_chart_data.pop(1)

        return str(current_chart_data)

    @cherrypy.expose
    def DrawChart3(self):

        # define variables
        global database_connection, power_chart_data, chart_display_range
        dynamic_data_val = []
        active_battery_systems = 0

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
        cursor = database_connection.cursor()

        cursor.execute(
            "SELECT system_name, inverter_grid_power, system_active "
            "FROM battery_system_dynamic_data ORDER BY system_name ASC")
        dynamic_data_val.extend(cursor.fetchall())

        cursor.execute(
            "SELECT system_demand FROM system_dynamic_data WHERE system_name = 'Server'")
        result = cursor.fetchall()[0][0]

        cursor.close()

        for data in dynamic_data_val:
            if data[2] is True:
                active_battery_systems += 1
        demand = result * active_battery_systems * 2500 * 0.01

        array = [time.clock()]
        for data in dynamic_data_val:
            array.append(data[1])

        array.append(array[1]+array[2]+array[3])
        array.append(demand)
        power_chart_data.append(array)

        if len(power_chart_data) > (chart_display_range * 60 / (self.UpdateCycle_slow / 1000)):
            power_chart_data.pop(1)

        return str(power_chart_data)

    @cherrypy.expose
    def DrawChart4(self):
        '''
        # define variables
        global database_connection, voltage_chart_data, chart_display_range
        dynamic_data_val = []

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
        cursor = database_connection.cursor()

        cursor.execute(
            "SELECT system_name, battery_voltage FROM battery_system_dynamic_data ORDER BY system_name ASC")
        dynamic_data_val.extend(cursor.fetchall())

        cursor.close()

        array = [time.clock()]
        for data in dynamic_data_val:
            array.append(data[1])

            voltage_chart_data.append(array)

        if len(voltage_chart_data) > (chart_display_range * 60 / (self.UpdateCycle_slow / 1000)):
            voltage_chart_data.pop(1)
        '''
        return str(voltage_chart_data)

    @cherrypy.expose
    def DrawChart5(self):

        # define variables
        global database_connection, delta_voltage_chart_data, chart_display_range
        dynamic_data_val = []

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
        cursor = database_connection.cursor()

        cursor.execute(
            "SELECT system_name, battery_delta_cell_voltage FROM battery_system_dynamic_data ORDER BY system_name ASC")
        dynamic_data_val.extend(cursor.fetchall())

        cursor.close()

        array = [time.clock()]
        for data in dynamic_data_val:
            array.append(data[1])

            delta_voltage_chart_data.append(array)

        if len(delta_voltage_chart_data) > (chart_display_range * 60 / (self.UpdateCycle_slow / 1000)):
            delta_voltage_chart_data.pop(1)

        return str(delta_voltage_chart_data)

    @cherrypy.expose
    def ConnectBatterySystem(self, param=""):

        system_name = "Sys_" + param

        # define variables
        global database_connection

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        try:

            database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
            cursor = database_connection.cursor()

            cursor.execute("UPDATE battery_system_static_data SET system_active = %s WHERE system_name = %s;",
                           (True, system_name))
            database_connection.commit()

            cursor.close()

            return str(True)

        except Exception as exception:

            print exception
            return str(False)

    @cherrypy.expose
    def DisconnectBatterySystem(self, param=""):

        system_name = "Sys_" + param

        # define variables
        global database_connection

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        try:

            database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
            cursor = database_connection.cursor()

            cursor.execute("UPDATE battery_system_static_data SET system_active = %s WHERE system_name = %s;",
                           (False, system_name))
            database_connection.commit()

            cursor.close()

            return str(True)

        except Exception as exception:

            print exception
            return str(False)

    @cherrypy.expose
    def SetDebugLevel(self, param=""):

        system_name = "Sys_" + param[0]
        debug_level = int(param[1])

        # define variables
        global database_connection

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        try:

            database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
            cursor = database_connection.cursor()

            cursor.execute("UPDATE battery_system_static_data SET system_debug_level = %s WHERE system_name = %s;",
                           (debug_level, system_name))
            database_connection.commit()

            cursor.close()

            return str(True)

        except Exception as exception:

            print exception
            return str(False)

    @cherrypy.expose
    def AddBatterySystems(self):

        # define variables
        global database_connection

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        try:

            database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
            cursor = database_connection.cursor()

            cursor.execute("UPDATE system_dynamic_data SET webserver_request = %s, webserver_last_request_update = %s "
                           "WHERE system_name = %s;", (SystemState_Update, datetime.datetime.now(), "Server"))
            database_connection.commit()

            cursor.close()

            return str(True)

        except Exception as exception:

            print exception
            return str(False)

    @cherrypy.expose
    def StartScenario(self):

        # define variables
        global database_connection

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        try:

            database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
            cursor = database_connection.cursor()

            cursor.execute("UPDATE system_dynamic_data SET webserver_request = %s, webserver_last_request_update = %s "
                           "WHERE system_name = %s;", (SystemState_Scenario, datetime.datetime.now(), "Server"))
            database_connection.commit()

            cursor.close()

            return str(True)

        except Exception as exception:

            print exception
            return str(False)

    @cherrypy.expose
    def ExportDatabaseEntries(self):

        # define variables
        global database_connection

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        try:

            archive_data = []
            array = []

            database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
            cursor = database_connection.cursor()

            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'battery_system_data_archive'")
            table_names = cursor.fetchall()

            for table_name in table_names:
                array.append(str(table_name[0]))
            archive_data.append(array)

            cursor.execute("SELECT * FROM battery_system_data_archive;")
            archive_data.extend(cursor.fetchall())

            cursor.close()

            path = "C:\\Users\\sz1t91\\Desktop"

            current_time = datetime.datetime.now()
            year = str(current_time.year)
            month = str(current_time.month)
            day = str(current_time.day)
            hour = str(current_time.hour)
            minute = str(current_time.minute)
            second = str(current_time.second)
            export_time = year + "_" + month + "_" + day + "-" + hour + "_" + minute + "_" + second + "_"

            filename = "\\" + export_time + "_BatterySystem_DataArchive.txt"
            file = open(path + filename, 'w')

            for data in archive_data:
                for element in data:
                    file.write(str(element)+"\t")
                file.write("\n")
            file.close()

            return str(True)

        except Exception as exception:

            print exception
            return str(False)

    @cherrypy.expose
    def SetDemand(self, param=""):

        demand = param

        # define variables
        global database_connection

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        try:

            database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
            cursor = database_connection.cursor()

            cursor.execute("UPDATE system_dynamic_data "
                           "SET webserver_demand = %s "
                           "WHERE system_name = %s;", (demand, "Server"))
            database_connection.commit()

            cursor.close()

            return str(True)

        except Exception as exception:

            print exception
            return str(False)

    @cherrypy.expose
    def ChangeMode(self, param=""):

        # define variables
        global database_connection
        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"
        database_connection = psycopg2.connect(dbname=database_name, user=database_user,
                                               password=database_password)
        cursor = database_connection.cursor()

        if param == "Auto":

            try:

                cursor.execute(
                    "UPDATE system_dynamic_data SET webserver_request = %s, webserver_last_request_update = %s "
                    "WHERE system_name = %s;", (SystemState_Standby, datetime.datetime.now(), "Server"))
                database_connection.commit()

            except Exception as exception:

                print exception
                return str(False)

        else:

            try:

                database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
                cursor = database_connection.cursor()

                cursor.execute(
                    "UPDATE system_dynamic_data SET webserver_request = %s, webserver_last_request_update = %s "
                    "WHERE system_name = %s;", (SystemState_ManualMode, datetime.datetime.now(), "Server"))
                database_connection.commit()

            except Exception as exception:

                print exception
                return str(False)

        cursor.close()

        return str(True)

    @cherrypy.expose
    def Shutdown(self):

        # define variables
        global database_connection

        database_name = "2ndLife"
        database_user = "postgres"
        database_password = "Opel2ndLife"

        try:

            database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
            cursor = database_connection.cursor()

            cursor.execute("UPDATE system_dynamic_data SET webserver_request = %s, webserver_last_request_update = %s "
                           "WHERE system_name = %s;", (SystemState_Shutdown, datetime.datetime.now(), "Server"))
            database_connection.commit()

            cursor.close()

            return str(True)

        except Exception as exception:

            print exception
            return str(False)

    @cherrypy.expose
    def index(self, param=""):

        self.html = ""
        self.html += """<!DOCTYPE html>"""
        self.html += """<!--"""
        self.html += """	Template MMA"""
        self.html += """-->"""
        self.html += """<html>"""
        self.html += """	<head>"""
        self.html += """		<title>Traffic Monitoring</title>"""
        self.html += """		<meta charset="utf-8" />"""
        self.html += """		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />"""
        self.html += """		<!--[if lte IE 8]><script src="js/ie/html5shiv.js"></script><![endif]-->"""
        self.html += """		<link rel="stylesheet" href="css2/main.css" />"""
        self.html += """		<!--[if lte IE 9]><link rel="stylesheet" href="css2/ie9.css" /><![endif]-->"""
        self.html += """		<!--[if lte IE 8]><link rel="stylesheet" href="css2/ie8.css" /><![endif]-->"""
        self.html += """        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>\n"""
        self.html += """        <script type="text/javascript" src="%s"></script>\n"""  % self.JAVA
        self.html += """        <link rel="stylesheet" href = "%s">\n"""  % self.CSS
        self.html += """</head>\n"""

        self.html += """	<body>"""  #
        # cyclic calls for status updates (Server connection)
        self.html += """<script>\n"""
        self.html += """ cyclicCall(%s);\n""" % self.UpdateCycle_fast
        self.html += """</script>\n"""
        self.html += """<script>\n"""
        self.html += """ cyclicCallslow(%s);\n""" % self.UpdateCycle_slow
        self.html += """</script>\n"""
        # end of cyclic call
        self.html += """		<!-- Wrapper -->"""
        self.html += """			<div id="wrapper">"""
        self.html += """"""
        self.html += """				<!-- Main -->"""
        self.html += """					<div id="main">"""
        self.html += """						<div class="inner">"""
        self.html += """"""
        self.html += """							<!-- Header -->"""
        self.html += """								<header id="header">"""
        self.html += """									<a href="index.html" class="logo"><strong>Traffic Monitoring</strong> Bahnhofstraße</a>"""
        self.html += """									<ul class="icons">"""
        self.html += """										<li><a href="#" class="icon fa-twitter"><span class="label">Twitter</span></a></li>"""
        self.html += """										<li><a href="#" class="icon fa-facebook"><span class="label">Facebook</span></a></li>"""
        self.html += """										<li><a href="#" class="icon fa-snapchat-ghost"><span class="label">Snapchat</span></a></li>"""
        self.html += """										<li><a href="#" class="icon fa-instagram"><span class="label">Instagram</span></a></li>"""
        self.html += """										<li><a href="#" class="icon fa-medium"><span class="label">Medium</span></a></li>"""
        self.html += """									</ul>"""
        self.html += """								</header>"""
        self.html += """"""
        self.html += """							<!-- Banner -->"""
        self.html += """								<section id="banner">"""
        self.html += """									<div class="content">"""
        self.html += """										<header>"""
        self.html += """											<h1>Traffic Monitoring Web Server</h1>"""
        self.html += """											<p>Developer / Maintenance Mode</p>"""
        self.html += """										</header>"""
        self.html += """										<p>This is currently a demonstration project to show the possibilties of the web server</p>"""
        #self.html += """										<ul class="actions">"""
        #self.html += """											<li><a href="#" class="button big">Learn More</a></li>"""
        #self.html += """										</ul>"""
        self.html += """									</div>"""
        #self.html += """									<span class="image object">"""
        #self.html += """										<img src="images/2016-chevrolet-volt-battery.jpg" alt="" />"""
        #self.html += """									</span>"""
        self.html += """								</section>"""
        self.html += """"""
        self.html += """							<!-- Section -->"""

        # Display system data
        self.html += """								<section>"""
        self.html += """									<header class="major">"""
        self.html += """										<h2>Calibration values</h2>"""
        self.html += """									</header>"""
        self.html += """									<div class="features">"""

        #SQL_Data = get_dynamic_system_data()

        self.html += """										<article>"""
        self.html += """											<span class="image object">"""
        self.html += """												<img id="Pic" src="images/car-black-right.png" alt="" style="width:100px"/>"""
        #self.html += """												<meter optimum="50" high="49" low="35" min="0" max="100" id ="Meter" value="%s"></meter>"""# % (SQL_Data[1][3])
        self.html += """											</span>"""
        self.html += """											<!--<span class="icon fa-paper-plane"></span>-->"""
        self.html += """											<div class="content">"""
        self.html += """												<h3 id ="TrafficCounter">%s</h3>"""% Traffic.TrafficCounter# % (SQL_Data[1][0])
        self.html += """												<p id ="State">State: %s</p>"""% Traffic.DetectionStatus# % (SQL_Data[1][1])
        self.html += """												<p id ="DirectionDetection">%s</p>"""% Traffic.direction# % (SQL_Data[1][3])
        self.html += """											</div>"""
        self.html += """										</article>"""
        self.html += """										<article>"""
        self.html += """											<span class="image object">"""
        self.html += """												<img id="ServerConnectionStatus" src="images/security-camera-black.png" alt="" style="width:100px" />"""
        self.html += """											</span>"""
        self.html += """											<!--<span class="icon fa-signal"></span>-->"""
        self.html += """											<div class="content">"""
        self.html += """												<h3>Camera Status</h3>"""
        self.html += """												<p id="DatabaseConnectionStatusText"></p>"""
        self.html += """											</div>"""
        self.html += """										</article>"""
        '''self.html += """										<article>"""
        self.html += """											<div class="content">"""
        self.html += """												<h3>Voltage</h3>"""
        self.html += """												<p id="VoltageChart"></p>"""
        self.html += """											</div>"""
        self.html += """										</article>"""
        self.html += """										<article>"""
        self.html += """											<div class="content">"""
        self.html += """												<h3>Delta Cell Voltage</h3>"""
        self.html += """												<p id="DeltaVoltageChart"></p>"""
        self.html += """											</div>"""
        self.html += """										</article>"""
        self.html += """										<article>"""
        self.html += """											<div class="content">"""
        self.html += """												<h3>SoC</h3>"""
        self.html += """												<p id="PerformanceChart"></p>"""
        self.html += """											</div>"""
        self.html += """										</article>"""
        self.html += """										<article>"""
        self.html += """											<div class="content">"""
        self.html += """												<h3>Current</h3>"""
        self.html += """												<p id="CurrentChart"></p>"""
        self.html += """											</div>"""
        self.html += """										</article>"""
        self.html += """										<article>"""
        self.html += """											<div class="content">"""
        self.html += """												<h3>Power</h3>"""
        self.html += """												<p id="PowerChart"></p>"""
        self.html += """											</div>"""
        self.html += """										</article>"""
        '''
        self.html += """									</div>"""

        # Display battery system data
        '''self.html += """									<header class="major">"""
        self.html += """										<h2>Demonstrator Battery System Overview</h2>"""
        self.html += """									</header>"""
        self.html += """									<div class="features">"""
        self.html += BatStatus(self)
        self.html += """									</div>"""
        
        # Display system tasks
        self.html += """									<header class="major">"""
        self.html += """										<h2>System Tasks</h2>"""
        self.html += """									</header>"""
        self.html += """									<div class="features">"""
        self.html += """										<article>"""
        self.html += """											<div class="content">"""
        self.html += """												<h3>System tasks</h3>"""
        self.html += """										        <div>"""
        self.html += """                                                    <button type="button" id="Add" onclick="add_battery_systems()">Add battery systems</button>"""
        self.html += """										        </div>"""
        self.html += """										        <div>"""
        self.html += """                                                    <button type="button" id="Sce" onclick="start_scenario()">Start scenario</button>"""
        self.html += """										        </div>"""
        self.html += """										        <div>"""
        self.html += """                                                    <button type="button" id="Exp" onclick="export_database_entries()">Export database</button>"""
        self.html += """										        </div>"""
        self.html += """										        <div>"""
        self.html += """                                                    <button type="button" id="Shut" onclick="shutdown()">Shutdown system</button>"""
        self.html += """										        </div>"""
        self.html += """											</div>"""
        self.html += """										</article>"""
        self.html += """										<article>"""
        self.html += """											<div class="content">"""
        self.html += """												<h3>System demand</h3>"""
        self.html += """										        <div class="toggle-buttons">"""
        self.html += """												    <h4>Change mode</h3>"""
        self.html += """										            <input type="radio" id="b1" name="group-b" onclick="change_mode()" checked="true">"""
        self.html += """										            <label for="b1">Auto</label>"""
        self.html += """										            <input type="radio" id="b2" name="group-b" onclick="change_mode()">"""
        self.html += """                                                    <label for="b2">Manual</label>"""
        self.html += """										        </div>"""
        self.html += """										        <div>"""
        self.html += """												    <h4>Set demand</h3>"""
        self.html += """										            <input type="text" id="Demand" disabled="disabled" value="0"></input>"""
        self.html += """                                                    <button type="button" id="Set" onclick="set_demand()" disabled="disabled">Set demand</button>"""
        self.html += """										        </div>"""
        self.html += """											</div>"""
        self.html += """										</article>"""
        self.html += """									</div>"""

        # Display system error log
        self.html += """									<header class="major">"""
        self.html += """										<h2>System Errors</h2>"""
        self.html += """									</header>"""
        self.html += """									<div class="features">"""
        self.html += """										<article>"""
        self.html += """											<div class="major">"""
        self.html += """												<h3>Error log</h3>"""
        self.html += """												<p id="ErrorLogTable"></p>"""
        self.html += """											</div>"""
        self.html += """										</article>"""
        self.html += """									</div>"""
        '''
        self.html += """								</section>"""
        self.html += """							"""
        self.html += """						</div>"""
        self.html += """					</div>"""
        self.html += """"""
        self.html += """				<!-- Sidebar -->"""
        self.html += """					<div id="sidebar">"""
        self.html += """						<div class="inner">"""
        self.html += """"""
        self.html += """							<!-- Search -->"""
        self.html += """								<section id="search" class="alt">"""
        self.html += """									<form method="post" action="#">"""
        self.html += """										<input type="text" name="query" id="query" placeholder="Search" />"""
        self.html += """									</form>"""
        self.html += """								</section>"""
        self.html += """"""
        self.html += """							<!-- Menu -->"""
        self.html += """								<nav id="menu">"""
        self.html += """									<header class="major">"""
        self.html += """										<h2>Menu</h2>"""
        self.html += """									</header>"""
        self.html += """									<ul>"""
        self.html += """										<li><a href="index.html">Homepage</a></li>"""
        self.html += """										<li><a href="generic.html">Generic</a></li>"""
        self.html += """										<li><a href="elements.html">Elements</a></li>"""
        self.html += """										<li>"""
        self.html += """											<span class="opener">Submenu</span>"""
        self.html += """											<ul>"""
        self.html += """												<li><a href="#">Lorem Dolor</a></li>"""
        self.html += """												<li><a href="#">Ipsum Adipiscing</a></li>"""
        self.html += """												<li><a href="#">Tempus Magna</a></li>"""
        self.html += """												<li><a href="#">Feugiat Veroeros</a></li>"""
        self.html += """											</ul>"""
        self.html += """										</li>"""
        self.html += """										<li><a href="#">Adipiscing</a></li>"""
        self.html += """										<li>"""
        self.html += """											<span class="opener">Another Submenu</span>"""
        self.html += """											<ul>"""
        self.html += """												<li><a href="#">Lorem Dolor</a></li>"""
        self.html += """												<li><a href="#">Ipsum Adipiscing</a></li>"""
        self.html += """												<li><a href="#">Tempus Magna</a></li>"""
        self.html += """												<li><a href="#">Feugiat Veroeros</a></li>"""
        self.html += """											</ul>"""
        self.html += """										</li>						"""
        self.html += """									</ul>"""
        self.html += """								</nav>"""
        self.html += """"""
        self.html += """							<!-- Section -->"""
        self.html += """								<section>"""
        self.html += """									<header class="major">"""
        self.html += """										<h2>Latest News</h2>"""
        self.html += """									</header>"""
        self.html += """									<div class="mini-posts">"""
        #self.html += """										<article>"""
        #self.html += """											<a href="http://elsa-h2020.eu/"" class="image"><img src="images/logo_elsa.png" alt="" /></a>"""
        #self.html += """											<p></p>"""
        #self.html += """											"""
        #self.html += """										</article>"""
        self.html += """										<article>"""
        self.html += """											<a href="https://github.com/MichaelMausbach/TrafficDetection" class="image"><img src="images/github.png" alt="" /></a>"""
        self.html += """											<p>My development area on github</p>"""
        self.html += """										</article>"""
        self.html += """									</div>"""
        self.html += """									<ul class="actions">"""
        self.html += """										<li><a href="#" class="button">More</a></li>"""
        self.html += """									</ul>"""
        self.html += """								</section>"""
        self.html += """"""
        self.html += """							<!-- Section -->"""
        self.html += """								<section>"""
        self.html += """									<header class="major">"""
        self.html += """										<h2>Get in touch</h2>"""
        self.html += """									</header>"""
        self.html += """									<p>In case you need additional support or any information about this project, please contact Michael Mausbach</p>"""
        self.html += """									<ul class="contact">"""
        self.html += """										<li class="fa-envelope-o"><a href="#">Mausbach.Michael@googlemail.com</a></li>"""
        self.html += """										<li class="fa-phone">(49) 178 5014774</li>"""
        self.html += """										<li class="fa-home"> Michael Mausbach <br/>"""
        self.html += """										Bahnhofstr. 14<br />"""
        self.html += """										65611 Brechen</li>"""
        self.html += """									</ul>"""
        self.html += """								</section>"""
        self.html += """"""
        self.html += """							<!-- Footer -->"""
        self.html += """								<footer id="footer">"""
        self.html += """									<p class="copyright">&copy; Design: <a href="https://html5up.net">HTML5 UP</a>.</p>"""
        self.html += """								</footer>"""
        self.html += """"""
        self.html += """						</div>"""
        self.html += """					</div>"""
        self.html += """"""
        self.html += """			</div>"""
        self.html += """"""
        self.html += """		<!-- Scripts -->"""
        self.html += """			<script src="js/jquery.min.js"></script>"""
        self.html += """			<script src="js/skel.min.js"></script>"""
        self.html += """			<script src="js/util.js"></script>"""
        self.html += """			<!--[if lte IE 8]><script src="js/ie/respond.min.js"></script><![endif]-->"""
        self.html += """			<script src="js/main.js"></script>"""
        self.html += """"""

        self.html += """	</body>"""
        self.html += """</html>"""
        return self.html

def BatStatus(self):

    # define variables
    html = ""
    counter = 1

    try:

        #SQL_Data = Fill_SQL_Data_Array()
        SQL_Data = get_dynamic_battery_system_data()

        for data in SQL_Data[1:]:
            html += """										<article>"""
            html += """											<span class="image object">"""
            html += """												<img id="Pic_%s" src="images/battery-grey-512x512.png" alt="" style="width:100px" />""" % (counter)
#            html += """												<img src="images/battery-512x512.png" alt="" style="width:100px" />"""

            html += """												<meter optimum="50" high="49" low="35" min="0" max="100" id ="Met_%s" value="%s"></meter>""" % \
                    (counter, data[3])
            html += """											</span>"""
            html += """											<!--<span class="icon fa-paper-plane"></span>-->"""
            html += """											<div class="content">"""
            html += """												<h3 id ="Bat_%s">%s</h3>""" % \
                    (counter, data[0])
            html += """												<p  id ="Sta_%s">Phase %s</p>""" % \
                    (counter, data[2])
            html += """												<p  id ="Val_%s">%s</p>""" % \
                    (counter, data[3])
            html += """											</div>"""
            html += """											<div class "content">"""
            html += """                                             <button type="button" id="Dis_%s" onclick="set_system_active(%s)">Connect</button>""" % (counter, counter)
            html += """											    <form action="#">"""
            html += """												    <label>Debug level:"""
            html += """													    <select name="Deb_%s" onchange="set_debug_level(%s, this.value)">""" % (counter, counter)
            html += """														    <option value="0">0</option>"""
            html += """														    <option value="1">1</option>"""
            html += """														    <option value="2">2</option>"""
            html += """														    <option value="3">3</option>"""
            html += """														    <option value="4">4</option>"""
            html += """														    <option value="5">5</option>"""
            html += """														    <option value="6">6</option>"""
            html += """													    </select>"""
            html += """												    </label>"""
            html += """											    </form>"""
            html += """											</div>"""
            html += """										</article>"""
            counter += 1

        return html

    except Exception as exception:

        print exception


def FetchDatabaseStatus():

    # define variables
    global database_connection
    global dynamic_data
    global static_data_val
    global dynamic_data_val

    database_name = "2ndLife"
    database_user = "postgres"
    database_password = "Opel2ndLife"

    database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
    cursor = database_connection.cursor()

    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'battery_system_dynamic_data'")
    dynamic_data.extend(cursor.fetchall())

    cursor.execute("SELECT * FROM battery_system_dynamic_data")
    dynamic_data_val.extend(cursor.fetchall())

    cursor.close()


def get_dynamic_battery_system_data():

    # define variables
    global database_connection
    static_data_val = []
    dynamic_data_val = []
    array2 = [["system_name", "system_active", "grid_phase", "battery_state_of_charge"]]

    database_name = "2ndLife"
    database_user = "postgres"
    database_password = "Opel2ndLife"

    database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
    cursor = database_connection.cursor()

    cursor.execute("SELECT system_name, system_active, grid_phase FROM battery_system_static_data ORDER BY system_name ASC")
    static_data_val.extend(cursor.fetchall())

    cursor.execute("SELECT system_name, battery_state_of_charge FROM battery_system_dynamic_data ORDER BY system_name ASC")
    dynamic_data_val.extend(cursor.fetchall())

    cursor.close()

    for data in static_data_val:
        array = []
        for i in range(len(data)):
            array.append(str(data[i]))
        array2.append(array)

    for data in dynamic_data_val:
        for data2 in array2:
            if data[0] == data2[0]:
                data2.append(str(data[1]))
                continue

    return array2


def get_dynamic_system_data():

    # define variables
    global database_connection
    static_data_val = []
    dynamic_data_val = []
    array2 = [["system_name", "system_state", "system_demand", "state_of_charge"]]

    database_name = "2ndLife"
    database_user = "postgres"
    database_password = "Opel2ndLife"

    database_connection = psycopg2.connect(dbname=database_name, user=database_user, password=database_password)
    cursor = database_connection.cursor()

    cursor.execute("SELECT system_name, system_state, system_demand, state_of_charge FROM system_dynamic_data")
    dynamic_data_val.extend(cursor.fetchall())

    cursor.close()

    for data in dynamic_data_val:
        array = []
        for i in range(len(data)):
            array.append(str(data[i]))
        array2.append(array)

    # evaluate system state
    if array2[1][1] == str(SystemState_Initialize):
        array2[1][1] = "Initialize"
    elif array2[1][1] == str(SystemState_Update):
        array2[1][1] = "Update"
    elif array2[1][1] == str(SystemState_Connect):
        array2[1][1] = "Connect"
    elif array2[1][1] == str(SystemState_Standby):
        array2[1][1] = "Standby"
    elif array2[1][1] == str(SystemState_Charge):
        array2[1][1] = "Charge"
    elif array2[1][1] == str(SystemState_Discharge):
        array2[1][1] = "Discharge"
    elif array2[1][1] == str(SystemState_Fault):
        array2[1][1] = "Fault"
    elif array2[1][1] == str(SystemState_Scenario):
        array2[1][1] = "Scenario"
    elif array2[1][1] == str(SystemState_ManualMode):
        array2[1][1] = "Manual Mode"
    elif array2[1][1] == str(SystemState_Shutdown):
        array2[1][1] = "Shutdown"

    return array2


def Fill_SQL_Data_Array():

    global dynamic_data
    global static_data_val
    global dynamic_data_val

    # define variables
    array = []
    array.append(dynamic_data)

    for i in range(len(dynamic_data_val)):
        array.append(dynamic_data_val[i])
    Dataarray2 = []
    for i in range(len(array)):
        Dataarray = []
        # 0 = system_name 9 = inverter_identifier 12 = battery_voltage 14 = battery_state_of_charge
        for x in [0,8,11,13]:
            if i >= 1 and x in [8,11,13]:
                a = array[i][x]
                Dataarray.append(float(a))
            else:
                a = array[i][x]
                a = str(a).replace("('", "")
                a = str(a).replace("',)", "")
                Dataarray.append(a)
        Dataarray2.append(Dataarray)
    return Dataarray2


def Fill_SQL_Data_Array2():

    # define variables
    array = []

    for a in [8, 11, 13]:
        array = []
        array.append(time.clock())
        for i in range(len(dynamic_data_val)):
            #print i, a, dynamic_data_val[i][a],str(int(dynamic_data_val[i][a])+ (random.random() * 20)) #todo-michael: remove random when getting productive
            array.append(int(dynamic_data_val[i][a])+ (random.random() * 20))#todo-michael: remove random part when getting productive
    return array


host_address = socket.gethostbyname(socket.gethostname())
host_port = 5810

B2L_WebServer = Cherrypy_Init(address=host_address, port=host_port)
WebServer_Obj = B2L_WebServer.start()

camera=OfflineVideo()
Traffic.TrafficDetection(camera)
#print Traffic.TrafficCounter