/**
 * Calculadora Geométrica de Distância Entre Estrelas
 * Interface Gráfica GTK4
 * 
 * Autor: Luiz Tiago Wilcke
 * Data: 2025
 */

#include <gtk/gtk.h>
#include <cairo.h>
#include <cmath>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include "../include/tipos.hpp"
#include "../include/geometria.hpp"

using namespace CalculadoraEstrelas;

// ============================================================================
// Variáveis Globais da Interface
// ============================================================================

// Entradas para Estrela 1
GtkWidget *entrada_nome1;
GtkWidget *entrada_ar_h1, *entrada_ar_m1, *entrada_ar_s1;
GtkWidget *entrada_dec_g1, *entrada_dec_m1, *entrada_dec_s1;
GtkWidget *combo_dec_sinal1;
GtkWidget *entrada_paralaxe1;

// Entradas para Estrela 2
GtkWidget *entrada_nome2;
GtkWidget *entrada_ar_h2, *entrada_ar_m2, *entrada_ar_s2;
GtkWidget *entrada_dec_g2, *entrada_dec_m2, *entrada_dec_s2;
GtkWidget *combo_dec_sinal2;
GtkWidget *entrada_paralaxe2;

// Área de resultados
GtkWidget *area_resultados;
GtkWidget *area_desenho;
GtkWidget *area_equacoes;

// Resultado atual
ResultadoCalculo resultado_atual;
Estrela estrela1, estrela2;
bool calculo_realizado = false;

// ============================================================================
// Funções Auxiliares
// ============================================================================

double obterValorEntrada(GtkWidget *entrada) {
    const char *texto = gtk_editable_get_text(GTK_EDITABLE(entrada));
    if (texto == nullptr || strlen(texto) == 0) return 0.0;
    return std::stod(texto);
}

int obterValorEntradaInt(GtkWidget *entrada) {
    const char *texto = gtk_editable_get_text(GTK_EDITABLE(entrada));
    if (texto == nullptr || strlen(texto) == 0) return 0;
    return std::stoi(texto);
}

std::string obterTextoEntrada(GtkWidget *entrada) {
    const char *texto = gtk_editable_get_text(GTK_EDITABLE(entrada));
    return texto ? std::string(texto) : "";
}

// ============================================================================
// Desenho do Plano Estelar
// ============================================================================

