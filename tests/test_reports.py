"""
Tests para módulo reports.py
IMPORTANTE para TIA: reports.py importa employee.py
Por lo tanto, cambiar employee.py TAMBIÉN afecta a estos tests
Esto demuestra DEPENDENCIA INDIRECTA
Proyecto: ejemplo-tia-demo_employee
Demo TIA - Diplomado QA + IA - Javeriana Cali
"""
import pytest
from src.reports import ReportGenerator


# --- Tests de headcountReport ---

def test_headcount_report_empty():
    """Reporte con cero empleados"""
    gen = ReportGenerator()
    report = gen.headcountReport()
    assert report['total'] == 0
    assert report['employees'] == []


def test_headcount_report_with_employees():
    """Reporte con empleados cargados"""
    gen = ReportGenerator()
    gen.emp_manager.addEmployee('Juan', 'Pérez', job_title='Developer')
    gen.emp_manager.addEmployee('María', 'López', job_title='QA Engineer')
    report = gen.headcountReport()
    assert report['total'] == 2


def test_headcount_report_title():
    """Verificar título del reporte"""
    gen = ReportGenerator()
    report = gen.headcountReport()
    assert report['title'] == 'Reporte de Headcount'


# --- Tests de leaveBalanceReport ---

def test_leave_balance_report():
    """Reporte de balance para empleado existente"""
    gen = ReportGenerator()
    emp_id = gen.emp_manager.addEmployee('Ana', 'García')
    report = gen.leaveBalanceReport(emp_id)
    assert 'vacation' in report['balances']
    assert report['balances']['vacation'] == 15


def test_leave_balance_report_not_found():
    """Error con empleado inexistente"""
    gen = ReportGenerator()
    with pytest.raises(ValueError, match="no encontrado"):
        gen.leaveBalanceReport('FAKE_ID')


# --- Tests de directReportsCount ---

def test_direct_reports_count():
    """Distribución por cargo"""
    gen = ReportGenerator()
    gen.emp_manager.addEmployee('Juan', 'Pérez', job_title='Developer')
    gen.emp_manager.addEmployee('Ana', 'García', job_title='Developer')
    gen.emp_manager.addEmployee('María', 'López', job_title='QA Engineer')
    report = gen.directReportsCount()
    assert report['distribution']['Developer'] == 2
    assert report['distribution']['QA Engineer'] == 1
