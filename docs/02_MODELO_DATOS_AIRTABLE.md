# Modelo de datos de Airtable

La base funciona como memoria del sistema. Se usan cuatro tablas relacionadas para evitar registros aislados.

## Customers

| Campo | Tipo | Uso |
|---|---|---|
| customer_id | Single line text, primario | Identificador de negocio |
| full_name | Single line text | Nombre del cliente |
| email | Email | Direccion de contacto |
| segment | Single select | Standard, Plus o VIP |
| consent_contact | Checkbox | Consentimiento de contacto |
| Orders | Link to Orders | Pedidos del cliente |
| Tickets | Link to Tickets | Historial de soporte |

## Orders

| Campo | Tipo | Uso |
|---|---|---|
| order_id | Single line text, primario | Identificador del pedido |
| Customer | Link to Customers | Propietario del pedido |
| order_status | Single select | shipped, delivered, canceled, processing |
| estimated_delivery | Date | Fecha prometida |
| last_tracking_event | Long text | Ultimo evento logistico |
| carrier | Single line text | Transportista |
| order_total | Currency | Monto del pedido |
| Tickets | Link to Tickets | Reclamos asociados |

## Tickets

| Campo | Tipo | Uso |
|---|---|---|
| ticket_id | Single line text, primario | Identificador del ticket |
| Customer | Link to Customers | Cliente relacionado |
| Order | Link to Orders | Pedido relacionado |
| customer_email | Email | Email recibido |
| message | Long text | Consulta original |
| status | Single select | Pendiente, Procesado por IA, Aprobado por Humano, Rechazado por Humano, Respondido, Error |
| priority | Single select | baja, media, alta, critica |
| sentiment | Single select | positivo, neutral, frustrado, enojado |
| category | Single select | demora, seguimiento, cancelacion, reembolso, otro |
| ai_summary | Long text | Resumen del caso |
| ai_draft_reply | Long text | Borrador de respuesta |
| needs_human_review | Checkbox | Control HITL |
| approved_by | Single line text | Aprobador |
| approved_at | Date with time | Momento de aprobacion |
| gmail_thread_id | Single line text | Hilo original de Gmail |
| gmail_message_id | Single line text | Mensaje enviado |
| created_at | Created time | Alta del registro |
| processed_at | Date with time | Fin del proceso |

## Error Logs

| Campo | Tipo | Uso |
|---|---|---|
| error_id | Formula o autonumber | Identificador |
| workflow | Single line text | Workflow de origen |
| execution_id | Single line text | Ejecucion de n8n |
| node | Single line text | Nodo que fallo |
| error_type | Single select | VALIDATION, ORDER_NOT_FOUND, OPENAI_API, GMAIL_API, UNHANDLED |
| message | Long text | Detalle sin secretos |
| ticket_id | Single line text | Ticket afectado |
| payload_excerpt | Long text | Fragmento depurado |
| created_at | Created time | Fecha del incidente |
| resolved | Checkbox | Estado operativo |

## Relaciones

```text
Customers 1 ---- N Orders
Customers 1 ---- N Tickets
Orders    1 ---- N Tickets
Tickets   1 ---- N Error Logs (por ticket_id o enlace opcional)
```

En la primera importacion, Airtable puede crear las columnas de los CSV como texto. Luego hay que convertir `Customer`, `Order`, `Orders` y `Tickets` en campos relacionados. La referencia completa tambien esta disponible en `airtable/schema_reference.json`.
