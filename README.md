# Generadores Pseudoaleatorios de Variables

Este proyecto contiene diferentes scripts en Python para generar variables pseudoaleatorias siguiendo dos distribuciones de probabilidad diferentes: **Uniforme** y **Normal**. 

Recientemente se han incorporado algoritmos manuales para la generación de estas variables, permitiendo elegir entre usar las funciones nativas de NumPy o emplear métodos analíticos paso a paso.

## Requisitos Previos

Asegúrate de tener instalado [Python](https://www.python.org/) (versión 3.6 o superior).
El script utiliza librerías de terceros para la generación de números y su visualización.

## Instalación

1. Clona o descarga este repositorio.
2. Abre una terminal en el directorio del proyecto.
3. (Opcional pero recomendado) Crea y activa un entorno virtual (el proyecto ya ignora la carpeta `venv` en `.gitignore`):
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```
4. Instala las dependencias necesarias ejecutando:
   ```bash
   pip install -r requirements.txt
   ```

## Uso del Programa

Para ejecutar el programa, simplemente corre el script que desees desde la terminal:

```bash
python [nombre_del_script].py
```

Al iniciar cualquiera de los scripts, se ejecutarán automáticamente las simulaciones utilizando **dos algoritmos analíticos propios**, comparándolos simultáneamente:
1. **Transformada Inversa**
2. **Aceptación-Rechazo**

### ¿Qué métodos se implementan?

- **Método de la Transformada Inversa**: Se aplica para generar la **Distribución Uniforme**. Invertimos analíticamente la Función de Distribución Acumulada (CDF) para mapear valores aleatorios base al rango objetivo.
- **Método de Aceptación-Rechazo**: Se aplica para generar la **Distribución Normal**. Se define una distribución de propuesta (Uniforme que actúa como techo) y se generan puntos candidatos $(X, Y)$. Los puntos que quedan debajo de la curva PDF objetivo (Campana de Gauss) son *Aceptados*, y los que caen fuera son *Rechazados*.

### ¿Qué hace cada script?

- **Generación de datos**: Se crean **10,000 muestras** por defecto. `uniforme.py` las genera en el rango [0, 10], mientras que `normal.py` las genera con media $\mu = 5$ y desviación estándar $\sigma = 2$.
- **Salida en Consola**: Se imprimen los 5 primeros valores generados para cada método.
- **Visualización**: Se abren ventanas con histogramas (utilizando `matplotlib`) para comparar ambas metodologías de generación.
  - **Distribución Uniforme (`uniforme.py`)**: Para el gráfico de Transformada Inversa se incluye una línea horizontal punteada indicando la densidad promedio esperada.
  - **Distribución Normal (`normal.py`)**: En el gráfico de Aceptación-Rechazo se incluye una nube de puntos (*scatter plot*) que detalla de forma didáctica qué coordenadas exactas fueron aceptadas (verde) y rechazadas (rojo) por el algoritmo, mostrando además la curva objetivo (PDF) y el techo de la propuesta uniforme.

### Cambiar parámetros en las distribuciones

Podemos modificar la cantidad de muestras y los parámetros matemáticos editando directamente las variables en el bloque principal `if __name__ == "__main__":` de cada archivo.

Para **Uniforme** en `uniforme.py`:
```python
n_muestras = 10000
a, b = 0, 10
```

Para **Normal** en `normal.py`:
```python
n_muestras = 10000
mu, sigma = 5, 2
```

Donde:
- `n_muestras`: Cantidad de muestras a generar.
- `a` y `b`: Límite inferior y superior de la distribución Uniforme.
- `mu` y `sigma`: Media y Desviación estándar de la distribución Normal.

## Archivos del Proyecto

- `normal.py`: Script enfocado en la generación de la distribución Normal mediante los métodos de Transformada Inversa (Aproximación Numérica) y Aceptación-Rechazo.
- `uniforme.py`: Script enfocado en la generación de la distribución Uniforme por los métodos de Transformada Inversa y Aceptación-Rechazo, mostrando gráficos comparativos y la densidad promedio teórica.
- `requirements.txt`: Lista de librerías de Python requeridas (`numpy` y `matplotlib`).
- `README.md`: Este archivo con la documentación actualizada del proyecto.
