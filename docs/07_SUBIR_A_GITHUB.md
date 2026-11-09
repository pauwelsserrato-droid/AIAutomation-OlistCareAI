# Subir el proyecto a GitHub

## Opcion recomendada con Git

1. Crear en GitHub un repositorio publico llamado `AIAutomation-OlistCareAI` sin README ni `.gitignore` automaticos.
2. Abrir PowerShell dentro de esta carpeta.
3. Ejecutar, reemplazando la URL por la del repositorio:

```powershell
git init
git add .
git status
git commit -m "Entrega final AIAutomation OlistCare AI"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/AIAutomation-OlistCareAI.git
git push -u origin main
```

4. Abrir el repositorio publicado y comprobar que el PDF, los JSON y las imagenes se visualizan.
5. Copiar la URL final en `docs/ENLACES_ENTREGA.md`.

## Opcion desde el navegador

1. Crear el repositorio vacio en GitHub.
2. Elegir **Add file > Upload files**.
3. Arrastrar el contenido de esta carpeta conservando la estructura.
4. Confirmar el commit.

La opcion con Git es preferible porque conserva mejor la estructura y facilita corregir la entrega.

## Revision de seguridad antes del push

```powershell
git status
git grep -n -E "sk-|pat[[:alnum:]]|hooks.slack.com/services/[A-Z0-9]"
```

La busqueda no debe mostrar secretos reales. Los textos `REEMPLAZAR` del archivo `.env.example` son marcadores intencionales.
