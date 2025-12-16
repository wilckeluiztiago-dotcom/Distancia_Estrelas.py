# Calculadora Geométrica de Distância Entre Estrelas
# Makefile para compilação C++
# Autor: Luiz Tiago Wilcke

CXX = g++
CXXFLAGS = -std=c++20 -Wall -Wextra -O2
GTK_FLAGS = $(shell pkg-config --cflags gtk4)
GTK_LIBS = $(shell pkg-config --libs gtk4)

INCLUDE_DIR = include
SRC_DIR = src
BUILD_DIR = build

TARGET = calculadora_estrelas

SOURCES = $(SRC_DIR)/main.cpp
HEADERS = $(INCLUDE_DIR)/tipos.hpp $(INCLUDE_DIR)/geometria.hpp

.PHONY: all clean run

all: $(TARGET)

$(TARGET): $(SOURCES) $(HEADERS)
	$(CXX) $(CXXFLAGS) $(GTK_FLAGS) -I$(INCLUDE_DIR) $(SOURCES) -o $(TARGET) $(GTK_LIBS)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)

debug: CXXFLAGS += -g -DDEBUG
debug: $(TARGET)

install-deps:
	@echo "Instalando dependências..."
	sudo apt-get update
	sudo apt-get install -y libgtk-4-dev

help:
	@echo "Comandos disponíveis:"
	@echo "  make        - Compila o programa"
	@echo "  make run    - Compila e executa"
	@echo "  make clean  - Remove arquivos compilados"
	@echo "  make debug  - Compila com símbolos de debug"
	@echo "  make install-deps - Instala dependências GTK4"
