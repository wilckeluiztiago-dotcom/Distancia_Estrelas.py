"""
Calculadora Geométrica de Distância Entre Estrelas
Módulo de Cálculos

Autor: Luiz Tiago Wilcke
Data: 2025
"""

import math
from dataclasses import dataclass
from typing import Tuple, Optional

# Constantes astronômicas
PI = math.pi
RADIANOS_POR_GRAU = PI / 180.0
GRAUS_POR_RADIANO = 180.0 / PI
SEGUNDOS_POR_GRAU = 3600.0
PARSEC_PARA_ANOS_LUZ = 3.26156


@dataclass
class CoordenadaHMS:
    """Coordenada em formato Horas-Minutos-Segundos (Ascensão Reta)"""
    horas: int = 0
    minutos: int = 0
    segundos: float = 0.0
    
    def para_graus(self) -> float:
        """Converte para graus decimais (24h = 360°)"""
        horas_decimais = self.horas + self.minutos / 60.0 + self.segundos / 3600.0
        return horas_decimais * 15.0  # 24h = 360°
    
    def para_radianos(self) -> float:
        """Converte para radianos"""
        return self.para_graus() * RADIANOS_POR_GRAU
    
    def __str__(self) -> str:
        return f"{self.horas}h {self.minutos}m {self.segundos:.2f}s"


@dataclass
class CoordenadaDMS:
    """Coordenada em formato Graus-Minutos-Segundos (Declinação)"""
    graus: int = 0
    minutos: int = 0
    segundos: float = 0.0
    positivo: bool = True  # True = Norte (+), False = Sul (-)
    
    def para_graus(self) -> float:
        """Converte para graus decimais"""
        resultado = abs(self.graus) + self.minutos / 60.0 + self.segundos / 3600.0
        return resultado if self.positivo else -resultado
    
    def para_radianos(self) -> float:
        """Converte para radianos"""
        return self.para_graus() * RADIANOS_POR_GRAU
    
    def __str__(self) -> str:
        sinal = "+" if self.positivo else "-"
        return f"{sinal}{abs(self.graus)}° {self.minutos}' {self.segundos:.2f}\""


@dataclass
class Estrela:
    """Representa uma estrela com suas coordenadas celestes"""
    nome: str = "Estrela"
    ascensao_reta: CoordenadaHMS = None
    declinacao: CoordenadaDMS = None
    paralaxe_mas: float = 0.0  # milissegundos de arco
    
    def __post_init__(self):
        if self.ascensao_reta is None:
            self.ascensao_reta = CoordenadaHMS()
        if self.declinacao is None:
            self.declinacao = CoordenadaDMS()
    
    @property
    def distancia_parsecs(self) -> float:
        """Calcula distância em parsecs a partir da paralaxe"""
        if self.paralaxe_mas > 0:
            return 1000.0 / self.paralaxe_mas
        return 0.0
    
    @property
    def distancia_anos_luz(self) -> float:
        """Calcula distância em anos-luz"""
        return self.distancia_parsecs * PARSEC_PARA_ANOS_LUZ
    
    @property
    def alfa_rad(self) -> float:
        """Ascensão reta em radianos"""
        return self.ascensao_reta.para_radianos()
    
    @property
    def delta_rad(self) -> float:
        """Declinação em radianos"""
        return self.declinacao.para_radianos()


@dataclass
class ResultadoCalculo:
    """Resultado do cálculo de distância entre duas estrelas"""
    nome_estrela1: str = ""
    nome_estrela2: str = ""
    separacao_angular_rad: float = 0.0
    separacao_angular_graus: float = 0.0
    distancia1_parsecs: float = 0.0
    distancia2_parsecs: float = 0.0
    distancia_real_parsecs: float = 0.0
    distancia_real_anos_luz: float = 0.0
    metodo_usado: str = ""
    equacao_usada: str = ""


