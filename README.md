# Generadores Pseudoaleatorios de Variables

Este proyecto contiene un script en Python para generar variables pseudoaleatorias siguiendo dos distribuciones de probabilidad diferentes: **Uniforme** y **Normal**. 

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

Para ejecutar el programa, simplemente corre el script principal desde la terminal:

```bash
python generadores.py
```

Al iniciarlo, el programa mostrará un **menú interactivo** que te permitirá elegir el método de simulación:
1. **Funciones nativas de NumPy:** Usa los generadores altamente optimizados de la librería matemática.
2. **Transformada Inversa y Aceptación-Rechazo (Algoritmos Propios):** Utiliza implementaciones matemáticas desde cero para generar los números aleatorios.

### ¿Qué métodos se implementan?

- **Método de la Transformada Inversa**: Se aplica para generar la **Distribución Uniforme**. Invertimos analíticamente la Función de Distribución Acumulada (CDF) para mapear valores aleatorios base al rango objetivo.
- **Método de Aceptación-Rechazo**: Se aplica para generar la **Distribución Normal**. Se define una distribución de propuesta (Uniforme que actúa como techo) y se generan puntos candidatos $(X, Y)$. Los puntos que quedan debajo de la curva PDF objetivo (Campana de Gauss) son *Aceptados*, y los que caen fuera son *Rechazados*.

### ¿Qué hace el script?

- **Generación de datos**: Crea **10,000 muestras** para una distribución Uniforme (por defecto en el rango [0, 10]) y **10,000 muestras** para una distribución Normal (por defecto con media $\mu = 5$ y desviación estándar $\sigma = 2$).
- **Salida en Consola**: Imprime los 5 primeros valores generados para cada distribución.
- **Visualización**: Abre una ventana con histogramas (utilizando `matplotlib`) donde se puede apreciar gráficamente la forma de las distribuciones.
  - **¡Novedad!**: Si seleccionas los algoritmos propios (Opción 2), el gráfico de la distribución Normal incluirá además una nube de puntos (*scatter plot*) que detalla visualmente de forma didáctica qué coordenadas exactas fueron aceptadas (verde) y rechazadas (rojo) por el algoritmo. También se grafica la curva objetivo (PDF) y el techo de propuesta.

### Cambiar parámetros en las distribuciones

Podemos modificar la cantidad de muestras y los parámetros de las distribuciones cambiando las variables dentro del bloque principal `if __name__ == "__main__":` en el archivo `generadores.py`:

```python
n_muestras = 10000
uniformes = generar_uniforme(n_muestras, a=0, b=10, metodo=metodo_uni)

# La función generar_normal devuelve detalles extra si activamos return_details=True
normales, detalles_ar = generar_normal(n_muestras, mu=5, sigma=2, metodo=metodo_norm, return_details=True)
```

Donde:
- `n_muestras`: Cantidad de muestras a generar.
- `a` y `b`: Límite inferior y superior de la distribución Uniforme.
- `mu` y `sigma`: Media y Desviación estándar de la distribución Normal.

### Mostrar más valores en la consola
De forma predeterminada, se muestran por consola los primeros 5 valores obtenidos para cada distribución. Podemos modificar esto cambiando la variable `n_mostrar` dentro de la sección principal del código:

```python
n_mostrar = 5
```

## Archivos del Proyecto

- `generadores.py`: Código principal con las funciones de generación (`generar_con_transformada_inversa`, `generar_con_aceptacion_rechazo`, `generar_uniforme`, `generar_normal`) y gráficos (`graficar_distribuciones`).
- `requirements.txt`: Lista de librerías de Python requeridas (`numpy` y `matplotlib`).
- `README.md`: Este archivo con la documentación actualizada del proyecto.
