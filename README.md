# 📋 Tasks API

Sistema completo de gestión de tareas en equipo construido con FastAPI, SQLAlchemy y MySQL.

## 🚀 Características

- ✅ **Gestión de Equipos**: CRUD completo con búsqueda y estadísticas
- ✅ **Gestión de Usuarios**: Creación, actualización y desactivación de usuarios
- ✅ **Relaciones N:M**: Usuarios pueden pertenecer a múltiples equipos con roles
- ✅ **Sistema de Tareas**: CRUD con estados, prioridades y fechas de vencimiento
- ✅ **Filtros Avanzados**: Búsqueda por equipo, usuario, estado, prioridad y texto
- ✅ **Asignación de Tareas**: Asignar y reasignar tareas a usuarios
- ✅ **Estadísticas**: Métricas agrupadas por estado y prioridad
- ✅ **Documentación Interactiva**: Swagger UI automática
- ✅ **Validación de Datos**: Pydantic con validaciones robustas

## 🛠️ Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **MySQL** - Base de datos relacional
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI

## 📋 Requisitos Previos

- Python 3.10 o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Jair-N-dev/tasks-api.git
cd tasks-api
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# Activar entorno virtual
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

Crear base de datos en MySQL:

```sql
CREATE DATABASE tasks_db;
```

### 5. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=mysql+pymysql://usuario:password@localhost/tasks_db
SECRET_KEY=tu_clave_secreta_cambiar_en_produccion
```

### 6. Poblar datos de ejemplo (opcional)

```bash
python seed.py
```

### 7. Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: **http://localhost:8000**

## 📚 Documentación

Una vez el servidor esté corriendo, accede a:

- **Swagger UI (interactiva)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📖 Endpoints Principales

### Teams

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/teams/` | Listar equipos (con búsqueda) |
| POST | `/teams/` | Crear equipo |
| GET | `/teams/{id}` | Obtener equipo por ID |
| GET | `/teams/{id}/members` | Ver miembros del equipo |
| PUT | `/teams/{id}` | Actualizar equipo |
| DELETE | `/teams/{id}` | Eliminar equipo |
| GET | `/teams/stats/general` | Estadísticas generales |

### Users

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/users/` | Listar usuarios (con filtros) |
| POST | `/users/` | Crear usuario |
| GET | `/users/{id}` | Obtener usuario por ID |
| GET | `/users/{id}/teams` | Ver equipos del usuario |
| PUT | `/users/{id}` | Actualizar usuario |
| DELETE | `/users/{id}` | Eliminar usuario |
| POST | `/users/{id}/teams/{team_id}` | Agregar usuario a equipo |
| DELETE | `/users/{id}/teams/{team_id}` | Remover usuario de equipo |

### Tasks

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/tasks/` | Listar tareas (con filtros múltiples) |
| POST | `/tasks/` | Crear tarea |
| GET | `/tasks/{id}` | Obtener tarea por ID |
| PUT | `/tasks/{id}` | Actualizar tarea |
| DELETE | `/tasks/{id}` | Eliminar tarea |
| PATCH | `/tasks/{id}/estado` | Cambiar estado de tarea |
| PATCH | `/tasks/{id}/asignar/{user_id}` | Asignar tarea a usuario |
| GET | `/tasks/stats/general` | Estadísticas de tareas |

## 💡 Ejemplos de Uso

### Crear un equipo

```bash
curl -X POST http://localhost:8000/teams/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Desarrollo Mobile",
    "descripcion": "Equipo de desarrollo de apps móviles"
  }'
```

### Crear un usuario

```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laura Gómez",
    "email": "laura@company.com",
    "activo": true
  }'
```

### Crear una tarea

```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Implementar notificaciones push",
    "descripcion": "Configurar Firebase Cloud Messaging",
    "prioridad": "high",
    "team_id": 1,
    "asignado_a": 2,
    "due_date": "2026-01-30T18:00:00"
  }'
```

### Filtrar tareas

```bash
# Tareas pendientes de alta prioridad
GET /tasks/?estado=pending&prioridad=high

# Tareas del equipo 1 asignadas al usuario 3
GET /tasks/?team_id=1&asignado_a=3

# Buscar tareas que contengan "API"
GET /tasks/?search=API
```

### Cambiar estado de tarea

```bash
curl -X PATCH http://localhost:8000/tasks/5/estado?nuevo_estado=completed
```

## 📁 Estructura del Proyecto

```
tasks-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point de la aplicación
│   ├── database.py          # Configuración de base de datos
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── team.py
│   │   ├── user.py
│   │   ├── user_team.py
│   │   └── task.py
│   ├── schemas/             # Schemas Pydantic (validación)
│   │   ├── __init__.py
│   │   ├── team.py
│   │   ├── user.py
│   │   ├── user_team.py
│   │   └── task.py
│   └── routers/             # Endpoints agrupados
│       ├── __init__.py
│       ├── teams.py
│       ├── users.py
│       └── tasks.py
├── seed.py                  # Script para datos de ejemplo
├── .env                     # Variables de entorno (no incluido en repo)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🗄️ Modelo de Datos

### Relaciones

```
Teams ←──────┐
             │
User_Teams ──┤  (N:M)
             │
Users ←──────┘

Teams ←────── Tasks (N:1)
Users ←────── Tasks (N:1, opcional)
```

### Enums

**TaskStatus**: `pending`, `in_progress`, `completed`, `cancelled`

**TaskPriority**: `low`, `medium`, `high`, `urgent`

**UserTeamRole**: `member`, `admin`, `owner`

## 🧪 Testing

(Próximamente: Tests con Pytest)

## 🚀 Deployment

### Preparación para producción

1. Cambiar `SECRET_KEY` en `.env`
2. Configurar base de datos en la nube (AWS RDS, DigitalOcean, etc.)
3. Usar servidor ASGI en producción (Gunicorn + Uvicorn workers)
4. Configurar CORS apropiadamente
5. Agregar rate limiting
6. Implementar logging

### Deploy sugerido

- **Backend**: Railway, Render, Heroku
- **Base de datos**: AWS RDS, PlanetScale, DigitalOcean

## 📝 Roadmap

- [ ] Implementar autenticación JWT
- [ ] Agregar sistema de comentarios en tareas
- [ ] Notificaciones por email
- [ ] WebSockets para actualizaciones en tiempo real
- [ ] Tests unitarios y de integración
- [ ] Paginación mejorada con cursores
- [ ] Exportar reportes en PDF/Excel
- [ ] Dashboard con gráficas

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👤 Autor

**Jair**

- GitHub: [@Jair-N-dev](https://github.com/Jair-N-dev)

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!