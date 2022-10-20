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

def pop_all(l):
    r, l[:] = l[:], []
    return r



ap = argparse.ArgumentParser()
ap.add_argument('-d','--dirVideo', required=True, help='Directorio del video')
ap.add_argument('-n','--nombreArchivo',required=True, help='Nombre del archivo donde guardar los datos')
ap.add_argument('-r','--reescalado', nargs='?', const=100, type=int, help='Valor de reescalado de video')
args = vars(ap.parse_args())

video = cv.VideoCapture('media/' + args['dirVideo'])

informacionTrackers = [] #[(tracker,color, identificador)]
frameNumero = 0
identificador = 0
flagPausa = False
flagRepeticion = False
datosRecolectados = open(args['nombreArchivo']+'.txt','w')

largoFrame = int(video.get(3))
anchoFrame = int(video.get(4))
#datosRecolectados.write(str(largoFrame) + ' '+ str(anchoFrame) + ' ')

puntosEnVideo = [] #Para poder ver los objectivos ya seleccionados cuando

while True:
    frameNumero += 1
    success, frame = video.read()
    
    puntosEnFrame = []

    
    if success:
        if not flagRepeticion:
            frame = reescalarImagen(frame, args['reescalado'])
            dimensiones = frame.shape
        primerTecla = cv.waitKey(1) & 0xff


        if flagRepeticion:
            for (coordSuperiorRectangulo, coordInferiorRectangulo) in puntosEnVideo[frameNumero-1]:
                cv.rectangle(frame, coordSuperiorRectangulo, coordInferiorRectangulo, (0,255,0), 2, 1)
        

        
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
        
        flagPausa = False


        #-Actualizar trackers------
        for i,(tracker,color,identificador) in enumerate(informacionTrackers):
            _, caja = tracker.update(frame)
            inicioRectangulo = (int(caja[0]), int(caja[1]))
            finRectangulo = (int(caja[0] + caja[2]), int(caja[1] + caja[3]))
                

            #-Verificar si el tracker esta dentro de los margenes del video---------------
            if estaDentro(inicioRectangulo, finRectangulo, dimensiones[0], dimensiones[1]):
                
                puntosEnFrame.append((inicioRectangulo,finRectangulo))
                
                cv.rectangle(frame, inicioRectangulo, finRectangulo, color, 2, 1)
                
                puntoMedioX = (finRectangulo[0] + inicioRectangulo[0])//2
                puntoMedioY = (finRectangulo[1] + inicioRectangulo[1])//2
                #datos = str(frameNumero) + ' '+ str(identificador) + ' ' + str(puntoMedioX) + ' ' + str(puntoMedioY) + ' '
                
                datosRecolectados.write(str(frameNumero) + ' '+ str(identificador) + ' ' + str(puntoMedioX) + ' ' + str(puntoMedioY) + ' ')

            else:
                informacionTrackers.pop(i)
        #--------------------------------------------------------------------
        frameConObjetos = frame.copy() # Para mostrar los rectángulos ya trackeados en la selección de nuevos rectángulos
        
        if flagRepeticion:
            puntosEnVideo[frameNumero-1].append(puntosEnFrame)
        else:
            puntosEnVideo.append(puntosEnFrame)



        cv.imshow("MultiTracker", frame)
        teclaDeControl = cv.waitKey(1) & 0xff 
        if teclaDeControl == ord("q"): # presionar q para salir del programa
            datosRecolectados.write(str(dimensiones[1]) + ' '+ str(dimensiones[0]) + ' ')
            break
        elif teclaDeControl == ord(" "): # presionar Espacio para salir del programa
            flagPausa = True
    


        

        
    else:
        #break
        frameNumero = 0
        flagRepeticion = True
        pop_all(informacionTrackers)
        video.set(cv.CAP_PROP_POS_FRAMES, 0)
        continue
          

datosRecolectados.close()
video.release()
cv.destroyAllWindows()        