class CalculadoraGeometrica:
    """Classe com todos os métodos geométricos para cálculo de distâncias estelares"""
    
    @staticmethod
    def calcular_distancia_paralaxe(paralaxe_mas: float) -> float:
        """
        Método 1: Calcular distância a partir da paralaxe
        
        Fórmula: d = 1000 / p
        Onde: d = distância em parsecs
              p = paralaxe em milissegundos de arco
        """
        if paralaxe_mas <= 0:
            return 0.0
        return 1000.0 / paralaxe_mas
    
    @staticmethod
    def calcular_separacao_angular(alfa1: float, delta1: float,
                                    alfa2: float, delta2: float) -> float:
        """
        Método 2: Calcular separação angular entre duas estrelas
        Usando a Lei dos Cossenos Esférica
        
        Fórmula: cos(θ) = sin(δ₁)·sin(δ₂) + cos(δ₁)·cos(δ₂)·cos(α₁-α₂)
        
        Args:
            alfa1: Ascensão reta da estrela 1 em radianos
            delta1: Declinação da estrela 1 em radianos
            alfa2: Ascensão reta da estrela 2 em radianos
            delta2: Declinação da estrela 2 em radianos
            
        Returns:
            Separação angular em radianos
        """
        cos_theta = (math.sin(delta1) * math.sin(delta2) + 
                     math.cos(delta1) * math.cos(delta2) * math.cos(alfa1 - alfa2))
        
        # Garantir que está no intervalo [-1, 1]
        cos_theta = max(-1.0, min(1.0, cos_theta))
        
        return math.acos(cos_theta)
    
    @staticmethod
    def calcular_distancia_real(distancia1: float, distancia2: float,
                                 separacao_angular: float) -> float:
        """
        Método 3: Calcular distância real entre duas estrelas
        Usando a Lei dos Cossenos para triângulos
        
        Fórmula: D = √(d₁² + d₂² - 2·d₁·d₂·cos(θ))
        
        Args:
            distancia1: Distância da estrela 1 em parsecs
            distancia2: Distância da estrela 2 em parsecs
            separacao_angular: Separação angular em radianos
            
        Returns:
            Distância real entre as estrelas em parsecs
        """
        d1_sq = distancia1 ** 2
        d2_sq = distancia2 ** 2
        produto = 2.0 * distancia1 * distancia2 * math.cos(separacao_angular)
        
        return math.sqrt(d1_sq + d2_sq - produto)
    
    @classmethod
    def calcular_distancia_entre_estrelas(cls, estrela1: Estrela, 
                                          estrela2: Estrela) -> ResultadoCalculo:
        """Calcular todos os parâmetros entre duas estrelas"""
        resultado = ResultadoCalculo()
        
        resultado.nome_estrela1 = estrela1.nome
        resultado.nome_estrela2 = estrela2.nome
        
        # Obter coordenadas em radianos
        alfa1 = estrela1.alfa_rad
        delta1 = estrela1.delta_rad
        alfa2 = estrela2.alfa_rad
        delta2 = estrela2.delta_rad
        
        # Calcular distâncias individuais
        resultado.distancia1_parsecs = cls.calcular_distancia_paralaxe(estrela1.paralaxe_mas)
        resultado.distancia2_parsecs = cls.calcular_distancia_paralaxe(estrela2.paralaxe_mas)
        
        # Calcular separação angular
        resultado.separacao_angular_rad = cls.calcular_separacao_angular(
            alfa1, delta1, alfa2, delta2
        )
        resultado.separacao_angular_graus = resultado.separacao_angular_rad * GRAUS_POR_RADIANO
        
        # Calcular distância real
        resultado.distancia_real_parsecs = cls.calcular_distancia_real(
            resultado.distancia1_parsecs,
            resultado.distancia2_parsecs,
            resultado.separacao_angular_rad
        )
        resultado.distancia_real_anos_luz = resultado.distancia_real_parsecs * PARSEC_PARA_ANOS_LUZ
        
        # Definir método
        resultado.metodo_usado = "Lei dos Cossenos Esférica + Distância 3D"
        
        # Gerar texto da equação
        resultado.equacao_usada = cls._gerar_texto_equacao(resultado)
        
        return resultado
    
    @staticmethod
    def _gerar_texto_equacao(resultado: ResultadoCalculo) -> str:
        """Gerar texto formatado da equação usada"""
        texto = []
        texto.append("MÉTODO GEOMÉTRICO:")
        texto.append("")
        texto.append("1. Distância por Paralaxe:")
        texto.append("   d = 1000 / p (parsecs)")
        texto.append("")
        texto.append("2. Separação Angular (Lei dos Cossenos Esférica):")
        texto.append("   cos(θ) = sin(δ₁)·sin(δ₂) + cos(δ₁)·cos(δ₂)·cos(α₁-α₂)")
        texto.append(f"   θ = {resultado.separacao_angular_graus:.4f}°")
        texto.append("")
        texto.append("3. Distância Real (Lei dos Cossenos):")
        texto.append("   D = √(d₁² + d₂² - 2·d₁·d₂·cos(θ))")
        texto.append(f"   D = √({resultado.distancia1_parsecs:.4f}² + "
                    f"{resultado.distancia2_parsecs:.4f}² - 2·"
                    f"{resultado.distancia1_parsecs:.4f}·{resultado.distancia2_parsecs:.4f}·"
                    f"cos({resultado.separacao_angular_graus:.4f}°))")
        texto.append(f"   D = {resultado.distancia_real_parsecs:.4f} parsecs")
        texto.append(f"   D = {resultado.distancia_real_anos_luz:.2f} anos-luz")
        
        return "\n".join(texto)
    
    @staticmethod
    def parsecs_para_anos_luz(parsecs: float) -> float:
        """Converter parsecs para anos-luz"""
        return parsecs * PARSEC_PARA_ANOS_LUZ
    
    @staticmethod
    def anos_luz_para_parsecs(anos_luz: float) -> float:
        """Converter anos-luz para parsecs"""
        return anos_luz / PARSEC_PARA_ANOS_LUZ


