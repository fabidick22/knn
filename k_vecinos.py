# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import seaborn
import os
import math
import pandas as pd

class knn:
    muestraBase=[]
    source="test.csv"
    df=None

    def saveData(self, dataFrame):
        dataFrame['class']=dataFrame.apply(lambda row: self.clearData(row['class']), axis=1)
        dataFrame.to_csv(self.source, index=False)
        self.loadData()

    def loadData(self):
        self.df=pd.read_csv(self.source)

    def createTuple(self, col1, col2, colClass):
        self.muestraBase.append((((col1,col2), colClass)))

    def clearData(self, colClass):
        da=colClass
        da=str(da)
        if(da[0:4]=="add="):
            return colClass[4:]
        else:
            return colClass

    def showData(self, edit=False, dataF=None):
        print(self.df)
        seaborn.set()
        if(edit):
            s=seaborn.lmplot('col1', 'col2', data=dataF, fit_reg=False, hue="class",
                       scatter_kws={"marker": "D", "s": 100})
        else:
            s=seaborn.lmplot('col1', 'col2', data=self.df, fit_reg=False, hue="class",
                       scatter_kws={"marker": "D", "s": 100})
        s.set_axis_labels("X", "Y")
        plt.show()


    # second algorith
    def euclideanDistancia(self, instance1, instance2, length=2):
        """
        :param instance1: vector 1 para calcular distncia
        :param instance2: vector 2 para calcular distncia
        :param length: tamaño de los vectores
        :return: retorno de la distancia entre los dos puntos
        """
        distance = 0
        for x in range(length):
            distance += pow((instance1[x] - instance2[x]), 2)
        return math.sqrt(distance)


    def get_class(self, smuestra, k_neighbours, muestra_entrenada, p):
        """
        Extrae la clase correcta en función de la maxima cantidad de vecinos a mínima distancia de la muestra de test,
        a igualdad de vecinos mínimos, se calcula por mínima distancia.
        Se asumen parámetros correctamente introducidos.
        :param smuestra: muestra de test a clasificar
        :param k_neighbours: k vecinos a menor distancia de la muestra smuestra
        :param muestra_entrenada: muestras de entrenamiento en caso de que se requiera desempate
        :param p: indicador de la distancia a emplear según la familia Lp
        :return: retorna la clase a la que meternece la muestra
        """
        hash_neigh = {}
        for k_neigh in k_neighbours:
            if k_neigh[0][1] not in hash_neigh:
                hash_neigh[k_neigh[0][1]] = 1
            else:
                hash_neigh[k_neigh[0][1]] += 1
        c_max = max(hash_neigh, key=hash_neigh.get)
        # Si hay alguna otra clase con el mismo número de vecinos, desempatar con el vecino de menor distancia entre las
        # clases y la muestra #
        c_equals = [c_max]
        for key in hash_neigh:
            if hash_neigh[key] == c_max: c_equals.append(key)
        min_distance = float('inf')
        for cls in c_equals:
            for v in muestra_entrenada:
                if v[1] == cls:
                    dist = self.euclideanDistancia(smuestra, v[0])
                    if dist < min_distance: min_distance, c_max = dist, cls
        return c_max


    def algorithKnn(self, muestra_test, muestra_entrenada, k, p):
        """
        Clasifica las muestras de test en funcion de las muestras de entrenamiento.
        Se asumen parámetros correctamente introducidos.
        :param muestra_test: muestras a clasificar
        :param muestra_entrenada: prototipos iniciales (muestras de entrenamiento ya clasificadas)
        :param k: nº de vecinos a emplear en el clasificador
        :param p: indicador de la distancia a emplear según la familia Lp
        :return: retorna la clase de la muestra
        """
        for stest in muestra_test:
            k_neigh = []
            for sentrenada in muestra_entrenada:
                # Si los k-vecinos aun no se han rellenado, llenarlos. #
                if len(k_neigh) < k:
                    k_neigh.append([sentrenada, self.euclideanDistancia(stest, sentrenada[0], p)])
                # Si ya hay k-vecinos seleccionados, mirar si mejora la distancia en comparación al vecino con máxima distancia. #
                else:
                    dist = self.euclideanDistancia(stest, sentrenada[0], p)
                    m = max(k_neigh, key=lambda x: x[1])
                    if dist < m[1]: k_neigh[k_neigh.index(m)] = [sentrenada, dist]
            respose=self.get_class(stest, k_neigh, muestra_entrenada, p)
            print("Muestra", stest, "clasificada en la clase", str(respose))
            print("\n" * 2)
            return respose


    def menu(self):
        self.loadData()
        print("\n" * 2)
        menu = {}
        menu['1'] = "Mostrar Datos."
        menu['2'] = "Ingresar Datos"
        menu['3'] = "Exit"
        while True:
            options = menu.keys()
            options.sort()
            for entry in options:
                print entry, menu[entry]

            selection = raw_input("Ingrese la Opcion:")
            if selection == '1':
                print("\n"*100)
                self.showData()
                print("\n" * 2)
            elif selection == '2':
                print("\n" * 100)
                self.df.apply(lambda row: self.createTuple(row['col1'], row['col2'], row['class']), axis=1)
                listMuestras=[]
                (muestraNueva)=input("\n Ingrese valores x,y (separados por coma):")
                kVecinos=input("\n Ingrese valores para (K):")
                listMuestras.append(muestraNueva)
                res=self.algorithKnn(listMuestras, self.muestraBase, kVecinos,2)

                graficar=list(muestraNueva)
                graficar.append("add="+str(res))

                df2 = pd.DataFrame([graficar], columns=('col1', 'col2', 'class'))
                res = self.df.append(df2, ignore_index=False, verify_integrity=False)
                self.showData(True, res)
                self.saveData(res)
            elif selection == '3':
                break
            else:
                print ("Option Error!")

    def main(self):
        if __name__ == "__main__":
            self.menu()

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
clear()
knn().main()