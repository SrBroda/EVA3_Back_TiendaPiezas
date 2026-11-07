def carrito_count(request):
    carrito = request.session.get('carrito', {})
    if not isinstance(carrito, dict):
        return {'cantidad_carrito': 0}

    cantidad_total = 0
    for cantidad in carrito.values():
        try:
            cantidad_total += max(int(cantidad), 0)
        except (TypeError, ValueError):
            continue
    return {'cantidad_carrito': cantidad_total}