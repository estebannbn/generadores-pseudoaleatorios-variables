import numpy as np
import matplotlib.pyplot as plt

def generar_normal_transformada_inversa(n, mu=0, sigma=1):
    """
    Genera 'n' valores utilizando una aproximación numérica del método de 
    la Transformada Inversa (Aproximación de Abramowitz y Stegun para 
    la inversa de la CDF Normal estándar).
    """
    u = np.random.uniform(0, 1, n)
    # Evitar valores de u exactamente 0 o 1 para no tener log(0)
    u = np.clip(u, 1e-10, 1 - 1e-10)
    
    # Constantes para la aproximación de Abramowitz y Stegun (Ec. 26.2.23)
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    
    # La fórmula es simétrica para p <= 0.5. Si p > 0.5, usamos 1-p e invertimos el signo al final
    is_greater = u > 0.5
    u_adj = np.where(is_greater, 1.0 - u, u)
    
    t = np.sqrt(-2.0 * np.log(u_adj))
    num = c0 + c1 * t + c2 * t**2
    den = 1.0 + d1 * t + d2 * t**2 + d3 * t**3
    
    # Z representa la magnitud
    z = t - (num / den)
    
    # Invertir el signo (si u <= 0.5, el cuantil es negativo)
    z = np.where(is_greater, z, -z)
    
    # Escalar a la media y desviación estándar deseadas
    return mu + sigma * z

def generar_normal_aceptacion_rechazo(n, mu=0, sigma=1, return_details=False):
    """
    Genera 'n' valores utilizando el método de Aceptación-Rechazo.
    Usa una propuesta Uniforme en el intervalo [mu - 4*sigma, mu + 4*sigma].
    """
    resultados = []
    x_acc, y_acc = [], []
    x_rej, y_rej = [], []
    
    # PDF de la Normal objetivo
    pdf_normal = lambda x: (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)
    
    # Acotamos el dominio a +/- 4 desviaciones estándar para la propuesta uniforme
    a_prop = mu - 4 * sigma
    b_prop = mu + 4 * sigma
    max_pdf_objetivo = 1 / (sigma * np.sqrt(2 * np.pi))
    
    lote = int(n * 2)
    while len(resultados) < n:
        x_cand = np.random.uniform(a_prop, b_prop, lote)
        y_cand = np.random.uniform(0, max_pdf_objetivo, lote)
        
        pdf_eval = pdf_normal(x_cand)
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
            'pdf': pdf_normal,
            'max_pdf': max_pdf_objetivo,
            'a': a_prop,
            'b': b_prop
        }
        return valores, details
        
    return valores

if __name__ == "__main__":
    print("=== Generación de Distribución Normal ===")
    n_muestras = 10000
    mu, sigma = 5, 2
    
    print(f"Generando {n_muestras} valores (Transformada Inversa)...")
    valores_ti = generar_normal_transformada_inversa(n_muestras, mu, sigma)
    
    print(f"Generando {n_muestras} valores (Aceptación-Rechazo)...")
    valores_ar, detalles_ar = generar_normal_aceptacion_rechazo(n_muestras, mu, sigma, return_details=True)
    
    print("\nPrimeros 5 valores (Transformada Inversa):", valores_ti[:5])
    print("Primeros 5 valores (Aceptación-Rechazo):", valores_ar[:5])
    
    print("\nGenerando gráficos...")
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    
    # Gráfico 1: Transformada Inversa
    axs[0].hist(valores_ti, bins=30, color='lightgreen', edgecolor='black', density=True)
    axs[0].set_title('Normal - Transformada Inversa (Aprox. Numérica)')
    axs[0].set_xlabel('Valor')
    axs[0].set_ylabel('Densidad')
    
    # Gráfico 2: Aceptación-Rechazo
    axs[1].hist(valores_ar, bins=30, color='lightgreen', edgecolor='black', density=True, alpha=0.5, zorder=0, label='Histograma')
    
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
    
    axs[1].set_title('Normal - Aceptación-Rechazo')
    axs[1].set_xlabel('Valor')
    axs[1].set_ylabel('Densidad')
    axs[1].legend(loc='upper right', fontsize='small')
    
    plt.tight_layout()
    plt.show()
