from app.database import SessionLocal
from app.models.team import Team
from app.models.user import User
from app.models.user_team import UserTeam
from app.models.task import Task, TaskStatus, TaskPriority
from datetime import datetime, timedelta

def seed_database():
    db = SessionLocal()
    
    try:
        # Verificar si ya hay datos
        if db.query(Team).first():
            print("❌ La base de datos ya tiene datos. No se ejecuta el seed.")
            return
        
        print("🌱 Iniciando seed de datos...")
        
        # ========== TEAMS ==========
        teams = [
            Team(nombre="Desarrollo Frontend", descripcion="Equipo de desarrollo de interfaces y UX/UI"),
            Team(nombre="Desarrollo Backend", descripcion="Equipo de APIs, bases de datos y lógica de negocio"),
            Team(nombre="DevOps", descripcion="Infraestructura, CI/CD y deployment"),
            Team(nombre="QA", descripcion="Quality Assurance y testing"),
            Team(nombre="Diseño", descripcion="Diseño gráfico y experiencia de usuario")
        ]
        
        db.add_all(teams)
        db.commit()
        print(f"✅ {len(teams)} equipos creados")
        
        # ========== USERS ==========
        users = [
            User(nombre="Juan Pérez", email="juan.perez@company.com", activo=True),
            User(nombre="María García", email="maria.garcia@company.com", activo=True),
            User(nombre="Carlos López", email="carlos.lopez@company.com", activo=True),
            User(nombre="Ana Martínez", email="ana.martinez@company.com", activo=True),
            User(nombre="Luis Rodríguez", email="luis.rodriguez@company.com", activo=True),
            User(nombre="Sofia Torres", email="sofia.torres@company.com", activo=True),
            User(nombre="Pedro Sánchez", email="pedro.sanchez@company.com", activo=False),
        ]
        
        db.add_all(users)
        db.commit()
        print(f"✅ {len(users)} usuarios creados")
        
        # ========== USER_TEAMS (Relaciones) ==========
        user_teams = [
            # Juan en Frontend y Backend
            UserTeam(user_id=1, team_id=1, role="admin"),
            UserTeam(user_id=1, team_id=2, role="member"),
            # María en Frontend
            UserTeam(user_id=2, team_id=1, role="member"),
            # Carlos en Backend
            UserTeam(user_id=3, team_id=2, role="admin"),
            # Ana en DevOps
            UserTeam(user_id=4, team_id=3, role="owner"),
            # Luis en QA
            UserTeam(user_id=5, team_id=4, role="admin"),
            # Sofia en Diseño
            UserTeam(user_id=6, team_id=5, role="member"),
        ]
        
        db.add_all(user_teams)
        db.commit()
        print(f"✅ {len(user_teams)} relaciones usuario-equipo creadas")
        
        # ========== TASKS ==========
        hoy = datetime.utcnow()
        
        tasks = [
            # Frontend tasks
            Task(
                titulo="Implementar landing page",
                descripcion="Crear página de inicio responsive con hero section y features",
                estado=TaskStatus.COMPLETED,
                prioridad=TaskPriority.HIGH,
                team_id=1,
                asignado_a=1,
                due_date=hoy - timedelta(days=5),
                completed_at=hoy - timedelta(days=3)
            ),
            Task(
                titulo="Diseñar componentes del dashboard",
                descripcion="Crear componentes reutilizables: tablas, cards, modals",
                estado=TaskStatus.IN_PROGRESS,
                prioridad=TaskPriority.HIGH,
                team_id=1,
                asignado_a=2,
                due_date=hoy + timedelta(days=3)
            ),
            Task(
                titulo="Optimizar rendimiento de imágenes",
                descripcion="Implementar lazy loading y compresión de assets",
                estado=TaskStatus.PENDING,
                prioridad=TaskPriority.MEDIUM,
                team_id=1,
                asignado_a=1,
                due_date=hoy + timedelta(days=7)
            ),
            
            # Backend tasks
            Task(
                titulo="Implementar autenticación JWT",
                descripcion="Sistema de login/logout con tokens y refresh tokens",
                estado=TaskStatus.IN_PROGRESS,
                prioridad=TaskPriority.URGENT,
                team_id=2,
                asignado_a=3,
                due_date=hoy + timedelta(days=2)
            ),
            Task(
                titulo="Crear endpoints de reportes",
                descripcion="APIs para generar reportes en PDF y Excel",
                estado=TaskStatus.PENDING,
                prioridad=TaskPriority.MEDIUM,
                team_id=2,
                asignado_a=3,
                due_date=hoy + timedelta(days=10)
            ),
            Task(
                titulo="Optimizar queries de base de datos",
                descripcion="Agregar índices y optimizar consultas lentas",
                estado=TaskStatus.PENDING,
                prioridad=TaskPriority.LOW,
                team_id=2,
                asignado_a=None,  # Sin asignar
                due_date=hoy + timedelta(days=14)
            ),
            
            # DevOps tasks
            Task(
                titulo="Configurar pipeline de CI/CD",
                descripcion="Setup de GitHub Actions para deploy automático",
                estado=TaskStatus.COMPLETED,
                prioridad=TaskPriority.HIGH,
                team_id=3,
                asignado_a=4,
                due_date=hoy - timedelta(days=10),
                completed_at=hoy - timedelta(days=8)
            ),
            Task(
                titulo="Implementar monitoreo con Prometheus",
                descripcion="Configurar métricas y alertas de sistema",
                estado=TaskStatus.IN_PROGRESS,
                prioridad=TaskPriority.MEDIUM,
                team_id=3,
                asignado_a=4,
                due_date=hoy + timedelta(days=5)
            ),
            
            # QA tasks
            Task(
                titulo="Escribir tests E2E",
                descripcion="Tests end-to-end con Cypress para flujos críticos",
                estado=TaskStatus.PENDING,
                prioridad=TaskPriority.HIGH,
                team_id=4,
                asignado_a=5,
                due_date=hoy + timedelta(days=6)
            ),
            Task(
                titulo="Documentar casos de prueba",
                descripcion="Crear matriz de casos de prueba y escenarios",
                estado=TaskStatus.CANCELLED,
                prioridad=TaskPriority.LOW,
                team_id=4,
                asignado_a=5,
                due_date=hoy - timedelta(days=2)
            ),
            
            # Diseño tasks
            Task(
                titulo="Crear sistema de diseño",
                descripcion="Design system con colores, tipografías y componentes",
                estado=TaskStatus.IN_PROGRESS,
                prioridad=TaskPriority.URGENT,
                team_id=5,
                asignado_a=6,
                due_date=hoy + timedelta(days=4)
            ),
            Task(
                titulo="Diseñar iconografía personalizada",
                descripcion="Set de iconos custom para la aplicación",
                estado=TaskStatus.PENDING,
                prioridad=TaskPriority.LOW,
                team_id=5,
                asignado_a=None,
                due_date=hoy + timedelta(days=15)
            ),
        ]
        
        db.add_all(tasks)
        db.commit()
        print(f"✅ {len(tasks)} tareas creadas")
        
        print("\n🎉 Seed completado exitosamente!")
        print(f"📊 Resumen:")
        print(f"   - {len(teams)} equipos")
        print(f"   - {len(users)} usuarios")
        print(f"   - {len(user_teams)} asignaciones")
        print(f"   - {len(tasks)} tareas")
        
    except Exception as e:
        print(f"❌ Error durante el seed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()