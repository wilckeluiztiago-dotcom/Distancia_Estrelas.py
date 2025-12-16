"""
Calculadora Geométrica de Distância Entre Estrelas
Interface Gráfica Tkinter com Matplotlib

Autor: Luiz Tiago Wilcke
Data: 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from calculos import (
    Estrela, CoordenadaHMS, CoordenadaDMS, 
    CalculadoraGeometrica, ResultadoCalculo,
    PARSEC_PARA_ANOS_LUZ
)

# Catálogo de estrelas conhecidas
CATALOGO_ESTRELAS = [
    {"nome": "Sirius", "ar_h": 6, "ar_m": 45, "ar_s": 8.9, "dec_sinal": "-", "dec_g": 16, "dec_m": 42, "dec_s": 58, "paralaxe": 379.21},
    {"nome": "Betelgeuse", "ar_h": 5, "ar_m": 55, "ar_s": 10.3, "dec_sinal": "+", "dec_g": 7, "dec_m": 24, "dec_s": 25, "paralaxe": 4.51},
    {"nome": "Proxima Centauri", "ar_h": 14, "ar_m": 29, "ar_s": 42.9, "dec_sinal": "-", "dec_g": 62, "dec_m": 40, "dec_s": 46, "paralaxe": 768.07},
    {"nome": "Alpha Centauri A", "ar_h": 14, "ar_m": 39, "ar_s": 36.5, "dec_sinal": "-", "dec_g": 60, "dec_m": 50, "dec_s": 2, "paralaxe": 747.1},
    {"nome": "Vega", "ar_h": 18, "ar_m": 36, "ar_s": 56.3, "dec_sinal": "+", "dec_g": 38, "dec_m": 47, "dec_s": 1, "paralaxe": 130.23},
    {"nome": "Arcturus", "ar_h": 14, "ar_m": 15, "ar_s": 39.7, "dec_sinal": "+", "dec_g": 19, "dec_m": 10, "dec_s": 57, "paralaxe": 88.83},
    {"nome": "Rigel", "ar_h": 5, "ar_m": 14, "ar_s": 32.3, "dec_sinal": "-", "dec_g": 8, "dec_m": 12, "dec_s": 6, "paralaxe": 3.78},
    {"nome": "Canopus", "ar_h": 6, "ar_m": 23, "ar_s": 57.1, "dec_sinal": "-", "dec_g": 52, "dec_m": 41, "dec_s": 44, "paralaxe": 10.55},
    {"nome": "Aldebaran", "ar_h": 4, "ar_m": 35, "ar_s": 55.2, "dec_sinal": "+", "dec_g": 16, "dec_m": 30, "dec_s": 33, "paralaxe": 48.94},
    {"nome": "Capella", "ar_h": 5, "ar_m": 16, "ar_s": 41.4, "dec_sinal": "+", "dec_g": 45, "dec_m": 59, "dec_s": 53, "paralaxe": 76.20},
    {"nome": "Polaris", "ar_h": 2, "ar_m": 31, "ar_s": 49.1, "dec_sinal": "+", "dec_g": 89, "dec_m": 15, "dec_s": 51, "paralaxe": 7.54},
    {"nome": "Antares", "ar_h": 16, "ar_m": 29, "ar_s": 24.5, "dec_sinal": "-", "dec_g": 26, "dec_m": 25, "dec_s": 55, "paralaxe": 5.40},
    {"nome": "Spica", "ar_h": 13, "ar_m": 25, "ar_s": 11.6, "dec_sinal": "-", "dec_g": 11, "dec_m": 9, "dec_s": 41, "paralaxe": 13.06},
    {"nome": "Deneb", "ar_h": 20, "ar_m": 41, "ar_s": 25.9, "dec_sinal": "+", "dec_g": 45, "dec_m": 16, "dec_s": 49, "paralaxe": 2.31},
    {"nome": "Altair", "ar_h": 19, "ar_m": 50, "ar_s": 47.0, "dec_sinal": "+", "dec_g": 8, "dec_m": 52, "dec_s": 6, "paralaxe": 194.95},
    {"nome": "Procyon", "ar_h": 7, "ar_m": 39, "ar_s": 18.1, "dec_sinal": "+", "dec_g": 5, "dec_m": 13, "dec_s": 30, "paralaxe": 284.56},
    {"nome": "Regulus", "ar_h": 10, "ar_m": 8, "ar_s": 22.3, "dec_sinal": "+", "dec_g": 11, "dec_m": 58, "dec_s": 2, "paralaxe": 41.13},
    {"nome": "Fomalhaut", "ar_h": 22, "ar_m": 57, "ar_s": 39.0, "dec_sinal": "-", "dec_g": 29, "dec_m": 37, "dec_s": 20, "paralaxe": 129.81},
]


class InterfaceCalculadora:
    """Interface gráfica principal da calculadora de distância estelar"""
    
    def __init__(self, raiz: tk.Tk):
        self.raiz = raiz
        self.raiz.title("Calculadora Geométrica de Distância Entre Estrelas - Autor: Luiz Tiago Wilcke")
        self.raiz.geometry("1400x950")
        self.raiz.configure(bg='#0a0a1a')
        
        # Variáveis
        self.resultado_atual = None
        self.estrela1 = None
        self.estrela2 = None
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Criar interface
        self.criar_interface()
    
    def configurar_estilo(self):
        """Configurar estilos personalizados"""
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')
        
        self.cores = {
            'fundo': '#0a0a1a',
            'frame': '#1a1a2e',
            'destaque': '#4fc3f7',
            'texto': '#e2e8f0',
            'texto_escuro': '#a0aec0',
            'sucesso': '#68d391',
            'amarelo': '#ffd700',
            'azul': '#4a90d9',
        }
        
        self.estilo.configure('TFrame', background=self.cores['frame'])
        self.estilo.configure('TLabel', background=self.cores['frame'], 
                             foreground=self.cores['texto'], font=('Segoe UI', 10))
        self.estilo.configure('Titulo.TLabel', font=('Segoe UI', 16, 'bold'),
                             foreground=self.cores['amarelo'])
        self.estilo.configure('TLabelframe', background=self.cores['frame'])
        self.estilo.configure('TLabelframe.Label', background=self.cores['frame'],
                             foreground=self.cores['destaque'], font=('Segoe UI', 10, 'bold'))
        self.estilo.configure('TNotebook', background=self.cores['frame'])
        self.estilo.configure('TNotebook.Tab', background=self.cores['frame'],
                             foreground=self.cores['texto'], padding=[10, 5])
    
    def criar_interface(self):
        """Criar todos os elementos da interface"""
        container = ttk.Frame(self.raiz, style='TFrame')
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        titulo = ttk.Label(container, text="★ CALCULADORA DE DISTÂNCIA ENTRE ESTRELAS ★",
                          style='Titulo.TLabel')
        titulo.pack(pady=(0, 5))
        
        autor = ttk.Label(container, text="Autor: Luiz Tiago Wilcke",
                         foreground=self.cores['texto_escuro'])
        autor.pack(pady=(0, 10))
        
        # Notebook com abas
        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba 1: Calculadora
        aba_calculadora = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(aba_calculadora, text="📐 Calculadora")
        self.criar_aba_calculadora(aba_calculadora)
        
        # Aba 2: Catálogo de Estrelas
        aba_catalogo = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(aba_catalogo, text="🌟 Catálogo de Estrelas")
        self.criar_aba_catalogo(aba_catalogo)
    
    def criar_aba_calculadora(self, parent):
        """Criar aba da calculadora"""
        frame_principal = ttk.Frame(parent, style='TFrame')
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Painel esquerdo
        painel_esq = ttk.Frame(frame_principal, style='TFrame')
        painel_esq.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        self.entradas1 = self.criar_frame_estrela(painel_esq, 1)
        self.entradas2 = self.criar_frame_estrela(painel_esq, 2)
        
        # Botões
        frame_botoes = ttk.Frame(painel_esq, style='TFrame')
        frame_botoes.pack(fill=tk.X, pady=10)
        
        tk.Button(frame_botoes, text="⚡ CALCULAR", command=self.calcular,
                 bg='#667eea', fg='white', font=('Segoe UI', 11, 'bold'),
                 relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=3)
        
        tk.Button(frame_botoes, text="🗑 Limpar", command=self.limpar,
                 bg='#e53e3e', fg='white', font=('Segoe UI', 10, 'bold'),
                 relief=tk.FLAT, padx=10, pady=8).pack(side=tk.LEFT, padx=3)
        
        # Resultados em texto
        frame_res = ttk.LabelFrame(painel_esq, text="📊 Resultados", padding=5)
        frame_res.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.texto_resultados = tk.Text(frame_res, bg='#1a202c', fg='#68d391',
                                        font=('Consolas', 9), height=10, width=45, relief=tk.FLAT)
        self.texto_resultados.pack(fill=tk.BOTH, expand=True)
        
        # Painel direito
        painel_dir = ttk.Frame(frame_principal, style='TFrame')
        painel_dir.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Plano Estelar
        frame_plano = ttk.LabelFrame(painel_dir, text="🌌 Plano Estelar", padding=3)
        frame_plano.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        self.fig_plano = Figure(figsize=(7, 3.5), facecolor='#0a0a1a')
        self.ax_plano = self.fig_plano.add_subplot(111)
        self.canvas_plano = FigureCanvasTkAgg(self.fig_plano, master=frame_plano)
        self.canvas_plano.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.desenhar_plano_inicial()
        
        # Equações em texto simples (não matplotlib)
        frame_eq = ttk.LabelFrame(painel_dir, text="📐 Método Geométrico e Equações", padding=5)
        frame_eq.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.texto_equacoes = tk.Text(frame_eq, bg='#0a0a1a', fg='#e2e8f0',
                                      font=('Consolas', 10), height=12, relief=tk.FLAT,
                                      wrap=tk.WORD)
        self.texto_equacoes.pack(fill=tk.BOTH, expand=True)
        self.texto_equacoes.tag_configure('titulo', foreground='#4fc3f7', font=('Consolas', 11, 'bold'))
        self.texto_equacoes.tag_configure('subtitulo', foreground='#ffd700', font=('Consolas', 10, 'bold'))
        self.texto_equacoes.tag_configure('equacao', foreground='white', font=('Consolas', 10))
        self.texto_equacoes.tag_configure('resultado', foreground='#68d391', font=('Consolas', 10, 'bold'))
        self.texto_equacoes.tag_configure('autor', foreground='#a0aec0', font=('Consolas', 9))
        self.mostrar_equacoes_iniciais()
    
    def criar_aba_catalogo(self, parent):
        """Criar aba com catálogo de estrelas"""
        # Título
        ttk.Label(parent, text="Catálogo de Estrelas Conhecidas",
                 font=('Segoe UI', 14, 'bold'), foreground='#4fc3f7').pack(pady=10)
        
        ttk.Label(parent, text="Clique em uma estrela para carregar seus dados na calculadora",
                 foreground='#a0aec0').pack(pady=(0, 10))
        
        # Frame com duas colunas de listas
        frame_listas = ttk.Frame(parent, style='TFrame')
        frame_listas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Lista para Estrela 1
        frame_e1 = ttk.LabelFrame(frame_listas, text="Selecionar para Estrela 1", padding=10)
        frame_e1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.lista_catalogo1 = tk.Listbox(frame_e1, bg='#1a202c', fg='#ffd700',
                                          font=('Segoe UI', 11), height=15,
                                          selectbackground='#667eea', relief=tk.FLAT)
        self.lista_catalogo1.pack(fill=tk.BOTH, expand=True)
        for estrela in CATALOGO_ESTRELAS:
            dist_al = (1000 / estrela['paralaxe']) * PARSEC_PARA_ANOS_LUZ
            self.lista_catalogo1.insert(tk.END, f"{estrela['nome']} ({dist_al:.1f} a.l.)")
        self.lista_catalogo1.bind('<Double-Button-1>', lambda e: self.carregar_do_catalogo(1))
        
        tk.Button(frame_e1, text="📥 Carregar para Estrela 1", 
                 command=lambda: self.carregar_do_catalogo(1),
                 bg='#ffd700', fg='black', font=('Segoe UI', 10, 'bold'),
                 relief=tk.FLAT, pady=5).pack(fill=tk.X, pady=(10, 0))
        
        # Lista para Estrela 2
        frame_e2 = ttk.LabelFrame(frame_listas, text="Selecionar para Estrela 2", padding=10)
        frame_e2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.lista_catalogo2 = tk.Listbox(frame_e2, bg='#1a202c', fg='#4a90d9',
                                          font=('Segoe UI', 11), height=15,
                                          selectbackground='#667eea', relief=tk.FLAT)
        self.lista_catalogo2.pack(fill=tk.BOTH, expand=True)
        for estrela in CATALOGO_ESTRELAS:
            dist_al = (1000 / estrela['paralaxe']) * PARSEC_PARA_ANOS_LUZ
            self.lista_catalogo2.insert(tk.END, f"{estrela['nome']} ({dist_al:.1f} a.l.)")
        self.lista_catalogo2.bind('<Double-Button-1>', lambda e: self.carregar_do_catalogo(2))
        
        tk.Button(frame_e2, text="📥 Carregar para Estrela 2",
                 command=lambda: self.carregar_do_catalogo(2),
                 bg='#4a90d9', fg='white', font=('Segoe UI', 10, 'bold'),
                 relief=tk.FLAT, pady=5).pack(fill=tk.X, pady=(10, 0))
        
        # Informações adicionais
        frame_info = ttk.LabelFrame(parent, text="ℹ️ Informações do Catálogo", padding=10)
        frame_info.pack(fill=tk.X, padx=20, pady=10)
        
        info_texto = """Este catálogo contém 18 estrelas brilhantes visíveis da Terra.
