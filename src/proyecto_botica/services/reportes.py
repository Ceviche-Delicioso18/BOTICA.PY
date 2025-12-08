"""
Modulo de Servicios - Reportes
Define la logica de generacion de reportes y analisis
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from ..models.producto import Producto
from ..repositories.inventario import Inventario


class GeneradorReportes:
    """
    Genera reportes y estadísticas del inventario.
    """

    def __init__(self, inventario: Inventario):
        """Inicializa el generador de reportes inyectando la dependencia Inventario."""
        self.inventario = inventario

    def valor_total_inventario(self) -> float:
        """Calcula el valor total monetario de todo el inventario."""
        productos = self.inventario.repositorio.obtener_todos()
        return sum(p.calcular_valor_total() for p in productos)

    def cantidad_total_productos(self) -> int:
        """Cuenta la cantidad total de TIPOS de productos (número de filas en el inventario)."""
        return len(self.inventario.repositorio.obtener_todos())
    
    def total_items_stock(self) -> int:
        """Calcula el total de ITEMS (unidades) en stock."""
        productos = self.inventario.repositorio.obtener_todos()
        return sum(p.cantidad for p in productos)
    
    def producto_mas_caro(self) -> Optional[Producto]:
        """Obtiene el producto con el precio unitario más alto."""
        productos = self.inventario.repositorio.obtener_todos()
        return max(productos, key=lambda p: p.precio) if productos else None

    def producto_mas_barato(self) -> Optional[Producto]:
        """Obtiene el producto con el precio unitario más bajo."""
        productos = self.inventario.repositorio.obtener_todos()
        return min(productos, key=lambda p: p.precio) if productos else None

    def reporte_completo(self) -> Dict[str, Any]:
        """Genera un diccionario con todos los datos del reporte."""
        productos_bajo_stock = self.inventario.obtener_productos_bajo_stock()
        
        return {
            "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_productos": self.cantidad_total_productos(),
            "total_items": self.total_items_stock(),
            "valor_total": self.valor_total_inventario(),
            "producto_mas_caro": self.producto_mas_caro(),
            "producto_mas_barato": self.producto_mas_barato(),
            "productos_bajo_stock": productos_bajo_stock # La lista completa de productos
        }