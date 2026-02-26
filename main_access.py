import cv2
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from datetime import datetime
import sqlite3
import numpy as np
import io
import warnings
import os

warnings.filterwarnings("ignore", category=FutureWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"--- SISTEMA INICIADO EN: {device} ---")

mtcnn = MTCNN(keep_all=True, device=device, post_process=True)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

registrados_en_esta_sesion = [] 

def registrar_acceso_en_db(nombre):
    try:
        ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect('usuarios_biometria.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO historial_accesos (nombre, fecha) VALUES (?, ?)", (nombre, ahora))
        conn.commit()
        conn.close()
        print(f"LOG: Acceso EXITOSO para {nombre} a las {ahora}")
    except Exception as e:
        print(f"Error DB: {e}")

def iniciar_sistema_gpu():
    global registrados_en_esta_sesion
    
    try:
        conn = sqlite3.connect('usuarios_biometria.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, encoding FROM rostros")
        filas = cursor.fetchall()
        nombres_db = [f[0] for f in filas]
        encodings_db = [torch.tensor(np.load(io.BytesIO(f[1]))).to(device) for f in filas]
        conn.close()
    except Exception as e:
        print(f"Error al cargar DB: {e}")
        return

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        ok, frame = cam.read()
        if not ok: break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes, _, landmarks = mtcnn.detect(frame_rgb, landmarks=True)

        if boxes is not None:
            for box, landmark in zip(boxes, landmarks):
                face = mtcnn.extract(frame_rgb, [box], save_path=None).to(device)
                encoding_actual = resnet(face).detach()

                nombre = "DESCONOCIDO"
                distancia_minima = 0.8 

                for idx, enc_db in enumerate(encodings_db):
                    dist = (encoding_actual - enc_db).norm().item()
                    if dist < distancia_minima:
                        nombre = nombres_db[idx]

                color_cuadro = (0, 0, 255) 
                mensaje = "IDENTIDAD NO CONFIRMADA"

                if nombre != "DESCONOCIDO":
                    ojo_izq = landmark[0].astype(int)
                    ojo_der = landmark[1].astype(int)
                    cv2.circle(frame, tuple(ojo_izq), 3, (255, 255, 0), -1)
                    cv2.circle(frame, tuple(ojo_der), 3, (255, 255, 0), -1)

                    if nombre not in registrados_en_esta_sesion:
                        registrar_acceso_en_db(nombre)
                        registrados_en_esta_sesion.append(nombre)
                    
                    color_cuadro = (0, 255, 0) 
                    mensaje = f"ACCESO CONCEDIDO: {nombre}"

                x1, y1, x2, y2 = box.astype(int)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color_cuadro, 2)
                cv2.putText(frame, mensaje, (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_cuadro, 2)

        cv2.imshow("Monitor Biometrico RTX 3050", frame)
        if cv2.waitKey(1) == 27: break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    iniciar_sistema_gpu()