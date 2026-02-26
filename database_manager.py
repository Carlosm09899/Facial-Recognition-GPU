import cv2
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
import sqlite3
import numpy as np
import io
import warnings
import sys 

warnings.filterwarnings("ignore", category=FutureWarning)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

def nuevo_registro():
    # --- LÓGICA DE RECEPCIÓN DE NOMBRE ---
    if len(sys.argv) > 1:
        nombre = sys.argv[1] # Recibe el nombre desde la interfaz
    else:
        nombre = input("Nombre del usuario: ") # Por si lo corres manual
    
    # Iniciamos cámara (CAP_DSHOW para que abra rápido en tu MSI)
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print(f"Registrando a: {nombre}. Presiona 'S' para capturar...")
    
    while True:
        _, frame = cam.read()
        cv2.imshow("Registro Biometrico - Presiona S", frame)
        
        if cv2.waitKey(1) == ord('s'):
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face = mtcnn(frame_rgb)
            
            if face is not None:
                encoding = resnet(face.unsqueeze(0).to(device)).detach().cpu().numpy()
                
                conn = sqlite3.connect('usuarios_biometria.db')
                cursor = conn.cursor()
                
                out = io.BytesIO()
                np.save(out, encoding)
                
                # INSERT específico para evitar el error de las 3 columnas
                cursor.execute("INSERT INTO rostros (nombre, encoding) VALUES (?, ?)", 
                               (nombre, out.getvalue()))
                
                conn.commit()
                conn.close()
                print(f"¡{nombre} registrado con éxito!")
                break
        
        if cv2.waitKey(1) == 27: break
        
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    nuevo_registro()