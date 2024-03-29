# -*- coding: utf-8 -*-
"""INVENTARIO.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C7gLTjlO0i0RrSDUvP3hZvXy2ddJPrnT
"""

import simpy
import numpy as np
def warehouse_run(env, order_cutoff, order_target): #FUNCIONAMIENTO DEL DEPOSITO TOMANDO 3 ARGUMENTOS, ENV PARA EL ENTORNO DE LA SIMULACION
    global inventory, balance, num_oredered    # order_cutoff es para el punto de reorden y order_target cantidad objetivo  # Se inicializan como variables globales
    inventory = order_target
    balance = 0.0
    num_ordered = 0
    while True:
        interarrival=generate_interarrival()  #Genera un tiempo de llegada
        yield env.timeout(interarrival) #Se espera el tiempo obtenido en interarrivañ
        balance -=  inventory*2*interarrival  # Se actualiza el saldo restando el costo de mantener el inventario en el almacen ese tiempo
        demand=generate_demand()  #genera una demanda entre 1 y 5
        """ Si la demanda es menor que el inventario actual, se venden los productos correspondientes y se actualiza el saldo y el inventario.
        Si la demanda es mayor o igual al inventario, se venden todos los productos disponibles y se muestra un mensaje indicando que no hay suficiente inventario."""
        if demand < inventory:
            balance += 100*demand
            inventory-=demand
            print('{:.2f} sold {}'.format(env.now,demand))
        else:
            balance += 100*inventory
            inventory =0
            print('{:.2f} Sold {} (out fo stock)'.format(env.now,inventory))
        """Si el inventario es menor que el punto de reorden (order_cutoff) y no hay pedidos en proceso, se llama a la función handle_order para realizar un pedido."""
        if inventory< order_cutoff and num_ordered==0:
            env.process(handle_order(env, order_target))
####
"""Simula el proceso de realizar un pedido. Se calcula la cantidad de productos a pedir (num_ordered), se actualiza el saldo y se espera un tiempo de 2.0 unidades(dias) utilizando env.timeout(2.0).
 Luego, se recibe el pedido, se actualiza el inventario y se muestra un mensaje indicando que el pedido ha sido recibido."""
def handle_order(env,order_target):
    global inventory,balance, num_ordered
    num_ordered = order_target -inventory
    print('{:.2f} Place order for {}'.format(env.now,num_ordered))
    balance -= 50*num_ordered
    yield env.timeout(2.0)
    inventory +=  num_ordered
    num_ordered = 0
    print('{:.2f} Received order {} in inventory'.format(env.now,inventory))
#Genera valores aleatorios para el tiempo de llegada entre pedidos
def generate_interarrival():
    return np.random.exponential(1./5)
#Genera valores aletorios de la demanda
def generate_demand():
    return np.random.randint(1,5)

#Listas para almacenar datos de observacion
obs_time = []
inventory_level = []
"""Observe se encarga de registrar los datos de observacion en las listas mencionadas anteriormente.
En un bucle infinito, se añade el tiempo actual (env.now) a obs_time y el nivel de inventario actual a inventory_level.
Luego, se espera un tiempo de 0.1 unidades utilizando env.timeout(0.1)."""
def observe(env):
    global inventory
    while True:
        obs_time.append(env.now)
        inventory_level.append(inventory)
        yield env.timeout(0.1)
#SEMILLA ALEATORIA
np.random.seed(0)
#SIMULACION
env = simpy.Environment()
#Crean dos procesos en el entorno de simulacion
env.process(warehouse_run(env,10,30))
env.process(observe(env))
#Se ejecuta la simulacion hasta un tiempo de 5 unidades utilizando
env.run(until=5.0)
#Se muestra un gráfico paso a paso (plt.step()) que representa el nivel de inventario en funcion del tiempo utilizando los datos almacenados en obs_time e inventory_level.
import matplotlib.pyplot as plt
plt.figure()
plt.step(obs_time, inventory_level, where = 'post')
plt.xlabel('Simulation time (days)')
plt.ylabel('Inventory level')

pip install simpy