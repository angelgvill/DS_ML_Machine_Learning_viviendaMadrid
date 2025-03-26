import pandas as pd

class Display(object):
    """Mostrar la representación HTML de varios objetos"""
    template = """<div style="float: left; padding: 10px;">
    <p style='font-family:"Courier New", Courier, monospace'>{0}</p>{1}
    </div>"""
    
    def __init__(self, *args, context=None):
        # Si no se pasa un contexto, se usa el entorno local por defecto
        if context is None:
            context = globals()
        
        # Convertir los nombres de variables a objetos reales si son cadenas
        self.args = [eval(a, context) if isinstance(a, str) else a for a in args]
        self.arg_names = [a if isinstance(a, str) else repr(a) for a in args]
        
    def _repr_html_(self):
        return '\n'.join(self.template.format(name, obj._repr_html_())
                         for name, obj in zip(self.arg_names, self.args))
    
    def __repr__(self):
        return '\n\n'.join(name + '\n' + repr(obj)
                           for name, obj in zip(self.arg_names, self.args))
    
def ini_inspec(df):
    # Tamaño y estructura de los datos
    print("=== TAMAÑO Y ESTRUCTURA DE LOS DATOS ===")
    print(f"Número total de registros (filas): {df.shape[0]}")
    print(f"Número de columnas: {df.shape[1]}")
    print(f"Uso de memoria: {df.memory_usage().sum() / 1024:.2f} KB")
    print("\n")

    # Tipos de datos y nombres de columnas
    print("=== TIPOS DE DATOS Y NOMBRES DE COLUMNAS ===")
    print(df.dtypes)
    print("\n")
    print("Información detallada del DataFrame:")
    print(df.info())
    print("\n")

    # Identificación de problemas iniciales
    print("=== IDENTIFICACIÓN DE PROBLEMAS INICIALES ===")
    print(f"Número de filas duplicadas: {df.duplicated().sum()}")
    print("\nValores nulos por columna:")
    print(df.isnull().sum())

    # Mostrar las primeras filas para verificar la estructura
    print("\nPrimeras filas del dataset:")
    print(df.head())

    # Mostrar las ultimas filas para verificar la estructura
    print("\nÚltimas filas del dataset:")
    print(df.tail(10))
    
def crear_tabla_resumen(df):
    resumen = []
    #quiero crear un nuevo df con las columnas como filas, 
    for col in df.columns:
        # Extraer la información de cada columna del DF original
        tipo_dato = df[col].dtype
        cardinalidad = df[col].nunique()

        if tipo_dato in ['object', 'string']:  # or df[col].nunique() < 10: #muy pocos vaores únicos
            categoria_dato = 'Categórica Nominal'
            if cardinalidad == 2:
                categoria_dato = 'Binaria'
        elif tipo_dato in ['int64','int32','int16','float64','float32','float16']:  # Columnas numéricas
            if cardinalidad == len(df):
                categoria_dato = 'Indice Numérico'
            else: 
                if df[col].dtype in ['float64', 'float32', 'float16']:
                    categoria_dato = 'Numérica Continua'
                else:
                    categoria_dato = 'Numérica Discreta'

        else:
            categoria_dato = 'Desconocida'        

        porcentaje_cardinalidad = (cardinalidad / len(df)) * 100

        valores_faltantes = df[col].isna().sum()
        porcentaje_valores_faltantes = (valores_faltantes / len(df)) * 100

        resumen.append({
            'Columna': col,
            'Tipo de dato': tipo_dato,
            'Categoría': categoria_dato,
            'Cardinalidad': cardinalidad,
            '% Cardinalidad': porcentaje_cardinalidad,
            'Valores faltantes': valores_faltantes,
            '% Valores faltantes': porcentaje_valores_faltantes,
            })

    #Convertir el resumen en un DataFrame
    resumen_df = pd.DataFrame(resumen)
    return resumen_df.set_index('Columna')


def numericas(df):
    resumen = []

    for col in df.columns:
        # Verificar si la columna es numérica
        if pd.api.types.is_numeric_dtype(df[col]):          #las columnas no numericas se omiten
            data = df[col].dropna()  # Ignorar valores NaN para los cálculos
            count = data.count()
            mean = data.mean()
            median = data.median()
            mode = data.mode().iloc[0] if not data.mode().empty else np.nan
            std = data.std()
            min_val = data.min()
            q25 = data.quantile(0.25)
            q50 = data.quantile(0.50)  # Igual a la mediana
            q75 = data.quantile(0.75)
            max_val = data.max()
            iqr = q75 - q25
            data_range = max_val - min_val
            variance = data.var()
            std_dev = std
            skewness = data.skew()
            kurtosis = data.kurtosis()
            missing = df[col].isna().sum()
            missing_percent = (missing / len(df)) * 100

            resumen.append({
                "columna": col,
                "count": count,
                "mean": mean,
                "median": median,
                "mode": mode,
                "std": std,
                "min": min_val,
                "25%": q25,
                "50%": q50,
                "75%": q75,
                "max": max_val,
                "iqr": iqr,
                "range": data_range,
                "variance": variance,
                "std_dev": std_dev,
                "skewness": skewness,
                "kurtosis": kurtosis,
                "missing": missing,
                "missing_percent": missing_percent
            })
    
    # Convertir el resumen en un DataFrame
    resumen_df = pd.DataFrame(resumen)
    return resumen_df.set_index("columna")