Os dados incluem: Ascensão Reta (α), Declinação (δ) e Paralaxe em milissegundos de arco.
A distância é calculada pela fórmula: d = 1000/p (em parsecs).

Duplo-clique ou use os botões para carregar uma estrela na calculadora."""
        
        ttk.Label(frame_info, text=info_texto, foreground='#a0aec0',
                 justify=tk.LEFT).pack(anchor='w')
    
    def carregar_do_catalogo(self, numero_estrela):
        """Carregar dados de uma estrela do catálogo"""
        if numero_estrela == 1:
            selecao = self.lista_catalogo1.curselection()
        else:
            selecao = self.lista_catalogo2.curselection()
        
        if not selecao:
            messagebox.showinfo("Aviso", f"Selecione uma estrela para Estrela {numero_estrela}")
            return
        
        idx = selecao[0]
        estrela = CATALOGO_ESTRELAS[idx]
        entradas = self.entradas1 if numero_estrela == 1 else self.entradas2
        
        # Preencher campos
        for campo in ['nome', 'ar_h', 'ar_m', 'ar_s', 'dec_g', 'dec_m', 'dec_s', 'paralaxe']:
            entradas[campo].delete(0, tk.END)
            if campo == 'nome':
                entradas[campo].insert(0, estrela['nome'])
                entradas[campo].config(fg='white')
            elif campo == 'ar_h':
                entradas[campo].insert(0, str(estrela['ar_h']))
                entradas[campo].config(fg='white')
            elif campo == 'ar_m':
                entradas[campo].insert(0, str(estrela['ar_m']))
                entradas[campo].config(fg='white')
            elif campo == 'ar_s':
                entradas[campo].insert(0, str(estrela['ar_s']))
                entradas[campo].config(fg='white')
            elif campo == 'dec_g':
                entradas[campo].insert(0, str(estrela['dec_g']))
                entradas[campo].config(fg='white')
            elif campo == 'dec_m':
                entradas[campo].insert(0, str(estrela['dec_m']))
                entradas[campo].config(fg='white')
            elif campo == 'dec_s':
                entradas[campo].insert(0, str(estrela['dec_s']))
                entradas[campo].config(fg='white')
            elif campo == 'paralaxe':
                entradas[campo].insert(0, str(estrela['paralaxe']))
                entradas[campo].config(fg='white')
        
        entradas['dec_sinal'].set(estrela['dec_sinal'])
        
        # Mudar para aba da calculadora
        self.notebook.select(0)
        
        messagebox.showinfo("Carregado", f"{estrela['nome']} carregada para Estrela {numero_estrela}")
    
    def criar_frame_estrela(self, parent, numero: int) -> dict:
        """Criar frame de entrada para uma estrela"""
        frame = ttk.LabelFrame(parent, text=f"★ Estrela {numero}", padding=8)
        frame.pack(fill=tk.X, pady=3)
        
        entradas = {}
        
        # Nome
        frame_nome = ttk.Frame(frame, style='TFrame')
        frame_nome.pack(fill=tk.X, pady=2)
        ttk.Label(frame_nome, text="Nome:").pack(side=tk.LEFT)
        entradas['nome'] = tk.Entry(frame_nome, width=25, bg='#2d3748', fg='white',
                                   insertbackground='white', relief=tk.FLAT)
        entradas['nome'].pack(side=tk.LEFT, padx=5)
        
        # Ascensão Reta
        frame_ar = ttk.Frame(frame, style='TFrame')
        frame_ar.pack(fill=tk.X, pady=2)
        ttk.Label(frame_ar, text="Asc. Reta (α):").pack(side=tk.LEFT)
        
        for campo, label, w in [('ar_h', 'h', 4), ('ar_m', 'm', 4), ('ar_s', 's', 6)]:
            entradas[campo] = tk.Entry(frame_ar, width=w, bg='#2d3748', fg='white',
                                       insertbackground='white', relief=tk.FLAT)
            entradas[campo].pack(side=tk.LEFT, padx=1)
            ttk.Label(frame_ar, text=label).pack(side=tk.LEFT)
        
        # Declinação
        frame_dec = ttk.Frame(frame, style='TFrame')
        frame_dec.pack(fill=tk.X, pady=2)
        ttk.Label(frame_dec, text="Declinação (δ):").pack(side=tk.LEFT)
        
        entradas['dec_sinal'] = ttk.Combobox(frame_dec, values=["+", "-"], width=2, state='readonly')
        entradas['dec_sinal'].set("+")
        entradas['dec_sinal'].pack(side=tk.LEFT, padx=1)
        
        for campo, label, w in [('dec_g', '°', 4), ('dec_m', "'", 4), ('dec_s', '"', 6)]:
            entradas[campo] = tk.Entry(frame_dec, width=w, bg='#2d3748', fg='white',
                                       insertbackground='white', relief=tk.FLAT)
            entradas[campo].pack(side=tk.LEFT, padx=1)
            ttk.Label(frame_dec, text=label).pack(side=tk.LEFT)
        
        # Paralaxe
        frame_par = ttk.Frame(frame, style='TFrame')
        frame_par.pack(fill=tk.X, pady=2)
        ttk.Label(frame_par, text="Paralaxe (mas):").pack(side=tk.LEFT)
        entradas['paralaxe'] = tk.Entry(frame_par, width=10, bg='#2d3748', fg='white',
                                        insertbackground='white', relief=tk.FLAT)
        entradas['paralaxe'].pack(side=tk.LEFT, padx=5)
        
        return entradas
    
    def mostrar_equacoes_iniciais(self):
        """Mostrar equações iniciais"""
        self.texto_equacoes.config(state=tk.NORMAL)
        self.texto_equacoes.delete(1.0, tk.END)
        
        self.texto_equacoes.insert(tk.END, "MÉTODO GEOMÉTRICO PARA DISTÂNCIA ESTELAR\n", 'titulo')
        self.texto_equacoes.insert(tk.END, "Autor: Luiz Tiago Wilcke\n\n", 'autor')
        
        self.texto_equacoes.insert(tk.END, "1. Distância por Paralaxe:\n", 'subtitulo')
        self.texto_equacoes.insert(tk.END, "   d = 1000 / p  [parsecs]\n\n", 'equacao')
        
        self.texto_equacoes.insert(tk.END, "2. Separação Angular (Lei dos Cossenos Esférica):\n", 'subtitulo')
        self.texto_equacoes.insert(tk.END, "   cos(θ) = sin(δ₁)sin(δ₂) + cos(δ₁)cos(δ₂)cos(α₁-α₂)\n\n", 'equacao')
        
        self.texto_equacoes.insert(tk.END, "3. Distância Real (Lei dos Cossenos):\n", 'subtitulo')
        self.texto_equacoes.insert(tk.END, "   D = √(d₁² + d₂² - 2·d₁·d₂·cos(θ))\n", 'equacao')
        
        self.texto_equacoes.config(state=tk.DISABLED)
    
    def desenhar_plano_inicial(self):
        """Desenhar plano estelar inicial"""
        self.ax_plano.clear()
        self.ax_plano.set_facecolor('#0a0a1a')
        
        np.random.seed(42)
        x_bg = np.random.uniform(-180, 180, 100)
        y_bg = np.random.uniform(-90, 90, 100)
        sizes = np.random.uniform(1, 20, 100)
        self.ax_plano.scatter(x_bg, y_bg, c='white', s=sizes, alpha=0.3)
        
        self.ax_plano.set_xlim(-180, 180)
        self.ax_plano.set_ylim(-90, 90)
        self.ax_plano.set_xlabel('Ascensão Reta (°)', color='#a0aec0', fontsize=8)
        self.ax_plano.set_ylabel('Declinação (°)', color='#a0aec0', fontsize=8)
        self.ax_plano.tick_params(colors='#a0aec0', labelsize=7)
        self.ax_plano.set_title('Selecione estrelas do catálogo ou insira dados manualmente', 
                               color='#4fc3f7', fontsize=9, style='italic')
        
        for spine in self.ax_plano.spines.values():
            spine.set_color('#2a2a4a')
        
        self.fig_plano.tight_layout()
        self.canvas_plano.draw()
    
    def obter_float(self, entrada, padrao: float = 0.0) -> float:
        try:
            valor = entrada.get().strip()
            if not valor:
                return padrao
            return float(valor)
        except ValueError:
            return padrao
    
    def obter_int(self, entrada, padrao: int = 0) -> int:
        try:
            valor = entrada.get().strip()
            if not valor:
                return padrao
            return int(float(valor))
        except ValueError:
            return padrao
    
    def ler_estrela(self, entradas: dict, numero: int) -> Estrela:
        nome = entradas['nome'].get().strip() or f"Estrela {numero}"
        
        ar = CoordenadaHMS(
            horas=self.obter_int(entradas['ar_h']),
            minutos=self.obter_int(entradas['ar_m']),
            segundos=self.obter_float(entradas['ar_s'])
        )
        
        dec = CoordenadaDMS(
            graus=self.obter_int(entradas['dec_g']),
            minutos=self.obter_int(entradas['dec_m']),
            segundos=self.obter_float(entradas['dec_s']),
            positivo=(entradas['dec_sinal'].get() == "+")
        )
        
        paralaxe = self.obter_float(entradas['paralaxe'])
        
        return Estrela(nome=nome, ascensao_reta=ar, declinacao=dec, paralaxe_mas=paralaxe)
    
    def calcular(self):
        try:
            self.estrela1 = self.ler_estrela(self.entradas1, 1)
            self.estrela2 = self.ler_estrela(self.entradas2, 2)
            
            if self.estrela1.paralaxe_mas <= 0 or self.estrela2.paralaxe_mas <= 0:
                messagebox.showwarning("Atenção", 
                    "A paralaxe deve ser maior que zero para ambas as estrelas.")
                return
            
            self.resultado_atual = CalculadoraGeometrica.calcular_distancia_entre_estrelas(
                self.estrela1, self.estrela2
            )
            
            self.atualizar_resultados()
            self.atualizar_plano()
            self.atualizar_equacoes()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao calcular: {str(e)}")
    
    def atualizar_resultados(self):
        self.texto_resultados.delete(1.0, tk.END)
        
        r = self.resultado_atual
        texto = f"""══════════════════════════════════════════
  RESULTADO DO CÁLCULO
