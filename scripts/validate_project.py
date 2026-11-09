from __future__ import annotations

import json
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]


def validate_workflow(path: Path) -> None:
    workflow = json.loads(path.read_text(encoding="utf-8"))
    names = [node["name"] for node in workflow["nodes"]]
    assert len(names) == len(set(names)), f"Nombres de nodos duplicados en {path.name}"
    known = set(names)
    for source, groups in workflow.get("connections", {}).items():
        assert source in known, f"Origen inexistente: {source}"
        for output in groups.get("main", []):
            for connection in output:
                assert connection["node"] in known, f"Destino inexistente: {connection['node']}"
    assert workflow["active"] is False, "El workflow se entrega desactivado por seguridad"


def main() -> None:
    json_files = list(ROOT.rglob("*.json"))
    for path in json_files:
        json.loads(path.read_text(encoding="utf-8"))

    validate_workflow(ROOT / "n8n" / "01_OlistCare_AI_Principal.json")
    validate_workflow(ROOT / "n8n" / "02_OlistCare_AI_Error_Handler.json")

    main_text = (ROOT / "n8n" / "01_OlistCare_AI_Principal.json").read_text(encoding="utf-8")
    required_env = {
        "AIRTABLE_BASE_ID",
        "AIRTABLE_TOKEN",
        "OPENAI_API_KEY",
        "OPENAI_MODEL",
        "SLACK_WEBHOOK_URL",
        "GMAIL_ACCESS_TOKEN",
        "GMAIL_FROM",
    }
    referenced_env = set(re.findall(r"\$env\.([A-Z0-9_]+)", main_text))
    assert required_env <= referenced_env, f"Faltan variables: {required_env - referenced_env}"

    pdf_path = ROOT / "arquitectura" / "Arquitectura_OlistCare_AI.pdf"
    reader = PdfReader(str(pdf_path))
    assert len(reader.pages) == 6, "El PDF debe tener seis paginas"
    assert pdf_path.stat().st_size > 100_000, "El PDF parece incompleto"

    evidence = [
        ROOT / "evidencias" / "01_arquitectura.png",
        ROOT / "evidencias" / "02_modelo_datos.png",
        ROOT / "evidencias" / "03_workflow_n8n.png",
    ]
    assert all(path.exists() and path.stat().st_size > 20_000 for path in evidence)

    print(f"OK: {len(json_files)} archivos JSON validos")
    print("OK: conexiones de ambos workflows validas")
    print("OK: variables de entorno referenciadas")
    print("OK: PDF de 6 paginas y 3 evidencias tecnicas")


if __name__ == "__main__":
    main()
