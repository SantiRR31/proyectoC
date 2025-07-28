from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ConceptoEgreso:
    clave_cucop: str
    descripcion: str
    partida_especifica: str
    cargo: float

@dataclass
class PolizaEgreso:
    poliza_id: Optional[int]
    no_poliza: str
    fecha: str
    monto: float
    nombre: str
    tipo_pago: str
    monto_letra: Optional[str] = None 
    clave_ref: Optional[str] = None
    denominacion: Optional[str] = None
    observaciones: Optional[str] = None
    no_cheque: Optional[str] = None
    estado: Optional[str] = "activo"
    conceptos: List[ConceptoEgreso] = field(default_factory=list)

    def agregar_concepto(self, concepto: ConceptoEgreso):
        self.conceptos.append(concepto)

    def esta_cancelada(self):
        return self.estado == "cancelado"

    def campos_faltantes(self):
        faltantes = []
        if not self.fecha:
            faltantes.append("Fecha")
        if not self.no_poliza:  # ← Este sí debe validarse
            faltantes.append("No. de Póliza")
        if self.monto is None or self.monto == 0:
            faltantes.append("Monto")
        return faltantes

