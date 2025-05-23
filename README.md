🍕 Sistema de Inventario para Pizzería
📅 Versión: 1.0 (02-05-2025)
Un sistema de gestión de inventario diseñado para pizzerías, que permite administrar ingredientes, visualizar stock y generar reportes gráficos.
📌 Características
✅ Gestión de ingredientes
Agregar, modificar, eliminar y buscar ingredientes
Validación de datos (ID en formato INGXXX, cantidades no negativas)

📊 Visualización de datos
Gráfico de barras de cantidades disponibles
Gráfico 3D interactivo (ID vs. Cantidad vs. Longitud del nombre)

💾 Persistencia de datos
Guardado y carga automática en formato JSON
Compatibilidad con múltiples sesiones

🖥 Interfaz intuitiva
Menú interactivo con emojis
Mensajes de confirmación y errores descriptivos

⚙️ Requisitos
Python 3.7 o superior
Bibliotecas requeridas: matplotlib

🚀 Instalación y Uso
Clonar el repositorio
git clone https://github.com/tu-usuario/inventario-pizzeria.git
cd inventario-pizzeria

Ejecutar el sistema
python evalucion1.py

Opciones del menú
1. ➕ Agregar ingrediente  
2. ✏️ Modificar cantidad  
3. ❌ Eliminar ingrediente  
4. 🔍 Buscar ingrediente  
5. 📋 Listar todos los ingredientes  
6. 💾 Guardar inventario  
7. 📉 Gráfico de barras  
8. 📊 Gráfico 3D  
9. 🚪 Salir
   
Estructura del Proyecto
📂 inventario-pizzeria/
├── 📄 evalucion1.py       # Código principal del sistema  
├── 📄 inventario_pizzeria.json  # Archivo de datos (se crea automáticamente)  
└── 📄 README.md           # Este archivo  

📜 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

🎉 ¡Gracias por usar este sistema!
Si te gustó el proyecto, ¡déjale una ⭐ en GitHub! 🚀
