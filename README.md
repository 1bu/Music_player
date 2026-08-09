# 🎵 Music Player

Un reproductor de música de escritorio ligero y moderno desarrollado en Python. Utiliza **CustomTkinter** para la interfaz gráfica adaptativa y **Pygame** para la reproducción de audio.

---

## 🚀 Características

- 📂 **Persistencia de carpeta:** Carga automáticamente la última carpeta seleccionada mediante un archivo `config.json`.
- 🔀 **Modo Aleatorio:** Mezcla las canciones sin interrumpir la reproducción actual y restaura el orden original al desactivarse.
- 🎚️ **Controles interactivos:** Barra de progreso interactiva con desplazamiento y control de volumen en tiempo real.
- ⏱️ **Indicadores de tiempo:** Visualización dinámica del tiempo transcurrido y la duración total en formato `MM:SS`.
- ⌨️ **Atajos de teclado:** Accesos rápidos integrados para pausar, avanzar o cambiar de pista.

---

### ⌨️ Atajos de Teclado

| Tecla / Acción | Función |
| :--- | :--- |
| `Espacio` / `F9` | Play / Pausar reproducción |
| `Doble Clic` *(en la lista)* | Reproducir la canción seleccionada |
| `F8` | Canción anterior |
| `F10` | Canción siguiente |
| `F7` | Detener música |
| `Ctrl + O` | Abrir la carpeta actual en el gestor de archivos |

---

## 📦 Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/1bu/Music_player.git](https://github.com/1bu/Music_player.git)
   cd Music_Player
