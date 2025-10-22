import pandas as pd
from math import comb
import os

def calcular_formula_1(E, N, I):
    """
    Formula 1: [(E-N) choose (I-N)] / [E choose I] * 100
    """
   
    k_numerador = I - N
    k_denominador = I
    
    
    if k_numerador < 0 or k_denominador < 0:
        return None, "Partida no valida"
    
    
    if (E - N) < k_numerador or E < k_denominador:
        return None, "Partida no valida"
    
    try:
        
        numerador = comb(E - N, k_numerador)
        denominador = comb(E, k_denominador)
        
        if denominador == 0:
            return None, "Partida no valida"
        

        resultado = (numerador / denominador) * 100
        return round(resultado, 6), "Valida"
    
    except (ValueError, ZeroDivisionError):
        return None, "Partida no valida"

def calcular_formula_2(E, N, I):
    """
    Formula 2: [(E-N+1) choose (I-N)] / [E choose (I-1)] * 100
    """
    
    k_numerador = I - N
    k_denominador = I - 1
    
    
    if k_numerador < 0 or k_denominador < 0:
        return None, "Partida no valida"
    
    
    if (E - N + 1) < k_numerador or E < k_denominador:
        return None, "Partida no valida"
    
    try:
        
        numerador = comb(E - N + 1, k_numerador)
        denominador = comb(E, k_denominador)
        
        if denominador == 0:
            return None, "Partida no valida"
        
        
        resultado = (numerador / denominador) * 100
        return round(resultado, 6), "Valida"
    
    except (ValueError, ZeroDivisionError):
        return None, "Partida no valida"

