"""
Tests para módulo leave.py (Licencias)
Demuestra mapeo directo: leave.py → test_leave.py
Proyecto: ejemplo-tia-demo_employee
Demo TIA - Diplomado QA + IA - Javeriana Cali
"""
import pytest
from src.leave import LeaveManager


# --- Tests de requestLeave ---

def test_request_leave():
    """Solicitar licencia válida"""
    mgr = LeaveManager()
    req = mgr.requestLeave('EMP001', 'vacation', 5, 'Viaje familiar')
    assert req['status'] == 'pending'
    assert req['days'] == 5


def test_request_leave_invalid_type():
    """Error con tipo de licencia inválido"""
    mgr = LeaveManager()
    with pytest.raises(ValueError, match="no válido"):
        mgr.requestLeave('EMP001', 'sabbatical', 30)


def test_request_leave_insufficient_balance():
    """Error cuando no hay balance suficiente"""
    mgr = LeaveManager()
    with pytest.raises(ValueError, match="insuficiente"):
        mgr.requestLeave('EMP001', 'personal', 10)  # max es 3


def test_request_leave_zero_days():
    """Error con cero días"""
    mgr = LeaveManager()
    with pytest.raises(ValueError, match="positivo"):
        mgr.requestLeave('EMP001', 'vacation', 0)


# --- Tests de approveLeave ---

def test_approve_leave():
    """Aprobar solicitud pendiente"""
    mgr = LeaveManager()
    req = mgr.requestLeave('EMP001', 'vacation', 3)
    approved = mgr.approveLeave(req['id'])
    assert approved['status'] == 'approved'


def test_approve_leave_updates_balance():
    """Aprobar descuenta del balance"""
    mgr = LeaveManager()
    req = mgr.requestLeave('EMP001', 'vacation', 3)
    mgr.approveLeave(req['id'])
    balance = mgr.getBalance('EMP001')
    assert balance['vacation'] == 12  # 15 - 3


def test_approve_already_processed():
    """No se puede aprobar solicitud ya procesada"""
    mgr = LeaveManager()
    req = mgr.requestLeave('EMP001', 'vacation', 3)
    mgr.approveLeave(req['id'])
    with pytest.raises(ValueError, match="pendientes"):
        mgr.approveLeave(req['id'])


# --- Tests de rejectLeave ---

def test_reject_leave():
    """Rechazar solicitud pendiente"""
    mgr = LeaveManager()
    req = mgr.requestLeave('EMP001', 'vacation', 5)
    rejected = mgr.rejectLeave(req['id'], 'Período no disponible')
    assert rejected['status'] == 'rejected'


# --- Tests de getBalance ---

def test_get_balance_initial():
    """Balance inicial tiene todos los tipos"""
    mgr = LeaveManager()
    balance = mgr.getBalance('EMP001')
    assert balance['vacation'] == 15
    assert balance['sick'] == 10
    assert balance['personal'] == 3


# --- Tests de getRequests ---

def test_get_requests_by_employee():
    """Filtrar solicitudes por empleado"""
    mgr = LeaveManager()
    mgr.requestLeave('EMP001', 'vacation', 3)
    mgr.requestLeave('EMP002', 'sick', 1)
    mgr.requestLeave('EMP001', 'personal', 1)
    requests = mgr.getRequests('EMP001')
    assert len(requests) == 2
