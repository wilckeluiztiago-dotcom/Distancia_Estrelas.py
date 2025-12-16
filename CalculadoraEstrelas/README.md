# Calculadora Geométrica de Distância Entre Estrelas

**Autor:** Luiz Tiago Wilcke  
**Data:** 2025

## Descrição

Sistema para calcular a distância real entre estrelas usando métodos geométricos. O projeto inclui implementações em **C++** (com GTK4) e **Python** (com Tkinter/Matplotlib)

## Método Geométrico

O sistema utiliza três métodos geométricos principais:

### 1. Distância por Paralaxe
```
d = 1000 / p   [parsecs]
```
Onde `p` é a paralaxe em milissegundos de arco (mas).

### 2. Separação Angular (Lei dos Cossenos Esférica)
```
cos(θ) = sin(δ₁)·sin(δ₂) + cos(δ₁)·cos(δ₂)·cos(α₁-α₂)
```
Onde:
- α = Ascensão Reta
- δ = Declinação
- θ = Separação angular

### 3. Distância Real (Lei dos Cossenos)
```
D = √(d₁² + d₂² - 2·d₁·d₂·cos(θ))
```

## Estrutura do Projeto

```
CalculadoraEstrelas/
├── cpp/
│   ├── include/
│   │   ├── tipos.hpp        # Estruturas de dados
│   │   └── geometria.hpp    # Funções de cálculo
│   ├── src/
│   │   └── main.cpp         # Interface GTK4
│   └── Makefile
├── python/
│   ├── calculos.py          # Módulo de cálculos
│   ├── interface.py         # Interface Tkinter
│   └── visualizacao.py      # Visualizações avançadas
└── README.md
```

## Instalação

### Dependências C++ (Linux)
```bash
sudo apt-get update
sudo apt-get install -y libgtk-4-dev build-essential
```

### Dependências Python
```bash
pip install matplotlib numpy
```

## Uso

### Versão C++
```bash
cd cpp
make
./calculadora_estrelas
```

### Versão Python
```bash
cd python
python3 interface.py
```

### Teste de Cálculos (Python)
```bash
cd python
python3 calculos.py
```

### Visualizações Avançadas (Python)
```bash
cd python
python3 visualizacao.py
```

## Exemplo de Uso

Dados de exemplo incluídos (Sirius e Betelgeuse):

| Estrela | Ascensão Reta | Declinação | Paralaxe (mas) |
|---------|---------------|------------|----------------|
| Sirius | 06h 45m 08.9s | -16° 42' 58" | 379.21 |
| Betelgeuse | 05h 55m 10.3s | +07° 24' 25" | 4.51 |

**Resultado esperado:** ~220 parsecs (~720 anos-luz)

## Funcionalidades

### Interface Gráfica
- Campos de entrada para coordenadas celestes (HMS e DMS)
- Botão para carregar dados de exemplo
- Renderização visual das equações
- Visualização do plano estelar com posição das estrelas
- Exibição detalhada dos resultados

### Visualizações (Python)
- Mapa celeste 2D
- Visualização 3D do sistema estelar
- Diagrama geométrico do triângulo Sol-Estrela1-Estrela2

## Licença

Este projeto é de código aberto para fins educacionais.

## Créditos

Desenvolvido por **Luiz Tiago Wilcke** - 2025
