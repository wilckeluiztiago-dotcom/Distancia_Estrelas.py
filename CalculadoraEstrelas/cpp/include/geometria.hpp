/**
 * Calculadora Geométrica de Distância Entre Estrelas
 * Funções de Cálculo Geométrico
 * 
 * Autor: Luiz Tiago Wilcke
 * Data: 2025
 */

#ifndef GEOMETRIA_HPP
#define GEOMETRIA_HPP

#include "tipos.hpp"
#include <cmath>
#include <sstream>
#include <iomanip>

namespace CalculadoraEstrelas {

/**
 * Classe com todos os métodos geométricos para cálculo de distâncias estelares
 */
class CalculadoraGeometrica {
public:
    
    /**
     * Método 1: Calcular distância a partir da paralaxe
     * 
     * Fórmula: d = 1000 / p
     * Onde: d = distância em parsecs
     *       p = paralaxe em milissegundos de arco
     */
    static double calcularDistanciaParalaxe(double paralaxeMas) {
        if (paralaxeMas <= 0) {
            return 0.0;
        }
        return 1000.0 / paralaxeMas;
    }
    
    /**
     * Método 2: Calcular separação angular entre duas estrelas
     * Usando a Lei dos Cossenos Esférica
     * 
     * Fórmula: cos(θ) = sin(δ₁)·sin(δ₂) + cos(δ₁)·cos(δ₂)·cos(α₁-α₂)
     * 
     * @param alfa1 Ascensão reta da estrela 1 em radianos
     * @param delta1 Declinação da estrela 1 em radianos
     * @param alfa2 Ascensão reta da estrela 2 em radianos
     * @param delta2 Declinação da estrela 2 em radianos
     * @return Separação angular em radianos
     */
    static double calcularSeparacaoAngular(
        double alfa1, double delta1,
        double alfa2, double delta2
    ) {
        double cosTeta = std::sin(delta1) * std::sin(delta2) +
                         std::cos(delta1) * std::cos(delta2) * 
                         std::cos(alfa1 - alfa2);
        
        // Garantir que está no intervalo [-1, 1]
        cosTeta = std::max(-1.0, std::min(1.0, cosTeta));
        
        return std::acos(cosTeta);
    }
    
    /**
     * Método 3: Calcular distância real entre duas estrelas
     * Usando a Lei dos Cossenos para triângulos
     * 
     * Fórmula: D = √(d₁² + d₂² - 2·d₁·d₂·cos(θ))
     * 
     * @param distancia1 Distância da estrela 1 em parsecs
     * @param distancia2 Distância da estrela 2 em parsecs
     * @param separacaoAngular Separação angular em radianos
     * @return Distância real entre as estrelas em parsecs
     */
    static double calcularDistanciaReal(
        double distancia1,
        double distancia2,
        double separacaoAngular
    ) {
        double d1sq = distancia1 * distancia1;
        double d2sq = distancia2 * distancia2;
        double produto = 2.0 * distancia1 * distancia2 * std::cos(separacaoAngular);
        
        return std::sqrt(d1sq + d2sq - produto);
    }
    
    /**
     * Calcular todos os parâmetros entre duas estrelas
     */
    static ResultadoCalculo calcularDistanciaEntreEstrelas(
        const Estrela& estrela1,
        const Estrela& estrela2
    ) {
        ResultadoCalculo resultado;
        
        resultado.nomeEstrela1 = estrela1.nome;
        resultado.nomeEstrela2 = estrela2.nome;
        
        // Obter coordenadas em radianos
        double alfa1 = estrela1.alfaRad();
        double delta1 = estrela1.deltaRad();
        double alfa2 = estrela2.alfaRad();
        double delta2 = estrela2.deltaRad();
        
        // Calcular distâncias individuais
        resultado.distancia1Parsecs = calcularDistanciaParalaxe(estrela1.paralaxeMas);
        resultado.distancia2Parsecs = calcularDistanciaParalaxe(estrela2.paralaxeMas);
        
        // Calcular separação angular
        resultado.separacaoAngularRad = calcularSeparacaoAngular(
            alfa1, delta1, alfa2, delta2
        );
        resultado.separacaoAngularGraus = resultado.separacaoAngularRad * GRAUS_POR_RADIANO;
        
        // Calcular distância real
        resultado.distanciaRealParsecs = calcularDistanciaReal(
            resultado.distancia1Parsecs,
            resultado.distancia2Parsecs,
            resultado.separacaoAngularRad
        );
        resultado.distanciaRealAnosLuz = resultado.distanciaRealParsecs * PARSEC_PARA_ANOS_LUZ;
        
        // Definir método
        resultado.metodoUsado = "Lei dos Cossenos Esférica + Distância 3D";
        
        // Gerar texto da equação
        resultado.equacaoUsada = gerarTextoEquacao(resultado);
        
        return resultado;
    }
    
    /**
     * Gerar texto formatado da equação usada
     */
    static std::string gerarTextoEquacao(const ResultadoCalculo& resultado) {
        std::ostringstream ss;
        ss << std::fixed << std::setprecision(4);
        
        ss << "MÉTODO GEOMÉTRICO:\n\n";
        
        ss << "1. Distância por Paralaxe:\n";
        ss << "   d = 1000 / p (parsecs)\n\n";
        
        ss << "2. Separação Angular (Lei dos Cossenos Esférica):\n";
        ss << "   cos(θ) = sin(δ₁)·sin(δ₂) + cos(δ₁)·cos(δ₂)·cos(α₁-α₂)\n";
        ss << "   θ = " << resultado.separacaoAngularGraus << "°\n\n";
        
        ss << "3. Distância Real (Lei dos Cossenos):\n";
        ss << "   D = √(d₁² + d₂² - 2·d₁·d₂·cos(θ))\n";
        ss << "   D = √(" << resultado.distancia1Parsecs << "² + " 
           << resultado.distancia2Parsecs << "² - 2·"
           << resultado.distancia1Parsecs << "·" << resultado.distancia2Parsecs 
           << "·cos(" << resultado.separacaoAngularGraus << "°))\n";
        ss << "   D = " << resultado.distanciaRealParsecs << " parsecs\n";
        ss << "   D = " << resultado.distanciaRealAnosLuz << " anos-luz\n";
        
        return ss.str();
    }
    
    /**
     * Converter parsecs para anos-luz
     */
    static double parsecsParaAnosLuz(double parsecs) {
        return parsecs * PARSEC_PARA_ANOS_LUZ;
    }
    
    /**
     * Converter anos-luz para parsecs
     */
    static double anosLuzParaParsecs(double anosLuz) {
        return anosLuz / PARSEC_PARA_ANOS_LUZ;
    }
};

} // namespace CalculadoraEstrelas

#endif // GEOMETRIA_HPP
