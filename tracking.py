import argparse
import cv2 as cv
from random import randint

def estaDentro(inicioRectangulo, finRectangulo, dimensionImagen):
   # True si el rectangulo esta dentro de la imagen y además no toca ningún borde
    return ((0 < inicioRectangulo[0]< dimensionImagen[0]) and (0 < inicioRectangulo[1]< dimensionImagen[1])) and ((0 < finRectangulo[0]< dimensionImagen[0]) and (0 < finRectangulo[1]< dimensionImagen[1]))

ap = argparse.ArgumentParser()
ap.add_argument('-d','--dirVideo', required=True, help='Directorio del video')
ap.add_argument('-n','--nombreArchivo',required=True, help='Nombre del archivo donde guardar los datos', )
args = vars(ap.parse_args())

videoPath = 'src/encierroSanFermin.mp4'

video = cv.VideoCapture('media/' + args['dirVideo'])

multiTracker = cv.legacy.MultiTracker_create()
coloresUsados = []
informacionGlobal = [] #[[objetoTrackeado, esTrackerValido]]
regionesDeInteresGlobal = []
frameNumero = 0
objetoTrackeado = 0
flagPausa = False
datosRecolectados = open(args['nombreArchivo']+'.txt','w')

while video.isOpened():
    success, frame = video.read()
    
    dimensionDeImagen = frame.shape
    
    if success:
        frameNumero += 1
        regionesDeInteres = []
        primerTecla = cv.waitKey(1) & 0xff

        #-Seleccion de Trackers-------------
        if primerTecla == ord(" ") or flagPausa: # Espacio para pausar
            zonasDeInteres = cv.selectROIs("MultiTracker", frameConObjetos)         
            regionesDeInteresGlobal.extend(zonasDeInteres)
                
            for zona in zonasDeInteres:
                color = (randint(50, 255), randint(50, 255), randint(50, 255))
                #while color in coloresUsados: #Me aseguro que va a ser un color diferente
                #    color = (randint(50, 255), randint(50, 255), randint(50, 255))
                coloresUsados.append(color)
                objetoTrackeado +=1
                multiTracker.add(cv.legacy.TrackerCSRT_create(), frame, zona)
                informacionGlobal.append([objetoTrackeado,True])
        #---------------------------------------------------------
        
        #-Validación de trackers, mostrar en pantalla y escribir datos------
        flagPausa = False
        _, cajas = multiTracker.update(frame)

        for i, caja in enumerate(cajas):
            inicioRectangulo = (int(caja[0]), int(caja[1]))
            finRectangulo = (int(caja[0] + caja[2]), int(caja[1] + caja[3]))
            if (estaDentro(inicioRectangulo, finRectangulo, dimensionDeImagen)) and informacionGlobal[i][1]:
                cv.rectangle(frame, inicioRectangulo, finRectangulo, coloresUsados[i], 2, 1)
                coordX = (finRectangulo[1] + inicioRectangulo[1])//2
                coordY = (finRectangulo[0] + inicioRectangulo[0])//2
                datos = '[F:' + str(frameNumero) + ' X:' + str(coordX) + ' Y:' + str(coordY) + ' I:'+ str(informacionGlobal[i][0]) + ']'
                datosRecolectados.write(datos)
            else:
                informacionGlobal[i][1] = False
        #--------------------------------------------------------------------
        frameConObjetos = frame.copy()
        cv.imshow("MultiTracker", frame)
        terminarPrograma = cv.waitKey(1) & 0xff # presionar Q para salir del programa
        if terminarPrograma == ord("q"):
            break
        elif terminarPrograma == ord(" "):
            flagPausa = True
        
datosRecolectados.close()
video.release()
cv.destroyAllWindows()        
