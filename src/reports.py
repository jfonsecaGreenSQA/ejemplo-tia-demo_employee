"""
Módulo de Reportes
Genera reportes que DEPENDEN de employee.py y leave.py
Esto demuestra dependencias indirectas en TIA
Proyecto: ejemplo-tia-demo_employee
Demo TIA - Diplomado QA + IA - Javeriana Cali
"""
from src.employee import EmployeeManager
from src.leave import LeaveManager


class ReportGenerator:
    """Generador de reportes - demuestra dependencia indirecta para TIA"""

    def __init__(self):
        self.emp_manager = EmployeeManager()
        self.leave_manager = LeaveManager()

    def headcountReport(self):
        """Reporte de headcount total"""
        employees = self.emp_manager.listEmployees()
        return {
            'title': 'Reporte de Headcount',
            'total': len(employees),
            'employees': [
                f"{e['first_name']} {e['last_name']} - {e['job_title']}"
                for e in employees
            ]
        }

    def leaveBalanceReport(self, emp_id):
        """Reporte de balance de licencias por empleado"""
        try:
            emp = self.emp_manager.viewEmployee(emp_id)
        except ValueError:
            raise ValueError(f"Empleado {emp_id} no encontrado para reporte")

        balance = self.leave_manager.getBalance(emp_id)
        return {
            'title': f"Balance de Licencias - {emp['first_name']} {emp['last_name']}",
            'employee_id': emp_id,
            'balances': balance
        }

    def directReportsCount(self):
        """Contar empleados por estado (demuestra dependencia de employee)"""
        all_employees = self.emp_manager.listEmployees()
        by_title = {}
        for emp in all_employees:
            title = emp['job_title']
            by_title[title] = by_title.get(title, 0) + 1
        return {
            'title': 'Distribución por Cargo',
            'distribution': by_title
        }