void desenharPlanoEstelar(GtkDrawingArea *area, cairo_t *cr, 
                           int largura, int altura, gpointer dados) {
    // Fundo céu noturno
    cairo_set_source_rgb(cr, 0.02, 0.02, 0.08);
    cairo_paint(cr);
    
    // Desenhar estrelas aleatórias de fundo
    srand(42);
    cairo_set_source_rgba(cr, 1.0, 1.0, 1.0, 0.3);
    for (int i = 0; i < 100; i++) {
        double x = rand() % largura;
        double y = rand() % altura;
        double r = (rand() % 10) / 10.0 + 0.5;
        cairo_arc(cr, x, y, r, 0, 2 * M_PI);
        cairo_fill(cr);
    }
    
    if (!calculo_realizado) {
        // Texto de instrução
        cairo_set_source_rgb(cr, 0.5, 0.5, 0.7);
        cairo_select_font_face(cr, "Sans", CAIRO_FONT_SLANT_ITALIC, CAIRO_FONT_WEIGHT_NORMAL);
        cairo_set_font_size(cr, 14);
        cairo_move_to(cr, largura/2 - 120, altura/2);
        cairo_show_text(cr, "Insira os dados e clique em Calcular");
        return;
    }
    
    // Centro do desenho
    double cx = largura / 2.0;
    double cy = altura / 2.0;
    double raio = std::min(largura, altura) * 0.35;
    
    // Desenhar círculo do céu (horizonte)
    cairo_set_source_rgba(cr, 0.2, 0.3, 0.5, 0.5);
    cairo_set_line_width(cr, 2);
    cairo_arc(cr, cx, cy, raio, 0, 2 * M_PI);
    cairo_stroke(cr);
    
    // Converter coordenadas para posição no círculo
    // Usando projeção estereográfica simples
    auto projetarEstrela = [cx, cy, raio](const Estrela& e) -> std::pair<double, double> {
        double ar = e.ascensaoReta.paraGraus() / 360.0 * 2 * M_PI;
        double dec = e.declinacao.paraGraus() / 90.0;
        
        double r = raio * (1 - std::abs(dec));
        double x = cx + r * std::cos(ar);
        double y = cy - r * std::sin(ar);
        
        return {x, y};
    };
    
    auto [x1, y1] = projetarEstrela(estrela1);
    auto [x2, y2] = projetarEstrela(estrela2);
    
    // Desenhar linha conectando as estrelas
    cairo_set_source_rgba(cr, 0.4, 0.8, 1.0, 0.6);
    cairo_set_line_width(cr, 2);
    cairo_move_to(cr, x1, y1);
    cairo_line_to(cr, x2, y2);
    cairo_stroke(cr);
    
    // Desenhar Estrela 1 (amarelo)
    cairo_set_source_rgb(cr, 1.0, 0.9, 0.2);
    cairo_arc(cr, x1, y1, 8, 0, 2 * M_PI);
    cairo_fill(cr);
    
    // Brilho
    cairo_set_source_rgba(cr, 1.0, 0.95, 0.5, 0.3);
    cairo_arc(cr, x1, y1, 15, 0, 2 * M_PI);
    cairo_fill(cr);
    
    // Nome da estrela 1
    cairo_set_source_rgb(cr, 1.0, 0.9, 0.2);
    cairo_select_font_face(cr, "Sans", CAIRO_FONT_SLANT_NORMAL, CAIRO_FONT_WEIGHT_BOLD);
    cairo_set_font_size(cr, 12);
    cairo_move_to(cr, x1 + 12, y1 - 10);
    cairo_show_text(cr, estrela1.nome.c_str());
    
    // Desenhar Estrela 2 (azul)
    cairo_set_source_rgb(cr, 0.4, 0.7, 1.0);
    cairo_arc(cr, x2, y2, 8, 0, 2 * M_PI);
    cairo_fill(cr);
    
    // Brilho
    cairo_set_source_rgba(cr, 0.5, 0.8, 1.0, 0.3);
    cairo_arc(cr, x2, y2, 15, 0, 2 * M_PI);
    cairo_fill(cr);
    
    // Nome da estrela 2
    cairo_set_source_rgb(cr, 0.4, 0.7, 1.0);
    cairo_move_to(cr, x2 + 12, y2 - 10);
    cairo_show_text(cr, estrela2.nome.c_str());
    
    // Distância no meio da linha
    double mx = (x1 + x2) / 2;
    double my = (y1 + y2) / 2;
    
    std::ostringstream ss;
    ss << std::fixed << std::setprecision(2) 
       << resultado_atual.distanciaRealAnosLuz << " a.l.";
    
    cairo_set_source_rgb(cr, 0.2, 1.0, 0.4);
    cairo_select_font_face(cr, "Sans", CAIRO_FONT_SLANT_NORMAL, CAIRO_FONT_WEIGHT_BOLD);
    cairo_set_font_size(cr, 11);
    cairo_move_to(cr, mx + 5, my - 5);
    cairo_show_text(cr, ss.str().c_str());
    
    // Informação do ângulo
    std::ostringstream ssAng;
    ssAng << std::fixed << std::setprecision(2) 
          << "θ = " << resultado_atual.separacaoAngularGraus << "°";
    
    cairo_set_source_rgb(cr, 0.8, 0.8, 0.9);
    cairo_set_font_size(cr, 10);
    cairo_move_to(cr, mx + 5, my + 10);
    cairo_show_text(cr, ssAng.str().c_str());
}

// ============================================================================
// Desenho das Equações
// ============================================================================

