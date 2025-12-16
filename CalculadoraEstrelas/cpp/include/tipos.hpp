/**
 * Calculadora Geométrica de Distância Entre Estrelas
 * Tipos e Estruturas de Dados
 * 
 * Autor: Luiz Tiago Wilcke
 * Data: 2025
 */

#ifndef TIPOS_HPP
#define TIPOS_HPP

#include <string>
#include <cmath>

namespace CalculadoraEstrelas {

// Constantes astronômicas
constexpr double PI = 3.14159265358979323846;
constexpr double RADIANOS_POR_GRAU = PI / 180.0;
constexpr double GRAUS_POR_RADIANO = 180.0 / PI;
constexpr double SEGUNDOS_POR_GRAU = 3600.0;
constexpr double PARSEC_PARA_ANOS_LUZ = 3.26156;

/**
 * Estrutura para representar coordenadas hora-minuto-segundo
 */
struct CoordenadaHMS {
    int horas;
    int minutos;
    double segundos;
    
    // Converte para graus decimais
    double paraGraus() const {
        double horasDecimais = horas + minutos / 60.0 + segundos / 3600.0;
        return horasDecimais * 15.0; // 24h = 360°
    }
    
    // Converte para radianos
    double paraRadianos() const {
        return paraGraus() * RADIANOS_POR_GRAU;
    }
};

/**
 * Estrutura para representar coordenadas grau-minuto-segundo
 */
struct CoordenadaDMS {
    int graus;
    int minutos;
    double segundos;
    bool positivo; // true = Norte/+, false = Sul/-
    
    // Converte para graus decimais
    double paraGraus() const {
        double resultado = std::abs(graus) + minutos / 60.0 + segundos / 3600.0;
        return positivo ? resultado : -resultado;
    }
    
    // Converte para radianos
    double paraRadianos() const {
        return paraGraus() * RADIANOS_POR_GRAU;
    }
};

/**
 * Estrutura principal para representar uma estrela
 */
struct Estrela {
    std::string nome;
    
    // Coordenadas celestes
    CoordenadaHMS ascensaoReta;      // α - Right Ascension
    CoordenadaDMS declinacao;         // δ - Declination
    
    // Paralaxe em milissegundos de arco (mas)
    double paralaxeMas;
    
    // Distância calculada em parsecs
    double distanciaParsecs;
    
    // Distância em anos-luz
    double distanciaAnosLuz;
    
    // Calcular distância a partir da paralaxe
    void calcularDistancia() {
        if (paralaxeMas > 0) {
            distanciaParsecs = 1000.0 / paralaxeMas; // paralaxe em mas → pc
            distanciaAnosLuz = distanciaParsecs * PARSEC_PARA_ANOS_LUZ;
        }
    }
    
    // Obter ascensão reta em radianos
    double alfaRad() const {
        return ascensaoReta.paraRadianos();
    }
    
    // Obter declinação em radianos
    double deltaRad() const {
        return declinacao.paraRadianos();
    }
};

/**
 * Resultado do cálculo de distância entre duas estrelas
 */
struct ResultadoCalculo {
    // Estrelas envolvidas
    std::string nomeEstrela1;
    std::string nomeEstrela2;
    
    // Separação angular no céu (radianos)
    double separacaoAngularRad;
    
    // Separação angular em graus
    double separacaoAngularGraus;
    
    // Distâncias individuais
    double distancia1Parsecs;
    double distancia2Parsecs;
    
    // Distância real entre as estrelas em parsecs
    double distanciaRealParsecs;
    
    // Distância real em anos-luz
    double distanciaRealAnosLuz;
    
    // Método usado para o cálculo
    std::string metodoUsado;
    
    // Texto da equação usada
    std::string equacaoUsada;
};

/**
 * Cores para a renderização da interface
 */
struct CorRGBA {
    double r, g, b, a;
    
    static CorRGBA branco() { return {1.0, 1.0, 1.0, 1.0}; }
    static CorRGBA preto() { return {0.0, 0.0, 0.0, 1.0}; }
    static CorRGBA amarelo() { return {1.0, 0.9, 0.0, 1.0}; }
    static CorRGBA azul() { return {0.2, 0.4, 0.9, 1.0}; }
    static CorRGBA vermelho() { return {0.9, 0.2, 0.2, 1.0}; }
    static CorRGBA ceuNoturno() { return {0.05, 0.05, 0.15, 1.0}; }
};

} // namespace CalculadoraEstrelas

#endif // TIPOS_HPP
