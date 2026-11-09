from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image as RLImage,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidencias"
ARCHITECTURE = ROOT / "arquitectura"
TMP = ROOT / "tmp" / "pdfs"
EVIDENCE.mkdir(parents=True, exist_ok=True)
ARCHITECTURE.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)

ARCH_PNG = EVIDENCE / "01_arquitectura.png"
DATA_PNG = EVIDENCE / "02_modelo_datos.png"
WORKFLOW_PNG = EVIDENCE / "03_workflow_n8n.png"
OUTPUT_PDF = ARCHITECTURE / "Arquitectura_OlistCare_AI.pdf"
WORKFLOW_JSON = ROOT / "n8n" / "01_OlistCare_AI_Principal.json"

NAVY = "#17324D"
BLUE = "#2F6BFF"
TEAL = "#00A39A"
AMBER = "#F2A93B"
RED = "#D74C4C"
GREEN = "#1F8A5B"
INK = "#1D2939"
MUTED = "#667085"
BG = "#F7F9FC"
LINE = "#C9D3E1"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str = BLUE, width: int = 6) -> None:
    draw.line((start, end), fill=color, width=width)
    x2, y2 = end
    x1, y1 = start
    if abs(x2 - x1) >= abs(y2 - y1):
        direction = 1 if x2 > x1 else -1
        points = [(x2, y2), (x2 - direction * 18, y2 - 11), (x2 - direction * 18, y2 + 11)]
    else:
        direction = 1 if y2 > y1 else -1
        points = [(x2, y2), (x2 - 11, y2 - direction * 18), (x2 + 11, y2 - direction * 18)]
    draw.polygon(points, fill=color)


def rounded_node(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, subtitle: str, fill: str, outline: str = LINE) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=22, fill=fill, outline=outline, width=3)
    draw.text((x1 + 18, y1 + 18), title, fill=NAVY, font=font(22, True))
    draw.multiline_text((x1 + 18, y1 + 58), subtitle, fill=INK, font=font(17), spacing=6)


def build_architecture_png() -> None:
    image = Image.new("RGB", (1800, 1050), BG)
    draw = ImageDraw.Draw(image)
    draw.text((70, 45), "Arquitectura de OlistCare AI", fill=NAVY, font=font(44, True))
    draw.text((70, 105), "Automatizacion de soporte logistico con memoria, IA, resiliencia y aprobacion humana", fill=MUTED, font=font(22))

    lane_y = 180
    lanes = [
        ("Entrada", 55, 250, "#EAF0FF"),
        ("Orquestacion n8n", 270, 800, "#EEF7FF"),
        ("Memoria e IA", 820, 1210, "#E9F8F5"),
        ("Validacion humana", 1230, 1515, "#FFF5E5"),
        ("Salida", 1535, 1745, "#EAF7EF"),
    ]
    for label, x1, x2, fill in lanes:
        draw.rounded_rectangle((x1, lane_y, x2, 960), radius=24, fill=fill, outline=LINE, width=2)
        draw.text((x1 + 18, lane_y + 18), label, fill=NAVY, font=font(20, True))

    nodes = {
        "trigger": (75, 325, 230, 465, "Webhook", "Ticket de\ncliente", "#FFFFFF"),
        "validate": (300, 300, 500, 450, "Validar", "Campos y\nanti loop", "#FFFFFF"),
        "lookup": (555, 300, 755, 450, "Consultar", "Pedido en\nAirtable", "#FFFFFF"),
        "airtable": (850, 285, 1175, 455, "Airtable", "Customers - Orders\nTickets - Error Logs", "#FFFFFF"),
        "openai": (850, 565, 1175, 735, "OpenAI", "Clasificacion y\nborrador JSON", "#FFFFFF"),
        "slack": (1260, 390, 1485, 565, "Slack", "Aprobar o\nrechazar", "#FFFFFF"),
        "gmail": (1560, 390, 1720, 565, "Gmail", "Enviar en\nel hilo", "#FFFFFF"),
        "error": (335, 700, 715, 860, "Rutas de error", "Validacion - pedido inexistente\nOpenAI - Gmail - error global", "#FFF1F1"),
    }
    for x1, y1, x2, y2, title, subtitle, fill in nodes.values():
        rounded_node(draw, (x1, y1, x2, y2), title, subtitle, fill)

    arrow(draw, (230, 395), (300, 375))
    arrow(draw, (500, 375), (555, 375))
    arrow(draw, (755, 375), (850, 370))
    arrow(draw, (1010, 455), (1010, 565))
    arrow(draw, (1175, 650), (1260, 500))
    arrow(draw, (1485, 480), (1560, 480), GREEN)
    arrow(draw, (1370, 565), (1370, 660), AMBER)
    draw.text((1260, 680), "Wait HITL: la ejecucion se detiene", fill="#8B5E00", font=font(18, True))
    arrow(draw, (400, 450), (475, 700), RED)
    arrow(draw, (655, 450), (620, 700), RED)
    arrow(draw, (850, 650), (715, 770), RED)
    draw.text((70, 985), "Principio: ninguna respuesta critica sale sin aprobacion humana y todo fallo deja trazabilidad.", fill=NAVY, font=font(23, True))
    image.save(ARCH_PNG, quality=95)


