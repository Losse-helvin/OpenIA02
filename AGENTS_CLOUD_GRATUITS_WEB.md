# Agents IA cloud gratuits intégrables dans une page Web

**Recherche documentaire au 27 novembre 2026 (UTC).** Cible : Madagascar, zéro euro, service distant, HTTPS, intégration Web/Django. Le « gratuit » hébergé signifie toujours un quota/une offre susceptible d'être modifiée, sauf preuve explicite d'un tarif et de conditions; aucune offre cloud de génération n'est qualifiée d'illimitée. Les capacités régionales ne sont garanties que si la documentation officielle énumère le pays. Les quotas et modèles affichés au compte font autorité sur ce document.

## Recommandation en bref

- **Le meilleur point de départ** : Google AI Studio / Gemini API. La page officielle des régions inclut Madagascar; certains modèles Flash sont facturés à 0 dans le quota Free. Il faut une clé, le quota est par projet et varie selon modèle; la page de tarifs met en garde sur l'usage du contenu du palier gratuit pour améliorer les produits Google. Ne pas envoyer de données sensibles sans vérifier les conditions.
- **Alternative plus orientée modèles ouverts** : Cloudflare Workers AI, quota documenté de 10 000 Neurons/jour partagé, sur compte Cloudflare et avec token. Endpoint HTTPS officiel exact ci-dessous; capacité en « requêtes » dépend du modèle et de la taille, donc ce n'est pas une promesse d'un certain nombre de conversations.
- **Alternative simple pour une démo** : Botpress Cloud gratuit : 100 conversations/mois et 3 agents selon sa page tarifaire. Le constructeur héberge le widget; la consommation des modèles/IA est soumise aux limites affichées. Dify Cloud Sandbox est utile pour essayer, mais ses 200 crédits sont une **allocation unique**, pas une allocation mensuelle permanente d'après sa documentation.
- **Sécurité Web** : une clé API fournisseur ne doit jamais être mise dans le JavaScript public. Le navigateur appelle une route Django (ou une fonction serveurless), qui appelle le fournisseur. Si on veut zéro serveur à administrer, choisir un widget SaaS intégré, accepter ses limites, et ne pas exposer une clé secrète.

## Accès depuis Madagascar — preuve et limites

