# Herramientas en Común

Sistema de gestión de herramientas para la Junta de Vecinos Villa Los Aromos.

## Descripción
La aplicación permite:
- Administrar categorías y herramientas.
- Registrar préstamos y su estado.
- Permitir que los encargados gestionen inventario y préstamos.
- Permitir a los socios solicitar herramientas desde un catálogo y confirmar una solicitud desde sesión.

## Requisitos
- Python 3.12
- Entorno virtual con Django y python-dotenv

## Instalación y ejecución
1. Crear entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   # o en Windows: venv\Scripts\activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Preparar variables de entorno:
   ```bash
   copy .env.example .env
   ```
   En Windows PowerShell:
   ```powershell
   Copy-Item .env.example .env
   ```
4. Migrar base de datos:
   ```bash
   python manage.py migrate
   ```
5. Cargar datos iniciales:
   ```bash
   python manage.py loaddata prestamos/fixtures/datos_iniciales.json
   ```
6. Ejecutar servidor:
   ```bash
   python manage.py runserver
   ```

## Credenciales de prueba

| Usuario | Contraseña | Rol |
| --- | --- | --- |
| admin | Admin2026! | Encargado (superusuario) |
| encargado | Encargado2026! | Encargado |
| socio1 | Socio2026! | Socio |

## Nota
Si necesitas crear nuevos usuarios, puedes hacerlo desde el panel administrativo de Django o con `python manage.py createsuperuser`.