void desenharEquacoes(GtkDrawingArea *area, cairo_t *cr,
                       int largura, int altura, gpointer dados) {
    // Fundo escuro
    cairo_set_source_rgb(cr, 0.1, 0.1, 0.15);
    cairo_paint(cr);
    
    cairo_set_source_rgb(cr, 0.9, 0.9, 0.95);
    cairo_select_font_face(cr, "Monospace", CAIRO_FONT_SLANT_NORMAL, CAIRO_FONT_WEIGHT_NORMAL);
    
    double y = 30;
    double espacamento = 22;
    
    // Título
    cairo_set_font_size(cr, 16);
    cairo_set_source_rgb(cr, 0.4, 0.8, 1.0);
    cairo_move_to(cr, 20, y);
    cairo_show_text(cr, "MÉTODO GEOMÉTRICO PARA DISTÂNCIA ESTELAR");
    y += espacamento * 1.5;
    
    // Autor
    cairo_set_font_size(cr, 11);
    cairo_set_source_rgb(cr, 0.6, 0.6, 0.7);
    cairo_move_to(cr, 20, y);
    cairo_show_text(cr, "Autor: Luiz Tiago Wilcke");
    y += espacamento * 1.5;
    
    cairo_set_font_size(cr, 13);
    
    // Equação 1 - Paralaxe
    cairo_set_source_rgb(cr, 1.0, 0.9, 0.3);
    cairo_move_to(cr, 20, y);
    cairo_show_text(cr, "1. Distância por Paralaxe:");
    y += espacamento;
    
    cairo_set_source_rgb(cr, 0.9, 0.9, 0.95);
    cairo_move_to(cr, 40, y);
    cairo_show_text(cr, "d = 1000 / p   [parsecs]");
    y += espacamento * 1.5;
    
    // Equação 2 - Lei dos Cossenos Esférica
    cairo_set_source_rgb(cr, 1.0, 0.9, 0.3);
    cairo_move_to(cr, 20, y);
    cairo_show_text(cr, "2. Separação Angular (Lei dos Cossenos Esférica):");
    y += espacamento;
    
    cairo_set_source_rgb(cr, 0.9, 0.9, 0.95);
    cairo_move_to(cr, 40, y);
    cairo_show_text(cr, "cos(θ) = sin(δ₁)·sin(δ₂) + cos(δ₁)·cos(δ₂)·cos(α₁-α₂)");
    y += espacamento * 1.5;
    
    // Equação 3 - Distância Real
    cairo_set_source_rgb(cr, 1.0, 0.9, 0.3);
    cairo_move_to(cr, 20, y);
    cairo_show_text(cr, "3. Distância Real (Lei dos Cossenos):");
    y += espacamento;
    
    cairo_set_source_rgb(cr, 0.9, 0.9, 0.95);
    cairo_move_to(cr, 40, y);
    cairo_show_text(cr, "D = √(d₁² + d₂² - 2·d₁·d₂·cos(θ))");
    y += espacamento * 2;
    
    // Resultados se disponíveis
    if (calculo_realizado) {
        cairo_set_source_rgb(cr, 0.3, 1.0, 0.5);
        cairo_move_to(cr, 20, y);
        cairo_show_text(cr, "RESULTADOS:");
        y += espacamento;
        
        std::ostringstream ss;
        
        cairo_set_source_rgb(cr, 0.8, 0.8, 0.9);
        ss << "• d₁ (" << estrela1.nome << ") = " 
           << std::fixed << std::setprecision(4) << resultado_atual.distancia1Parsecs 
           << " pc = " << std::setprecision(2) << resultado_atual.distancia1Parsecs * PARSEC_PARA_ANOS_LUZ << " a.l.";
        cairo_move_to(cr, 30, y);
        cairo_show_text(cr, ss.str().c_str());
        y += espacamento;
        
        ss.str(""); ss.clear();
        ss << "• d₂ (" << estrela2.nome << ") = " 
           << std::fixed << std::setprecision(4) << resultado_atual.distancia2Parsecs 
           << " pc = " << std::setprecision(2) << resultado_atual.distancia2Parsecs * PARSEC_PARA_ANOS_LUZ << " a.l.";
        cairo_move_to(cr, 30, y);
        cairo_show_text(cr, ss.str().c_str());
        y += espacamento;
        
        ss.str(""); ss.clear();
        ss << "• θ (separação angular) = " 
           << std::fixed << std::setprecision(4) << resultado_atual.separacaoAngularGraus << "°";
        cairo_move_to(cr, 30, y);
        cairo_show_text(cr, ss.str().c_str());
        y += espacamento;
        
        cairo_set_source_rgb(cr, 0.3, 1.0, 0.5);
        ss.str(""); ss.clear();
        ss << "• D (distância real) = " 
           << std::fixed << std::setprecision(4) << resultado_atual.distanciaRealParsecs 
           << " pc = " << std::setprecision(2) << resultado_atual.distanciaRealAnosLuz << " anos-luz";
        cairo_move_to(cr, 30, y);
        cairo_show_text(cr, ss.str().c_str());
    }
}

// ============================================================================
// Callback do Botão Calcular
// ============================================================================

