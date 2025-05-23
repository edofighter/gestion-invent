#Desarrolado por : Edo  
#Fecha: 02-05-2025     
#Version: 1.0

#Sistema de inventario para una pizzería
import json
import os #Propósito: Interactuar con el sistema operativo (archivos, rutas, directorios). Operating System
import re #Propósito: Validar patrones en texto (como formatos de ID).Regular Expressions
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Clase  ingrediente de la pizzería.
class Ingrediente: 
    """
    Clase que representa un ingrediente de la pizzeria.
    Atributos:
        id_ingrediente (str): Identificador único (formato: INGXXX).
        nombre (str): Nombre del ingrediente (ej: "queso mozzarella").
        cantidad (int): Cantidad disponible (≥ 0).
        ubicacion (str): Lugar de almacenamiento (no vacío).
    """
    def __init__(self, id_ingrediente, nombre, cantidad, ubicacion):
        self.id_ingrediente = id_ingrediente
        self.nombre = nombre
        self.cantidad = cantidad
        self.ubicacion = ubicacion
    
    def to_dict(self):             
        """Convierte el objeto a diccionario para JSON."""
        return {
            'id_ingrediente': self.id_ingrediente,
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'ubicacion': self.ubicacion
        }

class InventarioPizzeria:
    """Gestiona el inventario de ingredientes con persistencia en JSON."""
    def __init__(self):
        self.ingredientes = {}
        self.cargar_inventario()
    
    def _validar_inventario_no_vacio(self):
        """Método privado para validar que el inventario no esté vacío."""
        if not self.ingredientes:
            print("\nError: El inventario está vacío.")
            return False
        return True
    
    def _validar_id_formato(self, id_ingrediente):
        """Valida que el ID tenga formato INGXXX."""
        return re.match(r'^ING\d{3}$', id_ingrediente) is not None

    def agregar_ingrediente(self, id_ingrediente, nombre, cantidad, ubicacion):
        """
        Agrega un nuevo ingrediente al inventario.
        Valida: ID único, nombre no vacío, cantidad ≥ 0, ubicación no vacía.
        """
        if not self._validar_id_formato(id_ingrediente):
            print("\nError: El ID debe tener formato INGXXX (ej: ING001).")
            return False
        if id_ingrediente in self.ingredientes:
            print(f"\nError: El ID {id_ingrediente} ya existe.")
            return False
        if not nombre or not isinstance(nombre, str):
            print("\nError: El nombre debe ser un texto no vacío.")
            return False
        try:
            cantidad = int(cantidad)
            if cantidad < 0:
                print("\nError: La cantidad no puede ser negativa.")
                return False
        except ValueError:
            print("\nError: La cantidad debe ser un número entero.")
            return False
        if not ubicacion or not isinstance(ubicacion, str):
            print("\nError: La ubicación debe ser un texto no vacío.")
            return False
        
        self.ingredientes[id_ingrediente] = Ingrediente(id_ingrediente, nombre, cantidad, ubicacion)
        print(f"\n Ingrediente '{nombre}' agregado correctamente.")
        return True
    
    def modificar_cantidad(self, id_ingrediente, nueva_cantidad):
        """Modifica la cantidad de un ingrediente existente."""
        if id_ingrediente not in self.ingredientes:
            print(f"\nError: ID {id_ingrediente} no encontrado.")
            return False
        try:
            nueva_cantidad = int(nueva_cantidad)
            if nueva_cantidad < 0:
                print("\nError: La cantidad no puede ser negativa.")
                return False
        except ValueError:
            print("\nError: La cantidad debe ser un número entero.")
            return False
        
        self.ingredientes[id_ingrediente].cantidad = nueva_cantidad
        print(f"\n✅ Cantidad de {id_ingrediente} actualizada a {nueva_cantidad}.")
        return True
    
    def eliminar_ingrediente(self, id_ingrediente):
        """Elimina un ingrediente del inventario."""
        if id_ingrediente not in self.ingredientes:
            print(f"\nError: ID {id_ingrediente} no encontrado.")
            return False
        
        nombre = self.ingredientes[id_ingrediente].nombre
        del self.ingredientes[id_ingrediente]
        print(f"\n✅ Ingrediente '{nombre}' eliminado.")
        return True
    
    def buscar_ingrediente(self, id_ingrediente):
        """Busca un ingrediente por ID y muestra sus detalles."""
        ingrediente = self.ingredientes.get(id_ingrediente)
        if not ingrediente:
            print(f"\nError: ID {id_ingrediente} no encontrado.")
            return None
        
        print("\n--- Detalles del Ingrediente ---")
        print(f"ID: {ingrediente.id_ingrediente}")
        print(f"Nombre: {ingrediente.nombre}")
        print(f"Cantidad: {ingrediente.cantidad}")
        print(f"Ubicación: {ingrediente.ubicacion}")
        return ingrediente
    
    def listar_ingredientes(self):
        """Muestra una tabla con todos los ingredientes."""
        if not self._validar_inventario_no_vacio():
            return
        
        print("\n--- Inventario de la Pizzeria ---")
        print("{:<10} {:<20} {:<10} {:<15}".format("ID", "Nombre", "Cantidad", "Ubicación"))
        print("-" * 55)
        for ing in self.ingredientes.values():
            print("{:<10} {:<20} {:<10} {:<15}".format(
                ing.id_ingrediente, ing.nombre, ing.cantidad, ing.ubicacion
            ))
    
    def guardar_inventario(self, archivo="inventario_pizzeria.json"):
        """Guarda el inventario en un archivo JSON."""
        try:
            with open(archivo, 'w') as f:
                json.dump({id: ing.to_dict() for id, ing in self.ingredientes.items()}, f, indent=4)
            print(f"\n✅ Inventario guardado en '{archivo}'.")
            return True
        except Exception as e:
            print(f"\n❌ Error al guardar: {e}")
            return False
    
    def cargar_inventario(self, archivo="inventario_pizzeria.json"):
        """Carga el inventario desde un archivo JSON."""
        try:
            if not os.path.exists(archivo):
                print(f"\n⚠️ Archivo '{archivo}' no encontrado. Se creará uno nuevo al guardar.")
                return False
            
            with open(archivo, 'r') as f:
                datos = json.load(f)
            
            self.ingredientes = {}
            for id_ing, datos_ing in datos.items():
                self.ingredientes[id_ing] = Ingrediente(
                    datos_ing['id_ingrediente'],
                    datos_ing['nombre'],
                    datos_ing['cantidad'],
                    datos_ing['ubicacion']
                )
            print(f"\n✅ Inventario cargado desde '{archivo}'.")
            return True
        except Exception as e:
            print(f"\n❌ Error al cargar: {e}")
            return False
    
    def generar_grafico_barras(self):
        """Genera un gráfico de barras con las cantidades."""
        if not self._validar_inventario_no_vacio():
            return
        
        nombres = [ing.nombre for ing in self.ingredientes.values()]
        cantidades = [ing.cantidad for ing in self.ingredientes.values()]
        
        plt.figure(figsize=(10, 5))
        plt.bar(nombres, cantidades, color='tomato')
        plt.title("Cantidad de Ingredientes en Inventario", fontweight='bold')
        plt.xlabel("Ingredientes")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    
    def generar_grafico_3d(self):
        """Genera un gráfico 3D: ID numérico vs Cantidad vs Longitud del nombre."""
        if not self._validar_inventario_no_vacio():
            return
        
        ids = [int(ing.id_ingrediente[3:]) for ing in self.ingredientes.values()]
        cantidades = [ing.cantidad for ing in self.ingredientes.values()]
        long_nombres = [len(ing.nombre) for ing in self.ingredientes.values()]
        nombres = [ing.nombre for ing in self.ingredientes.values()]
        
        fig = plt.figure(figsize=(12, 7))
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(ids, cantidades, long_nombres, c=cantidades, cmap='viridis', s=100)
        
        ax.set_title("Relación ID vs Cantidad vs Longitud del Nombre", fontweight='bold')
        ax.set_xlabel("ID (numérico)")
        ax.set_ylabel("Cantidad")
        ax.set_zlabel("Longitud del Nombre")
        
        for i, nombre in enumerate(nombres):
            ax.text(ids[i], cantidades[i], long_nombres[i], nombre, fontsize=8)
        
        plt.colorbar(scatter, label="Cantidad")
        plt.tight_layout()
        plt.show()

