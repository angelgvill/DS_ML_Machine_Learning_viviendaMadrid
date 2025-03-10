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





