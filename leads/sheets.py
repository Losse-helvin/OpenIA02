from django.conf import settings
from django.utils import timezone

def _get_or_create_sheet(spreadsheet, title, headers):
    import gspread
    try:
        sheet = spreadsheet.worksheet(title)
    except gspread.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title=title, rows=1000, cols=max(24, len(headers)))
    if not sheet.row_values(1):
        sheet.append_row(headers)
    return sheet

def sync_lead(lead):
    if not settings.GOOGLE_SHEETS_ENABLED:
        return False
    if not settings.GOOGLE_SERVICE_ACCOUNT_FILE or not settings.GOOGLE_SPREADSHEET_ID:
        raise RuntimeError("Google Sheets est activé mais GOOGLE_SERVICE_ACCOUNT_FILE ou GOOGLE_SPREADSHEET_ID manque.")
    import gspread
    from google.oauth2.service_account import Credentials
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(settings.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=scopes)
    gc = gspread.authorize(creds)
    spreadsheet = gc.open_by_key(settings.GOOGLE_SPREADSHEET_ID)
    lead_headers = ["ID_Lead", "Date_Creation", "Nom", "Email", "Telephone", "Entreprise", "Fonction", "Pays", "Ville", "Adresse", "Langue", "Service", "Besoin", "Probleme", "Objectif", "Budget", "Delai", "Urgence", "Potentiel", "Resume_Conversation", "Consentement", "Canal_Contact", "Statut", "Source"]
    sheet = _get_or_create_sheet(spreadsheet, settings.GOOGLE_WORKSHEET_LEADS, lead_headers)
    values = lead.data
    convo = lead.conversation
    summary = "\n".join(f"{m.role}: {m.content}" for m in convo.messages.order_by("created_at"))[-12000:]
    row = [str(lead.id), lead.created_at.isoformat(), values.get("name", ""), values.get("email", ""), values.get("phone", ""), values.get("company", ""), values.get("job_title", ""), values.get("country", ""), values.get("city", ""), values.get("address", ""), values.get("language", convo.language), values.get("service", ""), values.get("need", ""), values.get("problem", ""), values.get("goal", ""), values.get("budget", ""), values.get("timeline", ""), values.get("urgency", ""), f"{lead.score}/100 ({lead.temperature})", summary, "Oui", values.get("contact_channel", ""), lead.status, str(lead.source)]
    # Idempotence: a lead ID can only be appended once.
    if str(lead.id) not in sheet.col_values(1):
        sheet.append_row(row, value_input_option="USER_ENTERED")
    conversation_sheet = _get_or_create_sheet(spreadsheet, "Conversations", ["ID_Conversation", "ID_Lead", "Date", "Role", "Message"])
    if str(lead.id) not in conversation_sheet.col_values(2):
        conversation_rows = [[str(convo.id), str(lead.id), m.created_at.isoformat(), m.role, m.content[:4000]] for m in convo.messages.order_by("created_at")]
        if conversation_rows:
            conversation_sheet.append_rows(conversation_rows, value_input_option="USER_ENTERED")
    stats_sheet = _get_or_create_sheet(spreadsheet, "Statistiques", ["Indicateur", "Valeur"])
    if stats_sheet.row_count < 2 or not stats_sheet.cell(2, 1).value:
        stats_sheet.append_rows([["Leads transmis", f'=COUNTA(Leads!A2:A)'], ["Prospects chauds", f'=COUNTIF(Leads!S2:S,"*hot*")'], ["Mis à jour le", timezone.now().isoformat()]])
    _get_or_create_sheet(spreadsheet, "Parametres", ["Cle", "Valeur"])
    lead.sheets_synced_at = timezone.now()
    lead.sheets_error = ""
    lead.save(update_fields=["sheets_synced_at", "sheets_error"])
    return True
