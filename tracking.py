'''
To Do:
-Guardar punto central de trackers durante el loop
-Intentar hacer reconocimiento por contornos en los otros videos

'''

import argparse
import cv2 as cv
from random import randint

def reescalarImagen (imagen, porcentajeDeEscalado):
    largo = int(imagen.shape[1] * porcentajeDeEscalado / 100)
    ancho = int(imagen.shape[0] * porcentajeDeEscalado / 100)
    dimension = (largo, ancho)
    imagen = cv.resize(imagen, dimension, interpolation= cv.INTER_AREA)
    return imagen

def estaDentro(inicioRectangulo, finRectangulo, anchoFrame, largoFrame):
   # True si el rectangulo esta dentro de la imagen y además no toca ningún borde
    return ((0 < inicioRectangulo[0]< largoFrame) and (0 < inicioRectangulo[1]< anchoFrame)) and ((0 < finRectangulo[0]< largoFrame) and (0 < finRectangulo[1]< anchoFrame))

#def pop_all(l):
#    r, l[:] = l[:], []
#    return r



ap = argparse.ArgumentParser()
ap.add_argument('-d','--dirVideo', required=True, help='Directorio del video')
ap.add_argument('-n','--nombreArchivo',required=True, help='Nombre del archivo donde guardar los datos')
args = vars(ap.parse_args())

video = cv.VideoCapture('media/' + args['dirVideo'])

informacionTrackers = [] #[(tracker,color, identificador)]
frameNumero = 0
identificador = 0
flagPausa = False
datosRecolectados = open(args['nombreArchivo']+'.txt','w')

largoFrame = int(video.get(3))
anchoFrame = int(video.get(4))
datosRecolectados.write(str(largoFrame) + ' '+ str(anchoFrame) + ' ')



while True:
    success, frame = video.read()
    
    #frame = reescalarImagen(frame, 85)
    
    if success:
        frameNumero += 1
        primerTecla = cv.waitKey(1) & 0xff

        #-Seleccion de Trackers-------------
        if primerTecla == ord(" ") or flagPausa: # Espacio para pausar
            zonasDeInteres = cv.selectROIs("MultiTracker", frameConObjetos)         
                
            for zona in zonasDeInteres:
                tracker = cv.legacy.TrackerCSRT_create()
                tracker.init(frame, zona)
                color = (randint(50, 255), randint(50, 255), randint(50, 255))
                identificador +=1
                informacionTrackers.append((tracker,color,identificador))
        #---------------------------------------------------------
        
        #-Validación de trackers, mostrar en pantalla y escribir datos------
        
        flagPausa = False
        for i,(tracker,color,identificador) in enumerate(informacionTrackers):
            _, caja = tracker.update(frame)
            inicioRectangulo = (int(caja[0]), int(caja[1]))
            finRectangulo = (int(caja[0] + caja[2]), int(caja[1] + caja[3]))
            if estaDentro(inicioRectangulo, finRectangulo, anchoFrame, largoFrame):
                
                cv.rectangle(frame, inicioRectangulo, finRectangulo, color, 2, 1)
                puntoMedioX = (finRectangulo[0] + inicioRectangulo[0])//2
                puntoMedioY = (finRectangulo[1] + inicioRectangulo[1])//2
                #cv.circle(frame,(puntoMedioX,puntoMedioY), 3, (0,255,0), -1 )
                datos = str(frameNumero) + ' '+ str(identificador) + ' ' + str(puntoMedioX) + ' ' + str(puntoMedioY) + ' '
                

                datosRecolectados.write(datos)

            else:
                informacionTrackers.pop(i)
        #--------------------------------------------------------------------
        frameConObjetos = frame.copy() # Para mostrar los rectángulos ya trackeados en la selección de nuevos rectángulos
        


        cv.imshow("MultiTracker", frame)
        teclaDeControl = cv.waitKey(1) & 0xff 
        if teclaDeControl == ord("q"): # presionar q para salir del programa
            break
        elif teclaDeControl == ord(" "): # presionar Espacio para salir del programa
            flagPausa = True
    
    else:
        break
        #frameNumero = 0
        #pop_all(informacionTrackers)
        #video.set(cv.CAP_PROP_POS_FRAMES, 0)
        #continue
          
        
datosRecolectados.close()
video.release()
cv.destroyAllWindows()        