void ao_clicar_calcular(GtkWidget *botao, gpointer dados) {
    // Ler dados da Estrela 1
    estrela1.nome = obterTextoEntrada(entrada_nome1);
    if (estrela1.nome.empty()) estrela1.nome = "Estrela 1";
    
    estrela1.ascensaoReta.horas = obterValorEntradaInt(entrada_ar_h1);
    estrela1.ascensaoReta.minutos = obterValorEntradaInt(entrada_ar_m1);
    estrela1.ascensaoReta.segundos = obterValorEntrada(entrada_ar_s1);
    
    estrela1.declinacao.graus = obterValorEntradaInt(entrada_dec_g1);
    estrela1.declinacao.minutos = obterValorEntradaInt(entrada_dec_m1);
    estrela1.declinacao.segundos = obterValorEntrada(entrada_dec_s1);
    
    guint idx1 = gtk_drop_down_get_selected(GTK_DROP_DOWN(combo_dec_sinal1));
    estrela1.declinacao.positivo = (idx1 == 0);
    
    estrela1.paralaxeMas = obterValorEntrada(entrada_paralaxe1);
    
    // Ler dados da Estrela 2
    estrela2.nome = obterTextoEntrada(entrada_nome2);
    if (estrela2.nome.empty()) estrela2.nome = "Estrela 2";
    
    estrela2.ascensaoReta.horas = obterValorEntradaInt(entrada_ar_h2);
    estrela2.ascensaoReta.minutos = obterValorEntradaInt(entrada_ar_m2);
    estrela2.ascensaoReta.segundos = obterValorEntrada(entrada_ar_s2);
    
    estrela2.declinacao.graus = obterValorEntradaInt(entrada_dec_g2);
    estrela2.declinacao.minutos = obterValorEntradaInt(entrada_dec_m2);
    estrela2.declinacao.segundos = obterValorEntrada(entrada_dec_s2);
    
    guint idx2 = gtk_drop_down_get_selected(GTK_DROP_DOWN(combo_dec_sinal2));
    estrela2.declinacao.positivo = (idx2 == 0);
    
    estrela2.paralaxeMas = obterValorEntrada(entrada_paralaxe2);
    
    // Realizar cálculo
    resultado_atual = CalculadoraGeometrica::calcularDistanciaEntreEstrelas(estrela1, estrela2);
    calculo_realizado = true;
    
    // Atualizar área de texto
    std::ostringstream ss;
    ss << "═══════════════════════════════════════════════════\n";
    ss << "  RESULTADO DO CÁLCULO\n";
    ss << "═══════════════════════════════════════════════════\n\n";
    ss << "  Estrela 1: " << estrela1.nome << "\n";
    ss << "  Distância: " << std::fixed << std::setprecision(4) 
       << resultado_atual.distancia1Parsecs << " pc ("
       << std::setprecision(2) << resultado_atual.distancia1Parsecs * PARSEC_PARA_ANOS_LUZ << " a.l.)\n\n";
    ss << "  Estrela 2: " << estrela2.nome << "\n";
    ss << "  Distância: " << std::fixed << std::setprecision(4)
       << resultado_atual.distancia2Parsecs << " pc ("
       << std::setprecision(2) << resultado_atual.distancia2Parsecs * PARSEC_PARA_ANOS_LUZ << " a.l.)\n\n";
    ss << "  Separação Angular: " << std::setprecision(4) 
       << resultado_atual.separacaoAngularGraus << "°\n\n";
    ss << "  ★ DISTÂNCIA REAL ENTRE AS ESTRELAS ★\n";
    ss << "     " << std::setprecision(4) << resultado_atual.distanciaRealParsecs << " parsecs\n";
    ss << "     " << std::setprecision(2) << resultado_atual.distanciaRealAnosLuz << " anos-luz\n";
    ss << "═══════════════════════════════════════════════════\n";
    
    GtkTextBuffer *buffer = gtk_text_view_get_buffer(GTK_TEXT_VIEW(area_resultados));
    gtk_text_buffer_set_text(buffer, ss.str().c_str(), -1);
    
    // Redesenhar
    gtk_widget_queue_draw(area_desenho);
    gtk_widget_queue_draw(area_equacoes);
}

// ============================================================================
// Callback do Botão Limpar
// ============================================================================

