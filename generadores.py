import numpy as np
import matplotlib.pyplot as plt

def generar_uniforme(n, a=0, b=1):
    """
    Genera 'n' valores con distribución Uniforme continua entre 'a' y 'b'.
    """
    valores = np.random.uniform(a, b, n)
    return valores

def generar_normal(n, mu=0, sigma=1):
    """
    Genera 'n' valores con distribución Normal con media 'mu' y desviación estándar 'sigma'.
    """
    valores = np.random.normal(mu, sigma, n)
    return valores

def graficar_distribuciones(valores_uniforme, valores_normal):
    """
    Genera histogramas para visualizar ambas distribuciones.
    """
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Gráfico para la distribución Uniforme
    axs[0].hist(valores_uniforme, bins=30, color='skyblue', edgecolor='black', density=True)
    axs[0].set_title('Distribución Uniforme')
    axs[0].set_xlabel('Valor')
    axs[0].set_ylabel('Frecuencia Relativa')

    # Gráfico para la distribución Normal
    axs[1].hist(valores_normal, bins=30, color='lightgreen', edgecolor='black', density=True)
    axs[1].set_title('Distribución Normal')
    axs[1].set_xlabel('Valor')
    axs[1].set_ylabel('Frecuencia Relativa')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    n_muestras = 10000
    n_mostrar = 5
    
    print(f"Generando {n_muestras} valores para cada distribución...")
    
    # Generar valores
    uniformes = generar_uniforme(n_muestras, a=0, b=10)
    normales = generar_normal(n_muestras, mu=5, sigma=2)
    
    print("\nPrimeros", n_mostrar, "valores Uniformes:", uniformes[:n_mostrar])
    print("Primeros", n_mostrar, "valores Normales:", normales[:n_mostrar])
    
    # Visualizar
    print("\nMostrando gráficos de las distribuciones...")
    graficar_distribuciones(uniformes, normales)
