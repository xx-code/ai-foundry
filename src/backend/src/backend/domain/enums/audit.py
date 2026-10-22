from enum import Enum

class AuditAction(str, Enum): 
    CREATE = 'CREATE',
    UPDATE = 'UPDATE',
    DELETE = 'DELETE',
    VIEW = 'VIEW',
    LOGIN = 'LOGIN',
    LOGOUT = 'LOGOUT',
    PERMISSION_CHANGE = 'PERMISSION_CHANGE'