void ao_clicar_limpar(GtkWidget *botao, gpointer dados) {
    // Limpar entradas da Estrela 1
    gtk_editable_set_text(GTK_EDITABLE(entrada_nome1), "");
    gtk_editable_set_text(GTK_EDITABLE(entrada_ar_h1), "");
    gtk_editable_set_text(GTK_EDITABLE(entrada_ar_m1), "");
    gtk_editable_set_text(GTK_EDITABLE(entrada_ar_s1), "");
    gtk_editable_set_text(GTK_EDITABLE(entrada_dec_g1), "");
    gtk_editable_set_text(GTK_EDITABLE(entrada_dec_m1), "");
    gtk_editable_set_text(GTK_EDITABLE(entrada_dec_s1), "");
    gtk_editable_set_text(GTK_EDITABLE(entrada_paralaxe1), "");
    
    // Limpar entradas da Estrela 2
    gtk_editable_set_text(GTK_EDITABLE(entrada_nome2), "");
    gtk_editable_set_text(GTK_EDITABLE(entrada_ar_h2), "");
    gtk_editable_set_text(GTK_EDITABLE(entrada_ar_m2), "");
    gtk_editable_set_text(GTK_EDITABLE(entrada_ar_s2), "");
    gtk_editable_set_text(GTK_EDITABLE(entrada_dec_g2), "");
    gtk_editable_set_text(GTK_EDITABLE(entrada_dec_m2), "");
    gtk_editable_set_text(GTK_EDITABLE(entrada_dec_s2), "");
    gtk_editable_set_text(GTK_EDITABLE(entrada_paralaxe2), "");
    
    // Limpar resultados
    GtkTextBuffer *buffer = gtk_text_view_get_buffer(GTK_TEXT_VIEW(area_resultados));
    gtk_text_buffer_set_text(buffer, "", -1);
    
    calculo_realizado = false;
    gtk_widget_queue_draw(area_desenho);
    gtk_widget_queue_draw(area_equacoes);
}

// ============================================================================
// Callback Carregar Exemplo
// ============================================================================

void ao_clicar_exemplo(GtkWidget *botao, gpointer dados) {
    // Carregar dados de Sirius
    gtk_editable_set_text(GTK_EDITABLE(entrada_nome1), "Sirius");
    gtk_editable_set_text(GTK_EDITABLE(entrada_ar_h1), "6");
    gtk_editable_set_text(GTK_EDITABLE(entrada_ar_m1), "45");
    gtk_editable_set_text(GTK_EDITABLE(entrada_ar_s1), "8.9");
    gtk_editable_set_text(GTK_EDITABLE(entrada_dec_g1), "16");
    gtk_editable_set_text(GTK_EDITABLE(entrada_dec_m1), "42");
    gtk_editable_set_text(GTK_EDITABLE(entrada_dec_s1), "58");
    gtk_drop_down_set_selected(GTK_DROP_DOWN(combo_dec_sinal1), 1); // Sul
    gtk_editable_set_text(GTK_EDITABLE(entrada_paralaxe1), "379.21");
    
    // Carregar dados de Betelgeuse
    gtk_editable_set_text(GTK_EDITABLE(entrada_nome2), "Betelgeuse");
    gtk_editable_set_text(GTK_EDITABLE(entrada_ar_h2), "5");
    gtk_editable_set_text(GTK_EDITABLE(entrada_ar_m2), "55");
    gtk_editable_set_text(GTK_EDITABLE(entrada_ar_s2), "10.3");
    gtk_editable_set_text(GTK_EDITABLE(entrada_dec_g2), "7");
    gtk_editable_set_text(GTK_EDITABLE(entrada_dec_m2), "24");
    gtk_editable_set_text(GTK_EDITABLE(entrada_dec_s2), "25");
    gtk_drop_down_set_selected(GTK_DROP_DOWN(combo_dec_sinal2), 0); // Norte
    gtk_editable_set_text(GTK_EDITABLE(entrada_paralaxe2), "4.51");
}

// ============================================================================
// Criar Frame de Entrada para uma Estrela
// ============================================================================

