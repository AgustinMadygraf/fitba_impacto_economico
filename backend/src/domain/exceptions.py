class FITBAError(Exception):
    """Excepción base para errores de negocio."""
    pass

class ErrorValidacionDatos(FITBAError):
    """Error cuando los datos provistos no cumplen el esquema o reglas de negocio."""
    pass

class ErrorCalculoFinanciero(FITBAError):
    """Error en los cálculos financieros."""
    pass
