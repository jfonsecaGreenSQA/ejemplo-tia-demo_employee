"""
Módulo de Gestión de Licencias (Leave)
Solicitud, aprobación y balance de licencias
Proyecto: ejemplo-tia-demo_employee
Demo TIA - Diplomado QA + IA - Javeriana Cali
"""


class LeaveManager:
    """Gestor de licencias - simula módulo Leave de OrangeHRM"""

    LEAVE_TYPES = {
        'vacation': {'max_days': 15, 'label': 'Vacaciones'},
        'sick': {'max_days': 10, 'label': 'Enfermedad'},
        'personal': {'max_days': 3, 'label': 'Personal'},
        'maternity': {'max_days': 90, 'label': 'Maternidad'},
    }

    def __init__(self):
        self.requests = []
        self.balances = {}
        self._next_id = 1

    def initBalance(self, emp_id):
        """Inicializar balance de licencias para un empleado"""
        self.balances[emp_id] = {
            lt: info['max_days'] for lt, info in self.LEAVE_TYPES.items()
        }
        return self.balances[emp_id]

    def requestLeave(self, emp_id, leave_type, days, reason=""):
        """Solicitar licencia"""
        if leave_type not in self.LEAVE_TYPES:
            raise ValueError(f"Tipo de licencia '{leave_type}' no válido")

        if days <= 0:
            raise ValueError("Días debe ser positivo")

        if emp_id not in self.balances:
            self.initBalance(emp_id)

        available = self.balances[emp_id].get(leave_type, 0)
        if days > available:
            raise ValueError(f"Balance insuficiente: {available} días disponibles")

        request = {
            'id': self._next_id,
            'emp_id': emp_id,
            'type': leave_type,
            'days': days,
            'reason': reason,
            'status': 'pending'
        }
        self._next_id += 1
        self.requests.append(request)
        return request

    def approveLeave(self, request_id):
        """Aprobar solicitud de licencia"""
        req = self._findRequest(request_id)
        if req['status'] != 'pending':
            raise ValueError("Solo se pueden aprobar solicitudes pendientes")

        req['status'] = 'approved'
        self.balances[req['emp_id']][req['type']] -= req['days']
        return req

    def rejectLeave(self, request_id, reason=""):
        """Rechazar solicitud de licencia"""
        req = self._findRequest(request_id)
        if req['status'] != 'pending':
            raise ValueError("Solo se pueden rechazar solicitudes pendientes")

        req['status'] = 'rejected'
        req['reject_reason'] = reason
        return req

    def getBalance(self, emp_id):
        """Consultar balance de licencias"""
        if emp_id not in self.balances:
            return self.initBalance(emp_id)
        return self.balances[emp_id]

    def getRequests(self, emp_id=None):
        """Obtener solicitudes, opcionalmente filtradas por empleado"""
        if emp_id:
            return [r for r in self.requests if r['emp_id'] == emp_id]
        return self.requests

    def _findRequest(self, request_id):
        """Buscar solicitud por ID"""
        for req in self.requests:
            if req['id'] == request_id:
                return req
        raise ValueError(f"Solicitud {request_id} no encontrada")
