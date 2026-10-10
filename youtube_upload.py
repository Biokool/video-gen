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

import marca

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
          categoria=DEFAULT_CATEGORY, progress=None, publicar_el=None):
    """Sube un video con subida reanudable.

    progress(recibido, total): callback opcional.
    publicar_el: "2026-10-10T18:00:00-06:00" (RFC 3339) para programar.
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
    status = {"privacyStatus": priv,
              "selfDeclaredMadeForKids": False}
    if publicar_el:
        status["publishAt"] = publicar_el
    body = {"snippet": {"title": titulo,
                        "description": descripcion or "",
                        "tags": [t for t in (tags or []) if t][:500],
                        "categoryId": categoria},
            "status": status}
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


def subir_miniatura(base, video_id, thumb_path):
    """Sube la miniatura del video con thumbnails().set.

    Requiere cuenta verificada en YouTube; si no, la API lo rechaza y se
    reporta con mensaje amigable (el video queda publicado sin miniatura
    personalizada).
    Devuelve True o lanza RuntimeError.
    """
    _, _, _, _, MediaFileUpload, HttpError = _importar()
    thumb_path = Path(thumb_path)
    if not thumb_path.exists():
        raise RuntimeError(f"No existe la miniatura: {thumb_path}")
    service = _servicio(base)
    ext = thumb_path.suffix.lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    media = MediaFileUpload(str(thumb_path), mimetype=mime, resumable=False)
    try:
        service.thumbnails().set(videoId=video_id,
                                 media_body=media).execute()
    except HttpError as e:
        msg = str(e)
        if "forbidden" in msg.lower() or "insufficient" in msg.lower():
            raise RuntimeError(
                "YouTube rechazó la miniatura: tu cuenta/canal debe estar "
                "verificada (youtube.com/verify) para usar miniaturas "
                "personalizadas. El video sí quedó publicado.") from e
        raise RuntimeError(
            f"YouTube rechazó la miniatura: {msg[:300]}") from e
    return True


_PAQ_HEADERS = ["TITULOS:", "DESCRIPCION:", "LO QUE VERAS:", "CAPITULOS:",
                "FUENTES:", "CTA:", "PREGUNTA:", "HASHTAGS:", "TAGS:",
                "COMENTARIO FIJADO:", "POST COMUNIDAD:", "SHORT SUGERIDO:",
                "PANTALLA FINAL:"]

_CTA_DEFAULT = marca.CTA_YOUTUBE


def _limpiar_md(t):
    """Quita artefactos de markdown que YouTube mostraría como texto crudo."""
    import re
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)      # **X** -> X
    t = re.sub(r"(?m)^\s*#{1,3}\s*$", "", t)    # líneas ## vacías
    t = re.sub(r"(?m)^\s*\*{1,2}\s*$", "", t)   # líneas ** vacías
    t = re.sub(r"(?m)^[ \t]+$", "", t)         # líneas solo con espacios
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def _extraer_inline(desc):
    """Saca sub-encabezados inline (formato viejo del panel) de la descripción.

    En paquetes viejos, "LO QUE VERAS:" y "CAPITULOS:" venían dentro de
    DESCRIPCION: como **LO QUE VERAS:**. Se separan para reemitirlos con
    el formato canónico (headers con emoji).
    """
    import re
    veras, caps = "", ""
    m = re.search(r"(?m)^LO QUE VERAS:\s*$", desc)
    if m:
        resto = desc[m.end():]
        desc = desc[:m.start()].strip()
        mc = re.search(r"(?m)^CAPITULOS:\s*$", resto)
        if mc:
            veras = resto[:mc.start()].strip()
            caps = resto[mc.end():].strip()
        else:
            veras = resto.strip()
    else:
        mc = re.search(r"(?m)^CAPITULOS:\s*$", desc)
        if mc:
            caps = desc[mc.end():].strip()
            desc = desc[:mc.start()].strip()
    return desc, veras, caps


def _secciones_paquete(txt):
    """Divide el PAQUETE.md por sus encabezados (## NOMBRE:), en orden."""
    import re
    pos = []
    for h in _PAQ_HEADERS:
        for m in re.finditer(r"(?m)^#{0,3}\s*" + re.escape(h), txt):
            pos.append((m.start(), h, m.end()))
    pos.sort()
    out = {}
    for i, (s, h, e) in enumerate(pos):
        fin = pos[i + 1][0] if i + 1 < len(pos) else len(txt)
        if h not in out:
            out[h] = txt[e:fin].strip()
    return out


def parse_paquete(paquete_md):
    """Extrae título/descripción/tags de un PAQUETE.md del panel.

    La descripción se reconstruye en orden canónico (gancho → LO QUE VERÁS
    → CAPÍTULOS → FUENTES → CTA → pregunta → hashtags) y sin markdown.
    Devuelve {"titulo":..., "descripcion":..., "tags":[...]} con fallbacks.
    """
    import re
    txt = Path(paquete_md).read_text(encoding="utf-8", errors="replace") \
        if Path(paquete_md).exists() else ""
    sec = _secciones_paquete(txt)

    titulo = ""
    m = re.search(r"T[ÍI]TULOS:\s*\n1\.\s*(.+)", txt)
    if m:
        titulo = _limpiar_md(m.group(1).strip())
    if not titulo:
        m = re.search(r"^1\.\s*(.+)", txt, re.M)
        titulo = _limpiar_md(m.group(1).strip()) if m else marca.NOMBRE_CANAL

    desc = _limpiar_md(sec.get("DESCRIPCION:", ""))
    veras = _limpiar_md(sec.get("LO QUE VERAS:", ""))
    caps = _limpiar_md(sec.get("CAPITULOS:", ""))
    if not veras or not caps:
        # Paquetes viejos: venían inline dentro de DESCRIPCION:
        desc, v2, c2 = _extraer_inline(desc)
        veras = veras or v2
        caps = caps or c2
    fuentes = _limpiar_md(sec.get("FUENTES:", ""))
    cta = _limpiar_md(sec.get("CTA:", "")) or _CTA_DEFAULT
    pregunta = _limpiar_md(sec.get("PREGUNTA:", ""))
    hashtags = re.findall(r"#(\w+)", sec.get("HASHTAGS:", ""))[:5]

    partes = [desc]
    if veras:
        partes.append("🔍 LO QUE VERÁS:\n" + veras)
    if caps:
        partes.append("⏱ CAPÍTULOS:\n" + caps)
    if fuentes:
        partes.append("📚 FUENTES:\n" + fuentes)
    partes.append(cta)
    if pregunta:
        partes.append(pregunta)
    if hashtags:
        partes.append(" ".join("#" + h for h in hashtags))
    descripcion = "\n\n".join(p for p in partes if p)[:4800]

    tags = []
    m = re.search(r"^TAGS:\s*(.+)", txt, re.M)
    if m:
        tags = [t.strip().lstrip("#") for t in m.group(1).split(",")
                if t.strip()][:15]
    for h in hashtags:
        if h.lower() not in [t.lower() for t in tags]:
            tags.append(h)
    return {"titulo": titulo[:100], "descripcion": descripcion,
            "tags": tags[:20]}
