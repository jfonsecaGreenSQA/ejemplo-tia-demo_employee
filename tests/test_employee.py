"""
Tests para módulo employee.py (PIM)
Demuestra mapeo directo: employee.py → test_employee.py
Proyecto: ejemplo-tia-demo_employee
Demo TIA - Diplomado QA + IA - Javeriana Cali
"""
import pytest
from src.employee import EmployeeManager


# --- Tests de addEmployee (crear) ---

def test_create_employee():
    """Crear empleado con datos válidos"""
    mgr = EmployeeManager()
    emp_id = mgr.addEmployee('Juan', 'Pérez', job_title='Developer')
    assert emp_id is not None
    emp = mgr.viewEmployee(emp_id)
    assert emp['first_name'] == 'Juan'
    assert emp['last_name'] == 'Pérez'


def test_create_employee_required_fields():
    """Validar campos requeridos"""
    mgr = EmployeeManager()
    with pytest.raises(ValueError, match="requeridos"):
        mgr.addEmployee('', 'Pérez')


def test_create_employee_min_length():
    """Validar longitud mínima de nombre"""
    mgr = EmployeeManager()
    with pytest.raises(ValueError, match="al menos 2"):
        mgr.addEmployee('J', 'Pérez')


def test_create_employee_duplicate_id():
    """No permitir ID duplicado"""
    mgr = EmployeeManager()
    mgr.addEmployee('Juan', 'Pérez', employee_id='EMP001')
    with pytest.raises(ValueError, match="ya existe"):
        mgr.addEmployee('María', 'López', employee_id='EMP001')


def test_create_employee_auto_id():
    """ID se genera automáticamente si no se provee"""
    mgr = EmployeeManager()
    emp_id = mgr.addEmployee('Ana', 'García')
    assert emp_id == '1001'


# --- Tests de searchEmployee (buscar) ---

def test_search_employee():
    """Buscar empleado por nombre"""
    mgr = EmployeeManager()
    mgr.addEmployee('Juan', 'Pérez')
    mgr.addEmployee('María', 'López')
    results = mgr.searchEmployee('Juan')
    assert len(results) == 1
    assert results[0]['first_name'] == 'Juan'


def test_search_employee_empty_query():
    """Búsqueda vacía retorna todos"""
    mgr = EmployeeManager()
    mgr.addEmployee('Juan', 'Pérez')
    mgr.addEmployee('María', 'López')
    results = mgr.searchEmployee('')
    assert len(results) == 2


def test_search_employee_no_results():
    """Búsqueda sin resultados"""
    mgr = EmployeeManager()
    mgr.addEmployee('Juan', 'Pérez')
    results = mgr.searchEmployee('Carlos')
    assert len(results) == 0


# --- Tests de editEmployee ---

def test_edit_employee():
    """Editar datos de empleado"""
    mgr = EmployeeManager()
    emp_id = mgr.addEmployee('Juan', 'Pérez', job_title='Junior Dev')
    updated = mgr.editEmployee(emp_id, job_title='Senior Dev')
    assert updated['job_title'] == 'Senior Dev'


def test_edit_employee_not_found():
    """Error al editar empleado inexistente"""
    mgr = EmployeeManager()
    with pytest.raises(ValueError, match="no encontrado"):
        mgr.editEmployee('FAKE_ID', job_title='Manager')


# --- Tests de deleteEmployee ---

def test_delete_employee():
    """Eliminar empleado existente"""
    mgr = EmployeeManager()
    emp_id = mgr.addEmployee('Juan', 'Pérez')
    result = mgr.deleteEmployee(emp_id)
    assert result is True
    with pytest.raises(ValueError):
        mgr.viewEmployee(emp_id)


def test_delete_employee_not_found():
    """Error al eliminar empleado inexistente"""
    mgr = EmployeeManager()
    with pytest.raises(ValueError, match="no encontrado"):
        mgr.deleteEmployee('FAKE_ID')


# --- Tests de viewEmployee y listEmployees ---

def test_view_employee():
    """Ver detalles de empleado"""
    mgr = EmployeeManager()
    emp_id = mgr.addEmployee('Juan', 'Pérez', job_title='QA Engineer')
    emp = mgr.viewEmployee(emp_id)
    assert emp['job_title'] == 'QA Engineer'
    assert emp['status'] == 'active'


def test_list_employees():
    """Listar todos los empleados activos"""
    mgr = EmployeeManager()
    mgr.addEmployee('Juan', 'Pérez')
    mgr.addEmployee('María', 'López')
    employees = mgr.listEmployees()
    assert len(employees) == 2
