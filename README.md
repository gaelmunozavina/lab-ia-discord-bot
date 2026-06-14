# ⚙️ Asistente Virtual - Laboratorio de IA

¡Bienvenido al repositorio de **Laboratorio de IA**! Este es un bot multifuncional para Discord desarrollado en **Python**. El sistema está diseñado con un enfoque híbrido: herramientas de productividad y gestión personal para el día a día, combinadas con un módulo completo de entretenimiento multimedia.

El bot utiliza una interfaz de usuario elegante basada en **Embeds** (cuadros de diálogo estructurados con barras de color) para facilitar la lectura de datos desde la consola de Discord.

---

## 🚀 Funciones Principales

El sistema está dividido en tres núcleos operativos principales:

### 1. 📅 Agenda Personal y Productividad
Ideal para gestionar entregas, tareas o eventos importantes directamente desde el chat. Las tareas se guardan de forma persistente en un archivo local (`json`), lo que significa que **no se borran** aunque el bot se apague o se reinicie.
* **Añadir pendientes:** Registra nuevas actividades en tu lista.
* **Visualización organizada:** Muestra todas tus tareas numeradas.
* **Limpieza de historial:** Permite eliminar tareas de la lista usando su número identificador una vez completadas.

### 2. 🌤️ Módulo Ambiental (Clima en tiempo real)
Consulta el estado meteorológico actual de cualquier ciudad del mundo. El bot conecta con una API externa para extraer y traducir los datos en tiempo real.
* Muestra la **temperatura** actual en grados Celsius (°C).
* Muestra el porcentaje de **humedad** ambiental.
* Proporciona el **estado del cielo** (completamente traducido al español).

### 3. 🎵 Reproducción Multimedia (Música)
Un módulo de audio nativo para canales de voz que se conecta directamente con plataformas como YouTube para reproducir música en alta fidelidad.
* Soporta enlaces directos o términos de búsqueda general.
* Incluye sistema de cola de reproducción y controles de estado (pausar, reanudar, saltar y detener).

---

## 🕹️ Guía de Comandos (Para Primeros Usuarios)

Todos los comandos utilizan el prefijo **`$`**. Si es la primera vez que usas el bot, aquí tienes la lista de instrucciones exactas de cómo interactuar con él:

| Comando | Sintaxis / Ejemplo | ¿Qué hace el sistema? |
| :--- | :--- | :--- |
| **`$info`** | `$info` | Despliega el panel de control con la ayuda y la lista de comandos activos. |
| **`$tarea_add`** | `$tarea_add Terminar el reporte de IA` | Guarda una nueva tarea en tu agenda personal. |
| **`$agenda`** | `$agenda` | Muestra en pantalla la lista con todas tus tareas pendientes actuales. |
| **`$tarea_del`** | `$tarea_del 1` | Borra de la agenda la tarea número 1 (o el número que indiques). |
| **`$clima`** | `$clima Guadalajara` | Muestra el reporte del tiempo actual para la ciudad que escribas. |
| **`$play`** | `$play Jere Klein` *ó* `$play <enlace_de_youtube>` | El bot se une a tu canal de voz actual y reproduce la canción solicitada. |
| **`$pause`** | `$pause` | Pausa temporalmente la canción que se está reproduciendo. |
| **`$resume`** | `$resume` | Reanuda la música en el punto exacto donde la pausaste. |
| **`$skip`** | `$skip` | Salta la canción actual y pasa a la siguiente en la lista de espera. |
| **`$stop`** | `$stop` | Detiene la música por completo, borra la cola y saca al bot del canal de voz. |

---

## 🛠️ Tecnologías Utilizadas

* **Python 3.10+** — Lenguaje base de programación.
* **Discord.py** — API wrapper para la conexión con los servidores de Discord.
* **yt-dlp** — Motor avanzado de extracción y procesamiento de contenido multimedia.
* **Davey & PyNaCl** — Librerías nativas para la encriptación de audio y soporte de voz en Windows.
* **Requests** — Gestión de peticiones HTTP para el módulo meteorológico.
* **JSON** — Base de datos local ligera para el almacenamiento persistente de la agenda.

---
🔬 *Desarrollado como proyecto de automatización e integración para el Laboratorio de IA.*
