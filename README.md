# Generadores Pseudoaleatorios de Variables

Este proyecto contiene un script en Python para generar variables pseudoaleatorias siguiendo dos distribuciones de probabilidad diferentes: **Uniforme** y **Normal**.

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

Para ejecutar el programa, simplemente corre el script principal desde la terminal:

```bash
python generadores.py
```

### ¿Qué hace el script?

- **Generación de datos**: Crea **10,000 muestras** para una distribución Uniforme (por defecto en el rango [0, 10]) y **10,000 muestras** para una distribución Normal (por defecto con media $\mu = 5$ y desviación estándar $\sigma = 2$).
- **Salida en Consola**: Imprime los 5 primeros valores generados para cada distribución.
- **Visualización**: Abre una ventana con dos histogramas (utilizando `matplotlib`) donde se puede apreciar gráficamente la forma de las distribuciones empíricas (la clásica campana de Gauss para la Normal y un bloque rectangular para la Uniforme).

### Cambiar parámetros en las distribuciones
Podemos modificar la cantidad de muestras y los parámetros de las distribuciones cambiando las siguientes variables en el archivo `generadores.py` (linea 40):

```python
n_muestras = 10000
uniformes = generar_uniforme(n_muestras, a=0, b=10)
normales = generar_normal(n_muestras, mu=5, sigma=2)
```

Donde:
- `n_muestras`: Cantidad de muestras a generar.
- `a`: Límite inferior de la distribución Uniforme.
- `b`: Límite superior de la distribución Uniforme.
- `mu`: Media de la distribución Normal.
- `sigma`: Desviación estándar de la distribución Normal.

### Mostrar más valores en los gráficos
De forma predeterminada, se muestran por consola los primeros 5 valores obtenidos para cada distribución. Podemos modificar la cantidad de valores a mostrar cambiando la variable `n_mostrar` en el archivo `generadores.py` (linea 41):

```python
n_mostrar = 5
```

## Archivos del Proyecto

- `generadores.py`: Código principal con las funciones de generación (`generar_uniforme`, `generar_normal`) y de gráficos (`graficar_distribuciones`).
- `requirements.txt`: Lista de librerías de Python requeridas (`numpy` y `matplotlib`).
- `README.md`: Este archivo con la documentación.