GtkWidget* criarFrameEstrela(int numero, 
    GtkWidget **nome, GtkWidget **ar_h, GtkWidget **ar_m, GtkWidget **ar_s,
    GtkWidget **dec_g, GtkWidget **dec_m, GtkWidget **dec_s, 
    GtkWidget **dec_sinal, GtkWidget **paralaxe) {
    
    std::string titulo = "★ Estrela " + std::to_string(numero);
    GtkWidget *frame = gtk_frame_new(titulo.c_str());
    gtk_widget_add_css_class(frame, "estrela-frame");
    
    GtkWidget *grid = gtk_grid_new();
    gtk_grid_set_row_spacing(GTK_GRID(grid), 8);
    gtk_grid_set_column_spacing(GTK_GRID(grid), 8);
    gtk_widget_set_margin_start(grid, 10);
    gtk_widget_set_margin_end(grid, 10);
    gtk_widget_set_margin_top(grid, 10);
    gtk_widget_set_margin_bottom(grid, 10);
    
    int linha = 0;
    
    // Nome
    gtk_grid_attach(GTK_GRID(grid), gtk_label_new("Nome:"), 0, linha, 1, 1);
    *nome = gtk_entry_new();
    gtk_widget_set_hexpand(*nome, TRUE);
    gtk_entry_set_placeholder_text(GTK_ENTRY(*nome), "Ex: Sirius");
    gtk_grid_attach(GTK_GRID(grid), *nome, 1, linha, 5, 1);
    linha++;
    
    // Ascensão Reta
    gtk_grid_attach(GTK_GRID(grid), gtk_label_new("Ascensão Reta (α):"), 0, linha, 1, 1);
    
    GtkWidget *box_ar = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 5);
    *ar_h = gtk_entry_new();
    gtk_entry_set_placeholder_text(GTK_ENTRY(*ar_h), "h");
    gtk_widget_set_size_request(*ar_h, 50, -1);
    *ar_m = gtk_entry_new();
    gtk_entry_set_placeholder_text(GTK_ENTRY(*ar_m), "m");
    gtk_widget_set_size_request(*ar_m, 50, -1);
    *ar_s = gtk_entry_new();
    gtk_entry_set_placeholder_text(GTK_ENTRY(*ar_s), "s");
    gtk_widget_set_size_request(*ar_s, 70, -1);
    
    gtk_box_append(GTK_BOX(box_ar), *ar_h);
    gtk_box_append(GTK_BOX(box_ar), gtk_label_new("h"));
    gtk_box_append(GTK_BOX(box_ar), *ar_m);
    gtk_box_append(GTK_BOX(box_ar), gtk_label_new("m"));
    gtk_box_append(GTK_BOX(box_ar), *ar_s);
    gtk_box_append(GTK_BOX(box_ar), gtk_label_new("s"));
    
    gtk_grid_attach(GTK_GRID(grid), box_ar, 1, linha, 5, 1);
    linha++;
    
    // Declinação
    gtk_grid_attach(GTK_GRID(grid), gtk_label_new("Declinação (δ):"), 0, linha, 1, 1);
    
    GtkWidget *box_dec = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 5);
    
    const char *sinais[] = {"+ (Norte)", "- (Sul)", NULL};
    *dec_sinal = gtk_drop_down_new_from_strings(sinais);
    gtk_widget_set_size_request(*dec_sinal, 100, -1);
    
    *dec_g = gtk_entry_new();
    gtk_entry_set_placeholder_text(GTK_ENTRY(*dec_g), "°");
    gtk_widget_set_size_request(*dec_g, 50, -1);
    *dec_m = gtk_entry_new();
    gtk_entry_set_placeholder_text(GTK_ENTRY(*dec_m), "'");
    gtk_widget_set_size_request(*dec_m, 50, -1);
    *dec_s = gtk_entry_new();
    gtk_entry_set_placeholder_text(GTK_ENTRY(*dec_s), "\"");
    gtk_widget_set_size_request(*dec_s, 70, -1);
    
    gtk_box_append(GTK_BOX(box_dec), *dec_sinal);
    gtk_box_append(GTK_BOX(box_dec), *dec_g);
    gtk_box_append(GTK_BOX(box_dec), gtk_label_new("°"));
    gtk_box_append(GTK_BOX(box_dec), *dec_m);
    gtk_box_append(GTK_BOX(box_dec), gtk_label_new("'"));
    gtk_box_append(GTK_BOX(box_dec), *dec_s);
    gtk_box_append(GTK_BOX(box_dec), gtk_label_new("\""));
    
    gtk_grid_attach(GTK_GRID(grid), box_dec, 1, linha, 5, 1);
    linha++;
    
    // Paralaxe
    gtk_grid_attach(GTK_GRID(grid), gtk_label_new("Paralaxe (mas):"), 0, linha, 1, 1);
    *paralaxe = gtk_entry_new();
    gtk_entry_set_placeholder_text(GTK_ENTRY(*paralaxe), "milissegundos de arco");
    gtk_widget_set_hexpand(*paralaxe, TRUE);
    gtk_grid_attach(GTK_GRID(grid), *paralaxe, 1, linha, 5, 1);
    
    gtk_frame_set_child(GTK_FRAME(frame), grid);
    
    return frame;
}

