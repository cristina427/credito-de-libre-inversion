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

def main():

    datos = pedir_datos()

    print("\nSOLICITUD RECIBIDA")

    ingresos = datos["salario"] + datos["otros"]

    print(f"Ingresos totales: ${ingresos:,.0f}")



if __name__ == "__main__":
    main()
