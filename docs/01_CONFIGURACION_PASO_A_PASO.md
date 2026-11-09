# Configuracion paso a paso de OlistCare AI

## 1 Preparar Airtable

1. Crear una base llamada `OlistCare AI`.
2. Crear las tablas y campos exactamente como aparecen en `02_MODELO_DATOS_AIRTABLE.md`.
3. Importar los CSV de `airtable/templates`.
4. Convertir los campos de relacion indicados en campos **Link to another record**.
5. Crear una vista compartida de solo lectura y copiar su enlace en `ENLACES_ENTREGA.md`.
6. Crear un Personal Access Token con acceso a esta base y permisos de lectura y escritura de registros.

Los nombres de tablas y campos se usan desde el JSON de n8n. Si se renombran, hay que actualizar las URL y los cuerpos de los nodos HTTP.

## 2 Preparar el modelo de IA con OpenRouter

1. Crear una API key de OpenRouter.
2. Guardarla en una credencial **Header Auth** de n8n; nunca escribirla dentro del workflow.
3. Seleccionar un modelo gratuito disponible y limitar `max_tokens` para controlar el consumo.
4. Mantener el prompt dinamico y solicitar una respuesta JSON estructurada.

El flujo usa `POST https://openrouter.ai/api/v1/chat/completions`. El prompt completo se documenta en `05_PROMPT_IA.md`.

## 3 Preparar Gmail y la aprobacion humana

La version entregada llama a Gmail API para poder incluir `threadId`.

1. Crear un proyecto en Google Cloud.
2. Habilitar Gmail API.
3. Configurar OAuth 2.0 con el alcance `gmail.send`.
4. Para la demo, crear una credencial **Bearer Auth** de n8n con el access token temporal.
5. Configurar `GMAIL_FROM` y `APPROVAL_EMAIL` fuera del workflow.
6. Para produccion, usar una credencial OAuth2 renovable en vez de un token temporal.

Gmail envia al aprobador un resumen, el borrador y dos enlaces construidos con `$execution.resumeUrl`. El nodo Wait conserva la ejecucion hasta recibir la decision.

## 4 Importar y configurar n8n

1. Importar `n8n/02_OlistCare_AI_Error_Handler.json`.
2. Importar `n8n/01_OlistCare_AI_Principal.json`.
3. Abrir el workflow principal y revisar que todos los nodos se visualicen sin advertencias de version.
4. En **Settings > Error workflow**, seleccionar `OlistCare AI - Error Handler`.
5. Definir las variables de `config/.env.example` en el entorno de la instancia.
6. Guardar y activar primero el manejador de errores y luego el flujo principal.
7. Copiar la URL de produccion del nodo `01 Trigger Webhook Ticket`.

## 5 Probar el flujo

Ejecutar desde PowerShell:

```powershell
.\scripts\test_webhook.ps1 -WebhookUrl "https://TU-N8N/webhook/olistcare-ticket"
```

El script envia cinco casos. Los resultados esperados se encuentran en `tests/RESULTADOS_ESPERADOS.md`.

## 6 Demostrar el HITL

1. Enviar el caso 01.
2. Mostrar la ejecucion en estado **Waiting**.
3. Abrir Airtable y mostrar el ticket con estado `Procesado por IA`.
4. Abrir el correo de aprobacion y pulsar el enlace **APROBAR**.
5. Volver a n8n y mostrar que el flujo se reanudo.
6. Mostrar el correo enviado y el ticket con estado `Respondido`.

Repetir con el caso 02 y pulsar **Rechazar** para demostrar que Gmail no se ejecuta.

## 7 Preparar la entrega

1. Completar `docs/ENLACES_ENTREGA.md`.
2. Agregar las capturas reales indicadas en `docs/03_PRUEBAS_Y_EVIDENCIAS.md`.
3. Grabar el video con el guion de `docs/04_GUION_VIDEO_3_MIN.md`.
4. Ejecutar el checklist de `docs/06_CHECKLIST_ENTREGA.md`.
5. Confirmar que ningun secreto aparezca en archivos, capturas o historial de Git.
