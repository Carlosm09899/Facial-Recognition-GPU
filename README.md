# 🔐 SECURE-ID — Sistema de Control de Acceso Biométrico

> Sistema de reconocimiento facial en tiempo real con aceleración GPU, desarrollado con PyTorch y FaceNet.

---

## 📸 Descripción

**SECURE-ID** es una aplicación de escritorio que implementa un sistema de control de acceso mediante reconocimiento facial. Utiliza redes neuronales profundas para detectar y autenticar identidades en tiempo real a través de la cámara web, registrando cada acceso en una base de datos local.

---

## ⚙️ Tecnologías Usadas

| Tecnología | Uso |
|---|---|
| `Python 3.x` | Lenguaje principal |
| `PyTorch` | Motor de inferencia con soporte CUDA |
| `facenet-pytorch` | Detección (MTCNN) y embedding facial (InceptionResnetV1) |
| `OpenCV` | Captura de video y renderizado |
| `CustomTkinter` | Interfaz gráfica moderna (tema oscuro) |
| `SQLite3` | Base de datos local para usuarios e historial |

---

## 🗂️ Estructura del Proyecto

```
Reconocimiento/
├── app_biometrica.py      # Interfaz gráfica principal (GUI)
├── database_manager.py    # Registro de nuevos usuarios biométricos
├── main_access.py         # Motor de reconocimiento en tiempo real
├── init_db.py             # Inicialización de la base de datos
└── usuarios_biometria.db  # Base de datos SQLite (generada automáticamente)
```

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Carlosm09899/Facial-Recognition-GPU.git
cd Facial-Recognition-GPU
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate   # Linux / macOS

pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install facenet-pytorch opencv-python customtkinter numpy
```

> ⚡ Para aprovechar la aceleración GPU, asegúrate de tener instalados los drivers NVIDIA y CUDA 11.8+.

### 3. Inicializar la base de datos

```bash
python init_db.py
```

---

## 🖥️ Uso

### Ejecutar la interfaz principal

```bash
python app_biometrica.py
```

Desde la interfaz puedes:

- **Iniciar Escaneo** — Activa la cámara y comienza el reconocimiento facial en tiempo real.
- **Registrar Usuario** — Captura y guarda el encoding facial de un nuevo usuario.
- **Gestionar Bajas** — Elimina un usuario de la base de datos.
- **Actualizar Registros** — Refresca el historial de accesos recientes.

---

## 🧠 Cómo Funciona

1. **Detección**: MTCNN localiza rostros en el frame de video.
2. **Embedding**: InceptionResnetV1 (entrenado con VGGFace2) genera un vector de 512 dimensiones por cada rostro.
3. **Comparación**: Se calcula la distancia euclidiana entre el embedding actual y los almacenados en la DB. Si la distancia es menor a `0.8`, el acceso es concedido.
4. **Registro**: El acceso exitoso se guarda automáticamente en la tabla `historial_accesos`.

```
Cámara → MTCNN → InceptionResnetV1 → Comparación en DB → Resultado
```

---

## 📋 Requisitos del Sistema

- Windows 10/11
- Python 3.9+
- NVIDIA GPU con soporte CUDA (recomendado) — también funciona en CPU
- Cámara web

---

## 📄 Licencia

Este proyecto es de uso educativo y personal. Libre para modificar y distribuir con atribución.

---

<p align="center">
  Desarrollado con ❤️ y una RTX 3050
</p>
