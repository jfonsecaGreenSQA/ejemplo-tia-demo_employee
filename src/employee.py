"""
Módulo de Gestión de Empleados (PIM)
Funciones CRUD para Personal Information Management
Proyecto: ejemplo-tia-demo_employee
Demo TIA - Diplomado QA + IA - Javeriana Cali
"""


class EmployeeManager:
    """Gestor de empleados - simula operaciones PIM de OrangeHRM"""

    def __init__(self):
        self.employees = {}
        self._next_id = 1001

    def addEmployee(self, first_name, last_name, employee_id=None, job_title=None):
        """Crear un nuevo empleado con validaciones"""
        if not first_name or not last_name:
            raise ValueError("Nombre y apellido son requeridos")

        if len(first_name) < 2 or len(last_name) < 2:
            raise ValueError("Nombre y apellido deben tener al menos 2 caracteres")

        emp_id = employee_id or str(self._next_id)
        self._next_id += 1

        if emp_id in self.employees:
            raise ValueError(f"Empleado con ID {emp_id} ya existe")

        self.employees[emp_id] = {
            'id': emp_id,
            'first_name': first_name,
            'last_name': last_name,
            'job_title': job_title or 'Sin asignar',
            'status': 'active'
        }
        return emp_id

    def searchEmployee(self, query):
        """Buscar empleados con filtros por nombre o apellido"""
        if not query:
            return list(self.employees.values())

        query_lower = query.lower()
        results = []
        for emp in self.employees.values():
            if (query_lower in emp['first_name'].lower() or
                    query_lower in emp['last_name'].lower()):
                results.append(emp)
        return results

    def editEmployee(self, emp_id, **kwargs):
        """Editar datos de un empleado existente"""
        if emp_id not in self.employees:
            raise ValueError(f"Empleado {emp_id} no encontrado")

        emp = self.employees[emp_id]
        for key, value in kwargs.items():
            if key in emp:
                emp[key] = value
        return emp

    def viewEmployee(self, emp_id):
        """Ver detalles de un empleado"""
        if emp_id not in self.employees:
            raise ValueError(f"Empleado {emp_id} no encontrado")
        return self.employees[emp_id]

    def deleteEmployee(self, emp_id):
        """Eliminar un empleado"""
        if emp_id not in self.employees:
            raise ValueError(f"Empleado {emp_id} no encontrado")
        del self.employees[emp_id]
        return True

    def listEmployees(self):
        """Listar todos los empleados activos"""
        return [e for e in self.employees.values() if e['status'] == 'active']
