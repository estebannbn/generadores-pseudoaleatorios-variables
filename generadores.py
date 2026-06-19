import numpy as np
import matplotlib.pyplot as plt

def generar_con_transformada_inversa(n, inversa_cdf):
    """
    Genera 'n' valores utilizando el método de la Transformada Inversa.
    """
    u = np.random.uniform(0, 1, n)
    return inversa_cdf(u)

def generar_con_aceptacion_rechazo(n, funcion_pdf, a, b, max_pdf, return_details=False):
    """
    Genera 'n' valores utilizando el método de Aceptación-Rechazo.
    Usa una propuesta Uniforme en el intervalo [a, b].
    Si return_details es True, también devuelve los puntos evaluados para graficar.
    """
    resultados = []
    x_acc, y_acc = [], []
    x_rej, y_rej = [], []
    
    lote = int(n * 2) # Generamos en lotes para mayor eficiencia con numpy
    while len(resultados) < n:
        x_cand = np.random.uniform(a, b, lote)
        y_cand = np.random.uniform(0, max_pdf, lote)
        
        pdf_eval = funcion_pdf(x_cand)
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
            'pdf': funcion_pdf,
            'max_pdf': max_pdf,
            'a': a,
            'b': b
        }
        return valores, details
        
    return valores

def generar_uniforme(n, a=0, b=1, metodo='numpy'):
    """
    Genera 'n' valores con distribución Uniforme continua entre 'a' y 'b'.
    """
    if metodo == 'numpy':
        return np.random.uniform(a, b, n)
    elif metodo == 'transformada_inversa':
        # Inversa de la CDF uniforme: F(x) = (x-a)/(b-a) -> F^-1(u) = a + u*(b-a)
        inversa_cdf = lambda u: a + u * (b - a)
        return generar_con_transformada_inversa(n, inversa_cdf)
    else:
        raise ValueError("Método no soportado")

def generar_normal(n, mu=0, sigma=1, metodo='numpy', return_details=False):
    """
    Genera 'n' valores con distribución Normal con media 'mu' y desviación estándar 'sigma'.
    """
    if metodo == 'numpy':
        valores = np.random.normal(mu, sigma, n)
        return (valores, None) if return_details else valores
    elif metodo == 'aceptacion_rechazo':
        # PDF de la Normal
        pdf_normal = lambda x: (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)
        # Acotamos el dominio a +/- 4 desviaciones estándar para la propuesta uniforme
        a_lim = mu - 4 * sigma
        b_lim = mu + 4 * sigma
        max_pdf = 1 / (sigma * np.sqrt(2 * np.pi))
        return generar_con_aceptacion_rechazo(n, pdf_normal, a_lim, b_lim, max_pdf, return_details)
    else:
        raise ValueError("Método no soportado")

def graficar_distribuciones(valores_uniforme, valores_normal, titulo_sufijo="", detalles_ar=None):
    """
    Genera histogramas para visualizar ambas distribuciones.
    Si se proveen detalles_ar, grafica los puntos de aceptación y rechazo.
    """
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # Gráfico para la distribución Uniforme
    axs[0].hist(valores_uniforme, bins=30, color='skyblue', edgecolor='black', density=True)
    axs[0].set_title(f'Distribución Uniforme {titulo_sufijo}')
    axs[0].set_xlabel('Valor')
    axs[0].set_ylabel('Densidad')

    # Gráfico para la distribución Normal
    if detalles_ar is not None:
        # Histograma de fondo
        axs[1].hist(valores_normal, bins=30, color='lightgreen', edgecolor='black', density=True, alpha=0.5, zorder=0, label='Histograma')
        
        # Para que no sea muy pesada la gráfica, mostramos un máximo de puntos
        max_pts = 2000
        x_acc = detalles_ar['x_acc'][:max_pts]
        y_acc = detalles_ar['y_acc'][:max_pts]
        x_rej = detalles_ar['x_rej'][:max_pts]
        y_rej = detalles_ar['y_rej'][:max_pts]
        
        axs[1].scatter(x_rej, y_rej, color='red', alpha=0.4, s=8, label='Rechazados', zorder=1)
        axs[1].scatter(x_acc, y_acc, color='green', alpha=0.4, s=8, label='Aceptados', zorder=2)
        
        # Líneas de las funciones
        x_line = np.linspace(detalles_ar['a'], detalles_ar['b'], 300)
        y_line = detalles_ar['pdf'](x_line)
        axs[1].plot(x_line, y_line, color='black', linewidth=2, label='PDF (Objetivo)', zorder=3)
        axs[1].axhline(detalles_ar['max_pdf'], color='blue', linestyle='--', linewidth=2, label='Propuesta (Uniforme)', zorder=3)
        
        axs[1].legend(loc='upper right', fontsize='small')
        axs[1].set_title(f'Aceptación-Rechazo Normal {titulo_sufijo}')
    else:
        axs[1].hist(valores_normal, bins=30, color='lightgreen', edgecolor='black', density=True)
        axs[1].set_title(f'Distribución Normal {titulo_sufijo}')
        
    axs[1].set_xlabel('Valor')
    axs[1].set_ylabel('Densidad')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Menú para elegir el método
    print("Seleccione el método de generación:")
    print("1. Funciones nativas de NumPy")
    print("2. Transformada Inversa (Uniforme) y Aceptación-Rechazo (Normal)")
    
    opcion = input("Opción (1 o 2): ")
    
    if opcion == "2":
        metodo_uni = 'transformada_inversa'
        metodo_norm = 'aceptacion_rechazo'
        sufijo = "\n(Algoritmos Propios)"
        usar_detalles = True
    else:
        if opcion != "1":
            print("Opción no válida. Usando NumPy por defecto.")
        metodo_uni = 'numpy'
        metodo_norm = 'numpy'
        sufijo = "\n(NumPy)"
        usar_detalles = False

    n_muestras = 10000
    n_mostrar = 5
    
    print(f"\nGenerando {n_muestras} valores...")
    
    # Generar valores
    uniformes = generar_uniforme(n_muestras, a=0, b=10, metodo=metodo_uni)
    
    if usar_detalles:
        normales, detalles_ar = generar_normal(n_muestras, mu=5, sigma=2, metodo=metodo_norm, return_details=True)
    else:
        normales = generar_normal(n_muestras, mu=5, sigma=2, metodo=metodo_norm, return_details=False)
        detalles_ar = None
    
    print("\nPrimeros", n_mostrar, "valores Uniformes:", uniformes[:n_mostrar])
    print("Primeros", n_mostrar, "valores Normales:", normales[:n_mostrar])
    
    # Visualizar
    print("\nMostrando gráficos de las distribuciones...")
    graficar_distribuciones(uniformes, normales, sufijo, detalles_ar)