def categoricas(df):
    resumen = []

    for col in df.columns:
        # Verificar si la columna no es numérica
        if not pd.api.types.is_numeric_dtype(df[col]):
            count = df[col].count()
            unique = df[col].nunique()
            top = df[col].mode().iloc[0] if not df[col].mode().empty else np.nan
            freq = df[col].value_counts().iloc[0] if not df[col].value_counts().empty else np.nan
            missing = df[col].isna().sum()
            missing_percent = (missing / len(df)) * 100

            resumen.append({
                "columna": col,
                "count": count,
                "unique": unique,
                "top": top,
                "freq": freq,
                "missing": missing,
                "missing_percent": missing_percent
            })
    
    # Convertir el resumen en un DataFrame
    resumen_df = pd.DataFrame(resumen)
    return resumen_df.set_index("columna")



#FUNCIONES ESPECÍFICA DEL TRABAJO EN DATASET IDEALISTA

#FUNCIÓN PARA EXPANDIR CELDAS CON CONTENIDO DICCIONARIOS
def expand_dict_columns(df):
    """
    Expande las columnas del dataframe de Idealista que contienen diccionarios.
    
    Parámetros:
    df (pandas.DataFrame): DataFrame con datos de Idealista
    
    Retorna:
    pandas.DataFrame: DataFrame con las columnas expandidas
    """
    # Hacer una copia del dataframe original para no modificarlo
    df_processed = df.copy()
    
    def parse_dict_safely(value):
        """Convierte strings a diccionarios de forma segura sin usar ast"""
        if pd.isna(value):
            return {}
        if isinstance(value, dict):
            return value
        if isinstance(value, str) and value.strip():
            try:
                # Intentar convertir usando json.loads
                return json.loads(value)
            except json.JSONDecodeError:
                try:
                    # Si falla, corregimos comillas simples a dobles
                    value = value.replace("'", "\"")
                    return json.loads(value)
                except json.JSONDecodeError:
                    # Si aún falla, retornar vacío
                    return {}
        return {}
    
    def process_column(column_name, field_mappings):
        """
        Procesa una columna de diccionario y extrae campos específicos.
        
        Parámetros:
        column_name (str): Nombre de la columna a procesar
        field_mappings (dict): Diccionario donde la clave es el nombre del campo 
                               a extraer y el valor es un valor por defecto
        """
        if column_name not in df_processed.columns:
            return
            
        # Convertir strings a diccionarios
        df_processed[column_name] = df_processed[column_name].apply(parse_dict_safely)
        
        # Extraer cada campo del diccionario
        for field, default_value in field_mappings.items():
            new_column_name = f"{column_name}_{field}"
            df_processed[new_column_name] = df_processed[column_name].apply(
                lambda x: x.get(field, default_value) if isinstance(x, dict) else default_value
            )
    
    # Definir los campos a extraer para cada columna
    column_fields = {
        'suggestedTexts': {'subtitle': None, 'title': None},
        'detailedType': {'typology': None, 'subTypology': None},
        'parkingSpace': {
            'hasParkingSpace': False, 
            'isParkingSpaceIncludedInPrice': None,
            'parkingSpacePrice': None
        }
    }
    
    # Procesar cada columna
    for column, fields in column_fields.items():
        process_column(column, fields)
    
    # Eliminar las columnas originales
    columns_to_drop = [col for col in column_fields.keys() if col in df_processed.columns]
    df_processed = df_processed.drop(columns=columns_to_drop)
    
    return df_processed


# Función para detectar si hay mención de terraza según los patrones
def tiene_terraza(texto):
    # Crear patrones de regex para buscar terrazas
    patrones_terraza = [
        r', terraza,', 
        r'la terraza', 
        r'doble terraza',
        r'balcón/ terraza', 
        r'balcón/terraza',
        r'con terraza',
        r'magnifica terraza',
        r'amplia terraza',
        r'gran terraza',
        r'grandes terrazas',
        r'terraza privada',
        r'una terraza',
        r'dos terrazas',
        r'terraza de \d+ metros',
        r'terraza de \d+ m2'
        ]
    # Combinar todos los patrones en una sola expresión regular
    patron_combinado = '|'.join(patrones_terraza)
        
    if pd.isna(texto):
        return 0
    # Convertir a minúsculas para hacer la búsqueda insensible a mayúsculas
    texto = texto.lower()
    return 1 if re.search(patron_combinado, texto) else 0

def imputar_floor(dataframe):
    """
    Imputa valores en la columna 'floor' basándose en palabras clave encontradas en la columna 'description'
    para las filas donde 'floor' es NaN.

    :param dataframe: DataFrame que debe contener las columnas 'floor' y 'description'.
    :return: DataFrame con los valores imputados en 'floor'.
    """
    # Diccionario que mapea palabras clave a valores de 'floor'
    floor_mapping = {
        1: ['1º', '1ª', 'primer piso', 'piso primero', 'planta primera', 'primera planta'],
        2: ['2º', '2ª', 'segundo piso', 'piso segundo', 'planta segunda', 'segunda planta'],
        3: ['3º', '3ª', 'tercer piso', 'piso tercero', 'tercera planta'],
        4: ['4º', '4ª', 'cuarto piso', 'cuarta planta'],
        5: ['5º', '5ª', 'quinto piso', 'quinta planta'],
        6: ['6º', '6ª','sexto piso', 'sexta planta']
    }

    # Filtrar las filas donde 'floor' es NaN
    filtro = dataframe[dataframe['floor'].isnull()]

    # Iterar sobre el filtro para verificar palabras clave
    for index, row in filtro.iterrows():
        descripcion = str(row['description']).lower()  # Convertir a minúsculas
        for floor, keywords in floor_mapping.items():
            # Verificar si alguna palabra clave está en la descripción
            if any(keyword in descripcion for keyword in keywords):
                dataframe.at[index, 'floor'] = floor  # Asignar el valor correspondiente
                break  # Romper el bucle después de encontrar una coincidencia

    return dataframe


