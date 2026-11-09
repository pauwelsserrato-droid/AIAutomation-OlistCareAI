# Pruebas y evidencias

## Plan de cinco ejecuciones

| Caso | Archivo | Camino | Resultado esperado |
|---|---|---|---|
| 01 | `01_demora_critica.json` | Feliz con aprobacion | IA procesa, Gmail solicita aprobacion y Gmail envia |
| 02 | `02_consulta_neutral.json` | HITL rechazado | IA procesa, el humano rechaza y no se contacta al cliente |
| 03 | `03_datos_incompletos.json` | Validacion | HTTP 400 y registro VALIDATION |
| 04 | `04_pedido_inexistente.json` | Pedido no encontrado | HTTP 202 inicial, alerta manual y registro ORDER_NOT_FOUND |
| 05 | `05_prevencion_bucle.json` | Anti loop | HTTP 400 y el flujo no vuelve a procesar su propia salida |

## Evidencias tecnicas incluidas

- `evidencias/01_arquitectura.png`: diagrama del ecosistema.
- `evidencias/02_modelo_datos.png`: relaciones de Airtable.
- `evidencias/03_workflow_n8n.png`: vista tecnica generada desde el JSON del flujo.

Estas imagenes prueban el diseno y la estructura del entregable. No sustituyen las capturas de una ejecucion real.

## Capturas reales incluidas

Las siguientes capturas estan guardadas en `evidencias/ejecucion-real/`:

1. `01_n8n_ejecucion_exitosa.png`: workflow completo, ejecucion exitosa e historial con mas de cinco pruebas.
2. `02_airtable_ticket_aprobado.png`: ticket procesado y aprobacion humana registrada en Airtable.
3. `03_gmail_aprobacion_humana.png`: correo HITL con resumen, borrador y enlaces de decision.
4. `04_airtable_error_log.png`: errores de validacion, IA y Gmail registrados para revision.

No se incluye una captura de una respuesta final recibida por el cliente porque ese mensaje no llego a la cuenta de prueba. El entregable no presenta evidencias simuladas.

Las capturas deben ocultar tokens, URLs privadas, correos reales y cualquier credencial.

## Registro de resultados

La captura `01_n8n_ejecucion_exitosa.png` muestra mas de cinco ejecuciones reales, incluida una ejecucion exitosa de extremo a extremo y varias pruebas fallidas utilizadas durante la configuracion. La evidencia de Airtable confirma tanto la aprobacion humana como el registro de errores. No se transcriben IDs que no hayan sido verificados directamente.
