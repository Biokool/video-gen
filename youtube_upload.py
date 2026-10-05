#!/usr/bin/env python3
"""Subida de videos a YouTube (API v3, OAuth 2.0).

IMPORTANTE: la API key de YouTube solo sirve para LECTURA (buscar videos,
sugerencias de temas). SUBIR videos exige OAuth 2.0 con la cuenta del canal:
  1. En Google Cloud Console → APIs y servicios → Credenciales → Crear
     credenciales → ID de cliente de OAuth → tipo "Aplicación de escritorio".
  2. Descarga el JSON, renómbralo a client_secret.json y ponlo en la carpeta
     youtube/ junto a este panel (video-gen/youtube/).
  3. En el panel, sección Publicar → "Conectar YouTube": se abre el navegador
     para autorizar (solo la primera vez) y se guarda token.json.
  4. "Subir video": usa videos().insert() con subida reanudable y reporta
     el progreso. La URL del video se muestra al terminar.

Cuota: cada subida cuesta ~1600 unidades del cupo diario (10.000 por
defecto) → ~6 videos/día. Suficiente para 2 videos/semana.

token.json y client_secret.json son SECRETOS: nunca van al ZIP ni a git.
"""
import json
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Etiquetas de la UI -> valores que acepta resource.status.privacyStatus.
_PRIVACIDAD = {"privado": "private", "oculto": "unlisted",
               "publico": "public", "público": "public",
               "private": "private", "unlisted": "unlisted",
               "public": "public"}
API_SERVICE = "youtube"
API_VERSION = "v3"

# Categoría por defecto: 28 = Ciencia y tecnología
DEFAULT_CATEGORY = "28"


def yt_dir(base):
    d = Path(base) / "youtube"
    d.mkdir(parents=True, exist_ok=True)
    return d


def secret_path(base):
    return yt_dir(base) / "client_secret.json"


def token_path(base):
    return yt_dir(base) / "token.json"


def estado(base):
    """Devuelve dict con el estado de la conexión (para la UI)."""
    sec = secret_path(base)
    tok = token_path(base)
    if not sec.exists():
        return {"nivel": "falta_secret",
                "mensaje": "Falta youtube/client_secret.json"}
    if not tok.exists():
        return {"nivel": "falta_auth",
                "mensaje": "Falta autorizar la cuenta del canal"}
    try:
        data = json.loads(tok.read_text(encoding="utf-8"))
        if not data.get("refresh_token") and not data.get("token"):
            return {"nivel": "token_roto",
                    "mensaje": "token.json inválido: vuelve a autorizar"}
    except Exception:
        return {"nivel": "token_roto",
                "mensaje": "token.json ilegible: vuelve a autorizar"}
    return {"nivel": "ok", "mensaje": "Conectado"}


def _importar():
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from googleapiclient.errors import HttpError
    except ImportError as e:
        raise RuntimeError(
            "Faltan las librerías de Google: ejecuta "
            "`pip install -r requirements.txt` (google-api-python-client, "
            "google-auth-oauthlib).") from e
    return InstalledAppFlow, Request, Credentials, build, MediaFileUpload, \
        HttpError


def autorizar(base):
    """Flujo OAuth: abre el navegador, guarda token.json. Devuelve (ok, msg)."""
    InstalledAppFlow, Request, Credentials, build, _, _ = _importar()
    sec = secret_path(base)
    if not sec.exists():
        return False, ("No existe youtube/client_secret.json. Créalo en "
                       "Google Cloud Console (ID de cliente de OAuth, tipo "
                       "'Aplicación de escritorio') y colócalo ahí.")
    flow = InstalledAppFlow.from_client_secrets_file(str(sec), SCOPES)
    try:
        creds = flow.run_local_server(port=0, prompt="consent")
    except Exception as e:
        return False, f"No se completó la autorización: {e}"
    token_path(base).write_text(creds.to_json(), encoding="utf-8")
    return True, "Cuenta autorizada y guardada (token.json)."


