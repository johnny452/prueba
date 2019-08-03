#!/usr/bin/python   
# -*- coding: utf-8 -*- 
from tkinter import *
import tkinter
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog as FileDialog
from datetime import date, datetime
import calendar
import sqlite3 # modulo de conexion con sqlite3 
from PIL import ImageTk, Image

class MainFrame(tk.Frame):

    #conexion con la base de datos
    db_lab = 'vitasis.db'

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.note_book = ttk.Notebook(self)
        self.note_book.pack()
        self.tab2 = tkinter.Frame(self.note_book, bg = 'gray') 
        self.note_book.add(self.tab2, text="Seguimiento", compound=tk.TOP)
        self.tab3 = tkinter.Frame(self.note_book, bg = 'gray') 
        self.note_book.add(self.tab3, text="Registro de pagos", compound=tk.TOP)
        
        style = ttk.Style()
        style.theme_use("classic")
        
        #carga de la imagen
        img = Image.open('logo QR.png')
        self._image_logo = ImageTk.PhotoImage(img) 
        widget = tk.Label(self.tab2, image = self._image_logo).grid( row= 0, column = 0, sticky = W)

        #creando el contenedor REGISTRO DE PACIENTE
        frame = LabelFrame(self.tab2, text = 'Seguimiento', labelanchor = N, font = ('bold'))
        frame.grid(row = 1, column = 0, padx = 5, pady = 20, ipadx = 30, sticky = W)
        frame.configure(background = 'gray')
        
        #entrada para nombre
        Label(frame, text = 'Fecha de inicio: ', bg = 'gray').grid(row = 1, column = 0, sticky = W + E)
        self.fecha_inicial = Entry(frame, width = 10)
        self.fecha_inicial.focus()
        self.fecha_inicial.grid(row = 1, column = 1, pady = 10, sticky = W)
        

        Label(frame, text = 'Fecha final: ', bg = 'gray',).grid(row = 2, column = 0, sticky = W + E)
        self.fecha_final = Entry(frame, width = 10)
        self.fecha_final.grid(row = 2, column = 1, pady = 10, sticky = W )
        

        Button(frame, text = 'Seleccionar mes', command = self.get_mes).grid(row =2, column = 2, pady = 10, padx = 10, sticky = W + E ) 
        
        columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10', '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18', '#19', '#20')
        #columns = ('#1', '#2', '#3', '#4', '#5', '#6')
        self.tree2 = ttk.Treeview(self.tab2, show='headings', height=10, columns=columns)
        self.tree2.grid(row = 3, column=0, columnspan=2, sticky = tk.W+tk.E+tk.N+tk.S)
        self.tab2.grid_rowconfigure(0, weight=1)
        self.tab2.grid_columnconfigure(0, weight=1)
        self.tab2.grid_columnconfigure(1, weight=1)    
        
        self.tree2.column("#1", width=70, anchor = tk.CENTER )
        self.tree2.column("#2", width=150, stretch=tk.NO)
        self.tree2.column("#3", width=150)
        self.tree2.column("#4", width=150, stretch=tk.NO)
        self.tree2.column("#5", width=50, stretch=tk.NO)
        self.tree2.column("#6", width=100, stretch=tk.NO)
        self.tree2.column("#7", width=300) # Prueba Clinica 1
        self.tree2.column("#8", width=300) # Prueba Clinica 2
        self.tree2.column("#9", width=300) # Prueba Clinica 3
        self.tree2.column("#10", width=300) # Prueba Clinica 4
        self.tree2.column("#11", width=300) # Prueba Clinica 5
        self.tree2.column("#12", width=200) # Fecha de estudio
        self.tree2.column("#13", width=200) # Fecha de entrega
        self.tree2.column("#14", width=150) # Atendido
        self.tree2.column("#15", width=150) # Promocion
        self.tree2.column("#16", width=150) #Subtotal
        self.tree2.column("#17", width=150) # Anticipo
        self.tree2.column("#18", width=150) # Total
        self.tree2.column("#19", width=150) # Saldo a pagar
        self.tree2.column("#20", width=150) # Status
        
        self.tree2.heading('#1', text='Folio', anchor=tk.CENTER)
        self.tree2.heading('#2', text='Nombre', anchor=tk.CENTER)
        self.tree2.heading('#3', text='Dirección', anchor=tk.CENTER)
        self.tree2.heading('#4', text='Teléfono', anchor=tk.CENTER)
        self.tree2.heading('#5', text='Edad', anchor=tk.CENTER)
        self.tree2.heading('#6', text='Sexo', anchor=tk.CENTER)
        self.tree2.heading('#7', text='Prueba Clinica 1', anchor=tk.CENTER)
        self.tree2.heading('#8', text='Prueba Clinica 2', anchor=tk.CENTER)
        self.tree2.heading('#9', text='Prueba Clinica 3', anchor=tk.CENTER)
        self.tree2.heading('#10', text='Prueba Clinica 4', anchor=tk.CENTER)
        self.tree2.heading('#11', text='Prueba Clinica 5', anchor=tk.CENTER)
        self.tree2.heading('#12', text='Fecha de estudio', anchor=tk.CENTER)
        self.tree2.heading('#13', text='Fecha de entrega', anchor=tk.CENTER)
        self.tree2.heading('#14', text='Atendido', anchor=tk.CENTER)
        self.tree2.heading('#15', text='Promoción', anchor=tk.CENTER)
        self.tree2.heading('#16', text='Subtotal', anchor=tk.CENTER)
        self.tree2.heading('#17', text='Anticipo', anchor=tk.CENTER)
        self.tree2.heading('#18', text='Total', anchor=tk.CENTER)
        self.tree2.heading('#19', text='Saldo a pagar', anchor=tk.CENTER)
        self.tree2.heading('#20', text='Status', anchor=tk.CENTER)

        vsb = ttk.Scrollbar(self.tab2, orient="vertical", command=self.tree2.yview)
        vsb.grid(row=3, column=2, sticky='ns')
        self.tree2.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(self.tab2, orient="horizontal", command=self.tree2.xview)
        hsb.grid(row = 4, column=0, columnspan=2, sticky = tk.W+tk.E)
        self.tree2.configure(xscrollcommand = hsb.set)
        self.get_pacients()


        #########  Registro de pagos   #########
        
        widget = tk.Label(self.tab3, image = self._image_logo).grid( row= 0, column = 0, sticky = W)
        
        frame = LabelFrame(self.tab3, text = 'EDITAR PAGOS', labelanchor = N, font = ('bold'))
        frame.grid(row = 1, column = 0, columnspan = 15, padx = 5, pady = 20, ipadx = 30, sticky = W)
        frame.configure(background = 'gray')

        Button(frame, text = 'Editar Status', command = self.edit_registro ).grid(row = 1, column = 0, pady = 10, padx = 10, sticky = W + E ) 

        columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10', '#11', '#12', '#13', '#14', '#15')
        self.tree3 = ttk.Treeview(self.tab3, show='headings', height=10, columns=columns)
        self.tree3.grid(row = 2, column=0, columnspan=2, sticky = tk.W+tk.E+tk.N+tk.S)
        self.tab3.grid_rowconfigure(0, weight=1)
        self.tab3.grid_columnconfigure(0, weight=1)
        self.tab3.grid_columnconfigure(1, weight=1)    
        
        self.tree3.column("#1", width=70, anchor = tk.CENTER ) #folio
        self.tree3.column("#2", width=150, stretch=tk.NO) #Nombre        
        self.tree3.column("#3", width=150, stretch=tk.NO) #Telefono   
        self.tree3.column("#4", width=300) # Prueba Clinica 1
        self.tree3.column("#5", width=300) # Prueba Clinica 2
        self.tree3.column("#6", width=300) # Prueba Clinica 3
        self.tree3.column("#7", width=300) # Prueba Clinica 4
        self.tree3.column("#8", width=300) # Prueba Clinica 5
        self.tree3.column("#9", width=100) # Fecha de estudio
        self.tree3.column("#10", width=100) # Fecha de entrega 
        self.tree3.column("#11", width=150) # Promocion
        self.tree3.column("#12", width=100) # Anticipo
        self.tree3.column("#13", width=100) # Total
        self.tree3.column("#14", width=100) # Saldo a pagar
        self.tree3.column("#15", width=100) # Status

        self.tree3.heading('#1', text='Folio', anchor=tk.CENTER)
        self.tree3.heading('#2', text='Nombre', anchor=tk.CENTER)
        self.tree3.heading('#3', text='Teléfono', anchor=tk.CENTER)
        self.tree3.heading('#4', text='Prueba Clinica 1', anchor=tk.CENTER)
        self.tree3.heading('#5', text='Prueba Clinica 2', anchor=tk.CENTER)
        self.tree3.heading('#6', text='Prueba Clinica 3', anchor=tk.CENTER)
        self.tree3.heading('#7', text='Prueba Clinica 4', anchor=tk.CENTER)
        self.tree3.heading('#8', text='Prueba Clinica 5', anchor=tk.CENTER)
        self.tree3.heading('#9', text='Fecha de estudio', anchor=tk.CENTER)
        self.tree3.heading('#10', text='Fecha de entrega', anchor=tk.CENTER)
        self.tree3.heading('#11', text='Promoción', anchor=tk.CENTER)
        self.tree3.heading('#12', text='Anticipo', anchor=tk.CENTER)
        self.tree3.heading('#13', text='Total', anchor=tk.CENTER)
        self.tree3.heading('#14', text='Saldo a pagar', anchor=tk.CENTER)
        self.tree3.heading('#15', text='Status', anchor=tk.CENTER)
        
        vsb = ttk.Scrollbar(self.tab3, orient="vertical", command=self.tree3.yview)
        vsb.grid(row=2, column=2, sticky='ns')
        self.tree3.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(self.tab3, orient="horizontal", command=self.tree3.xview)
        hsb.grid(row = 3, column=0, columnspan=2, sticky = tk.W+tk.E)
        self.tree3.configure(xscrollcommand = hsb.set)
        self.get_pacients_1()

    def run_query(self, query, parameters = ()): # Ejecutar consulta para la tabla paciente
        with sqlite3.connect(self.db_lab) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
        # Consulta de datos
        query = 'SELECT * FROM paciente ORDER BY folio DESC'
        db_rows = self.run_query(query)

    def run_query_3(self, query, parameters = ()): # Ejecutar consulta para la tabla paciente
        with sqlite3.connect(self.db_lab) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
        # Consulta de datos
        query = 'SELECT * FROM paciente ORDER BY folio DESC'
        db_rows = self.run_query(query)
        
    def get_pacients(self):
            
            # Limpiando la tabla
            records = self.tree2.get_children()
            for element in records:
                self.tree2.delete(element)
            # getting data
            query = 'SELECT * FROM paciente ORDER BY folio ASC'
            db_rows = self.run_query(query).fetchall()
            # filling data
           
            for row in db_rows:
                self.tree2.insert('', 0, text = row[0], values = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19]))

    def get_pacients_1(self):
            
            # Limpiando la tabla
            records = self.tree3.get_children()
            for element in records:
                self.tree3.delete(element)
            # getting data
            query = 'SELECT * FROM paciente ORDER BY folio ASC'
            db_rows = self.run_query(query).fetchall()
            # filling data
            for row in db_rows:
                self.tree3.insert('', 0, text = row[0], values = (row[0], row[1], row[3], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[14], row[16], row[17], row[18], row[19]))

    def get_mes(self):
            
        self.fecha_i = datetime.strptime(self.fecha_inicial.get(), '%d, %b, %Y')
        self.fecha_f = datetime.strptime(self.fecha_final.get(), '%d, %b, %Y')     
           
        # Limpiando la tabla
        records = self.tree2.get_children()
        for element in records:
            self.tree2.delete(element)
       # getting data
        query = ("SELECT * FROM paciente WHERE fecha_de_estudio BETWEEN ? AND ?", (self.fecha_i.date(), self.fecha_f.date()))
        db_rows = self.run_query("SELECT * FROM paciente WHERE fecha_de_estudio BETWEEN ? AND ?", (self.fecha_i.date(), self.fecha_f.date())).fetchall()
        self.meses = db_rows
        print(type(self.meses)) 
        print(self.meses)
        for row in db_rows:
            self.tree2.insert('', 0, text = row[0], values = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19]))

    def edit_registro(self):
        
        try:
            self.tree3.item(self.tree3.selection())['values'][0]
        except IndexError as e:
            messagebox.showinfo('Editar Status', 'Por favor elija un paciente')
            return
        folio = self.tree3.item(self.tree3.selection())['text']
        nombre = self.tree3.item(self.tree3.selection())['values'][1]
        telefono = self.tree3.item(self.tree3.selection())['values'][2]
        prueba1 = self.tree3.item(self.tree3.selection())['values'][3]
        prueba2 = self.tree3.item(self.tree3.selection())['values'][4]
        prueba3 = self.tree3.item(self.tree3.selection())['values'][5]
        prueba4 = self.tree3.item(self.tree3.selection())['values'][6]
        prueba5 = self.tree3.item(self.tree3.selection())['values'][7]
        fecha_de_estudio = self.tree3.item(self.tree3.selection())['values'][8]
        fecha_de_entrega = self.tree3.item(self.tree3.selection())['values'][9]
        promocion = self.tree3.item(self.tree3.selection())['values'][10]
        anticipo = self.tree3.item(self.tree3.selection())['values'][11]
        total = self.tree3.item(self.tree3.selection())['values'][12]
        saldo_a_pagar = self.tree3.item(self.tree3.selection())['values'][13]
        status = self.tree3.item(self.tree3.selection())['values'][14]
        
        self.edit_wind2 = Toplevel()
        self.edit_wind2.configure(background = 'gray')
        self.edit_wind2.title = 'Editar estudio'
        #Frame
        frame = LabelFrame(self.edit_wind2, text = 'Actualizar Status', labelanchor = N, font = ('bold'))
        frame.grid(row = 0, column = 0, padx = 5, pady = 20, ipadx = 30, sticky = W)
        frame.configure(background = 'gray')

        Label(frame, text = 'Folio: ', bg = 'gray').grid(row = 0, column = 0)
        numero = Label(frame, text = '', bg = 'gray', anchor = CENTER)
        numero.grid(row = 0, column = 1, columnspan = 1, sticky = W + E)  
        numero['text'] = '{}'.format(folio)  
        Label(frame, text = 'Nombre:', bg = 'gray').grid(row = 1, column = 0)
        paciente = Label(frame, text = '', bg = 'gray', anchor = CENTER)
        paciente.grid(row = 1, column = 1, columnspan = 1, sticky = W + E)  
        paciente['text'] = '{}'.format(nombre)
        Label(frame, text = 'Telefono:', bg = 'gray').grid(row = 2, column = 0)
        phone = Label(frame, text = '', bg = 'gray', anchor = CENTER)
        phone.grid(row = 2, column = 1, columnspan = 1, sticky = W + E)  
        phone['text'] = '{}'.format(telefono)
        Label(frame, text = 'Prueba Clínica 1: ', bg = 'gray').grid(row = 3, column = 0)
        prueba_c1 = Label(frame, text = '', bg = 'gray', anchor = CENTER)
        prueba_c1.grid(row = 3, column = 1, columnspan = 1, sticky = W + E)  
        prueba_c1['text'] = '{}'.format(prueba1)
        Label(frame, text = 'Prueba Clínica 2: ', bg = 'gray').grid(row = 4, column = 0)
        prueba_c2 = Label(frame, text = '', bg = 'gray', anchor = CENTER)
        prueba_c2.grid(row = 4, column = 1, columnspan = 1, sticky = W + E)  
        prueba_c2['text'] = '{}'.format(prueba2)
        Label(frame, text = 'Prueba Clínica 3: ', bg = 'gray').grid(row = 5, column = 0)
        prueba_c3 = Label(frame, text = '', bg = 'gray', anchor = CENTER)
        prueba_c3.grid(row = 5, column = 1, columnspan = 1, sticky = W + E)  
        prueba_c3['text'] = '{}'.format(prueba3)
        Label(frame, text = 'Prueba Clínica 4: ', bg = 'gray').grid(row = 6, column = 0)
        prueba_c4 = Label(frame, text = '', bg = 'gray', anchor = CENTER)
        prueba_c4.grid(row = 6, column = 1, columnspan = 1, sticky = W + E)  
        prueba_c4['text'] = '{}'.format(prueba4)
        Label(frame, text = 'Prueba Clínica 5: ', bg = 'gray').grid(row = 7, column = 0)    
        prueba_c5 = Label(frame, text = '', bg = 'gray', anchor = CENTER)
        prueba_c5.grid(row = 7, column = 1, columnspan = 1, sticky = W + E)  
        prueba_c5['text'] = '{}'.format(prueba5)
        Label(frame, text = 'Fecha de estudio: ', bg = 'gray').grid(row = 8, column = 0)
        fecha_e = Label(frame, text = '', bg = 'gray', anchor = CENTER)
        fecha_e.grid(row = 8, column = 1, columnspan = 1, sticky = W + E)  
        fecha_e['text'] = '{}'.format(fecha_de_estudio)
        Label(frame, text = 'Fecha de entrega: ', bg = 'gray').grid(row = 9, column = 0)
        fecha_en = Label(frame, text = '', bg = 'gray', anchor = CENTER)
        fecha_en.grid(row = 9, column = 1, columnspan = 1, sticky = W + E)  
        fecha_en['text'] = '{}'.format(fecha_de_entrega)
        Label(frame, text = 'Promoción: ', bg = 'gray').grid(row = 10, column = 0)
        prom = Label(frame, text = '', bg = 'gray', anchor = CENTER)
        prom.grid(row = 10, column = 1, columnspan = 1, sticky = W + E)  
        prom['text'] = '{}'.format(promocion)
        Label(frame, text = 'Anticipo:', bg = 'gray').grid(row = 11, column = 0)
        ant = Label(frame, text = '', bg = 'gray', anchor = CENTER)
        ant.grid(row = 11, column = 1, columnspan = 1, sticky = W + E)  
        ant['text'] = '$ {}'.format(anticipo)
        #New anti
        Label(frame, text = 'Editar anticipo:', bg = 'gray').grid(row = 12, column = 0, pady = 10)
        self.new_anti= Entry(frame)
        self.new_anti.grid(row = 12, column = 1) 
        Label(frame, text = 'Total:', bg = 'gray').grid(row = 13, column = 0)
        tot = Label(frame, text = '', bg = 'gray', anchor = CENTER)
        tot.grid(row = 13, column = 1, columnspan = 1, sticky = W + E)  
        tot['text'] = '$ {}'.format(total)
        Label(frame, text = 'Saldo a pagar:', bg = 'gray').grid(row = 14, column = 0)
        a_pagar = Label(frame, text = '', bg = 'gray', anchor = CENTER)
        a_pagar.grid(row = 14, column = 1, columnspan = 1, sticky = W + E)  
        a_pagar['text'] = '$ {}'.format(saldo_a_pagar)
        Label(frame, text = 'Status:', bg = 'gray').grid(row = 16, column = 0, pady = 10)
        st= Label(frame, text = '', bg = 'gray', anchor = CENTER)
        st.grid(row = 16, column = 1, columnspan = 1, sticky = W + E)  
        st['text'] = '{}'.format(status)
      
        Label(frame, text = 'Pagar saldo:', bg = 'gray').grid(row = 15, column = 0, pady = 10)
        self.new_saldo= Entry(frame)
        self.new_saldo.grid(row = 15, column = 1)
        Label(frame, text = 'Nuevo Status:', bg = 'gray').grid(row = 17, column = 0, pady = 10)
        self.new_status= Entry(frame)
        self.new_status.grid(row = 17, column = 1)
        
        Button(frame, text = 'Actualizar', command = lambda: self.edit_status(self.new_anti.get(), anticipo, self.new_saldo.get(), saldo_a_pagar, self.new_status.get(), status)).grid(row = 18, column = 1, sticky = W)
        #Button(self.edit_wind2, text = 'Cerrar ventana', command = self.cerrarventana2).grid(row = 1, column = 2, sticky = W + E, padx = 30, pady= 20) 
    
    def validation_4(self):

        return len(self.new_saldo.get()) !=0 and len(self.new_status.get()) !=0  and len(self.new_anti.get()) !=0

    
    def edit_status(self, new_anti, anticipo, new_saldo, saldo_a_pagar, new_status, status): # Funcion del llenado de la tabla para los nuevos estudios
        if self.validation_4():
            query = 'UPDATE paciente SET anticipo = ?, saldo_a_pagar = ?, status = ? WHERE anticipo = ? AND saldo_a_pagar = ? AND status = ?'
            parameters = (new_anti, new_saldo, new_status, anticipo, saldo_a_pagar, status)
            self.run_query_3(query, parameters)
            self.edit_wind2.destroy()
            messagebox.showinfo('Status Editado', 'Status editado')
        else:
            messagebox.showinfo('Atención', 'Favor de llenar todos los campos')
        self.get_pacients_1()
    
############# Hacer modificaciones en anticipo y ademas colocar el boton de nuevo recibo 



if __name__ == "__main__":
    root = tk.Tk()
    root.title('Vitasis Laboratorio Médico')
    root.configure(background = 'gray')
    root.geometry("1200x630")
    MainFrame(root).pack(side="top", fill="both", expand=True)
    root.mainloop()