══════════════════════════════════════════

  {r.nome_estrela1}:
  Distância: {r.distancia1_parsecs:.2f} pc ({r.distancia1_parsecs * PARSEC_PARA_ANOS_LUZ:.2f} a.l.)

  {r.nome_estrela2}:
  Distância: {r.distancia2_parsecs:.2f} pc ({r.distancia2_parsecs * PARSEC_PARA_ANOS_LUZ:.2f} a.l.)

  Separação Angular: {r.separacao_angular_graus:.4f}°

  ★ DISTÂNCIA REAL ENTRE AS ESTRELAS ★
     {r.distancia_real_parsecs:.4f} parsecs
     {r.distancia_real_anos_luz:.2f} anos-luz
══════════════════════════════════════════
"""
        self.texto_resultados.insert(tk.END, texto)
    
    def atualizar_plano(self):
        self.ax_plano.clear()
        self.ax_plano.set_facecolor('#0a0a1a')
        
        np.random.seed(42)
        x_bg = np.random.uniform(-180, 180, 100)
        y_bg = np.random.uniform(-90, 90, 100)
        sizes = np.random.uniform(1, 20, 100)
        self.ax_plano.scatter(x_bg, y_bg, c='white', s=sizes, alpha=0.3)
        
        x1, y1 = self.estrela1.ascensao_reta.para_graus(), self.estrela1.declinacao.para_graus()
        x2, y2 = self.estrela2.ascensao_reta.para_graus(), self.estrela2.declinacao.para_graus()
        if x1 > 180: x1 -= 360
        if x2 > 180: x2 -= 360
        
        self.ax_plano.plot([x1, x2], [y1, y2], color='#4fc3f7', linewidth=2, alpha=0.7)
        self.ax_plano.scatter([x1], [y1], c='#ffd700', s=150, marker='*', zorder=5)
        self.ax_plano.scatter([x2], [y2], c='#4a90d9', s=150, marker='*', zorder=5)
        
        self.ax_plano.annotate(self.estrela1.nome, (x1, y1), xytext=(8, 8),
                              textcoords='offset points', fontsize=9, color='#ffd700')
        self.ax_plano.annotate(self.estrela2.nome, (x2, y2), xytext=(8, 8),
                              textcoords='offset points', fontsize=9, color='#4a90d9')
        
        mx, my = (x1+x2)/2, (y1+y2)/2
        self.ax_plano.annotate(f'{self.resultado_atual.distancia_real_anos_luz:.1f} a.l.',
                              (mx, my), xytext=(0, -12), textcoords='offset points',
                              fontsize=9, color='#68d391', ha='center')
        
        self.ax_plano.set_xlim(-180, 180)
        self.ax_plano.set_ylim(-90, 90)
        self.ax_plano.set_xlabel('Ascensão Reta (°)', color='#a0aec0', fontsize=8)
        self.ax_plano.set_ylabel('Declinação (°)', color='#a0aec0', fontsize=8)
        self.ax_plano.tick_params(colors='#a0aec0', labelsize=7)
        self.ax_plano.set_title(f'{self.estrela1.nome} ↔ {self.estrela2.nome}',
                               color='#4fc3f7', fontsize=10)
        
        for spine in self.ax_plano.spines.values():
            spine.set_color('#2a2a4a')
        
        self.fig_plano.tight_layout()
        self.canvas_plano.draw()
    
    def atualizar_equacoes(self):
        r = self.resultado_atual
        
        self.texto_equacoes.config(state=tk.NORMAL)
        self.texto_equacoes.delete(1.0, tk.END)
        
        self.texto_equacoes.insert(tk.END, "MÉTODO GEOMÉTRICO PARA DISTÂNCIA ESTELAR\n", 'titulo')
        self.texto_equacoes.insert(tk.END, "Autor: Luiz Tiago Wilcke\n\n", 'autor')
        
        self.texto_equacoes.insert(tk.END, "1. Distância por Paralaxe:\n", 'subtitulo')
        self.texto_equacoes.insert(tk.END, "   d = 1000 / p\n", 'equacao')
        self.texto_equacoes.insert(tk.END, f"   → d₁ = {r.distancia1_parsecs:.2f} pc,  d₂ = {r.distancia2_parsecs:.2f} pc\n\n", 'resultado')
        
        self.texto_equacoes.insert(tk.END, "2. Separação Angular:\n", 'subtitulo')
        self.texto_equacoes.insert(tk.END, "   cos(θ) = sin(δ₁)sin(δ₂) + cos(δ₁)cos(δ₂)cos(α₁-α₂)\n", 'equacao')
        self.texto_equacoes.insert(tk.END, f"   → θ = {r.separacao_angular_graus:.4f}°\n\n", 'resultado')
        
        self.texto_equacoes.insert(tk.END, "3. Distância Real:\n", 'subtitulo')
        self.texto_equacoes.insert(tk.END, "   D = √(d₁² + d₂² - 2·d₁·d₂·cos(θ))\n", 'equacao')
        self.texto_equacoes.insert(tk.END, f"\n   ★ D = {r.distancia_real_parsecs:.4f} pc = {r.distancia_real_anos_luz:.2f} anos-luz ★\n", 'resultado')
        
        self.texto_equacoes.config(state=tk.DISABLED)
    
    def limpar(self):
        for entradas in [self.entradas1, self.entradas2]:
            for chave, entrada in entradas.items():
                if isinstance(entrada, tk.Entry):
                    entrada.delete(0, tk.END)
                elif isinstance(entrada, ttk.Combobox):
                    entrada.set("+")
        
        self.texto_resultados.delete(1.0, tk.END)
        self.resultado_atual = None
        self.desenhar_plano_inicial()
        self.mostrar_equacoes_iniciais()


def main():
    raiz = tk.Tk()
    app = InterfaceCalculadora(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
