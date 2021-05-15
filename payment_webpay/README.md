Por favor migrar a https://gitlab.com/dansanti/payment_webpay

# Pasarela de pagos Webpay para Odoo

- Nos basamos en **payment_paypal** y **payment_ogone**
- Funcional
- Falta Opción anular venta(devolver venta)
- Falta Opción captura diferida

## Instalación

Se deben instalar las librería:

    pip3 install transbank-sdk

## Ejemplo de uso

- Los datos de certificación ya van integrados, no es necesario ingresarlos
- Toda Información está la siguiente URL [https://www.transbankdevelopers.cl/?m=sdk](https://www.transbankdevelopers.cl/?m=sdk)

Ejemplo datos de uso:

### Pago Exitoso

```
Dato 	                    Valor
N° Tarjeta de Crédito 	    4051885600446623
Año de Expiración 	        Cualquiera
Mes de Expiración 	        Cualquiera
CVV 	                    123
```

En la simulación del banco usar:
```
Rut 	                    11.111.111-1
Clave 	                    123
```

### Pago Rechazado

```
Dato 	                    Valor
N° Tarjeta de Crédito 	    5186059559590568
Año de Expiración 	        Cualquiera
Mes de Expiración 	        Cualquiera
CVV 	                    123
```

En la simulación del banco usar:
```
Rut 	                    11.111.111-1
Clave 	                    123
```
