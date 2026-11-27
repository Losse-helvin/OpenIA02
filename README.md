# MANaja AI Conversational Landing Page

Landing page Django responsive où l'IA qualifie un prospect par conversation, sans formulaire classique. Les conversations sont conservées côté serveur pendant la session; aucun prospect n'est inscrit dans le CRM Google Sheets avant consentement explicite. L'adaptateur MANaja utilise une API compatible OpenAI Chat Completions configurable. **L'URL, le modèle et la clé du fournisseur MANaja n'étant pas fournis dans le dépôt, ces trois valeurs doivent être renseignées avant les appels réels.** Il n'y a pas de clé secrète factice ni d'appel simulé présenté comme fonctionnel.

## Arborescence

```text
config/                 paramètres Django, URL, WSGI
leads/                  modèles, API conversation/consentement, scoring, Sheets
static/app.css          interface responsive
static/app.js           chat, suggestions, progression, consentement
 templates/landing.html page conversationnelle
manage.py
requirements.txt
.env.example
```

## Démarrage local

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
# Remplir les trois paramètres MANaja selon les identifiants du fournisseur MANaja.
python manage.py migrate
python manage.py createsuperuser # facultatif, interface admin
python manage.py runserver 0.0.0.0:8000
```

Visiter `http://127.0.0.1:8000`. Sans configuration MANaja, le chat renvoie explicitement un message de configuration manquante. `/api/status` affiche si base URL + modèle sont définis; ne pas exposer cette route comme indicateur d'état détaillé public si cela vous gêne.

## Configuration MANaja AI

Dans `.env` :

```dotenv
MANAJA_API_BASE_URL=https://URL_OFFICIELLE_DU_FOURNISSEUR/v1
MANAJA_API_KEY=secret-server-side
MANAJA_MODEL=model-id
MANAJA_TIMEOUT_SECONDS=45
```

Le client appelle `POST {MANAJA_API_BASE_URL}/chat/completions` avec Bearer auth, `messages` et `response_format: json_object`. Cette intégration suppose une API compatible OpenAI. Si MANaja utilise un protocole différent, modifier uniquement `leads/services.py::call_manaja`. N'inscrire jamais une clé réelle dans HTML/JS, Git ou le navigateur. Choisir uniquement un endpoint HTTPS du fournisseur.

## API interne

- `GET /` : page + cookie CSRF, création/reprise de session et historique.
- `POST /api/chat` : `{ "message": "..." }` (max. 4 000 caractères); répond `{reply, consent_requested, progress, qualified}`.
- `POST /api/consent` : `{ "consent": true }`; accepté uniquement après demande de consentement signalée par l'agent; crée ID unique et Lead puis tente l'écriture Sheets.
- `POST /api/reset` : ferme la conversation non transmise et crée nouvelle session.
- `GET /api/status` : configuration générale.

Le frontend utilise ces routes relatives, même domaine. En production, configurez cookies Secure, HTTPS, domaine/CSRF, serveur cache partagé pour le rate-limit, proxy rate limiting et authentification/anti-abus appropriés.

## Google Sheets — raccordement sécurisé

L'intégration se fait par Google Sheets API et un compte de service, indépendant du connecteur Google Sheets d'Arena. **Aucun compte ni feuille n'a été autorisé ou connecté à ce dépôt**. Pour une configuration réelle :

1. Dans Google Cloud Console, créer un projet, activer Google Sheets API, créer un service account et télécharger son JSON dans un chemin hors Git.
2. Créer la Google Sheet et partager le document avec le champ `client_email` du service account (éditeur). Copier son ID depuis l'URL `/spreadsheets/d/<ID>/`.
3. Configurer `GOOGLE_SHEETS_ENABLED=true`, `GOOGLE_SERVICE_ACCOUNT_FILE=/chemin/secret.json`, `GOOGLE_SPREADSHEET_ID=...` et éventuellement `GOOGLE_WORKSHEET_LEADS=Leads`.
4. Le premier lead consenti crée les onglets `Leads`, `Conversations`, `Statistiques`, `Parametres` et leurs entêtes. L'ID de lead rend l'écriture Leads idempotente. Une erreur Sheets n'annule pas la demande : `sheets_error` est gardé sur le lead pour relance manuelle/admin.
5. Protéger les plages et accès; les lignes Conversations contiennent le contenu conversationnel consenti. Définir rétention et suppression compatibles avec votre politique et obligations de confidentialité.

Si vous voulez que j'opère directement un compte Google Sheet via l'app connectée Arena, activez Google Sheets dans les apps de cette conversation. Cela est distinct de la configuration du compte de service ci-dessus.

## Qualification, sécurité, limites

Scoring explicite 0–100, catégories `<50 cold`, `50–79 warm`, `80+ hot`. Les champs absents ne sont pas inventés; budget inconnu vaut 0. Le prompt demande une réponse JSON structurée, questions une à une, langue visiteur FR/MG/EN, et un champ de demande de consentement. Le clic explicite est toujours requis côté serveur. Revoir l'heuristique de scoring selon l'offre réelle avant usage commercial.

Les conversations non transmises restent en base jusqu'à la suppression/rétention. Fixer `CONVERSATION_RETENTION_DAYS` et mettre en œuvre un job de purge planifié avant production. Le statut de consentement n'est pas un avis juridique: publier une politique de confidentialité, base légale, durée, contact et processus de retrait conforme au droit applicable (y compris données à Madagascar et pays ciblés).

- Rate limiting de prototype en cache local par IP; utiliser Redis/proxy en production. Configurer correctement les en-têtes proxy pour empêcher IP spoofing.
- La vue ne lance pas de code fourni par le visiteur. Ne jamais ajouter d'exécution Python arbitraire au worker Django.
- `LEAD_NOTIFICATION_WEBHOOK` est optionnel et s'exécute après consentement; définir une URL HTTPS maîtrisée.
- Migrations à générer avec `python manage.py makemigrations leads`; SQLite par défaut. Pour PostgreSQL, renseigner `DB_ENGINE=django.db.backends.postgresql`, DB_* et installer `psycopg[binary]` en dépendance de production.
- Google Sheets sync s'effectue en requête synchrone pour le prototype. Pour production, déplacer dans Celery/queue et utiliser retries bornés/backoff.

## Tests

```bash
python manage.py makemigrations leads
python manage.py migrate
python manage.py test
python manage.py check
```

Les tests mockent MANaja; aucune clé réelle n'est nécessaire pour les tests unitaires. Les essais d'intégration live exigent un endpoint MANaja autorisé et un Google service account configuré.

## Déploiement cloud

Déployer sur un hôte Python supportant Django (Render, Railway, Fly.io, VPS ou équivalent) avec PostgreSQL managé en production. Construire image, installer `requirements.txt`, définir secrets d'environnement dans le tableau de bord, exécuter `python manage.py migrate`, lancer `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`. Activer HTTPS, domaine, `DJANGO_DEBUG=false`, `DJANGO_SECRET_KEY` aléatoire, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, cookies Secure (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` à activer pour environnement HTTPS), logs/alertes, backups DB et stockage sécurisé du JSON Sheets. Aucun plan d'hébergement gratuit n'est garanti permanent.