def mostrar_menu():
    """Muestra el menú interactivo."""
    print("\n" + "=" * 50)
    print("  SISTEMA DE INVENTARIO -  🍕 PIZZERÍA MAMA MIA")
    print("=" * 50)
    print("1. ➕ Agregar ingrediente")
    print("2. ✏️  Modificar cantidad")
    print("3. ❌ Eliminar ingrediente")
    print("4. 🔍 Buscar ingrediente")
    print("5. 💾 Listar todos los ingredientes")
    print("6. 💾 Guardar inventario")
    print("7. 📉 Mostrar gráfico de barras")
    print("8. 📊 Mostrar gráfico 3D")
    print("9. Salir")
    print("=" * 50)

def main():
    inventario = InventarioPizzeria()
    
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-9): ").strip()
        
        if opcion == "1":
            print("\n--- AGREGAR INGREDIENTE ---")
            id_ing = input("ID (formato INGXXX): ").strip().upper()
            nombre = input("Nombre: ").strip()
            cantidad = input("Cantidad: ").strip()
            ubicacion = input("Ubicación: ").strip()
            inventario.agregar_ingrediente(id_ing, nombre, cantidad, ubicacion)
        
        elif opcion == "2":
            print("\n--- MODIFICAR CANTIDAD ---")
            id_ing = input("ID del ingrediente: ").strip().upper()
            nueva_cantidad = input("Nueva cantidad: ").strip()
            inventario.modificar_cantidad(id_ing, nueva_cantidad)
        
        elif opcion == "3":
            print("\n--- ELIMINAR INGREDIENTE ---")
            id_ing = input("ID del ingrediente: ").strip().upper()
            inventario.eliminar_ingrediente(id_ing)
        
        elif opcion == "4":
            print("\n--- BUSCAR INGREDIENTE ---")
            id_ing = input("ID del ingrediente: ").strip().upper()
            inventario.buscar_ingrediente(id_ing)
        
        elif opcion == "5":
            inventario.listar_ingredientes()
        
        elif opcion == "6":
            inventario.guardar_inventario()
        
        elif opcion == "7":
            inventario.generar_grafico_barras()
        
        elif opcion == "8":
            inventario.generar_grafico_3d()
        
        elif opcion == "9":
            if input("\n¿Guardar cambios antes de salir? (s/n): ").lower() == "s":
                inventario.guardar_inventario()
            print("\n¡Hasta pronto! 👋")
            break
        
        else:
            print("\n❌ Opción no válida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()
