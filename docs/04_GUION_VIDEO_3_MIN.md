# Guion para video demo de 3 minutos

## 0 00 a 0 25 Contexto

Mostrar la portada del repositorio y decir:

> OlistCare AI automatiza el triage de reclamos por entregas. Integra n8n, Airtable, un modelo de IA mediante OpenRouter y Gmail, pero conserva una aprobacion humana antes del contacto con el cliente.

## 0 25 a 0 55 Arquitectura y memoria

Mostrar el PDF y luego Airtable. Explicar las relaciones Customers, Orders y Tickets, los estados obligatorios y la tabla Error Logs.

## 0 55 a 1 30 Trigger y razonamiento

Enviar el caso 01. Mostrar que el webhook responde 202, que n8n consulta el pedido y que el modelo devuelve prioridad, sentimiento, resumen y borrador en JSON.

## 1 30 a 2 10 HITL y salida

Mostrar la ejecucion en estado Waiting. Abrir el correo de aprobacion, revisar el borrador y aprobar. Volver a n8n para mostrar la reanudacion. Mostrar el correo final y el estado actualizado en Airtable.

## 2 10 a 2 40 Camino infeliz

Enviar el caso 03 o 04. Mostrar la ruta de error y el registro en Error Logs. Explicar que la falla no dispara el contacto al cliente.

## 2 40 a 3 00 Cierre y seguridad

Mostrar el historial de cinco ejecuciones y el repositorio. Mencionar el filtro anti loop, variables de entorno, limite de tokens y ausencia de secretos.

## Preparacion de la grabacion

- Desactivar notificaciones personales.
- Usar datos ficticios.
- Ocultar credenciales, headers y valores de entorno.
- Aumentar el zoom del navegador.
- Tener abiertas las pestanas en el orden del guion.
- No mostrar la URL completa de webhooks de produccion.
