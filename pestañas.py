from tkinter import *
import tkinter
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog as FileDialog
from datetime import date
import sqlite3 # modulo de conexion con sqlite3 
import openpyxl #modulo excel
from openpyxl import Workbook
from openpyxl.styles import Font, Border, Alignment, Side, PatternFill, Font, Color, colors, GradientFill
from openpyxl.drawing.image import Image
from PIL import ImageTk, Image



class Product:
    #conexion con la base de datos
    db_lab = 'vitasis.db'
    
    def __init__(self, window):

        self.wind = window
        self.wind.title('Vitasis Laboratorio Médico')
        self.wind.configure(background = 'gray')
        self.wind.geometry('1200x823')
        self.wind.resizable(0, 0)
        

        #carga de la imagen
        img = Image.open('logo QR.png')
        self._image_logo = ImageTk.PhotoImage(img) 
        widget = tk.Label(self.wind, image = self._image_logo).grid( row= 0, column = 0, sticky = W)

        #Pestañas
        self._tab_control = ttk.Notebook(self.wind)
        self._tab_control.grid(row= 1, column = 0) 
        self.tab1 = tkinter.Frame(self._tab_control, bg = 'gray')
        self._tab_control.add(self.tab1, text='Vitasis',)

     
        #contenedor 3 estudios
        frame = LabelFrame(self.tab1, text = 'Estudios de laboratorio', labelanchor = N)
        frame.grid(row = 2, column = 0, pady = 5, padx = 5, ipadx = 30, sticky = W)
        frame.configure(background = 'gray')
        
        self.menu_desplegable() 
        Label(frame, text = 'Pruebas Clinicas 1', bg = 'gray').grid(row = 1, column = 0, pady = 10, sticky = W + E)
        self.prueba = tk.StringVar(frame)
        self.prueba.set('---------------------------------------------------------------')
        pruebas = self.menu_p
        #pruebas = ('ANTIDOPING EN ORINA', 'BIOMETRIA HEMATICA COMPLETA BHC', 'COPROPARASITOSCOPICO EN SERIE DE 3', 'EXAMEN GENERAL DE ORINA', 'ESPERMATOBIOSCOPIA DIRECTA','EXUDADO FARINGEO CON ANTIBIOGRAMA', 'GLUCOSA DESTROXIS', 'GLUCOSA', 'GONADOTROFINA CORIONICA FRACCION BETA', 'GRUPO SANGUINEO Y FACTOR RH',
        #           'HEMOGLOBINA GLUCOSILADA', 'PAPANICOLAU', 'PRUEBA INMUNOLOGICA DE EMBARAZO', 'GLUCOSA,COLESTEROL Y TRIGLICERIDOS', 'QUIMICA DE 4 ELEMENTOS', 'QUIMICA DE 5 ELEMENTOS', 'QUIMICA DE 6 ELEMENTOS', 'QUIMICA DE 12 ELEMENTOS', 'QUIMICA DE 18 ELEMENTOS', 'QUIMICA DE 25 ELEMENTOS','QUIMICA DE 32 ELEMENTOS',
        #           'REACCIONES FEBRILES', 'TAMIZ METABOLICO NEONATAL CON AMINOACIDOS COMPLETO', 'TIEMPOS DE COAGULACION TTPA,TP, TS, TT', 'UROCULTIVO', 'VDRL', 'VIH PRUEBA DE TAMIZAJE', 'PERFIL HORMONAL FEMENINO BASICO', 'PERFIL HORMONAL GINECOLOGICO','PERFIL LIPIDOS', 'PERFIL PRENATAL', 'PERFIL PROSTATICO', 'PERFIL REUMATICO', 
        #           'PERFIL TIROIDEO COMPLETO')                
        self.menu_prueba = tk.OptionMenu(frame, self.prueba, *pruebas).grid(row = 1, column = 1, sticky = W + E, pady = 10)
        

        #contenedor desglose de costos 
        self.frame5 = LabelFrame(self.tab1, text = 'Costo a pagar', labelanchor = N)
        self.frame5.grid(row = 2, column = 1, pady = 10, padx = 5, sticky = N )
        self.frame5.configure(background = 'gray')
        
        Label(self.frame5, text = ' ', bg = 'gray').grid(row = 1, column = 1, pady = 10, sticky = W )
        message8 = Label(self.frame5, text = '', fg = 'black', font = ('Verdana', 12), bg = 'gray')
        message8.grid(row = 1, column = 1, pady = 10, padx = 10, sticky = W)  
        message8['text'] = 'Subtotal'

        Label(self.frame5, text = ' ', bg = 'gray').grid(row = 1, column = 2, pady = 10, sticky = W )
        self.message9 = Label(self.frame5, text = '', fg = 'black', font = ('Verdana', 12), bg = 'gray')
        self.message9.grid(row = 1, column = 2, pady = 10, padx = 10, sticky = W)  
        self.subtotal = 0
        self.message9['text'] = '$ {}.0'.format(self.subtotal)
        
        Button(self.frame5, text = 'Pagar', command = self.sumas).grid(row = 6, columnspan = 3, pady = 10, padx = 10, sticky = W + E) #command = self.ventana_paciente
        Button(self.frame5, text = 'Generar Recibo').grid(row = 7, columnspan = 3, pady = 10, padx = 10, sticky = W + E) #command = self.ventana_paciente
                

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_lab) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    #def menu_sub(self): #Precios de los estudios para los totales y subtotales
    #    query = 'SELECT price FROM price_list ORDER BY price'
    #    self.subto = self.run_query(query)
    #    if self.subto is None :
    #        self.subto = 'No hay precio'
    #    else:
    #        self.subto = list(self.subto)
    #        for row in self.subto:
    #            print(row)  
              
    def menu_desplegable(self): # Menu desplegable
        query = 'SELECT estudios_clinicos, precio FROM price_list ORDER BY estudios_clinicos ASC'
        self.menu_p = self.run_query(query)
        
        if self.menu_p is None :
            self.menu_p = 'No hay estudios'
        else:
            for row in self.menu_p:
               print(row)        
                        
            for a in self.menu_p:
                self.lista_p['estudio'] = a

            self.lista_p = {"estudio":  self.lista_p}

            print(type(self.lista_p))
                     
                     
                           
   

 
if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()



       

