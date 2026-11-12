# Bitácora de uso de IA

## 1) Diseño de interfaz y menú por roles
**Prompt utilizado:**
> Diseña una interfaz web para un sistema de herramientas vecinales con Bootstrap 5. Necesito una página base con navbar, bloque de mensajes, usuario conectado con rol (Encargado/Socio), cierre de sesión y menú diferente según el tipo de usuario.

**Respuesta obtenida:**
Se propuso una plantilla base con navbar y condición lógica para mostrar enlaces según `user.is_staff`, además del bloque `{% if messages %}` para alertas Bootstrap.

**Qué acepté o corregí:**
Acepté la estructura general de la base y ajusté los enlaces para incluir el acceso a catálogo, solicitudes y gestión de préstamos, además de mantener los mensajes con clases de Bootstrap y el cierre de sesión mediante formulario POST requerido en Django 5+.

## 2) Estructura del flujo de sesiones para préstamos
**Prompt utilizado:**
> Necesito implementar un carrito temporal de herramientas para socios, usando sesiones de Django. Quiero agregar herramientas, listarlas, quitar elementos y confirmar préstamos con transacción y validación de disponibilidad.

**Respuesta obtenida:**
Se recomendó guardar una lista de IDs en `request.session['solicitud']`, validar disponibilidad y límite de 3 herramientas, y confirmar el préstamo con `transaction.atomic` para asegurar consistencia.

**Qué acepté o corregí:**
Acepte la idea de usar sesión, pero validé además que la herramienta no estuviera en reparación, que la lista no duplicara elementos y que la creación del préstamo y el cambio de disponibilidad fueran consistentes. Ajusté el flujo para volver al catálogo con mensajes claros y limpiar la sesión final.

## 3) Revisión de seguridad y manejo de errores
**Prompt utilizado:**
> Revisa la seguridad del sistema para evitar IDOR y errores al eliminar categorías o herramientas con relaciones protegidas. Haz recomendaciones concretas y un ejemplo de validación en vistas.

**Respuesta obtenida:**
Se indicaron dos puntos clave: usar `get_object_or_404` filtrando por `socio=request.user` en la cancelación de préstamos, y capturar `ProtectedError` en eliminaciones cuando hay relaciones dependientes.

**Qué acepté o corregí:**
Aplicamos ambas medidas: `cancelar_prestamo` solo permite cancelar el préstamo del usuario autenticado; `categoria_delete` y `herramienta_delete` manejan `ProtectedError` para evitar borrados peligrosos y mostrar mensajes de error claros al encargado.
