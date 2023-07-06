# proyecto-inf451
Proyecto para el ramo Computación Gráfica USM 2023-1

## Dependencias
* Python 3.X.X
* PyOpenGL
* PyOpenGL_accelerate
* pygame
* numpy
* ctypes

## Uso
* Abrir una terminal en la carpeta donde se encuentre main.py
* Ejecutar con `$ python main.py` o `$ python3 main.py`
* La cara sur-oeste es A (el norte de la textura, es el norte de la cara), la sur-este es B (el norte de la textura, es el norte de la cara), y la norte es C (el norte de la textura es el nor-este de la cara)
* Apretar 0, ..., 6 para elegir un vértice:
  * 0 es el vertice central
  * 1 es el vertice mas al sur-oeste de la cara A
  * 2, ..., 6 son los vertices que le siguen siguiendo un sentido anti-horario
* Presionar click en un punto de la ventana para cambiar la posición del vertice seleccionado
* Presionar D para activar el modo epilepsia