def build_data_model_png() -> None:
    image = Image.new("RGB", (1800, 1050), "#FFFFFF")
    draw = ImageDraw.Draw(image)
    draw.text((70, 45), "Modelo relacional en Airtable", fill=NAVY, font=font(44, True))
    draw.text((70, 105), "La memoria conecta clientes, pedidos, tickets y errores para evitar datos aislados", fill=MUTED, font=font(22))

    tables = [
        ("Customers", 90, 230, 500, 610, ["customer_id  PK", "full_name", "email", "segment", "consent_contact", "Orders  link", "Tickets  link"], "#EAF0FF"),
        ("Orders", 695, 190, 1105, 630, ["order_id  PK", "Customer  link", "order_status", "estimated_delivery", "last_tracking_event", "carrier", "order_total", "Tickets  link"], "#E9F8F5"),
        ("Tickets", 1295, 170, 1710, 720, ["ticket_id  PK", "Customer  link", "Order  link", "status", "priority", "sentiment", "category", "ai_summary", "ai_draft_reply", "approved_by", "gmail_thread_id"], "#FFF5E5"),
        ("Error Logs", 650, 730, 1150, 1000, ["error_id  PK", "workflow", "execution_id", "node", "error_type", "message", "ticket_id", "resolved"], "#FFF1F1"),
    ]
    for title, x1, y1, x2, y2, fields, fill in tables:
        draw.rounded_rectangle((x1, y1, x2, y2), radius=22, fill=fill, outline=LINE, width=3)
        draw.rectangle((x1, y1, x2, y1 + 62), fill=NAVY)
        draw.text((x1 + 20, y1 + 15), title, fill="white", font=font(25, True))
        y = y1 + (74 if title == "Error Logs" else 85)
        field_font_size = 15 if title == "Error Logs" else 18
        field_step = 24 if title == "Error Logs" else 38
        for field in fields:
            draw.text((x1 + 24, y), field, fill=INK, font=font(field_font_size, "PK" in field))
            y += field_step

    arrow(draw, (500, 350), (695, 350), BLUE)
    draw.text((555, 315), "1 a N", fill=BLUE, font=font(18, True))
    arrow(draw, (1105, 400), (1295, 400), TEAL)
    draw.text((1160, 365), "1 a N", fill=TEAL, font=font(18, True))
    arrow(draw, (500, 520), (1295, 600), AMBER)
    draw.text((820, 535), "1 a N", fill="#8B5E00", font=font(18, True))
    arrow(draw, (1490, 720), (1150, 840), RED)
    draw.text((1260, 790), "trazabilidad", fill=RED, font=font(18, True))
    image.save(DATA_PNG, quality=95)


