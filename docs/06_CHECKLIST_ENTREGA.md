# Checklist final de entrega

## Arquitectura

- [ ] El workflow principal se importa sin errores.
- [ ] El workflow de errores esta seleccionado en Settings.
- [ ] Todos los nodos tienen nombres descriptivos y numerados.
- [ ] No hay datos personales ni secretos hardcodeados.
- [ ] Las variables se leen desde el entorno.

## Base de datos

- [ ] Airtable contiene Customers, Orders, Tickets y Error Logs.
- [ ] Customers se relaciona con Orders y Tickets.
- [ ] Orders se relaciona con Tickets.
- [ ] Tickets incluye los estados Pendiente, Procesado por IA, Aprobado por Humano, Rechazado por Humano, Respondido y Error.
- [ ] La vista compartida funciona sin iniciar sesion.

## IA y resiliencia

- [ ] El prompt usa variables dinamicas del ticket y del pedido.
- [ ] La salida del modelo de IA es JSON estructurado.
- [ ] `max_output_tokens` esta limitado.
- [ ] La falla de IA crea un registro en Error Logs.
- [ ] La falla de Gmail crea un registro en Error Logs.
- [ ] Existe un filtro para datos incompletos.
- [ ] Existe un control anti loop con `automation_source`.

## Human in the loop

- [ ] El workflow queda en estado Waiting antes de Gmail.
- [ ] El correo HITL permite aprobar o rechazar.
- [ ] Rechazar impide el envio al cliente.
- [ ] Aprobar registra persona y fecha.

## Pruebas y evidencia

- [ ] Se ejecutaron los cinco payloads.
- [ ] Se probo el camino feliz.
- [ ] Se probo el camino infeliz.
- [ ] Se probo la prevencion de bucle.
- [ ] Se capturo el historial de cinco ejecuciones.
- [ ] Las capturas no muestran credenciales.
- [ ] El video dura aproximadamente 3 minutos.

## GitHub

- [ ] El PDF abre correctamente.
- [ ] Los dos JSON estan versionados.
- [ ] Los enlaces obligatorios estan completos.
- [ ] El README explica como reproducir el proyecto.
- [ ] `.env` no aparece en Git.
- [ ] Se reviso el historial por secretos antes de publicar.
