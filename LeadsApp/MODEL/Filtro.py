class Filtro:
    def __init__(self, nombre, campo):
        self.nombre = nombre
        self.campo = campo


class Filtro_Float(Filtro):
    def __init__(self, campo, maximo, minimo):
        super().__init__(f"{campo} de {str(minimo)} a {str(maximo)}", campo)
        self.maximo = maximo
        self.minimo = minimo

    def obtener_datos_filtrados(self, df):
        return df.loc[(df[self.campo] >= self.minimo) & (df[self.campo] <= self.maximo)]


class Filtro_Date(Filtro):
    def __init__(self, campo, maximo, minimo):
        super().__init__(f"{campo} de {str(minimo)} a {str(maximo)}", campo)
        # self.maximo = np.datetime64(maximo.utcnow()).astype(datetime)#¿Por qué? Pandas es datetime64 y DateEntry es date
        # self.minimo = np.datetime64(minimo.utcnow()).astype(datetime)
        self.maximo = maximo
        self.minimo = minimo

    def obtener_datos_filtrados(self, df):
        print(self.minimo, self.maximo)
        return df.loc[(df[self.campo] >= self.minimo) & (df[self.campo] <= self.maximo)]


class Filtro_Valores(Filtro):
    def __init__(self, campo, lista_de_valores):
        str_valores = str(lista_de_valores)
        str_valores = str_valores.replace("[", "")
        str_valores = str_valores.replace("]", "")
        super().__init__(f"{campo} en: {str_valores}", campo)
        self.lista_de_valores = lista_de_valores

    def obtener_datos_filtrados(self, df):  # ¿Cómo se obtiene un filtro en pandas?
        return df.loc[df[self.campo].isin(self.lista_de_valores)]


class Filtro_Valor(Filtro):
    def __init__(self, campo, valor):
        super().__init__(f"{campo} contiene: {valor}", campo)  # el parámetro campo lo metemos a mano con el f str
        self.valor = valor

    def obtener_datos_filtrados(self, df):  # ¿Cómo se obtiene un filtro en pandas?
        # print(f"campo: {self.campo}")
        # print(f"valor: {self.valor}")
        # print(df[self.campo])
        try:
            df["auxiliar"] = [",".join(map(str, l)).lower() for l in
                              df[self.campo]]  # map nos aseguramos que un str cada elemento de la lista


        except TypeError:  # Si no es lista
            print("Estamos en el except")
            df["auxiliar"] = [str(l).lower() for l in
                              df[self.campo]]  # Aquí ya sería un str y lo pasamos a lower y en el try es una lista
        return df.loc[df["auxiliar"].str.contains(self.valor.lower())].drop(["auxiliar"],
                                                                            axis=1)  # axis 1 quita columnas en lugar de filas