def build_workflow_png() -> None:
    workflow = json.loads(WORKFLOW_JSON.read_text(encoding="utf-8"))
    nodes = workflow["nodes"]
    connections = workflow["connections"]
    min_x = min(node["position"][0] for node in nodes)
    max_x = max(node["position"][0] for node in nodes)
    min_y = min(node["position"][1] for node in nodes)
    max_y = max(node["position"][1] for node in nodes)
    canvas_w, canvas_h = 2200, 1150
    margin_x, margin_y = 80, 180
    usable_w, usable_h = canvas_w - 2 * margin_x, canvas_h - margin_y - 185

    def map_pos(position: list[int]) -> tuple[int, int]:
        x = margin_x + int((position[0] - min_x) / max(1, max_x - min_x) * usable_w)
        y = margin_y + int((position[1] - min_y) / max(1, max_y - min_y) * usable_h)
        return x, y

    image = Image.new("RGB", (canvas_w, canvas_h), "#F3F5F8")
    draw = ImageDraw.Draw(image)
    draw.text((70, 38), "Vista tecnica del workflow n8n", fill=NAVY, font=font(42, True))
    draw.text((70, 95), f"Generada desde 01_OlistCare_AI_Principal.json - {len(nodes)} nodos", fill=MUTED, font=font(21))

    positions = {node["name"]: map_pos(node["position"]) for node in nodes}
    for source, outputs in connections.items():
        start_x, start_y = positions[source]
        for output_group in outputs.get("main", []):
            for link in output_group:
                target_x, target_y = positions[link["node"]]
                color = RED if "error" in link["node"].lower() or "inexistente" in link["node"].lower() else "#9AA9BC"
                draw.line((start_x + 65, start_y + 25, target_x - 65, target_y + 25), fill=color, width=3)

    for node in nodes:
        x, y = positions[node["name"]]
        name = node["name"]
        if "error" in name.lower() or "inexistente" in name.lower():
            fill = "#FFECEC"
            outline = RED
        elif "Slack" in name or "HITL" in name or "decision" in name.lower() or "aprob" in name.lower() or "rechaz" in name.lower():
            fill = "#FFF2D9"
            outline = AMBER
        elif "Airtable" in name:
            fill = "#E4F7F2"
            outline = TEAL
        elif "OpenAI" in name or "IA" in name:
            fill = "#E9F0FF"
            outline = BLUE
        elif "Gmail" in name:
            fill = "#E7F6EC"
            outline = GREEN
        else:
            fill = "#FFFFFF"
            outline = LINE
        box = (x - 68, y, x + 68, y + 58)
        draw.rounded_rectangle(box, radius=10, fill=fill, outline=outline, width=3)
        words = name.split(" ", 2)
        label = " ".join(words[:2]) if len(words) > 1 else name
        if len(words) > 2:
            label += "\n" + words[2][:18]
        draw.multiline_text((x - 58, y + 10), label, fill=INK, font=font(13, True), spacing=2)

    draw.text((70, 1090), "Azul: IA  |  Verde agua: Airtable  |  Ambar: HITL  |  Verde: Gmail  |  Rojo: errores", fill=NAVY, font=font(20, True))
    image.save(WORKFLOW_PNG, quality=95)


PAGE_W, PAGE_H = landscape(A4)
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=27, leading=32, textColor=colors.HexColor(NAVY), alignment=TA_LEFT, spaceAfter=10))
styles.add(ParagraphStyle(name="SubtitleCustom", parent=styles["Normal"], fontName="Helvetica", fontSize=12.5, leading=18, textColor=colors.HexColor(MUTED), spaceAfter=12))
styles.add(ParagraphStyle(name="H1Custom", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=colors.HexColor(NAVY), spaceAfter=10))
styles.add(ParagraphStyle(name="BodyCustom", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.2, leading=15, textColor=colors.HexColor(INK), spaceAfter=7))
styles.add(ParagraphStyle(name="SmallCustom", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.7, leading=12, textColor=colors.HexColor(INK)))
styles.add(ParagraphStyle(name="CenterCustom", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=10, leading=14, textColor=colors.HexColor(NAVY), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="WhiteCenter", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=10, leading=14, textColor=colors.white, alignment=TA_CENTER))


def p(text: str, style: str = "BodyCustom") -> Paragraph:
    return Paragraph(text, styles[style])


