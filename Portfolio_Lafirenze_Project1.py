import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from PIL import ImageTk
import mysql.connector
import re
from datetime import datetime


#CREARE DATABASE SECONDO E DATABASE BACK E SCEGLIERE QUALE UTILIZZARE
def create_database(host, user, password, database_name):
    try:
        #Connessione al server MySQL XAMPP localhost
        db = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

        #Creazione del cursore DB
        cursor = db.cursor()

        #Creazione del database se non esiste, utilizzerà i parametri forniti sopra
        cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(database_name))

        #Chiudo il cursore e la connessione al DB
        cursor.close()
        db.close()
    except mysql.connector.Error:
        messagebox.showerror("errore creazione DataBase", "Il sistema non è riuscito a creare\n"
                                                          "o a connettersi al database")


# crea il database passandogli tramite stringa i parametri richiesti da mysql
create_database("localhost", "root", "", "data_engineer")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="data_engineer",
)


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        #Dimensioni della finestra
        width = 1700
        height = 910
        #Creazione della finestra con i parametri width, height definiti sopra
        self.geometry(f"{width}x{height}")
        self.title('Progetto_Lafirenze_Database_Engineer')

        #Frame ancorato alla parte inferiore della finestra
        self.barra_time = tk.Frame(self, bg="white", height=30)
        self.barra_time.pack(side='bottom', fill='x')

        #Trasformo la variabile tempotext in stringa, altrimenti non è possibile visualizzarla a video
        #Creo un label all'interno del frame barra_time e ci stampo il tempo
        self.tempotext = tk.StringVar()
        self.tempo_barra_time = ttk.Label(self.barra_time, background="white", textvariable=self.tempotext,
                                          font=("Arial", 12))
        self.tempo_barra_time.pack(side='left', padx=10)

        #SFONDO
        self.bg = ImageTk.PhotoImage(file="azure.jpg")
        self.my_canvas = Canvas(self, width=width, height=height)
        self.my_canvas.pack(fill="both", expand=True)
        self.my_canvas.create_image(0, 0, image=self.bg, anchor="nw")

        #Inizio definizioni dei widget che utilizzerò nel programma, essi verranno nascosti e richiamati dalle funzioni
        #show_main_interface, show_second_interface, show_third_interface
        self.text_Inserimento_nome = ttk.Label(self, text='Inserisci nome', background='#0080ff', font=("Arial", 18))
        self.text_Inserimento_nome.place_forget()
        self.set_text_nome = ttk.Entry(self)
        self.set_text_nome.place_forget()

        self.text_Inserimento_cognome = ttk.Label(self, text='Inserisci cognome', background='#0080ff',
                                                  font=("Arial", 18))
        self.text_Inserimento_cognome.place_forget()
        self.set_text_cognome = ttk.Entry(self)
        self.set_text_cognome.place_forget()

        self.set_Inserimento_indirizzo = ttk.Label(self, text='Inserisci indirizzo', background='#0080ff',
                                                   font=('Arial', 18))
        self.set_Inserimento_indirizzo.place_forget()
        self.set_text_indirizzo = ttk.Entry(self)
        self.set_text_indirizzo.place_forget()

        self.set_Inserimento_numero = ttk.Label(self, text='Inserisci Numero', background='#0080ff', font=('Arial', 18))

        self.set_text_numero = ttk.Entry(self)

        self.set_text_numero.place_forget()
        self.set_Inserimento_numero.place_forget()

        self.set_Inserimento_email = ttk.Label(self, text='Inserisci email', background="#0080ff", font=('Arial', 18))

        self.set_text_email = ttk.Entry(self)

        self.set_Inserimento_email.place_forget()
        self.set_text_email.place_forget()

        self.buttonDB = ttk.Button(self, text="Invio dati al database", command=self.invio_dati_db)
        self.buttonDB.place_forget()

        self.found_indices = []
        self.current_index = -1
        prefissi = [30, 31, 32, 33, 350, 351, 352, 353, 39]
        prefissi_str = ["+" + str(prefisso) for prefisso in prefissi]
        self.prefissi = ttk.Combobox(self, values=prefissi_str, state='readonly', width=5)
        self.prefissi.place_forget()

        self.text_CANC = ttk.Label(self, text='Premi tasto Canc per eliminare tutti i dati', background='',
                                   font=("Arial", 18))
        self.text_CANC.place_forget()
        self.text_Enter = ttk.Label(self, text='Premi tasto Enter per Registrare i dati in memoria', background='',
                                    font=("Arial", 18))
        self.text_Enter.place_forget()

        self.db_list = ttk.Label(self, text="Lista database", background="#0080ff", font=("Roboto", 30))
        self.db_list.place_forget()
        self.lista_nomi = ttk.Combobox(self, state='readonly')
        self.lista_nomi.place_forget()
        self.nome_label = ttk.Label(self, text="nomi", background="#0080ff", font=("Helvetica", 15))
        self.nome_label.place_forget()
        self.cognome_label = ttk.Label(self, text="cognomi", background="#0080ff", font=("Helvetica", 15))
        self.cognome_label.place_forget()
        self.indirizzo_label = ttk.Label(self, text="indirizzo", background="#0080ff", font=("Helvetica", 15))
        self.indirizzo_label.place_forget()
        self.prefisso_label = ttk.Label(self, text="prefisso", background="#0080ff", font=("Helvetica", 15), )
        self.prefisso_label.place_forget()
        self.numero_label = ttk.Label(self, text="numero", background="#0080ff", font=("Helvetica", 15))
        self.numero_label.place_forget()
        self.email_label = ttk.Label(self, text="email", background="#0080ff", font=("Helvetica", 15))
        self.email_label.place_forget()
        self.lista_cognomi = ttk.Combobox(self, state='readonly')
        self.lista_cognomi.place_forget()

        self.lista_indirizzi = ttk.Combobox(self, state='readonly')
        self.lista_indirizzi.place_forget()

        self.lista_prefissi = ttk.Combobox(self, state='readonly')
        self.lista_prefissi.place_forget()

        self.lista_numeri = ttk.Combobox(self, state='readonly')
        self.lista_numeri.place_forget()

        self.lista_email = ttk.Combobox(self, state='readonly')
        self.lista_email.place_forget()

        self.lista_tutto = ttk.Combobox(self, state='readonly')
        self.lista_tutto.place_forget()

        self.search_button = ttk.Button(self, text="Cerca ", command=self.search_tree)
        self.search_button.place_forget()

        self.search_entry = ttk.Entry(self)
        self.search_entry.place_forget()

        self.delete_button = ttk.Button(self, text="Elimina", command=self.delete_row)
        self.delete_button.place_forget()

        self.id_entry = ttk.Entry(self)
        self.id_entry.place_forget()

        self.update_nome = ttk.Button(self, text="Modifica riga", command=self.update_column_record_nome)
        self.update_nome.place_forget()
        self.update_nome_entry = ttk.Entry(self)
        self.update_nome_entry.place_forget()
        self.update_cognome = ttk.Button(self, text="Modifica riga", command=self.update_column_record_cognome)
        self.update_cognome.place_forget()
        self.update_cognome_entry = ttk.Entry(self)
        self.update_cognome_entry.place_forget()
        self.update_indirizzi = ttk.Button(self, text="Modifica riga", command=self.update_column_record_indirizzi)
        self.update_indirizzi.place_forget()
        self.update_indirizzi_entry = ttk.Entry(self)
        self.update_indirizzi_entry.place_forget()
        self.update_prefissi = ttk.Button(self, text="Modifica riga",
                                          command=lambda: self.update_column_record_prefissi(prefissi))

        self.update_indirizzi.place_forget()
        self.update_prefissi_entry = ttk.Entry(self)
        self.update_prefissi_entry.place_forget()
        self.update_numeri = ttk.Button(self, text="Modifica riga", command=self.update_column_record_numero)
        self.update_numeri.place_forget()
        self.update_numeri_entry = ttk.Entry(self)
        self.update_numeri_entry.place_forget()
        self.update_email = ttk.Button(self, text="Modifica riga", command=self.update_column_record_email)
        self.update_email.place_forget()
        self.update_email_entry = ttk.Entry(self)
        self.update_email_entry.place_forget()
        id_max = None
        self.id_count = ttk.Label(self, text=f"Il database ha {id_max} clienti", background="#0080ff",
                                  font=("Arial", 20))
        self.id_count.place_forget()

        self.tree_frame = Frame(self)
        self.tree_frame.place_forget()

        self.inserimento = ttk.Entry(width=30)
        self.inserimento.place_forget()

        self.explanation_frame = Frame(self)
        self.ex_frame = Frame(self)

        self.visual_tutto = ttk.Treeview()

        #Fine definizione widget utilizzati dalle funzioni principali

        #Questo bottone richiama l'interfaccia di inserimento dati
        self.button_to_second_interface = ttk.Button(self, text="Parte anagrafica", command=self.show_second_interface)
        self.button_to_second_interface.place(x=650, y=250)

        #Questo bottone richiama l'interfaccia visiva e di modifica
        self.button_to_third_interface = ttk.Button(self, text="Parte visual", command=self.show_third_interface)
        self.button_to_third_interface.place(x=575, y=250)

        self.text_benvenuto = ttk.Label(self, text='Benvenuto gentile cliente', background='#0080ff',
                                        font=("Arial", 30))
        self.text_benvenuto.place(x=450, y=10)

        self.text_spiegazione = ttk.Label(self, text="Con il tasto PARTE ANAGRAFICA verrà indirizzato alla schermata\n"
                                                     "di inserimento del programma\n\nMentre con il tasto PARTE VISUAL "
                                                     "verrà indirizzato alla schermata di \n"
                                                     "visualizzazione, eliminazione"
                                                     ", ricerca e di modifica del programma", background='#0080ff',
                                          font=("Arial", 15))
        self.text_spiegazione.place(x=450, y=100)

        self.button_to_main_interface = ttk.Button(self, text="HOME", command=self.show_main_interface)
        self.button_to_second_interface.place(x=650, y=250)

        #menù di aggiunta o di visualizzazione delle note dell'albero di visualizzazione della parte visual
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Aggiungi nota", command=self.input_note)
        self.popup_menu.add_command(label="Visualizza nota", command=self.visual_note)

        #Richiama ogni secondo la funzione tempo_real_time, che restituisce il tempo corrente
        self.tempo_real_time()

        #self.bind('<Configure>', self.resizer)

    #Le funzioni ottieni_***** aprono un cursore, selezionano dal database tutti i dati e l'id associato nella tabella
    #I risultati vengono depositati in una lista formata da l'id e dalla variabile e successivamente restituiti
    @staticmethod
    def ottieni_nomi():

        cursor = db.cursor()
        sql = "SELECT id, nome FROM tabella_clienti WHERE nome IS NOT NULL"
        cursor.execute(sql)
        results = cursor.fetchall()
        lista_nomi = [(row[0], row[1]) for row in results]
        cursor.close()
        return lista_nomi

    @staticmethod
    def ottieni_cognomi():

        cursor = db.cursor()
        sql = "SELECT id, cognome FROM tabella_clienti WHERE cognome IS NOT NULL"
        cursor.execute(sql)
        results = cursor.fetchall()
        lista_cognomi = [(row[0], row[1]) for row in results]
        cursor.close()
        return lista_cognomi

    @staticmethod
    def ottieni_indirizzo():

        cursor = db.cursor()
        sql = "SELECT id, indirizzo FROM tabella_clienti WHERE indirizzo IS NOT NULL"
        cursor.execute(sql)
        results = cursor.fetchall()
        lista_indirizzi = [(row[0], row[1]) for row in results]
        cursor.close()
        return lista_indirizzi

    @staticmethod
    def ottieni_prefisso():

        cursor = db.cursor()
        sql = "SELECT id, prefisso FROM tabella_clienti WHERE prefisso IS NOT NULL"
        cursor.execute(sql)
        results = cursor.fetchall()

        lista_prefissi = [(row[0], row[1]) for row in results]
        cursor.close()
        return lista_prefissi

    @staticmethod
    def ottieni_numero():

        cursor = db.cursor()
        sql = "SELECT id, numero FROM tabella_clienti WHERE numero IS NOT NULL"
        cursor.execute(sql)
        results = cursor.fetchall()

        lista_numeri = [(row[0], row[1]) for row in results]
        cursor.close()
        return lista_numeri

    @staticmethod
    def ottieni_email():

        cursor = db.cursor()
        sql = "SELECT id, email FROM tabella_clienti WHERE email IS NOT NULL"
        cursor.execute(sql)
        results = cursor.fetchall()

        lista_email = [(row[0], row[1]) for row in results]
        cursor.close()
        return lista_email

    #Crea una lista con le variabili inserite nei campi Entry, viene chiamato a ogni invio con L'ENTER
    @staticmethod
    def dati_inseriti(nome_inserito, cognome_inserito, indirizzo_inserito, prefisso_inserito,
                      numero_inserito, email_inserito):

        dati = (nome_inserito, cognome_inserito, indirizzo_inserito, prefisso_inserito,
                numero_inserito, email_inserito)

        global dati_tupla
        dati_tupla = dati
        return dati_tupla

    #Invia i dati al Database, crea la tabella se non esiste, prende dati_tupla da dati_inseriti, controlla i campi
    @staticmethod
    def invio_dati_db(dati_tupla):
        #Controlla che la prima parte, abbia caratteri dalla a alla z, dalla A alla Z, dal 0 al 9 e accetta . e _
        #Deve esserci per forza @, accetta qualsiasi carattere dopo il "." stessa cosa, ma accetta solo 1 punto
        email_check = r'^[a-zA-Z0-9._]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
        indirizzo_check = (r'^(Via|Viale|Corso|Piazza|Vicolo) [a-zA-Z]+ [a-zA-Z]+ '
                           r'(200|1[0-9]{2}|[1-9][0-9]?[A-F](/[A-F])?|[1-9][0-9]?(/[A-F])?)$')
        try:
            #Controlla la lunghezza del numero, deve essere per forza di 10 cifre
            if len(dati_tupla[4]) == 10 and dati_tupla[4].isdigit():
                #CONTROLLO CHE I CAMPI SIANO VUOTI, SE UNO È VUOTO FA PARTIRE MESSAGGIO ERRORE
                if all(elemento_dati != "" for elemento_dati in dati_tupla):
                    #CONTROLLO CHE IN NOME E COGNOME NON CI SIANO NUMERI
                    if dati_tupla[0].isalpha() and dati_tupla[1].isalpha():
                        #fa un controllo con email_check e il campo inserito
                        #controlla che la lunghezza sia maggiore di 10
                        if re.match(email_check, dati_tupla[5]) and 10 < len(dati_tupla[5]) < 40:
                            #Controlla con indirizzo_check che i campi e le regole siano rispettate
                            if re.match(indirizzo_check, dati_tupla[2]):
                                cursor = db.cursor()
                                query = """
                                    CREATE TABLE IF NOT EXISTS tabella_clienti (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    nome VARCHAR(255),
                                    cognome VARCHAR(255),
                                    indirizzo VARCHAR(255),
                                    prefisso INT,
                                    numero BIGINT,
                                    email VARCHAR(255)
                                    )
                                        """
                                cursor.execute(query)

                                query_insert = """
                                    INSERT INTO tabella_clienti (nome, cognome, indirizzo, prefisso, numero, email)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                    """
                                cursor.execute(query_insert, dati_tupla)
                                db.commit()
                                cursor.close()

                            else:
                                messagebox.showwarning("Errore", "Assicurati che l'indirizzo sia valido")
                        else:
                            messagebox.showwarning("Errore", "Assicurati che l'email sia valida")
                    else:
                        messagebox.showwarning("Errore", "Assicurati che nome e cognome siano stringhe")
                else:
                    messagebox.showwarning("Errore", "Assicurati di inserire tutti i paragrafi")
            else:
                messagebox.showwarning("Errore", "Assicurati di inserire un numero di 10 cifre!")
        except ValueError:
            messagebox.showwarning("Errore", "Assicurati di inserire un numero valido!")

    #Viene chiamata se premuta il tasto CANC nella sezione inserimento
    def clear_text(self):
        self.set_text_nome.delete(0, tk.END)
        self.set_text_cognome.delete(0, tk.END)
        self.set_text_indirizzo.delete(0, tk.END)
        self.set_text_numero.delete(0, tk.END)
        self.set_text_email.delete(0, tk.END)

    #Interfaccia di ricerca, visualizzazione, modifica ed eliminazione dei dati del database
    def show_third_interface(self):
        #Widget nascosti dell'interfaccia principale e secondaria
        self.text_Inserimento_nome.place_forget()
        self.text_spiegazione.place_forget()
        self.text_Inserimento_cognome.place_forget()
        self.button_to_third_interface.place_forget()
        self.text_benvenuto.place_forget()
        self.set_text_nome.place_forget()
        self.set_text_cognome.place_forget()
        self.set_text_indirizzo.place_forget()
        self.set_Inserimento_indirizzo.place_forget()
        self.button_to_main_interface.place(x=575, y=250)
        self.set_text_numero.place_forget()
        self.set_Inserimento_numero.place_forget()
        self.prefissi.place_forget()
        self.set_Inserimento_email.place_forget()
        self.set_text_email.place_forget()
        self.text_CANC.place_forget()
        self.text_Enter.place_forget()
        self.buttonDB.place_forget()
        self.ex_frame.place_forget()
        self.explanation_frame.place_forget()

        #Nel caso in cui si fosse eliminato il database e si accede all'interfaccia prima di aver creato la tabella
        #Nella seconda interfaccia durante l'inserimento, la tabella viene creata qui ma riporterà 0 campi
        cursor = db.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS tabella_clienti (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255),
        cognome VARCHAR(255),
        indirizzo VARCHAR(255),
        prefisso INT,                                            
        numero BIGINT,                                        
        email VARCHAR(255)
        )
        """
        cursor.execute(query)
        db.commit()
        cursor.close()

        self.db_list.place(x=450, y=10)

        #Prendo le tuple restituite dalle funzioni ottieni_***** e le converto in stringhe in modo da poterle visualizzare
        lista_nomi_tupla = self.ottieni_nomi()
        lista_nomi_str = [f"{i[0]} {i[1]}" for i in lista_nomi_tupla]

        lista_cognomi_tupla = self.ottieni_cognomi()
        lista_cognomi_str = [f"{i[0]} {i[1]}" for i in lista_cognomi_tupla]

        lista_indirizzi_tupla = self.ottieni_indirizzo()
        lista_indirizzi_str = [f"{i[0]} {i[1]}" for i in lista_indirizzi_tupla]

        lista_prefissi_tupla = self.ottieni_prefisso()
        lista_prefissi_str = [f"{i[0]} {i[1]}" for i in lista_prefissi_tupla]

        lista_numeri_tupla = self.ottieni_numero()
        lista_numeri_str = [f"{i[0]} {i[1]}" for i in lista_numeri_tupla]

        lista_email_tupla = self.ottieni_email()
        lista_email_str = [f"{i[0]} {i[1]}" for i in lista_email_tupla]

        #A differenza di altri widget, che non si modificano tra una funzione e l'altra, lista_******* riporta a video
        #I valori restituiti dalle funzioni ottieni_***** trasformati in stringa
        self.nome_label.place(x=10, y=96)
        self.lista_nomi = ttk.Combobox(self, values=lista_nomi_str, state='readonly')
        self.lista_nomi.place(x=100, y=100)
        self.update_nome.place(x=280, y=98)
        self.update_nome_entry.place(x=380, y=100)

        self.cognome_label.place(x=10, y=136)
        self.lista_cognomi = ttk.Combobox(self, values=lista_cognomi_str, state='readonly')
        self.lista_cognomi.place(x=100, y=140)
        self.update_cognome.place(x=280, y=138)
        self.update_cognome_entry.place(x=380, y=142)

        self.indirizzo_label.place(x=10, y=176)
        self.lista_indirizzi = ttk.Combobox(self, values=lista_indirizzi_str, state='readonly')
        self.lista_indirizzi.place(x=100, y=180)
        self.update_indirizzi.place(x=280, y=178)
        self.update_indirizzi_entry.place(x=380, y=182)

        self.prefisso_label.place(x=10, y=216)
        self.lista_prefissi = ttk.Combobox(self, values=lista_prefissi_str, state='readonly')
        self.lista_prefissi.place(x=100, y=220)
        self.update_prefissi.place(x=280, y=218)
        self.update_prefissi_entry.place(x=380, y=222)

        self.numero_label.place(x=10, y=256)
        self.lista_numeri = ttk.Combobox(self, values=lista_numeri_str, state='readonly')
        self.lista_numeri.place(x=100, y=260)
        self.update_numeri.place(x=280, y=258)
        self.update_numeri_entry.place(x=380, y=262)

        self.email_label.place(x=10, y=296)
        self.lista_email = ttk.Combobox(self, values=lista_email_str, state='readonly')
        self.lista_email.place(x=100, y=300)
        self.update_email.place(x=280, y=298)
        self.update_email_entry.place(x=380, y=302)

        #Inizia una query in cui prende i dati dal DB, li inserisce nella variabile records
        #Dopo aver creato un widget di visualizzazione, inserisce nel widget i dati precedentemente richiamati dal DB
        cursor = db.cursor()
        sql = "SELECT id ,nome, cognome, indirizzo, prefisso, numero, email FROM tabella_clienti"
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()

        self.tree_frame = Frame(self)
        self.tree_frame.place(x=800, y=80, width=865, height=400)

        tree_scrollbar = Scrollbar(self.tree_frame)
        tree_scrollbar.pack(side=RIGHT, fill=Y)

        colonne = ("ID", "Nome", "Cognome", "Indirizzo", "Prefisso", "Numero", "Email")
        self.visual_tutto = ttk.Treeview(self.tree_frame, columns=colonne, show='headings',
                                         yscrollcommand=tree_scrollbar.set)
        self.visual_tutto.place(x=0, y=0, width=850, height=400)

        larghezza_colonne = [50, 100, 100, 200, 50, 100, 300]
        for i, col in enumerate(colonne):
            self.visual_tutto.heading(col, text=col)
            self.visual_tutto.column(col, width=larghezza_colonne[i], minwidth=50, stretch=tk.YES)

        for record in records:
            self.visual_tutto.insert("", tk.NO, values=record)

        tree_scrollbar.config(command=self.visual_tutto.yview)
        self.visual_tutto.bind("<Button-3>", self.visual_evento_mouseclick)
        self.visual_tutto.bind("<Double-1>", self.visual_evento_mouseclick)

        self.search_button.place(x=670, y=425)
        self.search_entry.place(x=670, y=460)

        self.delete_button.place(x=500, y=425)
        self.id_entry.place(x=500, y=460)

        cursor = db.cursor()
        sql_count = "SELECT COUNT(id) FROM tabella_clienti"
        cursor.execute(sql_count)
        id_max = cursor.fetchone()
        cursor.close()
        id_max = id_max[0]

        self.id_count = ttk.Label(self, text=f"Il database ha {id_max} clienti", background="#0080ff",
                                  font=("Arial", 20))
        self.id_count.place(x=800, y=20)

    #Viene chiamata quando si clicca col tasto destro del mouse(button-3) una riga nell'albero di visualizzazione
    #All'evento del click, seleziona la riga e mostra il menò popup definito nel costruttore(si trova verso la fine)
    def visual_evento_mouseclick(self, event):
        # Selezionare la riga cliccata
        item = self.visual_tutto.identify_row(event.y)
        if item:
            self.visual_tutto.selection_set(item)
            # Mostra il menu contestuale
            self.popup_menu.post(event.x_root, event.y_root)

    #Viene chiamata nell'evento in cui si clicca "visualizza nota" all'interno del menù popup
    #Prende l'ID della riga selezionata e seleziona dal db la nota corrispettiva all'id selezionato
    #Se la nota è NULL, stampa un messaggio prefissato
    def visual_note(self):
        visual_note = tk.Toplevel(self)
        visual_note.title("Note Personalizzate")
        visual_note.geometry("300x150+1200+250")

        selected_item = self.visual_tutto.selection()[0]
        riga = self.visual_tutto.item(selected_item, "values")
        id_selected = riga[0]
        cursor = db.cursor()
        sql = "SELECT note FROM tabella_clienti WHERE id = %s"
        cursor.execute(sql, (id_selected,))
        record = cursor.fetchone()
        cursor.close()
        nota_str = record[0]
        if nota_str is None:
            nota_str = "Non esistono memo"
        testo_label = nota_str
        label = tk.Label(visual_note, text=testo_label)
        label.pack(padx=20, pady=20, fill=tk.X)

    #Viene chiamata nell'evento in cui si clicca "aggiungi nota" all'interno del menù popup
    #Crea un label in cui si scrive una stringa alphanumerica
    #Nell'evento in cui si clicca con il tasto ENTER viene chiamata la funzione di inserimento dati nel DataBase
    def input_note(self):
        inserisci_note = tk.Toplevel(self)
        inserisci_note.title("Note Personalizzate")
        inserisci_note.geometry("300x150+1200+250")

        self.inserimento = ttk.Entry(inserisci_note, width=30)
        self.inserimento.pack(padx=20, pady=20)
        self.inserimento.bind("<Return>", self.enter_event)

    #Richiama la funzione aggiungi_note, non è stato possibile farlo direttamente nella funzione input_note perché
    #Richiamava la funzione aggiungi_note indipendentemente dall'evento fisico di premere il tasto ENTER
    def enter_event(self, _):
        self.aggiungi_note()

    #Altera la tabella, aggiungendo la colonna note, seleziona l'ID della riga e inserisce nel DataBase
    #nella riga corrispettiva all'ID precedentemente selezionato
    def aggiungi_note(self):
        nota = self.inserimento.get()
        self.inserimento.delete(0, tk.END)
        cursor = db.cursor()
        sql = """
            ALTER TABLE tabella_clienti
            ADD COLUMN IF NOT EXISTS note VARCHAR(255)
            """
        cursor.execute(sql)
        db.commit()
        selected_item = self.visual_tutto.selection()[0]
        riga = self.visual_tutto.item(selected_item, "values")
        id_selected = riga[0]
        query = """
        UPDATE tabella_Clienti SET note =%s
        WHERE id = %s
        """
        cursor.execute(query, (nota, id_selected))
        db.commit()

    #Funzione di ricerca LOCALE nell'Albero di visualizzazione, ricerca nei dati inseriti(children) il corrispettivo
    #Di ciò che si è scritto nell'entry, se l'ha trovato, lo inserisce in found_indices
    #Dopodiché quando si preme il pulsante "CERCA" contrassegna in blu i found_indices corrispettivi dell'albero
    def search_tree(self):
        search_value = self.search_entry.get()
        if not search_value:
            messagebox.showwarning("Attenzione", "Per favore, inserisci un valore da cercare.")
            return

        self.found_indices = []
        for row in self.visual_tutto.get_children():
            row_values = self.visual_tutto.item(row, "values")
            if search_value in row_values:
                self.found_indices.append(row)  # Scorri fino alla riga trovata

        if not self.found_indices:
            messagebox.showinfo("Risultato della ricerca",
                                f"Nessuna riga trovata con il valore '{search_value}'.")
            return

        self.current_index = (self.current_index + 1) % len(self.found_indices)

        row = self.found_indices[self.current_index]
        self.visual_tutto.selection_set(row)
        self.visual_tutto.focus(row)
        self.visual_tutto.see(row)

    #Ottiene il campo e contrassegna tutta la regola per l'eliminazione dal DataBase
    #Se l'ID è vuoto, Errore
    def delete_row(self):
        id_to_delete = self.id_entry.get()
        if not id_to_delete:
            messagebox.showwarning("Attenzione", "Per favore, inserisci un ID.")
            return

        try:
            cursor = db.cursor()

            sql = "DELETE FROM tabella_clienti WHERE id = %s"
            cursor.execute(sql, (id_to_delete,))
            db.commit()

            id_deleted = cursor.rowcount
            cursor.close()
            if id_deleted > 0:
                self.id_entry.delete(0, tk.END)
                self.show_main_interface()
                self.show_third_interface()
                messagebox.showinfo("Successo", f"Sono state eliminate {id_deleted}"
                                                f" righe con ID {id_to_delete}.")

            else:
                messagebox.showinfo("Informazione", f"Nessuna riga trovata con ID {id_to_delete}.")
        except mysql.connector.Error as error:
            messagebox.showerror("Errore", f"Si è verificato un errore: {error}")

    #Le funzioni update_column_record_****** vengono chiamate quando viene premuto il tasto "modifica riga"
    #Esse ottengono l'ID della riga selezionata e il campo alla destra di "modifica riga" e va a modificare il DataBase
    #della riga corrispettiva con il nuovo campo selezionato
    def update_column_record_nome(self):
        record_change = self.update_nome_entry.get()
        selected_id = self.get_selected_id_nome()
        self.update_nome_entry.delete(0, tk.END)

        if record_change != "" and selected_id is not None:
            if record_change.isalpha():

                cursor = db.cursor()

                sql_update = "UPDATE tabella_clienti SET nome = %s WHERE id = %s"
                cursor.execute(sql_update, (record_change, selected_id))

                db.commit()

                cursor.close()
            else:
                messagebox.showerror("Errore", "Inserisci un nome valido")
        else:
            messagebox.showerror("Errore", "Non hai selezionato nulla")

        self.show_main_interface()
        self.show_third_interface()

    def update_column_record_cognome(self):
        record_change = self.update_cognome_entry.get()
        selected_id = self.get_selected_id_cognome()
        self.update_cognome_entry.delete(0, tk.END)

        if record_change != "" and selected_id is not None:
            if record_change.isalpha():
                cursor = db.cursor()

                sql_update = "UPDATE tabella_clienti SET cognome = %s WHERE id = %s"
                cursor.execute(sql_update, (record_change, selected_id))

                db.commit()

                self.show_main_interface()
                self.show_third_interface()

                cursor.close()
            else:
                messagebox.showerror("Errore", "Inserisci un cognome valido")
        else:
            messagebox.showerror("Errore", "Non hai selezionato nulla")

    def update_column_record_indirizzi(self):
        record_change = self.update_indirizzi_entry.get()
        selected_id = self.get_selected_id_indirizzi()
        self.update_indirizzi_entry.delete(0, tk.END)
        indirizzo_check = (r'^(via|viale|corso|piazza|vicolo) [a-zA-Z]+ [a-zA-Z]+ '
                           r'(200|1[0-9]{2}|[1-9][0-9]?[A-F](/[A-F])?|[1-9][0-9]?(/[A-F])?)$')

        if record_change != "" and selected_id is not None:
            if re.match(indirizzo_check, record_change):

                cursor = db.cursor()

                sql_update = "UPDATE tabella_clienti SET indirizzo = %s WHERE id = %s"
                cursor.execute(sql_update, (record_change, selected_id))

                db.commit()
                self.show_main_interface()
                self.show_third_interface()
                cursor.close()
            else:
                messagebox.showerror("Errore", "Inserisci un indirizzo valido")
        else:
            messagebox.showerror("Errore", "Non hai selezionato nulla")

    def update_column_record_prefissi(self, prefissi):
        record_change = self.update_prefissi_entry.get()
        selected_id = self.get_selected_id_prefissi()
        self.update_prefissi_entry.delete(0, tk.END)
        record__change = int(record_change)

        if record__change != "" and selected_id is not None:
            if record__change in prefissi:
                cursor = db.cursor()

                sql_update = "UPDATE tabella_clienti SET prefisso = %s WHERE id = %s"
                cursor.execute(sql_update, (record_change, selected_id))

                db.commit()
                self.show_main_interface()
                self.show_third_interface()
                cursor.close()
            else:
                messagebox.showerror("Errore", "Il prefisso non è valido")
        else:
            messagebox.showerror("Errore", "Non hai selezionato nulla")

    def update_column_record_numero(self):
        record_change = self.update_numeri_entry.get()
        selected_id = self.get_selected_id_numero()
        self.update_numeri_entry.delete(0, tk.END)

        if record_change != "" and selected_id is not None:
            if record_change.isdigit():
                if len(record_change) == 10:

                    cursor = db.cursor()

                    sql_update = "UPDATE tabella_clienti SET numero = %s WHERE id = %s"
                    cursor.execute(sql_update, (record_change, selected_id))

                    db.commit()
                    self.show_main_interface()
                    self.show_third_interface()
                    cursor.close()
                else:
                    messagebox.showerror("Errore", "Il numero deve essere di 10 cifre")
            else:
                messagebox.showerror("Errore", "Il numero può contenere solo cifre digitali")
        else:
            messagebox.showerror("Errore", "Non hai selezionato nulla")

    def update_column_record_email(self):
        record_change = self.update_email_entry.get()
        selected_id = self.get_selected_id_email()
        self.update_email_entry.delete(0, tk.END)
        email_check = r'^[a-zA-Z0-9._]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'

        if record_change != "" and selected_id is not None:
            if re.match(email_check, record_change) and 10 < len(dati_tupla[5]) < 40:

                cursor = db.cursor()

                sql_update = "UPDATE tabella_clienti SET email = %s WHERE id = %s"
                cursor.execute(sql_update, (record_change, selected_id))

                db.commit()

                self.show_main_interface()
                self.show_third_interface()

                cursor.close()
            else:
                messagebox.showerror("Errore", "L'email deve essere valida")
        else:
            messagebox.showerror("Errore", "Non hai selezionato nulla")

    #Le funzioni get_selected_id_***** vengono richiamate per modificare i campi nel DataBase
    #Seleziona la tupla selezionata nel Combobox, la divide dagli spazi e prende solo il primo campo, ovvero L'ID
    #restituisce alle funzioni l'ID Selezionato
    def get_selected_id_nome(self):
        selected_nome = self.lista_nomi.get()
        lista_divisa = selected_nome.split(' ')
        id_ = lista_divisa[0]
        return id_

    def get_selected_id_cognome(self):
        selected_cognome = self.lista_cognomi.get()
        lista_divisa = selected_cognome.split(' ')
        id_ = lista_divisa[0]
        return id_

    def get_selected_id_indirizzi(self):
        selected_indirizzi = self.lista_indirizzi.get()
        lista_divisa = selected_indirizzi.split(' ')
        id_ = lista_divisa[0]
        return id_

    def get_selected_id_prefissi(self):
        selected_prefissi = self.lista_prefissi.get()
        lista_divisa = selected_prefissi.split(' ')
        id_ = lista_divisa[0]
        return id_

    def get_selected_id_numero(self):
        selected_numero = self.lista_numeri.get()
        lista_divisa = selected_numero.split(' ')
        id_ = lista_divisa[0]
        return id_

    def get_selected_id_email(self):
        selected_email = self.lista_email.get()
        lista_divisa = selected_email.split(' ')
        id_ = lista_divisa[0]
        return id_

    #Interfaccia di Inserimento dati
    def show_second_interface(self):
        #Widget nascosti dell'interfaccia principale
        self.button_to_second_interface.place_forget()
        self.text_spiegazione.place_forget()
        self.text_benvenuto.place_forget()
        self.nome_label.place_forget()
        self.lista_nomi.place_forget()
        self.cognome_label.place_forget()
        self.lista_cognomi.place_forget()
        self.indirizzo_label.place_forget()
        self.lista_indirizzi.place_forget()
        self.prefisso_label.place_forget()
        self.lista_prefissi.place_forget()
        self.numero_label.place_forget()
        self.lista_numeri.place_forget()
        self.email_label.place_forget()
        self.lista_email.place_forget()
        self.tree_frame.place_forget()
        self.search_entry.place_forget()
        self.search_button.place_forget()
        self.delete_button.place_forget()
        self.id_entry.place_forget()
        self.update_nome_entry.place_forget()
        self.update_nome.place_forget()
        self.update_nome.place_forget()
        self.update_nome_entry.place_forget()
        self.update_cognome.place_forget()
        self.update_cognome_entry.place_forget()
        self.update_indirizzi.place_forget()
        self.update_indirizzi_entry.place_forget()
        self.update_indirizzi.place_forget()
        self.update_prefissi.place_forget()
        self.update_prefissi_entry.place_forget()
        self.update_numeri.place_forget()
        self.update_numeri_entry.place_forget()
        self.update_email.place_forget()
        self.update_email_entry.place_forget()
        self.id_count.place_forget()

        self.buttonDB = ttk.Button(self, text="Invio dati al database", command=lambda: self.invio_dati_db(dati_tupla))
        self.buttonDB.place(x=800, y=193)

        #Lista predefinita di prefissi, convertita poi in stringa per mostrare il "+" durante la parte visiva
        prefissi = [30, 31, 32, 33, 350, 351, 352, 353, 39]
        prefissi_str = ["+" + str(prefisso) for prefisso in prefissi]
        self.prefissi = ttk.Combobox(self, values=prefissi_str, state='readonly', width=5)
        self.prefissi.place(x=580, y=165)

        self.text_CANC = ttk.Label(self, text='Premi Canc per eliminare tutti i dati', background='#0080ff',
                                   font=("Arial", 18))
        self.text_CANC.place(x=990, y=70)
        self.text_Enter = ttk.Label(self, text='Premi Enter per Registrare i dati in memoria', background='#0080ff',
                                    font=("Arial", 18))
        self.text_Enter.place(x=990, y=130)

        #INSERIMENTO NOME
        self.text_Inserimento_nome.place(x=390, y=70)
        self.set_text_nome = ttk.Entry(self)
        self.set_text_nome.place(x=650, y=75)
        self.set_text_nome.bind("<Return>", lambda event: self.dati_inseriti(self.set_text_nome.get(),
                                                                             self.set_text_cognome.get(),
                                                                             self.set_text_indirizzo.get(),
                                                                             self.prefissi.get(),
                                                                             self.set_text_numero.get(),
                                                                             self.set_text_email.get()))
        self.set_text_nome.bind("<Delete>", lambda event: self.clear_text())

        #INSERIMENTO COGNOME
        self.text_Inserimento_cognome.place(x=390, y=100)
        self.set_text_cognome = ttk.Entry(self)
        self.set_text_cognome.place(x=650, y=105)
        self.set_text_cognome.bind("<Return>", lambda event: self.dati_inseriti(self.set_text_nome.get(),
                                                                                self.set_text_cognome.get(),
                                                                                self.set_text_indirizzo.get(),
                                                                                self.prefissi.get(),
                                                                                self.set_text_numero.get(),
                                                                                self.set_text_email.get()))
        self.set_text_cognome.bind("<Delete>", lambda event: self.clear_text())

        #INSERIMENTO INDIRIZZO
        self.set_Inserimento_indirizzo.place(x=390, y=130)
        self.set_text_indirizzo = ttk.Entry(self)
        self.set_text_indirizzo.place(x=650, y=135)
        self.set_text_indirizzo.bind("<Return>", lambda event: self.dati_inseriti(self.set_text_nome.get(),
                                                                                  self.set_text_cognome.get(),
                                                                                  self.set_text_indirizzo.get(),
                                                                                  self.prefissi.get(),
                                                                                  self.set_text_numero.get(),
                                                                                  self.set_text_email.get()))
        self.set_text_indirizzo.bind("<Delete>", lambda event: self.clear_text())

        #INSERIMENTO TELEFONO
        self.set_Inserimento_numero.place(x=390, y=160)
        self.set_text_numero = ttk.Entry(self)
        self.set_text_numero.place(x=650, y=165)
        self.set_text_numero.delete(0, tk.END)
        self.set_text_numero.bind("<Return>", lambda event: self.dati_inseriti(self.set_text_nome.get(),
                                                                               self.set_text_cognome.get(),
                                                                               self.set_text_indirizzo.get(),
                                                                               self.prefissi.get(),
                                                                               self.set_text_numero.get(),
                                                                               self.set_text_email.get()))
        self.set_text_numero.bind("<Delete>", lambda event: self.clear_text())

        #INSERIMENTO EMAIL
        self.set_Inserimento_email.place(x=390, y=190)
        self.set_text_email = ttk.Entry(self)
        self.set_text_email.place(x=650, y=195)
        self.set_text_email.bind("<Return>", lambda event: self.dati_inseriti(self.set_text_nome.get(),
                                                                              self.set_text_cognome.get(),
                                                                              self.set_text_indirizzo.get(),
                                                                              self.prefissi.get(),
                                                                              self.set_text_numero.get(),
                                                                              self.set_text_email.get()))
        self.set_text_email.bind("<Delete>", lambda event: self.clear_text())

        self.button_to_main_interface.place(x=650, y=250)

        self.explanation_frame.place(x=990, y=200, width=700, height=270)
        self.explanation_frame.config(background='#0066cc')
        explanation_nome = ttk.Label(self.explanation_frame, text="Un nome può essere composto "
                                                                  "solo da una serie di lettere.",
                                     font=("Arial", 15), background='#0066cc')
        explanation_nome.place(x=0, y=0)

        explanation_cognome = ttk.Label(self.explanation_frame,
                                        text="Un cognome può essere composto solo da una serie di lettere. ",
                                        font=("Arial", 15), background='#0066cc')
        explanation_cognome.place(x=0, y=40)

        explanation_indirizzo = ttk.Label(self.explanation_frame,
                                          text="Un indirizzo deve iniziare obbligatoriamente con Via/Viale,Corso/Piazza,"
                                               "Vicolo\nDeve poi continuare con nome e cognome della via e del civico \n"
                                               "il civico può essere composto da solo un numero o un numero e /Lettera",
                                          font=("Arial", 15), background='#0066cc')
        explanation_indirizzo.place(x=0, y=80)

        explanation_numero = ttk.Label(self.explanation_frame,
                                       text="Un numero può essere composto solo da 10 cifre numeriche",
                                       font=("Arial", 15), background='#0066cc')
        explanation_numero.place(x=0, y=170)

        explanation_email = ttk.Label(self.explanation_frame,
                                      text="Un'email deve per forza avere un campo alfanumerico, una chiocciola\n"
                                           "un campo alfanumerico, un dominio email un punto ed un TLD",
                                      font=("Arial", 15), background='#0066cc')
        explanation_email.place(x=0, y=210)

        self.ex_frame.place(x=25, y=70, width=350, height=200)
        self.ex_frame.config(background='#0066cc')

        ex = ttk.Label(self.ex_frame, text="ESEMPI", font=("Arial", 17), background='#0066cc')
        ex.place(x=105, y=0)
        ex_nome = ttk.Label(self.ex_frame, text="Nome:       Roberta", font=("Arial", 14), background='#0066cc')
        ex_nome.place(x=0, y=40)

        ex_cognome = ttk.Label(self.ex_frame, text="cognome: Gioia", font=("Arial", 14), background='#0066cc')
        ex_cognome.place(x=0, y=70)

        ex_indirizzo = ttk.Label(self.ex_frame, text="Indirizzo:   Via Gugliemo Marconi 14/F",
                                 font=("Arial", 14), background='#0066cc')
        ex_indirizzo.place(x=0, y=100)

        ex_numero = ttk.Label(self.ex_frame, text="Numero:    3455643226",
                              font=("Arial", 14), background='#0066cc')
        ex_numero.place(x=0, y=130)

        ex_email = ttk.Label(self.ex_frame, text="email:        Roberta.Gioia99@gmail.com",
                             font=("Arial", 14), background='#0066cc')
        ex_email.place(x=0, y=160)

    #INTERFACCIA PRINCIPALE
    def show_main_interface(self):
        # Nascondi widget dell'interfaccia secondaria
        self.button_to_main_interface.place_forget()
        self.text_Inserimento_nome.place_forget()
        self.text_Inserimento_cognome.place_forget()
        self.set_text_cognome.place_forget()
        self.set_text_nome.place_forget()
        self.set_text_numero.place_forget()
        self.set_Inserimento_numero.place_forget()
        self.set_text_indirizzo.place_forget()
        self.set_Inserimento_indirizzo.place_forget()
        self.set_Inserimento_email.place_forget()
        self.set_text_email.place_forget()
        self.prefissi.place_forget()
        self.buttonDB.place_forget()
        self.text_Enter.place_forget()
        self.text_CANC.place_forget()
        self.lista_nomi.place_forget()
        self.db_list.place_forget()
        self.nome_label.place_forget()
        self.lista_nomi.place_forget()
        self.cognome_label.place_forget()
        self.lista_cognomi.place_forget()
        self.indirizzo_label.place_forget()
        self.lista_indirizzi.place_forget()
        self.prefisso_label.place_forget()
        self.lista_prefissi.place_forget()
        self.numero_label.place_forget()
        self.lista_numeri.place_forget()
        self.email_label.place_forget()
        self.lista_email.place_forget()
        self.tree_frame.place_forget()
        self.search_entry.place_forget()
        self.search_button.place_forget()
        self.delete_button.place_forget()
        self.id_entry.place_forget()
        self.update_nome_entry.place_forget()
        self.update_nome.place_forget()
        self.update_nome_entry.place_forget()
        self.update_nome.place_forget()
        self.update_nome.place_forget()
        self.update_nome_entry.place_forget()
        self.update_cognome.place_forget()
        self.update_cognome_entry.place_forget()
        self.update_indirizzi.place_forget()
        self.update_indirizzi_entry.place_forget()
        self.update_indirizzi.place_forget()
        self.update_prefissi.place_forget()
        self.update_prefissi_entry.place_forget()
        self.update_numeri.place_forget()
        self.update_numeri_entry.place_forget()
        self.update_email.place_forget()
        self.update_email_entry.place_forget()
        self.id_count.place_forget()
        self.ex_frame.place_forget()
        self.explanation_frame.place_forget()

        self.text_spiegazione.place(x=450, y=100)
        self.text_benvenuto.place(x=450, y=10)
        self.button_to_third_interface.place(x=575, y=250)
        self.button_to_second_interface.place(x=650, y=250)

    #Nell'evento in cui le dimensioni della finestra cambino, viene richiamata creando un nuovo sfondo con le dimensioni
    #modificate, al momento crea problema di prestazione quindi non utilizzata
    """
    def resizer(self, e):
        global bg1, resized_bg, new_bg
        bg1 = Image.open("azure.jpg")
        new_width = self.winfo_width()
        new_height = self.winfo_height()
        resized_bg = bg1.resize((new_width, new_height), Image.Resampling.LANCZOS)
        new_bg = ImageTk.PhotoImage(resized_bg)
        self.my_canvas.create_image(0, 0, image=new_bg, anchor="nw")
    """
    #Ottiene il tempo reale e lo trasmuta in stringa con il formato %Y-%m-%d %H:%M:%S, aspetta 1 secondo per richiamarsi
    #Non è performante senza i secondi a quanto pare inizia il countdown appena avviata l'applicazione
    def tempo_real_time(self):
        self.tempotext.set(datetime.now().strftime('%d/%m/%Y    %H:%M:%S'))
        self.after(1000, self.tempo_real_time)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
