# Resultados esperados de las pruebas

## Caso 01 demora critica

- El webhook responde 202.
- Airtable encuentra `OLIST-1001`.
- El modelo clasifica el caso como `alta` o `critica`.
- Se crea el ticket con estado `Procesado por IA`.
- La ejecucion espera aprobacion.
- Al aprobar, Gmail envia y Airtable cambia a `Respondido`.

## Caso 02 consulta neutral

- El webhook responde 202.
- Se crea el borrador y se envia el correo de aprobacion.
- Al rechazar, el ticket cambia a `Rechazado por Humano`.
- Gmail no se ejecuta.

## Caso 03 datos incompletos

- El webhook responde 400.
- Se guarda un error `VALIDATION`.
- IA, Wait y Gmail no se ejecutan.

## Caso 04 pedido inexistente

- El webhook responde 202 porque la recepcion fue asincrona.
- La busqueda de Airtable devuelve cero registros.
- Se guarda `ORDER_NOT_FOUND` para revision.
- IA y Gmail no se ejecutan.

## Caso 05 prevencion de bucle

- El webhook responde 400.
- La validacion identifica `automation_source=olistcare_ai`.
- El mensaje no vuelve a entrar en el circuito de IA.
