# -*- coding: utf-8 -*-
'''
1)Вбиваешь число
2)Вбиваешь номер разряда с ошибкой
3)Жмешь "Ок"
4)...
5)Profit!

В последний момент добавлена кнопка "Перевод", выводящая заданное число в двоичной форме.
'''
import math
import random
from Tkinter import *
import ttk
root = Tk()
root.title('Линейные блоковые коды')
root.geometry("650x620+60+80")

test = Label(root,text = 'Введите десятичное число < 32767:',font = "Arial 11")
test.place(x = 5,y = 22)
mistake_mess = Label(root,text = 'Введите разряд с ошибкой:',font = "Arial 11")
mistake_mess.place(x = 5,y = 50)

enter_number = ttk.Entry(root,width = 10)#Поля ввода
enter_number.place(x = 270,y = 25)
enter_number2 = ttk.Entry(root,width = 10)
enter_number2.place(x = 270,y = 53)

btn1 = ttk.Button(root,text="Ок")
btn1.place(x=350,y=53)
btn2 = ttk.Button(root,text="Перевод")
btn2.place(x=350,y=25)

def quit(event):
   root.destroy()

def caption(event):#Перевод числа в двоичную систему счисления
   a = int(enter_number.get())
   a = map(int, list(bin(a)[2:]))

   text_user_num = Label(root,font = "Arial 11",text = 'Ваше число в двоичной системе счисления: ')
   text_user_num.place(x = 5,y = 81)
   user_num = Label(root,font = "Arial 11",text = a)
   user_num.place(x = 320,y = 81)
   return a

def adding_of_unit_matrix(size, offset, matrix):#Добавление единичной матрицы
   pos_of_one = 0
   for k in xrange(size):
      for i in xrange(size):
         if pos_of_one == i:
            matrix[k].insert(i + offset,1)
         else:
            matrix[k].insert(i + offset,0)
      pos_of_one += 1
   return matrix

def find_1(matrix,offset):#поиск единиц в строке матрицы со смещением
   founded_index = []
   for i in xrange(len(matrix) - offset):
      if matrix[i] == 1:
         founded_index.append(i)
   return founded_index

def reverse_0_and_1(number):
   if number == 1:
      return 0
   else:
      return 1

def principal(event):
     main_frame=Frame(root,width=650,heigh=620)
     main_frame.place(x = 0,y = 80)

     k_dist = 2#Кол-во контрольных разрядов
     a = caption(event)
     m = len(a)#Определение размера единичной матрицы
     while not (k_dist >= math.log((m+k_dist+1), 2)):#расчет К для введенного числа
        k_dist += 1
     DandK = Label(root,font = "Arial 9",text = 'Dmin=3\nK=%s'%k_dist)
     DandK.place(x = 580,y = 30)

     if k_dist == 2:
        Matrix_M = [[1,1]]
     elif k_dist == 3:
        Matrix_M = [[0,1,1],[1,0,1],[1,1,0],[1,1,1]]
     elif k_dist == 4:
        Matrix_M = [[0,1,1,1],[0,0,1,1],[1,1,0,1],[0,1,1,0],[1,1,0,0],[1,0,0,1],[1,0,1,1],[1,1,1,0],[1,0,1,0],[0,1,0,1],[1,1,1,1]]
     else:
        Matrix_M = [[0,1,0,1,1],[0,1,1,1,0],[0,0,1,1,1],[1,1,0,1,0],[0,1,1,0,1],[0,0,1,1,0],[1,1,0,0,0],[0,1,0,0,1],[0,0,1,0,1],[1,0,0,1,1],[1,0,1,1,0],[1,1,1,0,0],[1,1,0,0,1],[1,0,1,0,1],[1,0,0,1,0]]
     Matrix_M = Matrix_M[:m]

     Matrix_M = adding_of_unit_matrix(m,k_dist,Matrix_M)
     for k in xrange(m):
        Matrix_M[k].reverse()
     Matrix_M.reverse()#Порождающая матрица
     Matrix_H = [[],[],[],[],[]]
     for k in xrange(k_dist):#Транспонирование контрольной подматрицы порождающей матрицы
        for i in xrange(m):
           Matrix_H[k].append(Matrix_M[i][m + k])
     Matrix_H = adding_of_unit_matrix(k_dist,m,Matrix_H)#Проверочная матрица

     E = []
     for j in xrange(k_dist):
        E.append(find_1(Matrix_H[j],k_dist))

     E_info_list = []
     for j in xrange(k_dist):#--------------------------------------------------кодирование
        E1 = 0
        det_str = 'E' + str(j+1) + ' = '#    Строка 'Ex ='
        for i in xrange(len(E[j])):
              E1 = E1 ^ a[E[j][i]]#Подсчет E для каждой строки
