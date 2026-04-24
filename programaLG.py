import os
import re

# ==========================================
# CONFIGURACIÓN DE ELEMENTOS DEL LENGUAJE
# ==========================================

# Instrucciones exclusivas del Equipo 5
INSTRUCCIONES_EQ5 = {
    "CBW", "CLC", "LODSB", "LODSW", "STOSB", "AAA", "POP", "IDIV", "INT", 
    "AND", "ADC", "LEA", "LES", "JNZ", "JZ", "LOOPNZ", "JGE", "JNA", "JNL", "JB"
}

REGISTROS = {
    "AL", "AH", "AX", "BL", "BH", "BX", "CL", "CH", "CX", "DL", "DH", "DX",
    "SI", "DI", "SP", "BP", "CS", "DS", "SS", "ES"
}

PSEUDOINSTRUCCIONES = {
    "DB", "DW", "DD", "DQ", "DT", "EQU", "ORG", "ASSUME", "MACRO", "ENDM",
    "PROC", "ENDP", "END", "SEGMENT", "ENDS", "INCLUDE"
}

# ==========================================
# FUNCIONES DE ANÁLISIS
# ==========================================

def clasificar_elemento(token):
    token_upper = token.upper()

    # 1. Elementos Compuestos
    compuestos_pseudo = [".CODE SEGMENT", ".DATA SEGMENT", ".STACK SEGMENT", "BYTE PTR", "WORD PTR"]
    if token_upper in compuestos_pseudo:
        return "Pseudoinstrucción (Compuesto)"
    
    if token.startswith('[') and token.endswith(']'):
        return "Direccionamiento / Memoria (Compuesto)"
    
    if token_upper.startswith('DUP(') and token.endswith(')'):
        return "Operador DUP (Compuesto)"
    
    if (token.startswith('"') and token.endswith('"')) or (token.startswith("'") and token.endswith("'")):
        return "Constante (Caracter/Cadena)"

    # 2. Instrucciones válidas (Solo Equipo 5)
    if token_upper in INSTRUCCIONES_EQ5:
        return "Instrucción"

    # 3. Registros
    if token_upper in REGISTROS:
        return "Registro"

    # 4. Pseudoinstrucciones estándar
    if token_upper in PSEUDOINSTRUCCIONES:
        return "Pseudoinstrucción"

    # 5. Constantes Numéricas
    if re.fullmatch(r'[01]+[bB]', token):
        return "Constante (Numérica Binaria)"
    
    if re.fullmatch(r'[0-9A-Fa-f]+[hH]', token):
        return "Constante (Numérica Hexadecimal)"
    
    if re.fullmatch(r'[0-9]+[dD]?', token):
        return "Constante (Numérica Decimal)"

    # 6. Símbolos (Variables, Etiquetas, e Instrucciones NO asignadas)
    # Un símbolo válido empieza con letra, _, @ o ? y sigue con letras/números
    if re.fullmatch(r'[a-zA-Z_@?][a-zA-Z0-9_@?]*', token):
        return "Símbolo"

    # 7. Elemento no identificado
    return "Elemento no identificado"

def procesar_archivo(ruta_archivo):
    elementos_encontrados = []

    # Expresión regular para separar elementos.
    # Prioriza los compuestos (no los separa) y luego toma bloques de texto que NO sean separadores (espacio, coma, dos puntos)
    patron = re.compile(
        r'(?i)\.code\s+segment|\.data\s+segment|\.stack\s+segment|byte\s+ptr|word\s+ptr|dup\([^)]*\)|\[[^\]]*\]|"[^"]*"|\'[^\']*\'|[^\s:,]+'
    )

    try:
        # A.3 Abrir para lectura
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            print(f"\n--- Contenido de {ruta_archivo} ---\n")
            
            for linea in archivo:
                # A.4 Desplegar el archivo línea por línea
                print(linea, end="")
                
                # Ignorar comentarios: cortar la línea en el primer ';'
                linea_sin_comentario = linea.split(';', 1)[0].strip()
                if not linea_sin_comentario:
                    continue
                
                # A.5 Leer y separar elementos
                tokens = patron.findall(linea_sin_comentario)
                for token in tokens:
                    # B.7 Identificación de elementos
                    tipo = clasificar_elemento(token)
                    elementos_encontrados.append((token, tipo))
            
            print("\n-----------------------------------\n")
            
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    # A.6 Desplegar paginado
    mostrar_paginado(elementos_encontrados)

def mostrar_paginado(elementos, tamaño_pagina=20):
    total = len(elementos)
    if total == 0:
        print("No se encontraron elementos válidos en el archivo.")
        return

    print("\n--- Lista de Elementos Analizados ---\n")
    for i in range(0, total, tamaño_pagina):
        pagina = elementos[i:i+tamaño_pagina]
        for idx, (token, tipo) in enumerate(pagina, start=i+1):
            # Formato tabulado: Número, Token, Tipo
            print(f"{idx:3d}. {token:<20} | {tipo}")
        
        if i + tamaño_pagina < total:
            input("\n[Presiona ENTER para ver la siguiente página...]")

# ==========================================
# MENÚ PRINCIPAL
# ==========================================
def main():
    print("=== Proyecto Ensamblador - Fase 1 (Análisis Lexicográfico) ===")
    print("=== Equipo 5 ===")
    
    while True:
        # A.1 Preguntar el archivo
        ruta = input("\nIngresa la ruta del archivo fuente (o 'salir' para terminar): ")
        
        if ruta.lower() == 'salir':
            break
            
        # A.2 Validar la existencia del archivo
        if not os.path.isfile(ruta):
            print("Error: El archivo no existe o la ruta es incorrecta. Intenta de nuevo.")
            continue
            
        procesar_archivo(ruta)

if __name__ == "__main__":
    main()