def teste_calculos():
    """Função de teste com estrelas conhecidas"""
    print("=" * 60)
    print("TESTE: Calculadora Geométrica de Distância Entre Estrelas")
    print("Autor: Luiz Tiago Wilcke")
    print("=" * 60)
    
    # Sirius (α CMa)
    sirius = Estrela(
        nome="Sirius",
        ascensao_reta=CoordenadaHMS(6, 45, 8.9),
        declinacao=CoordenadaDMS(16, 42, 58, False),  # Sul
        paralaxe_mas=379.21
    )
    
    # Betelgeuse (α Ori)
    betelgeuse = Estrela(
        nome="Betelgeuse",
        ascensao_reta=CoordenadaHMS(5, 55, 10.3),
        declinacao=CoordenadaDMS(7, 24, 25, True),  # Norte
        paralaxe_mas=4.51
    )
    
    print(f"\nEstrela 1: {sirius.nome}")
    print(f"  Ascensão Reta: {sirius.ascensao_reta}")
    print(f"  Declinação: {sirius.declinacao}")
    print(f"  Paralaxe: {sirius.paralaxe_mas} mas")
    print(f"  Distância: {sirius.distancia_parsecs:.4f} pc ({sirius.distancia_anos_luz:.2f} a.l.)")
    
    print(f"\nEstrela 2: {betelgeuse.nome}")
    print(f"  Ascensão Reta: {betelgeuse.ascensao_reta}")
    print(f"  Declinação: {betelgeuse.declinacao}")
    print(f"  Paralaxe: {betelgeuse.paralaxe_mas} mas")
    print(f"  Distância: {betelgeuse.distancia_parsecs:.4f} pc ({betelgeuse.distancia_anos_luz:.2f} a.l.)")
    
    # Calcular
    resultado = CalculadoraGeometrica.calcular_distancia_entre_estrelas(sirius, betelgeuse)
    
    print("\n" + "=" * 60)
    print("RESULTADO")
    print("=" * 60)
    print(f"\nSeparação Angular: {resultado.separacao_angular_graus:.4f}°")
    print(f"Distância Real: {resultado.distancia_real_parsecs:.4f} parsecs")
    print(f"Distância Real: {resultado.distancia_real_anos_luz:.2f} anos-luz")
    print("\n" + resultado.equacao_usada)
    
    print("\n✅ Teste concluído com sucesso!")


if __name__ == "__main__":
    teste_calculos()
