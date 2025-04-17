import math
import time

def calcular_base_iterativa(suma, producto, precision=0.0001, max_iter=100):
   
    if suma <= 0 or producto <= 0:
        return None
    x = 2.0
    for i in range(max_iter):
        fx = pow(x, suma) - producto
        if abs(fx) < precision:
            return x
        dfx = suma * pow(x, suma - 1)
        if abs(dfx) < 1e-10:
            return None
        x = x - fx / dfx
    return x

def calcular_base_recursiva(suma, producto, x=2.0, precision=0.0001, iter_actual=0, max_iter=100):
    
    if suma <= 0 or producto <= 0:
        return None
    if iter_actual >= max_iter:
        return x
    fx = pow(x, suma) - producto
    if abs(fx) < precision:
        return x
    dfx = suma * pow(x, suma - 1)
    if abs(dfx) < 1e-10:
        return None
    nuevo_x = x - fx / dfx
    return calcular_base_recursiva(suma, producto, nuevo_x, precision, iter_actual + 1, max_iter)

def bubble_sort_cuartetos(resultados):
    n = len(resultados)
    for i in range(n):
        for j in range(0, n - i - 1):
            if not resultados[j][2] and resultados[j+1][2]:
                resultados[j], resultados[j+1] = resultados[j+1], resultados[j]
            # Si ambos son válidos, se ordenan por el valor de la base
            elif resultados[j][2] and resultados[j+1][2]:
                if resultados[j][1] > resultados[j+1][1]:
                    resultados[j], resultados[j+1] = resultados[j+1], resultados[j]
    
    return resultados

def busqueda_binaria(resultados_ordenados, base_buscada, epsilon=0.001):
  
    # Filtrar solo los resultados válidos para la búsqueda
    resultados_validos = [r for r in resultados_ordenados if r[2]]
    if not resultados_validos:
        return -1
    izquierda, derecha = 0, len(resultados_validos) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        base_actual = resultados_validos[medio][1]
        # Comparación con margen de error para valores float
        if abs(base_actual - base_buscada) < epsilon:
            return medio
        elif base_actual < base_buscada:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1

def busqueda_lineal(resultados, condicion):
    encontrados = []
    for i, resultado in enumerate(resultados):
        if condicion(resultado):
            encontrados.append((i, resultado))
    return encontrados

def procesar_cuartetos(cuartetos):
    resultados = []
    validos = 0
    invalidos = 0
    for cuarteto in cuartetos:
        a, b, c, d = cuarteto
        suma = a + d
        producto = b * c
        # Medición de tiempo para comparar rendimiento
        inicio_iterativo = time.time()
        base_iterativa = calcular_base_iterativa(suma, producto)
        tiempo_iterativo = (time.time() - inicio_iterativo) * 1000  # ms
        inicio_recursivo = time.time()
        base_recursiva = calcular_base_recursiva(suma, producto)
        tiempo_recursivo = (time.time() - inicio_recursivo) * 1000  # ms
        # Usar la base calculada iterativamente para los resultados
        base = base_iterativa
        # Validación y conteo
        valido = base is not None
        if valido:
            validos += 1
        else:
            invalidos += 1
        # Guardar resultados
        resultados.append((cuarteto, base, valido, tiempo_iterativo, tiempo_recursivo))
        
        # Mostrar resultados
        print(f"\nCuarteto {cuarteto}:")
        print(f"  * Suma (a+d): {suma}")
        print(f"  * Producto (b*c): {producto}")
        
        if valido:
            print(f"  * Base calculada (iterativa): {base_iterativa:.4f} ({tiempo_iterativo:.4f} ms)")
            print(f"  * Base calculada (recursiva): {base_recursiva:.4f} ({tiempo_recursivo:.4f} ms)")
            print(f"  * Estado: VÁLIDO")
        else:
            if suma <= 0:
                print(f"  * Error: La suma debe ser positiva.")
            if producto <= 0:
                print(f"  * Error: El producto debe ser positivo.")
            print(f"  * Estado: INVÁLIDO")
    
    # Ordenar resultados
    resultados_ordenados = bubble_sort_cuartetos(resultados.copy())
    
    # Mostrar resultados ordenados
    print("\n===== RESULTADOS ORDENADOS POR BASE =====")
    for i, (cuarteto, base, valido, _, _) in enumerate(resultados_ordenados):
        if valido:
            print(f"{i+1}. Cuarteto {cuarteto} - Base: {base:.4f}")
    
    # Buscar una base específica
    print("\n===== BÚSQUEDA DE BASE ESPECÍFICA =====")
    base_buscada = 1.43  # Ejemplo
    resultados_validos = [r for r in resultados_ordenados if r[2]]
    indice = busqueda_binaria(resultados_ordenados, base_buscada)
    
    if indice != -1:
        cuarteto, base, _, _, _ = resultados_validos[indice]
        print(f"Buscando base cercana a {base_buscada}:")
        print(f"Encontrado en el índice {indice}: Cuarteto {cuarteto} - Base: {base:.4f}")
    else:
        print(f"No se encontró ningún cuarteto con base cercana a {base_buscada}")
    
    # Mostrar estadísticas finales
    print("\n===== ESTADÍSTICAS FINALES =====")
    total = len(cuartetos)
    print(f"Total de cuartetos procesados: {total}")
    print(f"Cuartetos válidos: {validos} ({validos/total*100:.1f}%)")
    print(f"Cuartetos inválidos: {invalidos} ({invalidos/total*100:.1f}%)")
    return resultados

# Datos de prueba
cuartetos_prueba = [
    [2, 4, 4, 3],      # Caso válido: a+d=5, b*c=16, base≈1.8193
    [1, 2, 3, 4],      # Caso válido: a+d=5, b*c=6, base≈1.4310
    [0, 0, 5, 2],      # Caso inválido: producto es cero
    [5, 3, 0, -5],     # Caso inválido: suma cero
]
# Ejecutar el programa con los datos de prueba
print("===== RESULTADOS DE CUARTETOS =====")
resultados = procesar_cuartetos(cuartetos_prueba)
