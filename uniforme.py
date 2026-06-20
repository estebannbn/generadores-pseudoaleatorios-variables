import numpy as np
import matplotlib.pyplot as plt

def generar_uniforme_transformada_inversa(n, a=0, b=1):
    """
    Genera 'n' valores utilizando el método de la Transformada Inversa.
    Inversa de la CDF uniforme: F(x) = (x-a)/(b-a) -> F^-1(u) = a + u*(b-a)
    """
    u = np.random.uniform(0, 1, n)
    return a + u * (b - a)

def generar_uniforme_aceptacion_rechazo(n, a=0, b=1, return_details=False):
    """
    Genera 'n' valores utilizando el método de Aceptación-Rechazo.
    Usa una propuesta Uniforme en un intervalo más amplio [a-1, b+1] 
    para poder visualizar los rechazos.
    """
    resultados = []
    x_acc, y_acc = [], []
    x_rej, y_rej = [], []
    
    # Propuesta: Uniforme en [a-1, b+1]
    a_prop, b_prop = a - 1, b + 1
    max_pdf_objetivo = 1 / (b - a)
    # Factor M necesario tal que M * g(x) >= f(x)
    M = (b_prop - a_prop) / (b - a)
    
    lote = int(n * 2)
    while len(resultados) < n:
        # Generar candidatos a partir de la propuesta (Uniforme en [a-1, b+1])
        x_cand = np.random.uniform(a_prop, b_prop, lote)
        
        # M * g(x) es constante = max_pdf_objetivo en este caso de propuesta uniforme
        y_cand = np.random.uniform(0, max_pdf_objetivo, lote)
        
        # PDF objetivo: 1/(b-a) si a <= x <= b, 0 en otro caso
        pdf_eval = np.where((x_cand >= a) & (x_cand <= b), max_pdf_objetivo, 0)
        
        mask_acc = y_cand <= pdf_eval
        mask_rej = ~mask_acc
        
        if return_details:
            x_acc.extend(x_cand[mask_acc])
            y_acc.extend(y_cand[mask_acc])
            x_rej.extend(x_cand[mask_rej])
            y_rej.extend(y_cand[mask_rej])
            
        resultados.extend(x_cand[mask_acc])
        
    valores = np.array(resultados[:n])
    
    if return_details:
        details = {
            'x_acc': np.array(x_acc[:n]),
            'y_acc': np.array(y_acc[:n]),
            'x_rej': np.array(x_rej),
            'y_rej': np.array(y_rej),
            'pdf': lambda x: np.where((x >= a) & (x <= b), max_pdf_objetivo, 0),
            'max_pdf': max_pdf_objetivo,
            'a': a_prop,
            'b': b_prop
        }
        return valores, details
        
    return valores

if __name__ == "__main__":
    print("=== Generación de Distribución Uniforme ===")
    n_muestras = 10000
    a, b = 0, 10
    
    print(f"Generando {n_muestras} valores (Transformada Inversa)...")
    valores_ti = generar_uniforme_transformada_inversa(n_muestras, a, b)
    
    print(f"Generando {n_muestras} valores (Aceptación-Rechazo)...")
    valores_ar, detalles_ar = generar_uniforme_aceptacion_rechazo(n_muestras, a, b, return_details=True)
    
    print("\nPrimeros 5 valores (Transformada Inversa):", valores_ti[:5])
    print("Primeros 5 valores (Aceptación-Rechazo):", valores_ar[:5])
    
    print("\nGenerando gráficos...")
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    
    # Gráfico 1: Transformada Inversa
    axs[0].hist(valores_ti, bins=30, color='skyblue', edgecolor='black', density=True, label='Histograma')
    axs[0].axhline(1 / (b - a), color='red', linestyle='--', linewidth=2, label='Densidad promedio')
    axs[0].set_title('Uniforme - Transformada Inversa')
    axs[0].set_xlabel('Valor')
    axs[0].set_ylabel('Densidad')
    axs[0].legend(loc='upper right', fontsize='small')
    
    # Gráfico 2: Aceptación-Rechazo
    axs[1].hist(valores_ar, bins=30, color='skyblue', edgecolor='black', density=True, alpha=0.5, zorder=0, label='Histograma')
    
    max_pts = 2000
    x_acc = detalles_ar['x_acc'][:max_pts]
    y_acc = detalles_ar['y_acc'][:max_pts]
    x_rej = detalles_ar['x_rej'][:max_pts]
    y_rej = detalles_ar['y_rej'][:max_pts]
    
    axs[1].scatter(x_rej, y_rej, color='red', alpha=0.4, s=8, label='Rechazados', zorder=1)
    axs[1].scatter(x_acc, y_acc, color='green', alpha=0.4, s=8, label='Aceptados', zorder=2)
    
    x_line = np.linspace(detalles_ar['a'], detalles_ar['b'], 300)
    y_line = detalles_ar['pdf'](x_line)
    axs[1].plot(x_line, y_line, color='black', linewidth=2, label='PDF (Objetivo)', zorder=3)
    axs[1].axhline(detalles_ar['max_pdf'], color='blue', linestyle='--', linewidth=2, label='Propuesta (Uniforme)', zorder=3)
    
    axs[1].set_title('Uniforme - Aceptación-Rechazo')
    axs[1].set_xlabel('Valor')
    axs[1].set_ylabel('Densidad')
    axs[1].legend(loc='upper right', fontsize='small')
    
    plt.tight_layout()
    plt.show()
