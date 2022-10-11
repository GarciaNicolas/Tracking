# Tracking

## Pasos previos a la ejecución
1. Clonar repositorio.
2. Guardar el video en la carpeta media.

## Librerias Usadas
-argparse<br>
-cv2<br>
-random<br>

## Para ejecutar
En la consola: `$ python tracking.py -d 'video.mp4' -n nombreDelArchivo`

*-d = Directorio del video* <br>
*-n = El nombre con el que se va a llamar al archivo donde se guardan los datos del seguimiento*

## Durante la ejecución

### Para inicializar un segumiento.
*Durante cualquier momento de la ejecución*
1. Presionar `Espacio`.
2. Recuadrar el objeto a seguir manteniendo `Click Izquierdo` y arrastrando.
3. Presionar `Espacio` para confirmar selección.
4. Si desea seleccionar otro objeto, solo recuadrelo y confirmelo. Para finalizar la selección presionar `ESC`.

### Para finalizar el programa
1. Para finalizar el programa presionar la tecla `q`.

## Devolución de datos
El programa devuelve un archivo `.txt` con el siguiente formato **(teniendo en cuenta que los _ son espacios)**:<br>
1. Lo primero que aparece son la dimension de los frames utilizados: *DimensionX_DimensionY_*<br>
2. Luego los datos con respecto a los trackes: *FrameNro_Identificador_CoordenadaX_CoordenadaY_*<br>
