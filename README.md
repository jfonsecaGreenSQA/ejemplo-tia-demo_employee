# ejemplo-tia-demo_employee

Proyecto de demostración de **Test Impact Analysis (TIA)** con módulos de empleados, licencias y reportes.

**Diplomado en Aseguramiento de la Calidad de Software con IA**  
Pontificia Universidad Javeriana Cali

---

## 📋 ¿Qué es TIA?

**Test Impact Analysis (TIA)** es una técnica que determina qué tests ejecutar basándose en los archivos que cambiaron. En lugar de ejecutar TODOS los tests, TIA identifica solo los tests afectados, ahorrando tiempo en CI/CD.

## 🏗 Estructura del Proyecto

```
ejemplo-tia-demo_employee/
├── src/
│   ├── __init__.py
│   ├── employee.py        # Funciones de empleado (PIM)
│   ├── leave.py           # Funciones de licencias
│   └── reports.py         # Reportes (importa employee + leave)
├── tests/
│   ├── __init__.py
│   ├── test_employee.py   # 15 tests → employee.py
│   ├── test_leave.py      # 11 tests → leave.py
│   └── test_reports.py    #  7 tests → reports.py (indirecto)
├── .github/
│   └── workflows/
│       ├── ci-full.yml    # Ejecuta TODOS los tests
│       └── ci-tia.yml     # Ejecuta SOLO tests afectados
├── impact_analysis.py     # Script de análisis TIA
├── requirements.txt
└── README.md
```

## 🔗 Mapa de Dependencias (clave para TIA)

```
employee.py ──────→ test_employee.py  (DIRECTO)
     │
     └──→ reports.py ──→ test_reports.py  (INDIRECTO)

leave.py ─────────→ test_leave.py     (DIRECTO)
     │
     └──→ reports.py ──→ test_reports.py  (INDIRECTO)
```

**¿Por qué importa?**
- Cambiar `employee.py` afecta `test_employee.py` (directo) Y `test_reports.py` (indirecto, porque `reports.py` importa `employee.py`)
- Cambiar `leave.py` afecta `test_leave.py` (directo) Y `test_reports.py` (indirecto)
- `test_leave.py` NO se ve afectado por cambios en `employee.py`

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/jfonsecaGreenSQA/ejemplo-tia-demo_employee.git
cd ejemplo-tia-demo_employee

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows PowerShell:
venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## ✅ Ejecutar Tests

### Ejecutar TODOS los tests (sin TIA)
```bash
python -m pytest tests/ -v
```

### Ejecutar con cobertura
```bash
python -m pytest tests/ --cov=src --cov-report=term-missing
```

## 🎯 Usar TIA (Análisis de Impacto)

### Ejemplo 1: Cambio en employee.py
```bash
python impact_analysis.py --changed src/employee.py
```
**Resultado esperado:**
```
📁 Archivos cambiados:
   • src/employee.py

🎯 Tests afectados: 2
   ✅ tests/test_employee.py (importa employee)
   ✅ tests/test_reports.py (reports importa employee)

⏭ Tests omitidos: 1
   ⛔ tests/test_leave.py (no afectado)

📊 Resumen: 2/3 tests a ejecutar (33% omitidos)
```

### Ejemplo 2: Cambio en leave.py
```bash
python impact_analysis.py --changed src/leave.py
```
**Resultado esperado:**
```
🎯 Tests afectados: 2
   ✅ tests/test_leave.py (importa leave)
   ✅ tests/test_reports.py (reports importa leave)

⏭ Tests omitidos: 1
   ⛔ tests/test_employee.py (no afectado)
```

### Ejemplo 3: Múltiples archivos cambiados
```bash
python impact_analysis.py --changed src/employee.py src/leave.py
```

### Modo dinámico (analiza imports reales con AST)
```bash
python impact_analysis.py --changed src/employee.py --dynamic
```

## 🔄 Pipelines CI/CD

El proyecto incluye 2 workflows de GitHub Actions:

| Workflow | Archivo | Qué hace |
|----------|---------|----------|
| **CI Full** | `ci-full.yml` | Ejecuta TODOS los tests siempre |
| **CI TIA** | `ci-tia.yml` | Detecta cambios con `git diff` y ejecuta solo tests afectados |

### Comparación de tiempos (ejemplo con proyecto grande)

| Enfoque | Tests ejecutados | Tiempo |
|---------|-----------------|--------|
| Sin TIA | 33 tests | ~45s |
| Con TIA (cambio en employee.py) | 22 tests | ~30s |
| Con TIA (cambio en leave.py) | 18 tests | ~25s |

## 📚 Módulos

### employee.py (PIM - Personal Information Management)
- `addEmployee(first_name, last_name, ...)` - Crear empleado
- `searchEmployee(query)` - Buscar por nombre
- `editEmployee(emp_id, **kwargs)` - Editar datos
- `viewEmployee(emp_id)` - Ver detalles
- `deleteEmployee(emp_id)` - Eliminar empleado
- `listEmployees()` - Listar todos

### leave.py (Gestión de Licencias)
- `requestLeave(emp_id, leave_type, days)` - Solicitar licencia
- `approveLeave(request_id)` - Aprobar solicitud
- `rejectLeave(request_id, reason)` - Rechazar solicitud
- `getBalance(emp_id)` - Consultar balance
- `getRequests(emp_id)` - Ver solicitudes

### reports.py (Reportes - Dependencia Indirecta)
- `headcountReport()` - Reporte de headcount
- `leaveBalanceReport(emp_id)` - Balance de licencias
- `directReportsCount()` - Distribución por cargo

## 🎓 Contexto Académico

Este proyecto es parte del **Módulo 4: IA en el Proceso de Testing** del Diplomado en Aseguramiento de la Calidad de Software con IA, donde los estudiantes aprenden:

1. **TIA tradicional** - Mapeo estático de dependencias
2. **TIA con IA** - Herramientas como Launchable, Codecov ATS, Microsoft TICE
3. **CI/CD** - Integración de TIA en pipelines automatizados

---

*Diplomado QA + IA - Pontificia Universidad Javeriana Cali*