def generar_tabla_comparativa():
    
    E_min, E_max = 5, 20
    N_min, N_max = 1, 8
    I_min, I_max = 1, 15
    
    
    datos = []
    
    print("Generando calculos comparativos...")
    contador_total = 0
    contador_validos = 0
    contador_invalidos = 0
    
    
    for E in range(E_min, E_max + 1):
        for N in range(N_min, min(N_max + 1, E + 1)):
            for I in range(I_min, min(I_max + 1, E + 1)):
                contador_total += 1
                
                
                k1_f1 = I - N
                k2_f1 = I
                k1_f2 = I - N
                k2_f2 = I - 1
                
                
                valor_f1, estado_f1 = calcular_formula_1(E, N, I)
                valor_f2, estado_f2 = calcular_formula_2(E, N, I)
                
                
                partida_valida = (estado_f1 == "Valida" and estado_f2 == "Valida")
                
                
                if estado_f1 == "Valida":
                    display_f1 = valor_f1
                else:
                    display_f1 = estado_f1
                
                if estado_f2 == "Valida":
                    display_f2 = valor_f2
                else:
                    display_f2 = estado_f2
                
                
                datos_base = {
                    'E': E,
                    'N': N,
                    'I': I,
                    'E-N': E - N,
                    'I-N': I - N,
                    'E-N+1': E - N + 1,
                    'I-1': I - 1,
                    'K1_F1': k1_f1,
                    'K2_F1': k2_f1,
                    'K1_F2': k1_f2,
                    'K2_F2': k2_f2,
                    'Formula_1 (%)': display_f1,
                    'Formula_2 (%)': display_f2,
                    'Estado_F1': estado_f1,
                    'Estado_F2': estado_f2,
                    'Partida_Valida': partida_valida
                }
                
                if partida_valida:
                    contador_validos += 1
                    
                    if valor_f1 > valor_f2:
                        mayor = "Formula 1"
                    elif valor_f2 > valor_f1:
                        mayor = "Formula 2"
                    else:
                        mayor = "Iguales"
                    
                    
                    diferencia = round(abs(valor_f1 - valor_f2), 6)
                    
                    datos.append({
                        **datos_base,
                        'Diferencia': diferencia,
                        'Mayor_Probabilidad': mayor
                    })
                else:
                    contador_invalidos += 1
                    
                    datos.append({
                        **datos_base,
                        'Diferencia': "N/A",
                        'Mayor_Probabilidad': "Partida no valida"
                    })
    
    
    df = pd.DataFrame(datos)
    
    
    df = df.sort_values(['E', 'N', 'I']).reset_index(drop=True)
    
    
    nombre_archivo = 'tabla_completa_partidas.xlsx'
    try:
        df.to_excel(nombre_archivo, index=False, engine='openpyxl')
        print("Tabla completa guardada en '" + nombre_archivo + "'")
    except ImportError:
        nombre_archivo = 'tabla_completa_partidas.csv'
        df.to_csv(nombre_archivo, index=False)
        print("Tabla completa guardada en '" + nombre_archivo + "'")
    
    
    df_validas = df[df['Partida_Valida'] == True].copy()
    if len(df_validas) > 0:
        nombre_archivo_validas = 'partidas_validas.xlsx'
        try:
            df_validas.to_excel(nombre_archivo_validas, index=False, engine='openpyxl')
            print("Partidas validas guardadas en '" + nombre_archivo_validas + "'")
        except ImportError:
            nombre_archivo_validas = 'partidas_validas.csv'
            df_validas.to_csv(nombre_archivo_validas, index=False)
            print("Partidas validas guardadas en '" + nombre_archivo_validas + "'")
    
    
    print("\n" + "="*60)
    print("RESUMEN ESTADISTICO")
    print("="*60)
    
    print("Total de combinaciones analizadas: " + str(contador_total))
    print("Partidas validas: " + str(contador_validos) + " (" + str(round(contador_validos/contador_total*100, 1)) + "%)")
    print("Partidas no validas: " + str(contador_invalidos) + " (" + str(round(contador_invalidos/contador_total*100, 1)) + "%)")
    
    
    if contador_invalidos > 0:
        df_invalidas = df[df['Partida_Valida'] == False]
        
        print("\n" + "="*50)
        print("ANALISIS DE PARTIDAS NO VALIDAS")
        print("="*50)
        
        
        k1_f1_neg = len(df_invalidas[df_invalidas['K1_F1'] < 0])
        k2_f1_neg = len(df_invalidas[df_invalidas['K2_F1'] < 0])
        k1_f2_neg = len(df_invalidas[df_invalidas['K1_F2'] < 0])
        k2_f2_neg = len(df_invalidas[df_invalidas['K2_F2'] < 0])
        
        print("Razones de partidas no validas:")
        print("K1_F1 (I-N) negativo: " + str(k1_f1_neg) + " casos")
        print("K2_F1 (I) negativo: " + str(k2_f1_neg) + " casos")
        print("K1_F2 (I-N) negativo: " + str(k1_f2_neg) + " casos")
        print("K2_F2 (I-1) negativo: " + str(k2_f2_neg) + " casos")
        
        
        print("\nEjemplos de partidas no validas:")
        ejemplos = df_invalidas.head(5)[['E', 'N', 'I', 'K1_F1', 'K2_F1', 'K1_F2', 'K2_F2', 'Formula_1 (%)', 'Formula_2 (%)']]
        print(ejemplos.to_string(index=False))
    
    
    if contador_validos > 0:
        print("\n" + "="*50)
        print("ANALISIS DE PARTIDAS VALIDAS")
        print("="*50)
        
        
        casos_f1 = len(df_validas[df_validas['Mayor_Probabilidad'] == 'Formula 1'])
        casos_f2 = len(df_validas[df_validas['Mayor_Probabilidad'] == 'Formula 2'])
        casos_iguales = len(df_validas[df_validas['Mayor_Probabilidad'] == 'Iguales'])
        
        print("Distribucion de mayor probabilidad en partidas validas:")
        print("- Formula 1 mayor: " + str(casos_f1) + " (" + str(round(casos_f1/contador_validos*100, 1)) + "%)")
        print("- Formula 2 mayor: " + str(casos_f2) + " (" + str(round(casos_f2/contador_validos*100, 1)) + "%)")
        print("- Iguales: " + str(casos_iguales) + " (" + str(round(casos_iguales/contador_validos*100, 1)) + "%)")

        print("\nPrimeras 10 partidas validas:")
        columnas_muestra = ['E', 'N', 'I', 'Formula_1 (%)', 'Formula_2 (%)', 'Diferencia', 'Mayor_Probabilidad']
        print(df_validas[columnas_muestra].head(10).to_string(index=False))
        
    return df


if __name__ == "__main__":
    print("COMPARADOR DE PROBABILIDADES COMBINATORIAS")
    print("="*50)
    print("Formula 1: C(E-N, I-N) / C(E, I) * 100")
    print("Formula 2: C(E-N+1, I-N) / C(E, I-1) * 100")
    print("="*50)
    df_completa = generar_tabla_comparativa()