La page officielle « Available regions » de Google AI Studio/Gemini liste explicitement **Madagascar** ([source](https://ai.google.dev/gemini-api/docs/available-regions)). Pour Cloudflare, Hugging Face, Groq, OpenRouter et les agents SaaS recensés, je n'ai pas trouvé une liste officielle publique confirmant spécifiquement Madagascar. Ils sont des services Internet/API, mais l'accessibilité effective, les paiements, la vérification de compte, le routage réseau ou restrictions peuvent dépendre du compte et du fournisseur. Tester inscription et un appel de santé depuis une connexion malgache avant de bâtir dessus. Ne pas contourner les restrictions géographiques.

## Catégorie 1 — 10 agents/constructeurs hébergés à essayer

Classement orienté simplicité d'essai distant, pas classement de « meilleure intelligence ». Un widget public n'est pas automatiquement une API libre pour les développeurs.

| # | Produit, ce qu'on obtient | Site / démo / intégration | Gratuité et contraintes établies |
|---|---|---|---|
| 1 | **Google Gemini API + agent géré (preview)** : service cloud d'agent avec environnement Linux, outils de code/fichiers/recherche Web selon documentation; peut aussi être appelé comme modèle et outils depuis une application. | [AI Studio](https://aistudio.google.com/), [Agents docs](https://ai.google.dev/gemini-api/docs/agents), [régions](https://ai.google.dev/gemini-api/docs/available-regions), [API Gemini](https://ai.google.dev/gemini-api/docs). Ce n'est pas un widget sans code prêt à coller. | Documentation dit accès à un quota Free, mais interaction agentique peut déclencher 100k–3M tokens; coût dépend des tokens/outils. Environnement supprimé après 7 jours sans activité, VM s'endort et redémarre à la requête suivante. Preview; inspecter actions/résultats. Madagascar dans la liste régionale. Clé API. |
| 2 | **Botpress Cloud** : constructeur d'agents et Webchat intégrable, outils et actions via Studio/ADK. | [Site](https://botpress.com/), [tarifs](https://botpress.com/pricing), [Webchat docs](https://botpress.com/docs/webchat/get-started/introduction), [API docs](https://botpress.com/docs/api-reference). | Page de prix indique Free à $0, 100 conversations, 3 agents, 3 seats. Pas illimité; calcul de consommation IA et fonctions doivent être lus sur le plan courant. Le widget est le chemin direct; API/compte selon fonctionnalités. Compte nécessaire. |
| 3 | **Dify Cloud Sandbox** : créer application chat, workflow ou agent, publier une web app et API. | [Cloud](https://cloud.dify.ai/), [quick start](https://docs.dify.ai/en/quick-start), [API](https://docs.dify.ai/en/api-reference), [embed](https://docs.dify.ai/en/guides/application-publishing/embedding-in-websites). | 200 AI credits **à usage unique** au démarrage selon quick start; non renouvelés mensuellement. Certaines fonctions nécessitent sa propre clé fournisseur. Comptes GitHub ou Google selon l'inscription. Réseau et données hébergés par Dify; lire sa politique et résidence données. |
| 4 | **Hugging Face Spaces (apps Gradio publiques)** : démos de modèles/agents, page Web publique et API Gradio si l'auteur a laissé l'app active. | [Spaces](https://huggingface.co/spaces), [créer Space](https://huggingface.co/new-space), [Spaces API](https://huggingface.co/docs/hub/spaces-api-endpoints), [Gradio Client JS](https://www.gradio.app/guides/getting-started-with-the-js-client). Exemple public: [translation demo](https://huggingface.co/spaces/abidlabs/en2fr). | App tierce et disponibilité indépendantes; CPU gratuit peut dormir (environ 48h inactif selon docs), réveil à froid. Les Spaces Gradio/Docker nouvellement créés ont des conditions de création matérielle différentes; statique gratuit. L'auteur décide authenticité/quotas. Les appels de démonstration ne sont pas un SLA/API gratuite permanente. |
| 5 | **Gemini Apps (chat public)** : agent conversationnel hébergé pour usage humain; peut partager des Gems/URLs mais ce n'est pas le même produit que Gemini API. | [Gemini](https://gemini.google.com/), [aide](https://support.google.com/gemini/). | Offre utilisateur gratuit avec restrictions modèles/fonctions/région/compte. Pas d'API publique pour piloter le compte Gemini depuis une page tierce; utiliser Gemini API à la place. Ne pas intégrer par scraping. |
| 6 | **ChatGPT (interface publique)** : conversation, certains outils côté produit. | [ChatGPT](https://chatgpt.com/), [plans](https://openai.com/chatgpt/pricing/), [API séparée](https://platform.openai.com/docs/overview). | Accès gratuit au site ne signifie pas appels API gratuits. La plateforme API est facturée selon usage/conditions; pas recommandé sous contrainte budget zéro pour backend. Pas d'intégration via iframe/API non documentée. |
| 7 | **Claude.ai** : assistant public hébergé. | [Claude](https://claude.ai/), [plans](https://www.anthropic.com/pricing), [API](https://docs.anthropic.com/en/api/getting-started). | Site utilisateur peut avoir accès gratuit limité, mais l'API est distincte et payante. Aucune API gratuite permanente établie ici; ne pas utiliser l'interface par automatisation non autorisée. |
| 8 | **HuggingChat** : chat web sur modèles ouverts sélectionnés. | [huggingface.co/chat](https://huggingface.co/chat/), [code](https://github.com/huggingface/chat-ui). | Interface de démo/produit, accès aux modèles et comptes peuvent évoluer. Le code d'interface ne donne pas un endpoint d'inférence hébergé gratuit garanti ni droit de l'embarquer comme API tierce. Vérifier les conditions de chaque modèle. |
| 9 | **OpenRouter Playground + Free Router** : démo Web et routeur API des modèles gratuits disponibles. | [Playground](https://openrouter.ai/playground), [Free Models Router](https://openrouter.ai/docs/guides/overview/for-providers#free-models) (route documentée [ici](https://openrouter.ai/docs/cookbook/get-started/free-models-router-playground)). | API de modèles `:free` avec limites documentées, pas un produit d'agent clé-en-main. Selon docs, requêtes/jour dépendent des crédits achetés; consulter son endpoint `/api/v1/key`. Accès API nécessite une clé. Les modèles gratuits peuvent changer/disparaître. |
| 10 | **Démos publiques Gradio** (agents particuliers) : toute app publique qui expose un composant prédictif peut donner une démo et API. | [découvrir Spaces](https://huggingface.co/spaces?sort=trending), [exemples agent](https://huggingface.co/spaces?search=agent), [API client docs](https://huggingface.co/docs/hub/spaces-api-endpoints). | Pas de quota uniforme. La démo peut être à l'arrêt, endormie, privée, en file d'attente ou limitée. Vérifier « Use via API » et l'API name dans chaque Space. Licence du code/modèle et commercialité du Space séparées. |

**À ne pas confondre** : framework open source (LangGraph/CrewAI/Dify communautaire) != SaaS hébergé gratuitement. n8n, Flowise, Langflow et la plupart des projets GitHub doivent être hébergés quelque part; leurs versions cloud gratuites, si existantes, sont distinctes et limitées. Une URL de chat publique est souvent réservée à l'utilisation humaine et non à l'intégration externe.

## Catégorie 2 — 10 API cloud gratuites/à palier gratuit

| # | API et endpoint documenté | Quota / inscription / Madagascar | Atouts et réserves |
|---|---|---|---|
| 1 | **Gemini Developer API** — `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent` (pour streaming, route documentée `:streamGenerateContent?alt=sse`). | Plusieurs modèles Flash affichent gratuit au palier Free; limites par modèle/projet visibles dans AI Studio et changeantes. Création de clé. Madagascar explicitement pris en charge dans les régions listées. | Multimodal, function calling, streaming, SDK Python/JS. Free contents peuvent être utilisés pour amélioration selon conditions de prix; quota gratuit non SLA et pas un droit sur les modèles. [Quickstart](https://ai.google.dev/gemini-api/docs/quickstart), [pricing](https://ai.google.dev/gemini-api/docs/pricing), [limits](https://ai.google.dev/gemini-api/docs/rate-limits). |
| 2 | **Cloudflare Workers AI** — `POST https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}`; compatible OpenAI `https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1/chat/completions` si prise en charge. | Gratuit : 10 000 Neurons/jour, total partagé. Compte, Account ID et token Worker AI; capacité requêtes dépend du modèle. Service indique 403/429 si modèle plan payant ou quota épuisé. Madagascar n'est pas vérifié par liste dédiée. | Bon pour modèles ouverts, REST, streaming selon modèle. Utiliser modèle autorisé en Free. [Tarifs officiels](https://developers.cloudflare.com/workers-ai/platform/pricing/), [API run](https://developers.cloudflare.com/api/operations/workers-ai-post-run), [erreurs](https://developers.cloudflare.com/workers-ai/platform/errors/), [catalogue](https://developers.cloudflare.com/workers-ai/models/). |
| 3 | **OpenRouter** — `POST https://openrouter.ai/api/v1/chat/completions` (ou endpoint Responses selon fonctionnalité). Modèle `openrouter/free` ou modèle catalogué `:free`. | Pas de carte nécessaire pour créer une clé généralement; les plafonds free changent et sont exposés par `/api/v1/key`. Docs indiquent faible limite, 50 requêtes/jour si compte sans achat de crédits dans les limites actuelles; vérifier compte. Aucun support pays par pays identifié ici. | Nombreux modèles et une seule clé; API OpenAI-compatible, streaming et outils seulement si modèle les supporte. La clé est secrète; ne pas l'exposer navigateur. [Quickstart](https://openrouter.ai/docs/quickstart), [limits](https://openrouter.ai/docs/api_reference/limits), [catalogue API](https://openrouter.ai/api/v1/models). |
| 4 | **GroqCloud** — `https://api.groq.com/openai/v1/chat/completions` | Free Developer tier soumis à quotas modèle/org, exacts visibles console et rate limits; clé requise. Pas de confirmation publique spécifique Madagascar dans les sources consultées. | Très faible latence; OpenAI SDK, streaming/function calls par modèle. Rate limit en RPM/TPM/RPD; vérifier [model list](https://console.groq.com/docs/models) et [rate limits](https://console.groq.com/docs/rate-limits). Gratuit ne veut pas dire production fiable. |
| 5 | **Hugging Face Inference Providers** — modèle/provider via SDK ou router compatible `https://router.huggingface.co/v1` (routes selon guide). | Docs pricing consultées : Free user n'a pas de crédits Inference Providers inclus; usage de provider nécessite achat de crédits ou plan Pro. D'anciennes pages mentionnent crédits symboliques, donc ne pas compter sur un quota permanent gratuit. Token nécessaire. | Modèles open weights au choix, mais facture d'inférence sous-jacente et licence du modèle différente. [Tarifs officiels](https://huggingface.co/docs/inference-providers/en/pricing), [quickstart](https://huggingface.co/docs/inference-providers/quicktour), [API endpoint Spaces](https://huggingface.co/docs/hub/spaces-api-endpoints). |
| 6 | **Hugging Face Space Gradio public** — endpoint selon app/`api_name`, à lire depuis page du Space; client HTTP/`gradio_client`. | Certains Space publics acceptent sans clé, mais la capacité, les files, veille, disponibilité dépendent du propriétaire. Token HF conseillé/nécessaire selon Space. Gratuit CPU Basic avec sommeil après inactivité; modèle lourd non garanti. | Permet tester démos/API sans déployer. Ne pas compter comme backend d'un produit commercial; code/modèle/licence et termes Space vérifiés individuellement. [Docs](https://huggingface.co/docs/hub/spaces-api-endpoints). |
| 7 | **Mistral La Plateforme API** — `https://api.mistral.ai/v1/chat/completions` | Offre d'essai/de découverte possible selon région/compte et règles actuelles; quota exact se vérifie dans console. Clé requise. Pas de garantie permanente de gratuité ou de support Madagascar extraite de documentation vérifiée ici. | Modèles de qualité et client Python; séparer prix API et licence du poids, certains modèles ouverts. [Docs](https://docs.mistral.ai/), [tarifs](https://mistral.ai/pricing). Ne pas retenir comme fondation zéro-euro sans voir le compte. |
| 8 | **Cohere API** — v2 `https://api.cohere.com/v2/chat` | Trial/development selon compte et durée; clé. Ne pas supposer quota récurrent gratuit; accès régional à confirmer. | Chat, Rerank, embeddings. [Docs](https://docs.cohere.com/), [pricing](https://cohere.com/pricing). Pas open source; conditions d'essai à confirmer. |
| 9 | **Tavily Search API** — `POST https://api.tavily.com/search` | Plan développeur avec crédits gratuits annoncé sur page de prix (le nombre et renouvellement sont à revérifier lors de la création); clé. Aucune liste Madagascar explicitement vérifiée. | Recherche orientée agents/extraction; service fermé, quota ne couvre pas LLM. [Docs](https://docs.tavily.com/), [pricing](https://tavily.com/#pricing). |
| 10 | **Brave Search API** — `GET https://api.search.brave.com/res/v1/web/search?q=...` | Crédits et moyen de paiement/identité varient par plan; vérifier dashboard, ne pas supposer carte inutile. Clé. | Index indépendant; l'API n'est ni logiciel open source ni agent. [Docs](https://api.search.brave.com/app/documentation), [pricing](https://brave.com/search/api/). |

**Exclu du TOP gratuit garanti** : Exa (crédits/tarification susceptibles d'évoluer), NVIDIA NIM (accès développeur/crédits à conditions), OpenAI/Anthropic APIs (pas de palier API permanent gratuit vérifié), Replicate et services similaires à crédits/consommation. Pages de chat gratuites de ces sociétés ne rendent pas leur API gratuite.

## Catégorie 3 — 10 modèles appelables en cloud (sélection dynamique)
Les modèles hébergés sont appelés via les fournisseurs des deux tableaux. La licence ci-dessous est celle annoncée pour les poids/projet du modèle, non celle du service de serving. Vérifier la carte de la révision exacte, quantisation et fine-tune. Disponibilité par API est variable. Les modèles `:free` OpenRouter constituent un catalogue mutable; on peut le découvrir par `GET https://openrouter.ai/api/v1/models`, filtre `id` suffixe `:free`, puis lire la fiche et capacités du moment.

| Modèle/famille à tester | Modèle/API et capacité visée | Licence/usage commercial — point à contrôler |
|---|---|---|
| Google Gemini Flash (choisir version marquée Free dans AI Studio) | Gemini API; conversations, image, function calling/streaming selon modèle | Modèle/service propriétaires; utiliser selon conditions Google, ne pas appeler open source. Quota Free et data policy distincts. |
| Qwen3 instruct | Cloudflare/OpenRouter/serveur listé, si variante active | Plusieurs versions Qwen3 annoncées Apache-2.0; vérifier la model card du checkpoint exact. Base ouverte n'implique pas que toutes variantes hébergées le soient. |
| DeepSeek R1 distill | Groq/OpenRouter si modèle présent | R1 et dérivés ont licences distinctes; les distillations basées sur Qwen/Llama peuvent hériter des termes de la base. Vérifier chaque carte. |
| DeepSeek V3/R1 | OpenRouter ou autre endpoint actif | Licence exacte selon dépôt/version; ne pas déduire licence du nom. Déploiement API tiers n'est pas la licence du modèle. |
| Meta Llama instruct | Cloudflare/OpenRouter/Groq si variante courante | Llama Community License / Acceptable Use Policy, pas OSI open source; commercial sous conditions. |
| Google Gemma instruct | Cloudflare / HF / OpenRouter si variante disponible | Gemma Terms of Use (ou licence de la génération exacte), conditions propres; ne pas appeler OSI-open sans preuve. |
| OpenAI gpt-oss | OpenRouter/Groq ou autres fournisseurs compatibles au jour d'usage | Dépôt/modèle peut avoir licence permissive; vérifier les poids effectivement servis et les conditions provider. |
| Mistral Small / Ministral | API Mistral ou agrégateur | Licence varie par version (certaines Apache-2.0, d'autres service fermé); la version « API » est un service propriétaire. |
| Kimi / Moonshot open-weight releases | OpenRouter/HF si distribution active | Licence et accès API à distinguer; version et conditions commerciales à contrôler sur la carte. |
| GLM open-weight (famille Z.ai) | Cloudflare/HF/OpenRouter si endpoint activé | Les licences varient par release; vérifier modèle précis et conditions provider. |

**Comment déterminer le véritable endpoint et la licence à l'instant du choix** :
1. OpenRouter: appeler `GET https://openrouter.ai/api/v1/models`, retenir uniquement les modèles dont l'ID finit en `:free`, puis appeler `GET https://openrouter.ai/api/v1/model/{id}`; lire `pricing`, `supported_parameters`, `endpoints`, date d'expiration et lien de détails. Tester un appel; un modèle peut être saturé même si listé gratuitement.
2. Cloudflare: ouvrir le catalogue officiel `/workers-ai/models/`, vérifier « Workers Free » / erreur 5035, licence du modèle liée, et coût Neurons. 
3. HF: model card + champ license + page provider/inference pricing. Un poids téléchargeable ne garantit pas un service API gratuit.
4. API Gemini: n'utiliser que le `model id` présent dans le guide/pricing actuel et le tier visible par le projet.

## API : vrais exemples d'appels HTTP vérifiés

### Gemini — Python côté serveur Django
Créer une clé dans [Google AI Studio](https://aistudio.google.com/app/apikey); ajouter `GEMINI_API_KEY` dans les variables secrètes du serveur, jamais dans le JS livré au navigateur.

```python
import os, requests

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"
r = requests.post(
    url,
    params={"key": os.environ["GEMINI_API_KEY"]},
    json={"contents": [{"parts": [{"text": "Réponds en français: bonjour"}]}]},
    timeout=45,
)
r.raise_for_status()
print(r.json()["candidates"][0]["content"]["parts"][0]["text"])
```
Le modèle ID est exemple de guide Gemini actuel; prendre le nom actif de la console et pricing, pas copier indéfiniment un preview. Lire [REST API](https://ai.google.dev/api/generate-content) et [quickstart Python](https://ai.google.dev/gemini-api/docs/quickstart).

### Cloudflare Workers AI — REST
Créer compte [Cloudflare](https://dash.cloudflare.com/), noter Account ID, créer un API Token avec permission Workers AI. Le modèle doit figurer dans le catalogue et l'offre Free.

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$CF_ACCOUNT_ID/ai/run/@cf/meta/llama-3.1-8b-instruct" \
  -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Réponds en français: bonjour"}]}'
```
Modèle exemple à vérifier dans le catalogue au jour d'exécution. La base officielle de l'API REST et les routes sont [ici](https://developers.cloudflare.com/workers-ai/get-started/rest-api/); les tarifs ici: [pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/).

### OpenRouter — modèle entièrement gratuit uniquement
Créer compte et clé sur [OpenRouter Keys](https://openrouter.ai/settings/keys). API compatible OpenAI. Pour ne pas avoir de fallback payant, sélectionner `openrouter/free` ou un ID `:free` et ne jamais ajouter de modèles payants comme fallback.

```python
import os, requests
r = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
             "Content-Type": "application/json"},
    json={"model":"openrouter/free",
          "messages":[{"role":"user","content":"Réponds en français: bonjour"}]},
    timeout=60,
)
r.raise_for_status()
print(r.json()["choices"][0]["message"]["content"])
```
Ref: [free router official guide](https://openrouter.ai/docs/cookbook/get-started/free-models-router-playground), [limits](https://openrouter.ai/docs/api_reference/limits). Vérifier modèle et tarifs dynamiquement.

### Groq — OpenAI-compatible
Créer compte [Groq Console](https://console.groq.com/), produire clé et relever le modèle permis dans `/docs/models` et ses limites. Ne pas mettre la clé en JS.

```python
from openai import OpenAI
import os
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.environ["GROQ_API_KEY"])
res = client.chat.completions.create(
    model="MODÈLE_ACTIF_DE_LA_CONSOLE",
    messages=[{"role":"user","content":"Réponds en français: bonjour"}],
    stream=False,
)
print(res.choices[0].message.content)
```
L'utilisation du placeholder invite à choisir un modèle actuel, plutôt que d'inventer ou figer un model ID.

### Hugging Face Space public (API propre à la démo)
Trouver le bouton **Use via API** sur le Space; utiliser API name et paramètres affichés (non uniformes). Exemple Python documenté par HF :

```python
from gradio_client import Client
client = Client("abidlabs/en2fr")
print(client.predict("Hello, world!", api_name="/predict"))
```
Pour une app publique l'accès peut fonctionner sans token; espaces privés ou limites peuvent exiger HF token. Cela appelle une démo d'un tiers, non une API garantie. Docs: [Spaces as API endpoints](https://huggingface.co/docs/hub/spaces-api-endpoints).

### Widget hébergé (si l'objectif est un chat immédiat dans une page)
Botpress donne un Webchat construit dans l'espace du bot; utiliser l'installation/copy-code officielle des [Webchat docs](https://botpress.com/docs/webchat/get-started/introduction). Les identifiants de bot destinés au widget public ne sont pas les clés privées de l'API admin. Les routes exactes sont générées par configuration du workspace, ne pas inventer un snippet générique.

**Pas de clé fournisseur en front-end** : une clé statique dans `fetch()` peut être copiée par n'importe qui, utilisée pour épuiser le quota, et rend les prompts accessibles au fournisseur. Pour une API cloud, le schéma conseillé est navigateur → `POST /api/chat` Django → fournisseur avec clé en variable d'environnement; appliquer auth, limite IP/utilisateur, taille d'entrée et budget.

## Classements demandés

### TOP 10 — agents hébergés / interfaces prêtes à visiter
1. Gemini managed agents preview (API agent, Madagascar listé; coûts token/outils à borner).
2. Botpress Cloud (meilleur widget/site prêt, 100 conversations/mois au plan gratuit indiqué).
3. Dify Cloud Sandbox (app web + API, 200 crédits one-shot; pas le meilleur choix « gratuit permanent »).
4. Hugging Face Spaces agents publics (démos API possibles, disponibilité/endormissement non garantis).
5. HuggingChat (assistant web, API d'intégration non garantie).
6. Gemini web app (interface gratuite limitée, pas API intégrable de cette offre).
7. OpenRouter Playground / Free Router (API accessible, pas widget de production).
8. ChatGPT web (produit utilisateur gratuit selon offre, API séparée payante).
9. Claude.ai (produit utilisateur gratuit limité selon pays/compte, API séparée payante).
10. Espaces Gradio communautaires (démonstration API seulement si l'owner l'expose).

### TOP 10 — API de cloud gratuites ou ayant une offre gratuite
1. Gemini Developer API (quota gratuit affiché; Madagascar supporté; clé).
2. Cloudflare Workers AI (10K Neurons/jour; clé/token; capacité variable).
3. OpenRouter free-model router (modèles et quotas variables; clé).
4. GroqCloud developer free tier (modèle/org quota consultable; clé).
5. HF Spaces public Gradio API (app par app, files/veille).
6. Mistral API (essai/conditions compte à confirmer, pas quota permanent garanti).
7. Cohere API (trial; non permanent garanti).
8. Tavily search (crédits free selon plan publié, vérifier compte).
9. Brave Search API (crédits/conditions vérifiés au tableau de bord).
10. Exa API (crédit dépend de l'offre, ne pas considérer permanent garanti).

Les rangs 6–10 sont des pistes à tester, pas des recommandations garanties à zéro euro. Hugging Face Inference Providers n'est pas dans le top réellement gratuit: la documentation de facturation indique zéro crédits d'inférence pour utilisateurs Free (achat nécessaire); le modèle/Space public peut avoir une route distincte.

### TOP 10 — modèles accessibles par API (conseil d'essai; pas tous gratuits/licence ouverte)
1. Gemini Flash marqué « Free » dans AI Studio.
2. Qwen3 instruct via endpoint gratuit actuellement listé.
3. OpenAI gpt-oss via endpoint gratuit actuellement listé.
4. DeepSeek R1 / distill disponible dans le catalogue free actif.
5. Llama instruct si disponible et conforme à son Community License.
6. Gemma instruct si disponible, sous Gemma Terms.
7. Mistral Small/Ministral si quota ou provider gratuit actif.
8. GLM instruct si endpoint gratuit actif.
9. Kimi open-weight si endpoint et conditions disponibles.
10. Modèle de vision (Qwen-VL/Gemma-Vision ou Gemini Flash) si nécessaire et pris en charge.

C'est un **top de familles à essayer**, pas une garantie que chaque nom exact soit listé gratuit aujourd'hui. La méthode d'énumération API est plus fiable que des model IDs repris dans un article. Vérifier surtout les fonctions d'outils, vision, quotas et licence par ID.

### TOP 5 — sans carte bancaire (meilleure chance; confirmer à l'inscription)
1. Google AI Studio / Gemini API (clé, pays Madagascar listé; quota model-specific).
2. Cloudflare Workers AI (compte + API token, 10K Neurons/jour; vérifier si demande de paiement dans le parcours local).
3. OpenRouter (clé gratuite; petites limites pour modèles `:free`).
4. GroqCloud (compte/clé développeur; disponibilité account-specific).
5. Hugging Face Space public Gradio (pas de carte à l'appel public; l'espace peut dormir/être indisponible).

La preuve « pas de carte requise » n'est pas équivalente à quota illimité ou disponibilité Madagascar. Botpress/Dify sont intéressants pour un widget mais le mode compte/paiement peut varier et leurs quotas ne sont pas pérennes; ils ne sont donc pas dans ce top sans carte ferme.

### TOP 5 — intégration dans une page Web
1. **Botpress Webchat** : intégration widget la plus immédiate, quota gratuit annoncé; clé privée non exposée.
2. **Dify Cloud web app/widget** : générateur d'app et API, mais crédits d'essai one-shot.
3. **Gemini API via backend Django** : meilleur compromis documenté avec Madagascar; API nativement pas à appeler directement depuis JS public.
4. **Cloudflare Workers AI via Worker proxy** : endpoint HTTPS et quota journalier; garder secret dans Worker, exposer une route contrôlée.
5. **Hugging Face Space Gradio** : simple client JS `@gradio/client` vers démo publique; déconseillé comme disponibilité de production.

## Parcours démarrage express (budget zéro)

### Option A — intégration sécurisée, recommandé
1. Créer un projet Google AI Studio, vérifier la disponibilité Madagascar et le modèle Free dans `/pricing` et l'onglet de quotas.
2. Créer `GEMINI_API_KEY`; la stocker uniquement en secret backend/Django.
3. Dans Django, ajouter une vue `POST /api/chat` avec authentification ou quota strict, limite du corps, timeout et contrôle du modèle.
4. Front-end fait `fetch('/api/chat', {method:'POST', headers:{'Content-Type':'application/json','X-CSRFToken':...}, body: JSON.stringify({message})})` vers son propre domaine. Il ne connaît jamais la clé fournisseur.
5. Ajouter un compteur et arrêter proprement à 429/quota épuisé; ne pas basculer silencieusement vers un endpoint payant.

### Option B — ne gérer aucun serveur
1. Créer un bot dans Botpress Cloud, tester sous Free (100 conversations d'après la page de tarifs).
2. Copier le snippet généré depuis les docs / votre espace, l'insérer dans la page.
3. Vérifier si les actions désirées et coûts IA inclus sont couverts. La limite de conversation bloque la poursuite une fois atteinte; pas « permanent illimité ».

### Option C — modèle open-weight sur cloud gratuit
Créer Cloudflare account/token, tester modèle Workers AI autorisé au palier gratuit. Héberger le petit proxy dans Cloudflare Worker (pas besoin de serveur local), appliquer un rate limit par utilisateur et ne pas faire confiance à une clé API dans la page. L'enveloppe 10K Neurons/jour est partagée; observer consommation avant diffusion.

## Tableau décisionnel compact

| Choix | Cloud / aucune machine locale | 0€ plausible | Madagascar explicitement confirmé | Intégration Web | Clé | Réserve principale |
|---|---|---|---|---|---|---|
| Gemini API Free | Oui | Oui dans quotas actifs | **Oui** (liste officielle) | Django/JS via backend | Oui | limites projet, données Free |
| Cloudflare Workers AI | Oui | Oui dans 10K Neurons/j | Non vérifié explicitement | Worker proxy/API | Oui | quota compute variable |
| OpenRouter `:free` | Oui | Oui sous quota | Non vérifié | Django/backend | Oui | modèles gratuits mutable/saturés |
| Groq free | Oui | Oui sous quotas du compte | Non vérifié | Django/backend | Oui | limites par modèle/org |
| HF Spaces public | Oui | Peut-être | non vérifié | Gradio JS/Python | parfois | sommeil, auteur, file d'attente |
| Botpress Cloud | Oui | 100 conversations au prix Free affiché | non vérifié | widget embed | compte | quota et usage IA plafonnés |
| Dify Cloud Sandbox | Oui | 200 crédits de démarrage | non vérifié | web app/API | compte, parfois clé modèle | allocation one-shot |
| Hugging Face Inference Providers | Oui | **Non garanti**; $0 crédits pour compte Free selon facturation actuelle | non vérifié | SDK/API | token + crédits | facturation compute |
| ChatGPT/Claude web apps | Oui | usage humain gratuit limité selon compte | non vérifié | non via API gratuite | compte | API facturée à part |

## Sources officielles prioritaires

- Google Gemini: [pricing](https://ai.google.dev/gemini-api/docs/pricing), [rate limits](https://ai.google.dev/gemini-api/docs/rate-limits), [billing](https://ai.google.dev/gemini-api/docs/billing), [regions (Madagascar)](https://ai.google.dev/gemini-api/docs/available-regions), [managed agents](https://ai.google.dev/gemini-api/docs/agents), [API reference](https://ai.google.dev/api/generate-content).
- OpenRouter: [quickstart](https://openrouter.ai/docs/quickstart), [free model router](https://openrouter.ai/docs/cookbook/get-started/free-models-router-playground), [quota/rate limits](https://openrouter.ai/docs/api_reference/limits), [catalogue réel](https://openrouter.ai/api/v1/models).
- Hugging Face: [Inference provider billing](https://huggingface.co/docs/inference-providers/en/pricing), [Spaces API](https://huggingface.co/docs/hub/spaces-api-endpoints), [Spaces sleeping/hardware](https://huggingface.co/docs/hub/en/spaces-overview), [ZeroGPU](https://huggingface.co/docs/hub/en/spaces-gpus).
- Cloudflare: [Workers AI pricing (10,000 Neurons/day)](https://developers.cloudflare.com/workers-ai/platform/pricing/), [REST API](https://developers.cloudflare.com/workers-ai/get-started/rest-api/), [model catalog](https://developers.cloudflare.com/workers-ai/models/), [quota/model errors](https://developers.cloudflare.com/workers-ai/platform/errors/).
- Groq: [models](https://console.groq.com/docs/models), [rate limits](https://console.groq.com/docs/rate-limits), [API quickstart](https://console.groq.com/docs/quickstart).
- Botpress: [official pricing](https://botpress.com/pricing), [Webchat docs](https://botpress.com/docs/webchat/get-started/introduction), [API](https://botpress.com/docs/api-reference).
- Dify: [official quick start / 200 one-time credits](https://docs.dify.ai/en/quick-start), [API reference](https://docs.dify.ai/en/api-reference), [cloud subscription](https://docs.dify.ai/en/cloud/use-dify/workspace/subscription-management).

**Prudence sur les dates** : moteurs de recherche retournent parfois pages cachées/versions preview. Tarifs et quotas ci-dessus décrivent les pages officielles consultées, mais la console de création de compte et les docs sont la vérité opérationnelle. Tester le premier appel et fixer des plafonds explicites avant d'afficher le service au public.
