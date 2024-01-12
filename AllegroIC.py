""" 

Autora: Daniela Feoli Grant
Creación: 09.01.2024

El siguiente código corresponde al problema a resolver para la entrevista técnica de 
Allegro Microsystems para el puesto de Test Engineer.
Clase llamada AlegroIC que simula la funcionalidad de los IC de Allegro para ajustar
la corriente mediante el método adjust_I.

"""

import random
import csv
import os
import matplotlib.pyplot as plt

"""
Objeto tipo AllegroIC que recibe como argumento el valor deseado de corriente.
"""
class AllegroIC:
    def __init__(self, targ_current:float):
        self.targ_current = targ_current
        
    def __str__(self):
        return f"Target current is: {self.targ_current}."


 # Método encargado del ajuste de la corriente inicial recibe como argumento un 
 # número entero que funciona de semilla para generar algún valor aleatorio de 
 # corriente inicial acotado entre 1 uA y 5 uA. Devuelve los valores de corriente
 # inicial y final, así como el valor del registro.
    def adjust_I(self, seed):
        self.seed = random.seed(seed)
        current = random.uniform(1e-6, 5e-6)
        current_init = current                        # Guarda la corriente inicial
        current_diff = self.targ_current - current

        print("La corriente inicial es: ", current_init)
        reg=0
        if -0.05e-6 < current_diff < 0.05e-6:
            reg += 1
            #print("La corriente es de",current," A.\nEl registro es:", reg)

        elif current_diff <= -0.05e-6:    
            reg = 8   
            while current_diff <= -0.05e-6 and reg <= 15:
                current = current - float(0.100e-6)
                current_diff = self.targ_current - current
                #print("Current diff first while: ",current_diff)
                reg += 1
            #print("La corriente es de",current," A.\nEl registro es:", reg-1)

        elif current_diff >= 0.05e-6: 
            reg = 1
            while current_diff >= 0.05e-6 and reg <= 7:
                current = current + float(0.100e-6)
                current_diff = self.targ_current - current
                #print("Current diff second while: ",current_diff)
                reg += 1
            #print("La corriente es de",current," A.\nEl registro es:", reg-1)

        return current_init, current, reg-1

    def save2csv(self,current_init,current,reg,filename:str):
        self.current_init = current_init
        self.current = current
        self.reg = reg
        self.filename = filename

        if not os.path.exists('./'+filename+'.csv'):
            with open(filename+'.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Corriente inicial (A)','Corriente final (A)','Valor del registro (decimal)', 'Valor del registro (binario)'])
        
        with open(filename+'.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_init,current,reg,bin(reg)])

aic1 = AllegroIC(2.5e-6)
seed_arr = range(0,9999,1)
init_arr = []
current_arr = []

for i in seed_arr:
    [init,current,reg]=aic1.adjust_I(i)
    aic1.save2csv(init,current,reg,'prueba_musaso')
    init_arr.append(init)
    current_arr.append(current)

plt.title('Histogramas')
plt.subplot(211)
plt.hist(init_arr,color='r')
plt.xlabel('Corriente inicial (A)')
plt.subplot(212)
plt.hist(current_arr,color='g')
plt.xlabel('Corriente final (A)')
plt.show()