def _servicio(base):
    InstalledAppFlow, Request, Credentials, build, _, HttpError = _importar()
    tok = token_path(base)
    if not tok.exists():
        raise RuntimeError("Sin autorización: usa 'Conectar YouTube' primero.")
    creds = Credentials.from_authorized_user_file(str(tok), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        tok.write_text(creds.to_json(), encoding="utf-8")
    return build(API_SERVICE, API_VERSION, credentials=creds)


def subir(base, video_path, titulo, descripcion, tags, privacidad="privado",
          categoria=DEFAULT_CATEGORY, progress=None):
    """Sube un video con subida reanudable.

    progress(recibido, total): callback opcional.
    Devuelve (video_id, url) o lanza RuntimeError con mensaje amigable.
    """
    _, _, _, _, MediaFileUpload, HttpError = _importar()
    # La UI habla español; la API exige los valores oficiales de YouTube.
    priv = _PRIVACIDAD.get(
        (privacidad or "").strip().lower().replace("ú", "u"), "private")
    video_path = Path(video_path)
    if not video_path.exists():
        raise RuntimeError(f"No existe el video: {video_path}")
    if len(titulo) > 100:
        titulo = titulo[:100]
    body = {"snippet": {"title": titulo,
                        "description": descripcion or "",
                        "tags": [t for t in (tags or []) if t][:500],
                        "categoryId": categoria},
            "status": {"privacyStatus": priv,
                       "selfDeclaredMadeForKids": False}}
    service = _servicio(base)
    media = MediaFileUpload(str(video_path), chunksize=8 * 1024 * 1024,
                            resumable=True)
    try:
        req = service.videos().insert(part="snippet,status", body=body,
                                      media_body=media)
        resp = None
        while resp is None:
            status, resp = req.next_chunk()
            if status and progress:
                try:
                    progress(status.resumable_progress, status.total_size)
                except Exception:
                    pass
    except HttpError as e:
        msg = str(e)
        if "quotaExceeded" in msg or "quota" in msg.lower():
            raise RuntimeError("Cuota diaria de la API de YouTube agotada "
                               "(~6 subidas/día). Intenta mañana.") from e
        if "invalidCredentials" in msg or "auth" in msg.lower():
            raise RuntimeError("La autorización caducó o fue revocada: "
                               "borra youtube/token.json y vuelve a "
                               "conectar.") from e
        raise RuntimeError(f"YouTube rechazó la subida: {msg[:300]}") from e
    vid = (resp or {}).get("id", "")
    return vid, f"https://youtu.be/{vid}" if vid else ""


def parse_paquete(paquete_md):
    """Extrae título/descripción/tags de un PAQUETE.md del panel.

    Devuelve {"titulo":..., "descripcion":..., "tags":[...]} con fallbacks.
    """
    txt = Path(paquete_md).read_text(encoding="utf-8", errors="replace") \
        if Path(paquete_md).exists() else ""
    titulo, descripcion, tags = "", "", []

    def seccion(nombre, siguiente=None):
        import re
        ini = txt.find(nombre)
        if ini < 0:
            return ""
        ini += len(nombre)
        fin = len(txt)
        if siguiente:
            j = txt.find(siguiente, ini)
            if j > 0:
                fin = j
        return txt[ini:fin].strip()

    # TÍTULOS: toma la opción 1
    import re
    m = re.search(r"T[ÍI]TULOS:\s*\n1\.\s*(.+)", txt)
    if m:
        titulo = m.group(1).strip()
    if not titulo:
        m = re.search(r"^1\.\s*(.+)", txt, re.M)
        titulo = m.group(1).strip() if m else "El Porqué"

    desc = seccion("DESCRIPCION:", "LO QUE VERAS:")
    veras = seccion("LO QUE VERAS:", "CAPITULOS:")
    fuentes = seccion("FUENTES:", "HASHTAGS:")
    partes = [p for p in (desc, veras, fuentes) if p]
    descripcion = "\n\n".join(partes)[:4800]

    m = re.search(r"^TAGS:\s*(.+)", txt, re.M)
    if m:
        tags = [t.strip().lstrip("#") for t in m.group(1).split(",")
                if t.strip()][:15]
    m = re.search(r"^HASHTAGS:\s*(.+)", txt, re.M)
    if m:
        for h in re.findall(r"#(\w+)", m.group(1)):
            if h not in tags:
                tags.append(h)
    return {"titulo": titulo[:100], "descripcion": descripcion,
            "tags": tags[:20]}
