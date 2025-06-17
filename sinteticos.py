import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os

class SyntheticsFilterApp:
    def __init__(self, master):
        self.master = master
        master.title("Filtro de Sintéticos")
        master.geometry('600x600')
        master.resizable(False, False)
        
        # Configurar colores modernos
        self.colors = {
            'primary': '#2563eb',      # Azul moderno
            'primary_hover': '#1d4ed8', # Azul más oscuro
            'secondary': '#64748b',     # Gris azulado
            'success': '#059669',       # Verde
            'background': '#f8fafc',    # Gris muy claro
            'card_bg': '#ffffff',       # Blanco
            'text_primary': '#1e293b',  # Gris oscuro
            'text_secondary': '#64748b', # Gris medio
            'border': '#e2e8f0'        # Gris claro
        }
        
        # Configurar el fondo principal
        master.config(bg=self.colors['background'])
        
        # Configurar estilos
        self.setup_styles()
        
        # Crear interfaz
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        # Variables de ruta
        self.excel_path = None
        self.txt_path = None

    def setup_styles(self):
        """Configurar estilos personalizados"""
        style = ttk.Style()
        
        # Estilo para botones principales
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['primary_hover']),
                           ('pressed', self.colors['primary_hover'])])
        
        # Estilo para botones secundarios
        style.configure('Secondary.TButton',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       relief='solid',
                       focuscolor='none',
                       font=('Segoe UI', 9))
        
        # Estilo para frames
        style.configure('Card.TFrame',
                       background=self.colors['card_bg'],
                       relief='flat',
                       borderwidth=1)

    def create_header(self):
        """Crear encabezado moderno"""
        header_frame = tk.Frame(self.master, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Título principal
        title_label = tk.Label(header_frame, 
                              text="🔍 Filtro de Sintéticos",
                              font=('Segoe UI', 18, 'bold'),
                              fg='white',
                              bg=self.colors['primary'])
        title_label.pack(expand=True)
        
        # Subtítulo
        subtitle_label = tk.Label(header_frame,
                                 text="Herramienta avanzada para filtrado de datos",
                                 font=('Segoe UI', 9),
                                 fg='white',
                                 bg=self.colors['primary'])
        subtitle_label.pack(pady=(0, 10))

    def create_main_content(self):
        """Crear contenido principal"""
        # Frame principal con padding
        main_frame = tk.Frame(self.master, bg=self.colors['background'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Card para selección de Excel
        self.create_file_card(main_frame, 
                             "📊 Archivo Excel",
                             "Seleccione el archivo Excel con la columna 'SINTETICOS'",
                             "excel")
        
        # Separador
        separator = tk.Frame(main_frame, height=15, bg=self.colors['background'])
        separator.pack(fill='x')
        
        # Card para selección de TXT
        self.create_file_card(main_frame,
                             "📄 Archivo TXT", 
                             "Seleccione el archivo TXT que desea filtrar",
                             "txt")
        
        # Separador antes del botón
        separator2 = tk.Frame(main_frame, height=20, bg=self.colors['background'])
        separator2.pack(fill='x')
        
        # Botón principal de filtrado
        self.btn_filter = tk.Button(main_frame,
                                   text="🚀 Procesar y Filtrar Datos",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=self.colors['success'],
                                   fg='white',
                                   relief='flat',
                                   padx=30,
                                   pady=12,
                                   cursor='hand2',
                                   command=self.filter_lines)
        self.btn_filter.pack(pady=10)
        
        # Efecto hover para botón principal
        def on_enter_main(e):
            e.widget.config(bg='#047857')  # Verde más oscuro
        def on_leave_main(e):
            e.widget.config(bg=self.colors['success'])
        
        self.btn_filter.bind('<Enter>', on_enter_main)
        self.btn_filter.bind('<Leave>', on_leave_main)
        
        # Barra de progreso (oculta inicialmente)
        self.progress_frame = tk.Frame(main_frame, bg=self.colors['background'])
        self.progress_frame.pack(fill='x', pady=(10, 0))
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, 
                                          mode='indeterminate',
                                          style='TProgressbar')

    def create_file_card(self, parent, title, description, file_type):
        """Crear tarjeta para selección de archivo"""
        # Frame de la tarjeta
        card_frame = tk.Frame(parent, 
                             bg=self.colors['card_bg'],
                             relief='solid',
                             bd=1)
        card_frame.pack(fill='x', pady=5)
        
        # Contenido de la tarjeta
        content_frame = tk.Frame(card_frame, bg=self.colors['card_bg'])
        content_frame.pack(fill='x', padx=20, pady=15)
        
        # Título
        title_label = tk.Label(content_frame,
                              text=title,
                              font=('Segoe UI', 12, 'bold'),
                              fg=self.colors['text_primary'],
                              bg=self.colors['card_bg'],
                              anchor='w')
        title_label.pack(fill='x')
        
        # Descripción
        desc_label = tk.Label(content_frame,
                             text=description,
                             font=('Segoe UI', 9),
                             fg=self.colors['text_secondary'],
                             bg=self.colors['card_bg'],
                             anchor='w')
        desc_label.pack(fill='x', pady=(2, 8))
        
        # Frame para botón y archivo seleccionado
        button_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        button_frame.pack(fill='x')
        
        # Botón de selección
        if file_type == "excel":
            btn = tk.Button(button_frame,
                           text="📁 Seleccionar Excel",
                           font=('Segoe UI', 9, 'bold'),
                           bg=self.colors['primary'],
                           fg='white',
                           relief='flat',
                           padx=20,
                           pady=8,
                           cursor='hand2',
                           command=self.load_excel)
            self.lbl_excel_file = tk.Label(button_frame,
                                          text="Ningún archivo seleccionado",
                                          font=('Segoe UI', 9),
                                          fg=self.colors['text_secondary'],
                                          bg=self.colors['card_bg'])
        else:
            btn = tk.Button(button_frame,
                           text="📁 Seleccionar TXT",
                           font=('Segoe UI', 9, 'bold'),
                           bg=self.colors['primary'],
                           fg='white',
                           relief='flat',
                           padx=20,
                           pady=8,
                           cursor='hand2',
                           command=self.load_txt)
            self.lbl_txt_file = tk.Label(button_frame,
                                        text="Ningún archivo seleccionado",
                                        font=('Segoe UI', 9),
                                        fg=self.colors['text_secondary'],
                                        bg=self.colors['card_bg'])
        
        btn.pack(side='left')
        
        # Efecto hover para botones
        def on_enter(e):
            e.widget.config(bg=self.colors['primary_hover'])
        def on_leave(e):
            e.widget.config(bg=self.colors['primary'])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        # Label para mostrar archivo seleccionado
        if file_type == "excel":
            self.lbl_excel_file.pack(side='left', padx=(15, 0))
        else:
            self.lbl_txt_file.pack(side='left', padx=(15, 0))

    def create_footer(self):
        """Crear pie con información adicional"""
        footer_frame = tk.Frame(self.master, bg=self.colors['background'], height=40)
        footer_frame.pack(fill='x', side='bottom', padx=20, pady=5)
        footer_frame.pack_propagate(False)
        
        # Información del pie
        info_label = tk.Label(footer_frame,
                             text="💡 Asegúrese de que el Excel tenga una columna llamada 'SINTETICOS'",
                             font=('Segoe UI', 8),
                             fg=self.colors['text_secondary'],
                             bg=self.colors['background'])
        info_label.pack(expand=True)

    def load_excel(self):
        """Cargar archivo Excel"""
        path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx *.xls")]
        )
        if path:
            self.excel_path = path
            filename = os.path.basename(path)
            if len(filename) > 30:
                filename = filename[:27] + "..."
            self.lbl_excel_file.config(text=f"✅ {filename}",
                                      fg=self.colors['success'])

    def load_txt(self):
        """Cargar archivo TXT"""
        path = filedialog.askopenfilename(
            title="Seleccionar archivo TXT",
            filetypes=[("Archivos de Texto", "*.txt")]
        )
        if path:
            self.txt_path = path
            filename = os.path.basename(path)
            if len(filename) > 30:
                filename = filename[:27] + "..."
            self.lbl_txt_file.config(text=f"✅ {filename}",
                                    fg=self.colors['success'])

    def show_progress(self):
        """Mostrar barra de progreso"""
        self.progress_bar.pack(fill='x', pady=10)
        self.progress_bar.start(10)
        self.btn_filter.config(state='disabled', text="🔄 Procesando...")
        self.master.update()

    def hide_progress(self):
        """Ocultar barra de progreso"""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.btn_filter.config(state='normal', text="🚀 Procesar y Filtrar Datos")

    def filter_lines(self):
        """Filtrar líneas del archivo TXT"""
        if not self.excel_path or not self.txt_path:
            messagebox.showwarning("⚠️ Archivos Faltantes", 
                                 "Por favor, seleccione ambos archivos antes de continuar.")
            return

        try:
            # Mostrar progreso
            self.show_progress()
            
            # Leer sintéticos del Excel
            df = pd.read_excel(self.excel_path, dtype=str)
            if 'SINTETICOS' not in df.columns:
                self.hide_progress()
                messagebox.showerror("❌ Error de Columna", 
                                   "La columna 'SINTETICOS' no se encontró en el archivo Excel.\n\n"
                                   "Verifique que el archivo tenga la estructura correcta.")
                return
            
            synthetics = df['SINTETICOS'].dropna().astype(str).str.strip().tolist()

            # Procesar archivo TXT con codificación latin-1
            filtered = []
            total_lines = 0
            
            with open(self.txt_path, 'r', encoding='latin-1') as f:
                for line in f:
                    total_lines += 1
                    fields = [fld.strip('"') for fld in line.split(';')]
                    # Asumimos que el sintético está en la posición 8 (índice 7)
                    if len(fields) > 7 and fields[7] in synthetics:
                        filtered.append(line)

            # Guardar resultado
            base, ext = os.path.splitext(self.txt_path)
            out_path = f"{base}_filtrado.txt"
            with open(out_path, 'w', encoding='latin-1') as f_out:
                f_out.writelines(filtered)

            # Ocultar progreso
            self.hide_progress()
            
            # Mostrar resultado con estilo
            result_msg = (f"✅ Procesamiento completado con éxito!\n\n"
                         f"📊 Estadísticas:\n"
                         f"• Líneas totales procesadas: {total_lines:,}\n"
                         f"• Líneas filtradas: {len(filtered):,}\n"
                         f"• Porcentaje filtrado: {(len(filtered)/total_lines*100):.1f}%\n\n"
                         f"💾 Archivo guardado en:\n{os.path.basename(out_path)}")
            
            messagebox.showinfo("🎉 Proceso Completado", result_msg)
            
        except Exception as e:
            self.hide_progress()
            messagebox.showerror("❌ Error de Procesamiento", 
                               f"Se produjo un error durante el procesamiento:\n\n{str(e)}\n\n"
                               f"Verifique que los archivos estén en el formato correcto.")

if __name__ == '__main__':
    root = tk.Tk()
    app = SyntheticsFilterApp(root)
    root.mainloop()