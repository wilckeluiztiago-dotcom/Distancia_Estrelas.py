"""
Calculadora Geométrica de Distância Entre Estrelas
Módulo de Visualização Avançada

Autor: Luiz Tiago Wilcke
Data: 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
import math

from calculos import (
    Estrela, CoordenadaHMS, CoordenadaDMS, 
    CalculadoraGeometrica, ResultadoCalculo,
    PARSEC_PARA_ANOS_LUZ, RADIANOS_POR_GRAU
)


class VisualizadorEstelar:
    """Classe para visualizações avançadas do sistema estelar"""
    
    def __init__(self):
        # Configurar estilo
        plt.style.use('dark_background')
        self.cores = {
            'fundo': '#0a0a1a',
            'estrela1': '#ffd700',
            'estrela2': '#4a90d9',
            'linha': '#4fc3f7',
            'texto': '#e2e8f0',
            'grid': '#2a2a4a'
        }
    
    def criar_mapa_celeste(self, estrela1: Estrela, estrela2: Estrela,
                           resultado: ResultadoCalculo) -> plt.Figure:
        """
        Criar mapa celeste mostrando as duas estrelas e sua conexão
        """
        fig, ax = plt.subplots(figsize=(12, 6), facecolor=self.cores['fundo'])
        ax.set_facecolor(self.cores['fundo'])
        
        # Desenhar estrelas de fundo aleatórias
        np.random.seed(42)
        n_estrelas_fundo = 200
        ra_bg = np.random.uniform(0, 360, n_estrelas_fundo)
        dec_bg = np.random.uniform(-90, 90, n_estrelas_fundo)
        sizes_bg = np.random.uniform(1, 30, n_estrelas_fundo)
        alphas_bg = np.random.uniform(0.1, 0.5, n_estrelas_fundo)
        
        for i in range(n_estrelas_fundo):
            ax.scatter(ra_bg[i], dec_bg[i], c='white', s=sizes_bg[i], 
                      alpha=alphas_bg[i], marker='.')
        
        # Converter coordenadas
        ra1 = estrela1.ascensao_reta.para_graus()
        dec1 = estrela1.declinacao.para_graus()
        ra2 = estrela2.ascensao_reta.para_graus()
        dec2 = estrela2.declinacao.para_graus()
        
        # Desenhar linha de conexão
        ax.plot([ra1, ra2], [dec1, dec2], color=self.cores['linha'], 
               linewidth=2, alpha=0.7, linestyle='-', zorder=3)
        
        # Desenhar estrela 1 com efeito de brilho
        for size, alpha in [(400, 0.1), (250, 0.2), (150, 0.4), (80, 0.8)]:
            ax.scatter([ra1], [dec1], c=self.cores['estrela1'], s=size, 
                      alpha=alpha, marker='*', zorder=4)
        ax.annotate(f'{estrela1.nome}\n({estrela1.distancia_anos_luz:.1f} a.l.)', 
                   (ra1, dec1), textcoords="offset points", xytext=(15, 15),
                   fontsize=11, color=self.cores['estrela1'], fontweight='bold',
                   ha='left', zorder=5)
        
        # Desenhar estrela 2 com efeito de brilho
        for size, alpha in [(400, 0.1), (250, 0.2), (150, 0.4), (80, 0.8)]:
            ax.scatter([ra2], [dec2], c=self.cores['estrela2'], s=size,
                      alpha=alpha, marker='*', zorder=4)
        ax.annotate(f'{estrela2.nome}\n({estrela2.distancia_anos_luz:.1f} a.l.)',
                   (ra2, dec2), textcoords="offset points", xytext=(15, 15),
                   fontsize=11, color=self.cores['estrela2'], fontweight='bold',
                   ha='left', zorder=5)
        
        # Anotação de distância
        mid_ra = (ra1 + ra2) / 2
        mid_dec = (dec1 + dec2) / 2
        ax.annotate(f'Distância: {resultado.distancia_real_anos_luz:.2f} anos-luz\n'
                   f'Separação angular: {resultado.separacao_angular_graus:.2f}°',
                   (mid_ra, mid_dec), textcoords="offset points", xytext=(0, -30),
                   fontsize=10, color='#68d391', ha='center',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a3a1a', 
                            edgecolor='#68d391', alpha=0.8), zorder=5)
        
        # Configurações do gráfico
        ax.set_xlim(0, 360)
        ax.set_ylim(-90, 90)
        ax.set_xlabel('Ascensão Reta (graus)', color=self.cores['texto'], fontsize=11)
        ax.set_ylabel('Declinação (graus)', color=self.cores['texto'], fontsize=11)
        ax.set_title('Mapa Celeste - Posição das Estrelas', 
                    color=self.cores['linha'], fontsize=14, fontweight='bold')
        
        # Grid
        ax.grid(True, color=self.cores['grid'], alpha=0.3, linestyle='--')
        ax.axhline(y=0, color=self.cores['grid'], linewidth=1, alpha=0.5)
        ax.tick_params(colors=self.cores['texto'])
        
        for spine in ax.spines.values():
            spine.set_color(self.cores['grid'])
        
        # Autor
        fig.text(0.99, 0.01, 'Autor: Luiz Tiago Wilcke', fontsize=8,
                color=self.cores['grid'], ha='right', va='bottom')
        
        plt.tight_layout()
        return fig
    
    def criar_visualizacao_3d(self, estrela1: Estrela, estrela2: Estrela,
                               resultado: ResultadoCalculo) -> plt.Figure:
        """
        Criar visualização 3D das estrelas no espaço
        """
        fig = plt.figure(figsize=(10, 8), facecolor=self.cores['fundo'])
        ax = fig.add_subplot(111, projection='3d', facecolor=self.cores['fundo'])
        
        # Converter coordenadas esféricas para cartesianas
        def esfericas_para_cartesianas(ar_graus: float, dec_graus: float, 
                                        distancia: float) -> tuple:
            ar_rad = ar_graus * RADIANOS_POR_GRAU
            dec_rad = dec_graus * RADIANOS_POR_GRAU
            x = distancia * np.cos(dec_rad) * np.cos(ar_rad)
            y = distancia * np.cos(dec_rad) * np.sin(ar_rad)
            z = distancia * np.sin(dec_rad)
            return x, y, z
        
        # Posição do Sol (origem)
        ax.scatter([0], [0], [0], c='yellow', s=200, marker='o', label='Sol')
        
        # Posição da Estrela 1
        x1, y1, z1 = esfericas_para_cartesianas(
            estrela1.ascensao_reta.para_graus(),
            estrela1.declinacao.para_graus(),
            resultado.distancia1_parsecs
        )
        ax.scatter([x1], [y1], [z1], c=self.cores['estrela1'], s=150, 
                  marker='*', label=estrela1.nome)
        
        # Posição da Estrela 2
        x2, y2, z2 = esfericas_para_cartesianas(
            estrela2.ascensao_reta.para_graus(),
            estrela2.declinacao.para_graus(),
            resultado.distancia2_parsecs
        )
        ax.scatter([x2], [y2], [z2], c=self.cores['estrela2'], s=150,
                  marker='*', label=estrela2.nome)
        
        # Linhas conectando
        ax.plot([0, x1], [0, y1], [0, z1], color=self.cores['estrela1'], 
               alpha=0.5, linestyle='--')
        ax.plot([0, x2], [0, y2], [0, z2], color=self.cores['estrela2'],
               alpha=0.5, linestyle='--')
        ax.plot([x1, x2], [y1, y2], [z1, z2], color=self.cores['linha'],
               linewidth=2, label=f'D = {resultado.distancia_real_parsecs:.2f} pc')
        
        # Configurações
        ax.set_xlabel('X (parsecs)', color=self.cores['texto'])
        ax.set_ylabel('Y (parsecs)', color=self.cores['texto'])
        ax.set_zlabel('Z (parsecs)', color=self.cores['texto'])
        ax.set_title('Visualização 3D do Sistema Estelar',
                    color=self.cores['linha'], fontsize=14, fontweight='bold')
        
        ax.tick_params(colors=self.cores['texto'])
        ax.legend(facecolor=self.cores['fundo'], edgecolor=self.cores['grid'],
                 labelcolor=self.cores['texto'])
        
        # Ajustar cores do fundo do 3D
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor(self.cores['grid'])
        ax.yaxis.pane.set_edgecolor(self.cores['grid'])
        ax.zaxis.pane.set_edgecolor(self.cores['grid'])
        
        return fig
    
    def criar_diagrama_geometrico(self, resultado: ResultadoCalculo) -> plt.Figure:
        """
        Criar diagrama geométrico mostrando o triângulo formado
        """
        fig, ax = plt.subplots(figsize=(10, 8), facecolor=self.cores['fundo'])
        ax.set_facecolor(self.cores['fundo'])
        
        # Posições do triângulo (Sol, Estrela1, Estrela2)
        # Normalizar para visualização
        escala = 1.0
        d1 = resultado.distancia1_parsecs * escala
        d2 = resultado.distancia2_parsecs * escala
        theta = resultado.separacao_angular_rad
        
        # Sol na origem
        sol_x, sol_y = 0, 0
        
        # Estrela 1 diretamente acima
        e1_x = 0
        e1_y = d1
        
        # Estrela 2 baseada no ângulo
        e2_x = d2 * np.sin(theta)
        e2_y = d2 * np.cos(theta)
        
        # Desenhar o triângulo
        triangulo_x = [sol_x, e1_x, e2_x, sol_x]
        triangulo_y = [sol_y, e1_y, e2_y, sol_y]
        ax.fill(triangulo_x, triangulo_y, color=self.cores['linha'], alpha=0.1)
        
        # Desenhar as linhas
        ax.plot([sol_x, e1_x], [sol_y, e1_y], color=self.cores['estrela1'], 
               linewidth=2, label=f'd₁ = {resultado.distancia1_parsecs:.2f} pc')
        ax.plot([sol_x, e2_x], [sol_y, e2_y], color=self.cores['estrela2'],
               linewidth=2, label=f'd₂ = {resultado.distancia2_parsecs:.2f} pc')
        ax.plot([e1_x, e2_x], [e1_y, e2_y], color='#68d391', linewidth=3,
               label=f'D = {resultado.distancia_real_parsecs:.2f} pc')
        
        # Desenhar pontos
        ax.scatter([sol_x], [sol_y], c='yellow', s=300, marker='o', zorder=5)
        ax.annotate('Sol (Terra)', (sol_x, sol_y), textcoords="offset points",
                   xytext=(10, -20), fontsize=11, color='yellow', fontweight='bold')
        
        ax.scatter([e1_x], [e1_y], c=self.cores['estrela1'], s=200, marker='*', zorder=5)
        ax.annotate(resultado.nome_estrela1, (e1_x, e1_y), textcoords="offset points",
                   xytext=(10, 10), fontsize=11, color=self.cores['estrela1'], fontweight='bold')
        
        ax.scatter([e2_x], [e2_y], c=self.cores['estrela2'], s=200, marker='*', zorder=5)
        ax.annotate(resultado.nome_estrela2, (e2_x, e2_y), textcoords="offset points",
                   xytext=(10, 10), fontsize=11, color=self.cores['estrela2'], fontweight='bold')
        
        # Arco para mostrar o ângulo
        arco_r = min(d1, d2) * 0.3
        angulos = np.linspace(np.pi/2 - theta, np.pi/2, 30)
        arco_x = arco_r * np.cos(angulos)
        arco_y = arco_r * np.sin(angulos)
        ax.plot(arco_x, arco_y, color='white', linewidth=1)
        ax.annotate(f'θ = {resultado.separacao_angular_graus:.2f}°', 
                   (arco_r * 0.5, arco_r * 0.8),
                   fontsize=10, color='white')
        
        # Equações
        eq_texto = (
            f"Lei dos Cossenos:\n"
            f"D² = d₁² + d₂² - 2d₁d₂cos(θ)\n"
            f"D² = {resultado.distancia1_parsecs:.2f}² + {resultado.distancia2_parsecs:.2f}² "
            f"- 2×{resultado.distancia1_parsecs:.2f}×{resultado.distancia2_parsecs:.2f}×"
            f"cos({resultado.separacao_angular_graus:.2f}°)\n"
            f"D = {resultado.distancia_real_parsecs:.4f} parsecs\n"
            f"D = {resultado.distancia_real_anos_luz:.2f} anos-luz"
        )
        ax.text(0.02, 0.98, eq_texto, transform=ax.transAxes, fontsize=10,
               color=self.cores['texto'], verticalalignment='top',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e',
                        edgecolor=self.cores['linha'], alpha=0.9))
        
        # Configurações
        ax.set_xlabel('X (parsecs)', color=self.cores['texto'], fontsize=11)
        ax.set_ylabel('Y (parsecs)', color=self.cores['texto'], fontsize=11)
        ax.set_title('Diagrama Geométrico - Triângulo Sol-Estrela1-Estrela2',
                    color=self.cores['linha'], fontsize=14, fontweight='bold')
        ax.set_aspect('equal')
        ax.legend(loc='lower right', facecolor=self.cores['fundo'], 
                 edgecolor=self.cores['grid'], labelcolor=self.cores['texto'])
        ax.grid(True, color=self.cores['grid'], alpha=0.3, linestyle='--')
        ax.tick_params(colors=self.cores['texto'])
        
        for spine in ax.spines.values():
            spine.set_color(self.cores['grid'])
        
        # Autor
        fig.text(0.99, 0.01, 'Autor: Luiz Tiago Wilcke', fontsize=8,
                color=self.cores['grid'], ha='right', va='bottom')
        
        plt.tight_layout()
        return fig


def demonstracao():
    """Demonstração das visualizações"""
    print("=" * 60)
    print("DEMONSTRAÇÃO: Visualizador Estelar")
    print("Autor: Luiz Tiago Wilcke")
    print("=" * 60)
    
    # Criar estrelas de exemplo
    sirius = Estrela(
        nome="Sirius",
        ascensao_reta=CoordenadaHMS(6, 45, 8.9),
        declinacao=CoordenadaDMS(16, 42, 58, False),
        paralaxe_mas=379.21
    )
    
    betelgeuse = Estrela(
        nome="Betelgeuse",
        ascensao_reta=CoordenadaHMS(5, 55, 10.3),
        declinacao=CoordenadaDMS(7, 24, 25, True),
        paralaxe_mas=4.51
    )
    
    # Calcular
    resultado = CalculadoraGeometrica.calcular_distancia_entre_estrelas(sirius, betelgeuse)
    
    print(f"\nEstrelas: {sirius.nome} e {betelgeuse.nome}")
    print(f"Distância real: {resultado.distancia_real_anos_luz:.2f} anos-luz")
    print("\nGerando visualizações...")
    
    # Criar visualizador
    viz = VisualizadorEstelar()
    
    # Gerar e salvar figuras
    fig1 = viz.criar_mapa_celeste(sirius, betelgeuse, resultado)
    fig1.savefig('mapa_celeste.png', dpi=150, facecolor=fig1.get_facecolor(),
                bbox_inches='tight')
    print("✓ Mapa celeste salvo: mapa_celeste.png")
    
    fig2 = viz.criar_visualizacao_3d(sirius, betelgeuse, resultado)
    fig2.savefig('visualizacao_3d.png', dpi=150, facecolor=fig2.get_facecolor(),
                bbox_inches='tight')
    print("✓ Visualização 3D salva: visualizacao_3d.png")
    
    fig3 = viz.criar_diagrama_geometrico(resultado)
    fig3.savefig('diagrama_geometrico.png', dpi=150, facecolor=fig3.get_facecolor(),
                bbox_inches='tight')
    print("✓ Diagrama geométrico salvo: diagrama_geometrico.png")
    
    print("\n✅ Demonstração concluída!")
    plt.show()


if __name__ == "__main__":
    demonstracao()