#              det_str = det_str + str(a[E[j][i]]) + '+'
              det_str = det_str + "a" + str((E[j][i])+1) + '+'
        a.append(E1)
        E_info_list.append(det_str[:len(det_str) - 1])#Список выводимых строк E'(для каждой строки убран последний "+")

     koded_num_text = Label(root,font = "Arial 11",text = 'Закодированное число:')
     koded_num_text.place(x = 5,y = 109)
     koded_num = Label(root,font = "Arial 11",text = a)
     koded_num.place(x = 250,y = 109)

     mistake = int(enter_number2.get())#Ошибочный разряд
     a[-mistake] = reverse_0_and_1(a[-mistake])#число а с ошибкой в заданном разряде

     S = []
     S_info_list = []
     for k in xrange(k_dist):#------------------------------------------------декодирование
        E1 = 0
        S_temp = 0
        S_temp = S_temp ^ a[len(a) - k_dist + k]
        dekode_str_S = 'S' + str(k+1) + ' = E` + E' + str(k+1) + ' = ' + str(a[len(a) - k_dist + k]) + '+'#    Строка 'Sx = E' + Ex ='
        for i in xrange(len(E[k])):
              E1 = E1 ^ a[E[k][i]]#Подсчет E' для каждой строки
              dekode_str_S = dekode_str_S + str(a[E[k][i]]) + '+'
        S_temp = S_temp ^ E1#    (E + E')
        S.append(S_temp)
        S_info_list.append(dekode_str_S[:len(dekode_str_S) - 1])#Список выводимых строк S(для каждой строки убран последний "+")
     S_str = 'Синдром S = ' + str(S)

     raz = 0
     '''Дорогой будущий я, у меня правда не было времени
      чтобы сделать распознование синдрома алгоритмически
      не ругайся на меня за эту громаду ифов'''
     if k_dist == 2:
        if S == [0,1]: raz = 1
        elif S == [1,0]: raz = 2
        elif S == [1,1]: raz = 3
     elif k_dist == 3:
        if S == [0,0,1]: raz = 1
        elif S == [0,1,0]: raz = 2
        elif S == [1,0,0]: raz = 3
        elif S == [1,1,0]: raz = 4
        elif S == [1,0,1]: raz = 5
        elif S == [0,1,1]: raz = 6
     elif k_dist == 4:
        if S == [0,0,0,1]: raz = 1
        elif S == [0,0,1,0]: raz = 2
        elif S == [0,1,0,0]: raz = 3
        elif S == [1,0,0,0]: raz = 4
        elif S == [1,1,1,0]: raz = 5
        elif S == [1,1,0,0]: raz = 6
        elif S == [1,0,1,1]: raz = 7
        elif S == [0,1,1,0]: raz = 8
        elif S == [0,0,1,1]: raz = 9
        elif S == [1,0,0,1]: raz = 10
        elif S == [1,1,0,1]: raz = 11
        elif S == [0,1,1,1]: raz = 12
        elif S == [0,1,0,1]: raz = 13
        elif S == [1,0,1,0]: raz = 14
        elif S == [1,1,1,1]: raz = 15
     elif k_dist == 5:
        if S == [0,0,0,0,1]: raz = 1
        elif S == [0,0,0,1,0]: raz = 2
        elif S == [0,0,1,0,0]: raz = 3
        elif S == [0,1,0,0,0]: raz = 4
        elif S == [1,0,0,0,0]: raz = 5
        elif S == [1,1,0,1,0]: raz = 6
        elif S == [0,1,1,1,0]: raz = 7
        elif S == [1,1,1,0,0]: raz = 8
        elif S == [0,1,0,1,1]: raz = 9
        elif S == [1,0,1,1,0]: raz = 10
        elif S == [0,1,1,0,0]: raz = 11
        elif S == [0,0,0,1,1]: raz = 12
        elif S == [1,0,0,1,0]: raz = 13
        elif S == [1,0,1,0,0]: raz = 14
        elif S == [1,1,0,0,1]: raz = 15
        elif S == [0,1,1,0,1]: raz = 16
        elif S == [0,0,1,1,1]: raz = 17
        elif S == [1,0,0,1,1]: raz = 18
        elif S == [1,0,1,0,1]: raz = 19
        elif S == [0,1,0,0,1]: raz = 20
     err_str = 'ошибка в %i разряде\nт.к. S совпадает с %i столбцом\nпроверочной матрицы' % (raz, raz)

     for i in xrange(m):#Отрисовка панелек с матрицами и прочим
         Matrix_M1 = Label(root,width = 30,font = "Arial 11",text = Matrix_M[i],bg = "white")
         Matrix_M1.place(x = 15,y = 190+20*i)
     for i in xrange(k_dist):
         E_report = Label(root,width = 30,font = "Arial 11",text = E_info_list[i],bg = "white")
         E_report.place(x = 360,y = 325+20*i)
         S_report = Label(root,width = 30,font = "Arial 11",text = S_info_list[i],bg = "white")
         S_report.place(x = 360,y = 460+20*i)
         Matrix_H1 = Label(root,width = 30,font = "Arial 11",text = Matrix_H[i],bg = "white")
         Matrix_H1.place(x = 360,y = 190+20*i)

     mist_mess = Label(root,font = "Arial 11",text = 'Принятая комбинация(с ошибкой):')
     mist_mess.place(x = 5,y = 137)
     mist_num = Label(root,font = "Arial 11",text = a)
     mist_num.place(x = 250,y = 137)

     matrix_M_text = Label(root,width = 30,font = "Arial 11",text = 'Порождающая матрица:',bg = "grey")
     matrix_M_text.place(x = 15,y = 170)
     matrix_H_text = Label(root,width = 30,font = "Arial 11",text = 'Проверочная матрица:',bg = "grey")
     matrix_H_text.place(x = 360,y = 170)

     E_text = Label(root,width = 30,font = "Arial 11",text = 'Вычисление контрольных разрядов',bg = "grey")
     E_text.place(x = 360,y = 305)
     S_text = Label(root,width = 30,font = "Arial 11",text = 'Вычисление синдрома',bg = "grey")
     S_text.place(x = 360,y = 440)

     S_str = Label(root,width = 30,font = "Arial 11",text = S_str,bg = "grey")
     S_str.place(x = 360,y = 560)

     error_text = Label(root,width = 30,font = "Arial 11",text = err_str,bg = "Orange")
     error_text.place(x = 15,y = 550)

root.bind('<Control-z>',quit)
btn2.bind("<Button-1>", caption)
btn1.bind("<Button-1>",principal)

root.mainloop()