// ============================================================================
// Ativação do Aplicativo
// ============================================================================

static void activate(GtkApplication *app, gpointer user_data) {
    GtkWidget *janela = gtk_application_window_new(app);
    gtk_window_set_title(GTK_WINDOW(janela), "Calculadora Geométrica de Distância Entre Estrelas - Autor: Luiz Tiago Wilcke");
    gtk_window_set_default_size(GTK_WINDOW(janela), 1200, 800);
    
    // CSS
    GtkCssProvider *css = gtk_css_provider_new();
    gtk_css_provider_load_from_string(css, 
        "window { background: linear-gradient(to bottom, #1a1a2e, #16213e); }"
        ".estrela-frame { background: rgba(30, 40, 70, 0.8); border-radius: 8px; }"
        "frame > label { color: #4fc3f7; font-weight: bold; font-size: 14px; }"
        "entry { background: #2d3748; color: #e2e8f0; border: 1px solid #4a5568; border-radius: 4px; padding: 6px; }"
        "label { color: #a0aec0; }"
        "button { background: linear-gradient(to bottom, #667eea, #764ba2); color: white; "
        "         font-weight: bold; border-radius: 6px; padding: 10px 20px; border: none; }"
        "button:hover { background: linear-gradient(to bottom, #764ba2, #667eea); }"
        ".btn-exemplo { background: linear-gradient(to bottom, #38a169, #2f855a); }"
        ".btn-limpar { background: linear-gradient(to bottom, #e53e3e, #c53030); }"
        "textview { background: #1a202c; color: #68d391; font-family: monospace; }"
    );
    gtk_style_context_add_provider_for_display(
        gdk_display_get_default(),
        GTK_STYLE_PROVIDER(css),
        GTK_STYLE_PROVIDER_PRIORITY_APPLICATION
    );
    
    // Layout principal
    GtkWidget *box_principal = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 10);
    gtk_widget_set_margin_start(box_principal, 10);
    gtk_widget_set_margin_end(box_principal, 10);
    gtk_widget_set_margin_top(box_principal, 10);
    gtk_widget_set_margin_bottom(box_principal, 10);
    
    // Painel esquerdo (entradas)
    GtkWidget *painel_esquerdo = gtk_box_new(GTK_ORIENTATION_VERTICAL, 10);
    gtk_widget_set_size_request(painel_esquerdo, 450, -1);
    
    // Título
    GtkWidget *titulo = gtk_label_new("★ CALCULADORA DE DISTÂNCIA ESTELAR ★");
    gtk_widget_add_css_class(titulo, "titulo");
    gtk_box_append(GTK_BOX(painel_esquerdo), titulo);
    
    // Frame Estrela 1
    GtkWidget *frame1 = criarFrameEstrela(1, 
        &entrada_nome1, &entrada_ar_h1, &entrada_ar_m1, &entrada_ar_s1,
        &entrada_dec_g1, &entrada_dec_m1, &entrada_dec_s1,
        &combo_dec_sinal1, &entrada_paralaxe1);
    gtk_box_append(GTK_BOX(painel_esquerdo), frame1);
    
    // Frame Estrela 2
    GtkWidget *frame2 = criarFrameEstrela(2,
        &entrada_nome2, &entrada_ar_h2, &entrada_ar_m2, &entrada_ar_s2,
        &entrada_dec_g2, &entrada_dec_m2, &entrada_dec_s2,
        &combo_dec_sinal2, &entrada_paralaxe2);
    gtk_box_append(GTK_BOX(painel_esquerdo), frame2);
    
    // Botões
    GtkWidget *box_botoes = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 10);
    gtk_widget_set_halign(box_botoes, GTK_ALIGN_CENTER);
    
    GtkWidget *btn_calcular = gtk_button_new_with_label("⚡ CALCULAR");
    g_signal_connect(btn_calcular, "clicked", G_CALLBACK(ao_clicar_calcular), NULL);
    
    GtkWidget *btn_exemplo = gtk_button_new_with_label("📋 Exemplo");
    gtk_widget_add_css_class(btn_exemplo, "btn-exemplo");
    g_signal_connect(btn_exemplo, "clicked", G_CALLBACK(ao_clicar_exemplo), NULL);
    
    GtkWidget *btn_limpar = gtk_button_new_with_label("🗑 Limpar");
    gtk_widget_add_css_class(btn_limpar, "btn-limpar");
    g_signal_connect(btn_limpar, "clicked", G_CALLBACK(ao_clicar_limpar), NULL);
    
    gtk_box_append(GTK_BOX(box_botoes), btn_calcular);
    gtk_box_append(GTK_BOX(box_botoes), btn_exemplo);
    gtk_box_append(GTK_BOX(box_botoes), btn_limpar);
    gtk_box_append(GTK_BOX(painel_esquerdo), box_botoes);
    
    // Área de resultados texto
    GtkWidget *frame_resultados = gtk_frame_new("Resultados");
    area_resultados = gtk_text_view_new();
    gtk_text_view_set_editable(GTK_TEXT_VIEW(area_resultados), FALSE);
    gtk_text_view_set_wrap_mode(GTK_TEXT_VIEW(area_resultados), GTK_WRAP_WORD);
    gtk_widget_set_vexpand(area_resultados, TRUE);
    
    GtkWidget *scroll_resultados = gtk_scrolled_window_new();
    gtk_scrolled_window_set_child(GTK_SCROLLED_WINDOW(scroll_resultados), area_resultados);
    gtk_widget_set_size_request(scroll_resultados, -1, 150);
    gtk_frame_set_child(GTK_FRAME(frame_resultados), scroll_resultados);
    gtk_box_append(GTK_BOX(painel_esquerdo), frame_resultados);
    
    gtk_box_append(GTK_BOX(box_principal), painel_esquerdo);
    
    // Painel direito (visualizações)
    GtkWidget *painel_direito = gtk_box_new(GTK_ORIENTATION_VERTICAL, 10);
    gtk_widget_set_hexpand(painel_direito, TRUE);
    
    // Área de desenho do plano estelar
    GtkWidget *frame_desenho = gtk_frame_new("Plano Estelar");
    area_desenho = gtk_drawing_area_new();
    gtk_widget_set_size_request(area_desenho, 400, 300);
    gtk_widget_set_vexpand(area_desenho, TRUE);
    gtk_drawing_area_set_draw_func(GTK_DRAWING_AREA(area_desenho),
        (GtkDrawingAreaDrawFunc)desenharPlanoEstelar, NULL, NULL);
    gtk_frame_set_child(GTK_FRAME(frame_desenho), area_desenho);
    gtk_box_append(GTK_BOX(painel_direito), frame_desenho);
    
    // Área de renderização das equações
    GtkWidget *frame_equacoes = gtk_frame_new("Método Geométrico e Equações");
    area_equacoes = gtk_drawing_area_new();
    gtk_widget_set_size_request(area_equacoes, 400, 300);
    gtk_widget_set_vexpand(area_equacoes, TRUE);
    gtk_drawing_area_set_draw_func(GTK_DRAWING_AREA(area_equacoes),
        (GtkDrawingAreaDrawFunc)desenharEquacoes, NULL, NULL);
    gtk_frame_set_child(GTK_FRAME(frame_equacoes), area_equacoes);
    gtk_box_append(GTK_BOX(painel_direito), frame_equacoes);
    
    gtk_box_append(GTK_BOX(box_principal), painel_direito);
    
    gtk_window_set_child(GTK_WINDOW(janela), box_principal);
    gtk_window_present(GTK_WINDOW(janela));
}

// ============================================================================
// Função Principal
// ============================================================================

int main(int argc, char **argv) {
    GtkApplication *app = gtk_application_new(
        "com.luiztiago.calculadora.estrelas",
        G_APPLICATION_DEFAULT_FLAGS
    );
    
    g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);
    
    int status = g_application_run(G_APPLICATION(app), argc, argv);
    g_object_unref(app);
    
    return status;
}
