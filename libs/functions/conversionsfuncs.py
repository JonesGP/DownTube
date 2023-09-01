import datetime
class ConversionsFuncs:
    def formtimeseg(self, time):
        segundos = time
        horas, resto = divmod(segundos, 3600)
        minutos, segundos = divmod(resto, 60)
        formated_time = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        return formated_time
    
    def viewsconv(self, views):
        if views >= 1000000000:
            return f"{int(views / 1000000000)} BI"
        elif views >= 1000000:
            return f"{int(views / 1000000)} MI"
        elif views >= 1000:
            return f"{int(views / 1000)} mil"
        else:
            return f"{views}"
    
    def dateconv(self, date):
        date = str(date)[:10]
        data = datetime.datetime.strptime(date, '%Y-%m-%d')
        dias = (datetime.datetime.now() - data).days
        if dias > 365:
            return f"{dias // 365} anos atrás"
        elif dias > 31:
            return f"{dias // 30} meses atrás"
        elif dias > 13:
            semanas = dias // 7
            return f"{semanas} semanas atrás"
        elif dias > 1:
            return f"{dias} dias atrás"
        elif dias == 1:
            return "Ontem"
        else:
            return "Hoje"