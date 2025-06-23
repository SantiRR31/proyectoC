class ConceptoEgreso:
    def __init__(self, clave_cucop, descripcion, partida_especifica, cargo):
        self.clave_cucop = clave_cucop
        self.descripcion = descripcion
        self.partida_especifica = partida_especifica
        self.cargo = cargo

    def __repr__(self):
        return f"<ConceptoEgreso clave={self.clave_cucop} cargo={self.cargo}>"

class PolizaEgreso:
    def __init__(
        self,
        poliza_id,
        fecha,
        monto,
        montoletr,
        nombre,
        tipo_pago,
        clave_ref=None,      # opcional
        denominacion=None,
        observaciones=None,
        no_cheque=None       # opcional
    ):
        self.poliza_id = poliza_id 
        self.fecha = fecha
        self.monto = monto
        self.montoletr = montoletr
        self.nombre = nombre
        self.tipo_pago = tipo_pago
        self.clave_ref = clave_ref
        self.denominacion = denominacion
        self.observaciones = observaciones
        self.no_cheque = no_cheque
        self.conceptos = []  # Lista de ConceptoEgreso

    def agregar_concepto(self, concepto: ConceptoEgreso):
        self.conceptos.append(concepto)
        
    def campos_faltantes(self):
        faltantes = []
        if not self.fecha: faltantes.append("Fecha")
        if not self.poliza_id: faltantes.append("No. de Póliza")
        return faltantes


    def __repr__(self):
        return f"<PolizaEgreso fecha={self.fecha} monto={self.monto} conceptos={len(self.conceptos)}>"