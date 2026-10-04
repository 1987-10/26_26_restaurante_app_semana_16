# 🍽️ Restaurante App — Semana 16

**Asignatura:** Programación Orientada a Objetos (POO)  
**Universidad:** Universidad Estatal Amazónica  
**Estudiante:** Manuel Rafael Ayala Arévalo  
 

---

## 📌 Descripción del Proyecto

Evolución y consolidación de la aplicación gráfica de escritorio **Restaurante App** mediante la implementación avanzada del **manejo de eventos en Tkinter utilizando `bind()`** en el módulo administrativo de **Gestión de Usuarios**. El sistema mantiene una arquitectura modular limpia en capas (MVC), persistencia en archivos JSON, códigos únicos por entidad y un control estricto de acceso basado en roles.

---

## ⚙️ Eventos e Innovaciones Implementadas (Semana 16)

1. **`<<TreeviewSelect>>`**: 
   * Captura la selección de filas en la tabla de usuarios. 
   * Consulta automáticamente al servicio (`RestauranteServicio`) para extraer y autocompletar los campos del formulario con los datos correspondientes de forma segura.
2. **`<Return>` (Tecla Enter)**: 
   * Atajo de teclado integrado en las cajas de texto principales para confirmar y registrar operaciones de forma rápida sin necesidad de hacer clic en el botón.
3. **`<Escape>` (Tecla Esc)**: 
   * Evento global asignado para limpiar de forma instantánea el formulario de usuarios y deseleccionar cualquier registro activo en la tabla.
4. **`<<ComboboxSelected>>`**: 
   * Control dinámico de eventos en las listas desplegables para asegurar la interactividad y actualización de los elementos de selección.
5. **Identificador Único (`codigo_unico`) por Entidad**: 
   * Implementación de una propiedad única y representativa para cada modelo , diferenciada de su ID numérico secuencial.
6. **Control de Acceso Basado en Roles (RBAC)**: 
   * Restricción visual y lógica de la pestaña de **Usuarios**: es visible e interactiva exclusivamente para los usuarios autenticados con el rol de `Administrador`. Los perfiles de `Empleado` operan únicamente sobre los módulos permitidos de productos y ventas.