def page_decor(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFillColor(colors.HexColor(NAVY))
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(16 * mm, PAGE_H - 10 * mm, "OLISTCARE AI")
    canvas.setFillColor(colors.HexColor(MUTED))
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(PAGE_W - 16 * mm, 9 * mm, f"Pagina {doc.page}")
    canvas.drawString(16 * mm, 9 * mm, "Proyecto final del modulo AIAutomation")
    canvas.restoreState()


def build_pdf() -> None:
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=landscape(A4),
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=17 * mm,
        bottomMargin=15 * mm,
        title="Arquitectura OlistCare AI",
        author="Proyecto academico AIAutomation",
        subject="Ecosistema autonomo de automatizacion IA para soporte logistico",
    )
    story = []
    story.append(Spacer(1, 15 * mm))
    story.append(p("Arquitectura de OlistCare AI", "TitleCustom"))
    story.append(p("Ecosistema autonomo de triage y respuesta para reclamos por entregas", "SubtitleCustom"))
    summary = Table(
        [
            [p("Caso de uso", "WhiteCenter"), p("Tecnologias", "WhiteCenter"), p("Control critico", "WhiteCenter")],
            [p("Reclamos por pedidos demorados", "BodyCustom"), p("n8n + Airtable + OpenAI + Slack + Gmail", "BodyCustom"), p("Aprobacion humana antes de Gmail", "BodyCustom")],
        ],
        colWidths=[80 * mm, 100 * mm, 75 * mm],
    )
    summary.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(NAVY)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor(LINE)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(summary)
    story.append(Spacer(1, 13 * mm))
    story.append(p("El sistema recibe un ticket, valida y normaliza sus datos, recupera el pedido desde la base operativa, solicita a la IA una clasificacion y un borrador estructurado, guarda el resultado y espera una decision humana. Solo una aprobacion explicita habilita el envio del correo. Cada desvio relevante queda registrado y genera una alerta.", "BodyCustom"))
    story.append(Spacer(1, 8 * mm))
    phases = Table([
        [p("1", "CenterCustom"), p("2", "CenterCustom"), p("3", "CenterCustom"), p("4", "CenterCustom"), p("5", "CenterCustom")],
        [p("Trigger y validacion", "CenterCustom"), p("Memoria contextual", "CenterCustom"), p("Razonamiento IA", "CenterCustom"), p("HITL en Slack", "CenterCustom"), p("Salida y trazabilidad", "CenterCustom")],
    ], colWidths=[51 * mm] * 5)
    phases.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9F0FF")),
        ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor(LINE)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(phases)

    story.append(PageBreak())
    story.append(p("Diagrama de arquitectura", "H1Custom"))
    story.append(RLImage(str(ARCH_PNG), width=260 * mm, height=151.7 * mm))

    story.append(PageBreak())
    story.append(p("Cerebro del sistema", "H1Custom"))
    story.append(RLImage(str(DATA_PNG), width=260 * mm, height=151.7 * mm))

    story.append(PageBreak())
    story.append(Spacer(1, 4 * mm))
    workflow_image = RLImage(str(WORKFLOW_PNG), width=250 * mm, height=130.7 * mm)
    workflow_image.hAlign = "CENTER"
    story.append(workflow_image)
    story.append(Spacer(1, 3 * mm))
    story.append(p("La vista se genera directamente desde el JSON entregado. Los nodos de error de OpenAI y Gmail usan salidas de error separadas; el manejador global captura fallos no previstos.", "SmallCustom"))

    story.append(PageBreak())
    story.append(p("Cumplimiento de requisitos", "H1Custom"))
    requirements = [
        ["Requisito", "Implementacion", "Evidencia"],
        ["Trigger inteligente", "Webhook POST con respuesta 202 asincrona", "Nodos 01 a 04"],
        ["Base dinamica", "Airtable con cuatro tablas y relaciones", "Modelo de datos"],
        ["Motor IA", "Responses API, JSON Schema y limite de 650 tokens", "Nodos 08 y 09"],
        ["Human in the loop", "Slack + Wait + decision aprobar o rechazar", "Nodos 11 a 14"],
        ["Salida multicanal", "Slack operativo y Gmail al cliente", "Nodos 17, 19 y 21"],
        ["Hilos", "threadId de Gmail conservado cuando existe", "Nodo 16"],
        ["Resiliencia", "Validacion, pedido inexistente, OpenAI, Gmail y error global", "Nodos 22 a 29 + workflow 02"],
        ["Anti loop", "automation_source distinto de olistcare_ai", "Nodo 02"],
        ["Sin hardcodeo", "Secretos y IDs de cuenta por variables de entorno", ".env.example"],
    ]
    table_data = [[p(cell, "WhiteCenter") for cell in requirements[0]]]
    table_data += [[p(row[0], "SmallCustom"), p(row[1], "SmallCustom"), p(row[2], "SmallCustom")] for row in requirements[1:]]
    table = Table(table_data, colWidths=[55 * mm, 140 * mm, 60 * mm], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(NAVY)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F5F9")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(LINE)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(table)

    story.append(PageBreak())
    story.append(p("Pruebas, seguridad y entrega", "H1Custom"))
    columns = Table([
        [p("Plan de pruebas", "WhiteCenter"), p("Controles de seguridad", "WhiteCenter"), p("Entregables", "WhiteCenter")],
        [
            p("1. Demora critica aprobada<br/>2. Consulta neutral rechazada<br/>3. Datos incompletos<br/>4. Pedido inexistente<br/>5. Prevencion de bucle", "BodyCustom"),
            p("Secretos fuera de Git<br/>Datos ficticios<br/>Prompt sin promesas inventadas<br/>Aprobacion previa<br/>Registro de errores depurado", "BodyCustom"),
            p("PDF de arquitectura<br/>Dos workflows JSON<br/>Plantillas Airtable<br/>Cinco payloads<br/>Guion de video<br/>Checklist y guia de evidencias", "BodyCustom"),
        ],
    ], colWidths=[85 * mm] * 3)
    columns.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(NAVY)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor(LINE)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(columns)
    story.append(Spacer(1, 8 * mm))
    story.append(p("Criterio de aceptacion", "H1Custom"))
    story.append(p("La demostracion queda completa cuando las cinco ejecuciones aparecen en el historial, el camino feliz envia un correo aprobado, el rechazo no envia correo y al menos un camino infeliz queda registrado en Error Logs y notificado en Slack. Las capturas reales se agregan despues de conectar las cuentas del alumno.", "BodyCustom"))
    doc.build(story, onFirstPage=page_decor, onLaterPages=page_decor)


if __name__ == "__main__":
    build_architecture_png()
    build_data_model_png()
    build_workflow_png()
    build_pdf()
    print(OUTPUT_PDF)
