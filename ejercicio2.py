def pedir_texto(mensaje):
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato.title()
        print("-> El texto no puede estar vacío.")


def pedir_entero(mensaje, minimo, maximo):
    while True:
        try:
            dato = int(input(mensaje))

            if minimo <= dato <= maximo:
                return dato

            print(f"Escriba un número entre {minimo} y {maximo}")

        except ValueError:
            print("Debe escribir un número entero.")


def pedir_dinero(mensaje, minimo, maximo):
    return pedir_entero(mensaje, minimo, maximo)


def pedir_si_no(mensaje):
    while True:
        respuesta = input(mensaje + " (S/N): ").strip().upper()

        if respuesta in ["S", "N"]:
            return respuesta == "S"

        print("Responda S o N.")


def pedir_datos():
    print("\nSOLICITUD DE CRÉDITO DE LIBRE INVERSIÓN")

    nombre = pedir_texto("Nombre completo: ")

    tipo_documento = input(
        "Tipo de documento (CC/CE/PA): "
    ).strip().upper()

    while tipo_documento not in ["CC", "CE", "PA"]:
        print("Opciones válidas: CC, CE, PA")
        tipo_documento = input(
            "Tipo de documento: "
        ).strip().upper()

    while True:
        documento = input(
            "Número de documento (6 a 10 dígitos): "
        ).strip()

        if documento.isdigit() and 6 <= len(documento) <= 10:
            break

        print("Escriba entre 6 y 10 dígitos, sin puntos.")

    edad = pedir_entero("Edad (18 a 75 años): ", 18, 75)

    ciudad = pedir_texto("Ciudad: ")

    contrato = input(
        "Contrato (INDEFINIDO/FIJO/SERVICIOS/INDEPENDIENTE): "
    ).strip().upper()

    while contrato not in [
        "INDEFINIDO",
        "FIJO",
        "SERVICIOS",
        "INDEPENDIENTE"
    ]:
        print("Tipo de contrato no válido.")
        contrato = input(
            "Tipo de contrato: "
        ).strip().upper()

    antiguedad = pedir_entero(
        "Antigüedad laboral en meses: ",
        0,
        600
    )

    salario = pedir_dinero(
        "Salario mensual: ",
        1,
        100_000_000
    )

    otros = pedir_dinero(
        "Otros ingresos mensuales: ",
        0,
        100_000_000
    )

    deudas = pedir_dinero(
        "Deudas mensuales: ",
        0,
        100_000_000
    )

    reportado = pedir_si_no(
        "¿Está reportado en centrales de riesgo?"
    )

    monto_solicitado = pedir_dinero(
        "Monto solicitado ($1.000.000 a $50.000.000): ",
        1_000_000,
        50_000_000
    )

    while True:
        plazo = pedir_entero(
            "Plazo en meses (6 a 72): ",
            6,
            72
        )

        if plazo % 6 == 0:
            break

        print("El plazo debe ser múltiplo de 6.")

    return {
        "nombre": nombre,
        "tipo_documento": tipo_documento,
        "documento": documento,
        "edad": edad,
        "ciudad": ciudad,
        "contrato": contrato,
        "antiguedad": antiguedad,
        "salario": salario,
        "otros": otros,
        "deudas": deudas,
        "reportado": reportado,
        "monto": monto_solicitado,
        "plazo": plazo
    }
def calcular_cuota(monto, tasa, plazo):
    return monto * (1 + tasa * plazo / 12) / plazo
    
def mostrar_tabla(monto, tasa, plazo):
    capital_mes = monto / plazo
    interes_mes = monto * tasa / 12
    cuota = capital_mes + interes_mes

    saldo = monto

    print("\nTABLA DE AMORTIZACIÓN")
    print("Mes | Cuota | Capital | Interés | Saldo")

    for mes in range(1, plazo + 1):

        saldo -= capital_mes

        if mes == plazo:
            saldo = 0

        print(
            f"{mes:2} | "
            f"${cuota:,.0f} | "
            f"${capital_mes:,.0f} | "
            f"${interes_mes:,.0f} | "
            f"${saldo:,.0f}"
        )    

def main():

    datos = pedir_datos()

    tasas = {
        "INDEFINIDO": 0.18,
        "FIJO": 0.22,
        "SERVICIOS": 0.26,
        "INDEPENDIENTE": 0.30
    }

    puntos_contrato = {
        "INDEFINIDO": 20,
        "FIJO": 15,
        "SERVICIOS": 10,
        "INDEPENDIENTE": 5
    }

    tasa = tasas[datos["contrato"]]

    ingresos = datos["salario"] + datos["otros"]

    capacidad = 0.40 * (ingresos - datos["deudas"])

    cuota = calcular_cuota(
        datos["monto"],
        tasa,
        datos["plazo"]
    )

    print("\nRESUMEN")
    print("Solicitante:", datos["nombre"])
    print(f"Ingresos totales: ${ingresos:,.0f}")
    print(f"Capacidad de pago: ${capacidad:,.0f}")
    print(f"Tasa anual: {tasa:.0%}")
    print(f"Cuota estimada: ${cuota:,.0f}")

    if (
        datos["reportado"]
        or datos["antiguedad"] < 6
        or capacidad <= 0
    ):

        print("\nCRÉDITO RECHAZADO: no cumple una condición básica.")

        if datos["reportado"]:
            print("- Está reportado en centrales de riesgo.")

        if datos["antiguedad"] < 6:
            print("- Tiene menos de 6 meses de antigüedad laboral.")

        if capacidad <= 0:
            print("- Su capacidad de pago es negativa o nula.")

        return

    puntos_antiguedad = (
        min(datos["antiguedad"] / 36, 1) * 30
    )

    relacion = cuota / ingresos if ingresos > 0 else 1

    puntos_relacion = max(
        0,
        30 * (1 - relacion)
    )

    puntos_edad = (
        20 if 25 <= datos["edad"] <= 55
        else 10
    )

    puntaje = (
        puntos_antiguedad
        + puntos_relacion
        + puntos_contrato[datos["contrato"]]
        + puntos_edad
    )

    print(f"\nPuntaje de riesgo: {puntaje:.1f}/100 puntos")

    if puntaje < 60:
        print("CRÉDITO RECHAZADO: puntaje menor a 60.")
        return

    aprobado = datos["monto"]

    while aprobado >= 1_000_000:

        if (
            calcular_cuota(
                aprobado,
                tasa,
                datos["plazo"]
            )
            <= capacidad
        ):
            break

        if aprobado == 1_000_000:
            aprobado = 0
            break

        aprobado -= 500_000

    if aprobado == 0:

        print(
            "CRÉDITO RECHAZADO: "
            "no alcanza para el monto mínimo."
        )

    elif aprobado == datos["monto"]:

        print(
            f"\nCRÉDITO APROBADO "
            f"por ${aprobado:,.0f}"
        )

        mostrar_tabla(
            aprobado,
            tasa,
            datos["plazo"]
        )

    else:

        print(
            f"\nSe solicitó "
            f"${datos['monto']:,.0f}"
        )

        print(
            f"CRÉDITO APROBADO "
            f"por un monto menor: "
            f"${aprobado:,.0f}"
        )

        print(
            f"Nueva cuota: "
            f"${calcular_cuota(aprobado, tasa, datos['plazo']):,.0f}"
        )

        mostrar_tabla(
            aprobado,
            tasa,
            datos["plazo"]
        )


if __name__ == "__main__":
    main()
