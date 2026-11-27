# Recherche R&D — construire un agent IA autonome à budget zéro

**État de la recherche : 27 novembre 2026 (UTC).** Ce document distingue soigneusement logiciel open source, poids de modèle, licence, service hébergé et quotas gratuits. Les quotas des SaaS changent fréquemment : ils sont signalés comme variables lorsqu'ils dépendent du compte ou d'une console. Les liens officiels sont fournis pour l'intégration; les sources de vérification sont citées en fin de document. « Gratuit » signifie ici zéro coût initial, pas disponibilité, confidentialité ni quota garanti.

> **Important — limites de vérification.** Une recherche web peut confirmer la documentation et des métadonnées publiques, mais pas garantir le fonctionnement de chaque compte, les quotas individualisés, ni l'avis juridique d'une licence modèle/dépendance. Avant commercialisation, épingler la version et conserver les fichiers LICENSE, model card, conditions de service et notices exactes. « Open-weight » n'est pas synonyme d'« open source ».

## Synthèse décisionnelle

Pour un prototype Django réellement à coût marginal zéro : Django + PostgreSQL/pgvector (ou SQLite au départ) + PydanticAI ou LangGraph + Ollama avec un modèle de poids permissifs (Qwen3 quantifié si la machine le permet) + sentence-transformers local + SearXNG/Crawl4AI en local + Whisper local pour l'audio + Playwright pour navigateur. Choisir un petit modèle (1.5B–8B quantifié) selon RAM/VRAM et accepter une qualité inférieure à un service frontier. Le matériel, l'électricité et le temps d'administration ne sont pas gratuits.

Pour un prototype hébergé sans GPU : utiliser un quota Gemini/Groq/OpenRouter avec clé secrète, mais traiter les données comme tierce-partie et consulter les conditions précises de confidentialité. Prévoir Ollama et un fournisseur interchangeable comme solution de repli; les plafonds gratuits ne doivent jamais être une dépendance de production.

---

## 1. Les 20 meilleures API et solutions (sélection)

Les endpoints ci-dessous sont des bases officielles ou routes documentées, pas des garanties de quotas. Les services de génération hébergés exigent généralement une clé; les logiciels auto-hébergés n'en exigent pas en local, sauf authentification que l'opérateur ajoute.

| # | Solution / rôle | API ou accès | Licence / modèle & service | Gratuité, clé, intégration, intérêt et vigilance |
|---|---|---|---|---|
| 1 | **Ollama** — modèles locaux, API de génération et embeddings | `http://localhost:11434/api` (API locale); [API docs](https://docs.ollama.com/api) | Runtime MIT; licence distincte pour chaque modèle | Gratuit sur sa machine, sans clé locale. REST/SDK Python, option OpenAI-compatible. Très simple; qualité et latence dépendent du matériel; lire le modèle téléchargé. [Repo](https://github.com/ollama/ollama), [site](https://ollama.com). |
| 2 | **Google Gemini API / AI Studio** — multimodal, appels d'outils | `https://generativelanguage.googleapis.com/v1beta` | Service fermé; modèles propriétaires ou ouverts séparément | Offre gratuite sur certains modèles, quotas précis par projet dans AI Studio et sujets à évolution. Clé requise. SDK Python officiel. Bon niveau multimodal; vérifier politique d'utilisation des données gratuites et régions. [Docs](https://ai.google.dev/gemini-api/docs), [tarifs](https://ai.google.dev/gemini-api/docs/pricing). |
| 3 | **GroqCloud** — inférence rapide de modèles ouverts | `https://api.groq.com/openai/v1` | Service fermé; poids/modèles indépendamment licenciés | Palier de développement gratuit soumis à limites par modèle, compte et organisation; clé requise. Compatible SDK OpenAI/Python. Rapide, mais modèles disponibles et limites changent. [Docs](https://console.groq.com/docs/quickstart), [modèles/limites](https://console.groq.com/docs/rate-limits). |
| 4 | **OpenRouter** — routeur multi-fournisseurs | `https://openrouter.ai/api/v1` | Passerelle propriétaire; licence du modèle et conditions de l'hébergeur distinctes | Certains modèles `:free`, plafonds de requêtes variables; clé obligatoire. Client OpenAI Python. Excellent pour tester plusieurs modèles, pas une API open source ni une SLA gratuite. [Docs](https://openrouter.ai/docs), [modèles](https://openrouter.ai/models). |
| 5 | **Hugging Face Inference Providers** — modèles distants | `https://router.huggingface.co/v1` (route compatible selon provider) | Hub/API propriétaire; poids et licences propres à chaque modèle | crédits gratuits limités/variables, clé HF; compatibilité et fournisseur selon modèle. SDK Python et API. Un catalogue n'implique pas que tous les modèles soient gratuits ou servis. [Docs](https://huggingface.co/docs/inference-providers/index), [modèles](https://huggingface.co/models). |
| 6 | **NVIDIA NIM / build.nvidia.com** — inférence hébergée ou conteneurs | URL d'API fournie par portail/instance NIM; compatibilité OpenAI dépend de NIM | Service commercial; licence et droits de chaque modèle séparés | accès développeur/crédits soumis à inscription et limites; clé. Très utile pour accélérateurs et tests; pas un service durablement gratuit garanti. [Catalogue](https://build.nvidia.com/), [docs](https://docs.nvidia.com/nim/). |
| 7 | **Mistral API / La Plateforme** — modèles généralistes et outils | `https://api.mistral.ai/v1` | Service fermé; licences des modèles varient (Apache ou conditions Mistral) | crédits ou essai selon conditions en vigueur, clé. SDK Python. Bons modèles multilingues; bien vérifier licence du checkpoint ciblé, pas seulement le nom Mistral. [Docs](https://docs.mistral.ai/), [tarifs](https://mistral.ai/pricing). |
| 8 | **Cohere API** — génération, reranking, embeddings | `https://api.cohere.com/v2` | API propriétaire | accès de développement limité selon compte/usage; clé. SDK Python; Rerank est utile au RAG. Conditions commerciales/data séparées. [Docs](https://docs.cohere.com/), [tarifs](https://cohere.com/pricing). |
| 9 | **Brave Search API** — index web indépendant | `https://api.search.brave.com/res/v1/web/search` | API fermée; index propriétaire | crédits gratuits mensuels annoncés et activation/conditions pouvant demander moyen de paiement; clé. Bon complément conventionnel, pas logiciel open source. Confirmer le plan courant. [Docs](https://api.search.brave.com/app/documentation), [tarifs](https://brave.com/search/api/). |
| 10 | **Tavily** — recherche et extraction orientées agents | `https://api.tavily.com/search` | SaaS fermé | palier de crédits mensuels limité, clé. Réponses/contextes adaptés au RAG. Les opérations avancées consomment davantage de crédits. [Docs](https://docs.tavily.com/), [tarifs](https://tavily.com/#pricing). |
| 11 | **Exa** — recherche sémantique et contenu web | `https://api.exa.ai/search` | SaaS fermé | crédit gratuit selon compte et tarification courante, clé. Python SDK, recherche par similarité et récupération de contenu. Quota non garanti. [Docs](https://docs.exa.ai/), [tarifs](https://exa.ai/pricing). |
| 12 | **SearXNG** — métamoteur auto-hébergé | `/search?q=...&format=json` sur son instance | AGPL-3.0 | logiciel gratuit, sans clé d'API interne; requêtes limitées indirectement par moteurs sources et politique anti-abus. Python/HTTP. Le plus autonome sans fournisseur, mais disponibilité et conformité aux moteurs relèvent de l'opérateur. [Docs API](https://docs.searxng.org/dev/search_api.html), [repo](https://github.com/searxng/searxng). |
| 13 | **Firecrawl** — scrape/crawl/convertir en Markdown | cloud `https://api.firecrawl.dev/v2/scrape` et `/v2/crawl`; local via déploiement | serveur AGPL-3.0 principalement; SDK/UI certaines parties MIT; cloud fermé | cloud à crédits/clé; auto-hébergement gratuit en licence, mais infrastructure et complexité à charge. Vérifier restrictions AGPL pour service modifié offert sur réseau. [Docs](https://docs.firecrawl.dev/), [repo](https://github.com/firecrawl/firecrawl). |
| 14 | **Crawl4AI** — crawler Python pour agents/RAG | bibliothèque Python; cloud API distincte | Apache-2.0 pour projet open source; cloud séparé | exécution locale sans clé, coût d'infrastructure propre; API cloud éventuellement payante. Très bon contrôle Python; respecter robots.txt, droits d'accès et conditions de sites. [Docs](https://docs.crawl4ai.com/), [repo](https://github.com/unclecode/crawl4ai). |
| 15 | **Hugging Face Transformers + Sentence Transformers** — inférence/embeddings locaux | Python local; modèles sur Hub | MIT/Apache pour bibliothèques; licence propre à chaque poids/dataset | sans clé pour modèles publics; compute local requis. RAG, reranking, génération. Incontournable en local, mais environnement/VRAM parfois difficiles. [Transformers](https://huggingface.co/docs/transformers), [Sentence Transformers](https://sbert.net/), [repo](https://github.com/UKPLab/sentence-transformers). |
| 16 | **Qdrant** — base vectorielle | REST `http://localhost:6333`; gRPC 6334 | Apache-2.0 pour serveur | auto-hébergé gratuit, clé non requise par défaut localement (sécuriser réseau); service cloud séparé. Python SDK, filtres/hybride. [Docs](https://qdrant.tech/documentation/), [repo](https://github.com/qdrant/qdrant). |
| 17 | **PostgreSQL + pgvector** — base SQL + recherche vectorielle | protocole PostgreSQL, SQL | PostgreSQL License (extension), PostgreSQL licence permissive | gratuit auto-hébergé; clé d'API non pertinente, authentification DB nécessaire. Très adapté Django/Postgres, transactions et jointures; vector search moins spécialisé que Qdrant à grande échelle. [Repo](https://github.com/pgvector/pgvector), [docs](https://github.com/pgvector/pgvector#installation). |
| 18 | **Whisper / faster-whisper** — reconnaissance vocale locale | Python/librairie locale, pas d'endpoint SaaS par défaut | Whisper MIT; faster-whisper MIT; modèles et dépendances à vérifier | gratuit en local, sans clé; CPU/GPU nécessaires. Multilingue, Python accessible, STT/transcription. [Whisper](https://github.com/openai/whisper), [faster-whisper](https://github.com/SYSTRAN/faster-whisper). |
| 19 | **PaddleOCR** — OCR local et documents | Python/librairie locale | Apache-2.0 pour code; poids/configs à vérifier | local sans clé; coûts matériels. Multilingue et documents, intégration Python; tester précision sur documents réels. [Repo](https://github.com/PaddlePaddle/PaddleOCR), [docs](https://paddlepaddle.github.io/PaddleOCR/). |
| 20 | **Playwright** — automation navigateur | bibliothèque Python/Node locale; pas d'API SaaS | Apache-2.0 | gratuit sans clé; navigateur/serveur nécessaires. Tests, extraction et actions déterministes. Ce n'est pas un bac à sable: isoler les comptes, domaines et secrets. [Docs Python](https://playwright.dev/python/), [repo](https://github.com/microsoft/playwright). |

### Autres briques audio/vision à considérer
- **TTS** : [Piper (repo)](https://github.com/OHF-Voice/piper1-gpl) est GPL-3.0-or-later; modèles vocaux ont leurs propres licences. [Kokoro](https://github.com/hexgrad/kokoro) et les modèles TTS HF exigent aussi un contrôle des licences individuelles. Coqui TTS a connu une fermeture de société et les dépôts/modèles ne partagent pas forcément la même licence; XTTS v2 est soumis à CPML avec restriction non commerciale : éviter de le présenter comme commercialisable sans autorisation explicite.
- **Vision** : Transformers avec modèles Vision-Language, [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR), [Tesseract](https://github.com/tesseract-ocr/tesseract) (Apache-2.0) et [OpenCV](https://github.com/opencv/opencv) (Apache-2.0). Licences par poids distinctes.
- **Vidéo** : extraire les images avec FFmpeg, analyser des échantillons avec un VLM local/API et transcrire la piste audio avec Whisper. FFmpeg et les codecs peuvent avoir des obligations de licence propres au mode de compilation.

---

## 2. Les 20 meilleurs projets open source GitHub

Tous ne sont pas des API hébergées; certains sont des bibliothèques ou serveurs à exécuter. Licences et usage commercial ci-dessous concernent le dépôt logiciel, pas automatiquement modèles, données, plugins ou cloud.

| # | Projet | Catégorie / apport | Licence du code | Commercial / caveat | Dépôt et documentation |
|---|---|---|---|---|---|
| 1 | Ollama | Runtime LLM local, API HTTP | MIT | généralement permis pour le runtime; modèle individuel à auditer | [GitHub](https://github.com/ollama/ollama) · [Docs](https://docs.ollama.com/) |
| 2 | vLLM | Serving GPU haut débit | Apache-2.0 | permis sous licence; dépendances/poids à examiner | [GitHub](https://github.com/vllm-project/vllm) · [Docs](https://docs.vllm.ai/) |
| 3 | llama.cpp | Inférence quantifiée CPU/GPU | MIT | poids exclus de cette licence | [GitHub](https://github.com/ggml-org/llama.cpp) |
| 4 | LangGraph | workflow agent stateful, checkpoints, HITL | MIT | runtime OSS; plateforme gérée distincte | [GitHub](https://github.com/langchain-ai/langgraph) · [Docs](https://docs.langchain.com/oss/python/langgraph/overview) |
| 5 | PydanticAI | agents Python typés, outils, sorties validées | MIT | code utilisable commercialement; services Pydantic facultatifs | [GitHub](https://github.com/pydantic/pydantic-ai) · [Docs](https://ai.pydantic.dev/) |
| 6 | CrewAI | équipes d'agents et Flows | MIT | cloud/control plane et limites séparés | [GitHub](https://github.com/crewAIInc/crewAI) · [Docs](https://docs.crewai.com/) |
| 7 | Google ADK | kit agent multi-modèle | Apache-2.0 | modèles/cloud ont conditions propres | [GitHub](https://github.com/google/adk-python) · [Docs](https://google.github.io/adk-docs/) |
| 8 | Haystack | pipeline RAG, agents et recherche | Apache-2.0 | plateforme entreprise séparée | [GitHub](https://github.com/deepset-ai/haystack) · [Docs](https://docs.haystack.deepset.ai/) |
| 9 | LlamaIndex | ingestion, RAG, agents documentaires | MIT | certains parseurs/services sont payants | [GitHub](https://github.com/run-llama/llama_index) · [Docs](https://docs.llamaindex.ai/) |
| 10 | MCP Python SDK | client/serveur Model Context Protocol | MIT | spécification/protocoles évolutifs; authentifier les outils | [GitHub](https://github.com/modelcontextprotocol/python-sdk) · [Docs](https://modelcontextprotocol.io/) |
| 11 | Qdrant | base vectorielle distribuable | Apache-2.0 | utilisable commercialement; sécuriser instance | [GitHub](https://github.com/qdrant/qdrant) · [Docs](https://qdrant.tech/documentation/) |
| 12 | Chroma | base embeddings, démarrage facile | Apache-2.0 | Cloud séparé | [GitHub](https://github.com/chroma-core/chroma) · [Docs](https://docs.trychroma.com/) |
| 13 | pgvector | vecteurs dans PostgreSQL | PostgreSQL License | permissive; dépend de PostgreSQL | [GitHub](https://github.com/pgvector/pgvector) |
| 14 | SearXNG | métarecherche auto-hébergée | AGPL-3.0 | obligations AGPL pour modifications réseau; vérifier moteurs sources | [GitHub](https://github.com/searxng/searxng) · [Docs](https://docs.searxng.org/) |
| 15 | Crawl4AI | crawler Python orienté LLM | Apache-2.0 | logiciel permissif; respect sites et règles d'extraction | [GitHub](https://github.com/unclecode/crawl4ai) · [Docs](https://docs.crawl4ai.com/) |
| 16 | Firecrawl | crawl/scrape et conversion Markdown | AGPL-3.0 principalement | piège de licence pour service modifié; cloud commercial séparé | [GitHub](https://github.com/firecrawl/firecrawl) · [Docs](https://docs.firecrawl.dev/) |
| 17 | Playwright | automatisation de navigateurs | Apache-2.0 | commercial OK sous licence; pas de sandbox de confiance | [GitHub](https://github.com/microsoft/playwright) · [Docs](https://playwright.dev/python/) |
| 18 | Whisper / faster-whisper | ASR multilingue local | MIT / MIT | vérifier modèle/dépendances; Whisper code et poids annoncés MIT | [Whisper](https://github.com/openai/whisper) · [faster](https://github.com/SYSTRAN/faster-whisper) |
| 19 | PaddleOCR | OCR et parsing visuel | Apache-2.0 | vérifier les poids et données dérivées | [GitHub](https://github.com/PaddlePaddle/PaddleOCR) · [Docs](https://paddlepaddle.github.io/PaddleOCR/) |
| 20 | Django + Celery | backend web / tâches asynchrones | BSD-3-Clause / BSD-3-Clause | approprié commercialement; protéger workers et secrets | [Django](https://github.com/django/django) · [docs](https://docs.djangoproject.com/) · [Celery](https://github.com/celery/celery) |

**Projets à utiliser avec discernement** : AutoGen historique est en maintenance et Microsoft dirige les nouveaux projets vers Microsoft Agent Framework; consulter son README courant avant d'adopter. n8n est **fair-code/source-available**, sous Sustainable Use License et licence Enterprise, donc ne pas le qualifier d'OSI open source ni présumer qu'un SaaS construit dessus est autorisé sans lire sa FAQ/licence. [n8n repo/licence](https://github.com/n8n-io/n8n). Le code de LangGraph/CrewAI est ouvert, mais leurs services de déploiement/observabilité ne le sont pas nécessairement.

---

## 3. Solutions réellement gratuites et limites

### Gratuit en local (pas de frais logiciels/API, mais matériel à votre charge)
- Ollama, llama.cpp, Transformers/vLLM et modèles téléchargés; génération possible sans clé ni internet après téléchargement. Limite majeure : ressources mémoire, vitesse et licence du poids.
- Qdrant, Chroma, pgvector/PostgreSQL, SQLite, Django, Celery, Playwright, SearXNG, Crawl4AI, Whisper/faster-whisper, PaddleOCR. Tous demandent installation, mises à jour, stockage et supervision.
- Embeddings avec sentence-transformers : local, aucun quota fournisseur; choisir un modèle multilingue adapté au français et vérifier licence des poids.

### Gratuit à distance (quota, clé et données confiées au fournisseur)
- Gemini, Groq, OpenRouter `:free`, HF Inference Providers, NVIDIA, Cohere/Mistral selon leurs offres à date : plafonds, modèles, accès géographique, demandes et politiques changent. Pas de SLA, quota ou permanence de gratuité à présumer.
- Tavily/Exa/Brave : crédits limités et inscription; pas du logiciel open source. Confirmer prix/conditions au tableau de bord officiel.
- Google Gemini gratuit : le palier n'équivaut pas à un contrat de confidentialité payant; vérifier explicitement l'usage des données avant d'envoyer des documents privés.

**Calculateur de coûts à zéro** : appels API externes = zéro uniquement dans les limites du quota; consommation locale = coût électrique et amortissement machine. Un agent qui boucle ou lance recherche + extraction + outils peut multiplier les appels. Mettre budgets par tâche, nombre max d'étapes, délai, plafond tokens et circuit breaker.

---

## 4. API accessibles directement par URL

- Modèle OpenAI-compatible (selon fournisseur): Groq `https://api.groq.com/openai/v1`, OpenRouter `https://openrouter.ai/api/v1`, HF router `https://router.huggingface.co/v1` (consulter les modèles/providers supportés).
- Gemini: `https://generativelanguage.googleapis.com/v1beta`.
- Ollama local: `http://localhost:11434/api` (ne pas exposer publiquement sans authentification/proxy).
- Brave Search: `https://api.search.brave.com/res/v1/web/search`.
- Tavily: `https://api.tavily.com/search`.
- Exa: `https://api.exa.ai/search`.
- Firecrawl Cloud: `POST https://api.firecrawl.dev/v2/scrape` ou `/v2/crawl`, Bearer key.
- Qdrant: `http://localhost:6333`; API locale selon configuration.
- SearXNG: `GET https://<votre-instance>/search?q=...&format=json` si format JSON activé.
- API locales OCR/ASR et Playwright : non fournies par défaut, exposez-les derrière une API Django interne si nécessaire.

Éviter de qualifier une URL de « endpoint exact » si elle dépend d'un déploiement, d'une région ou d'une version. Ne jamais mettre les clés dans JS/navigateur ou dans le dépôt.

---

## 5. Meilleures solutions sans clé API

1. **Ollama local** pour le LLM; aucun compte ni clé en mode local.
2. **llama.cpp** pour contrôle bas niveau / modèles GGUF.
3. **SearXNG auto-hébergé** sans clé interne; cependant les moteurs en amont peuvent bloquer ou limiter les requêtes.
4. **Crawl4AI local** / **Playwright** pour exploration limitée à des domaines autorisés.
5. **Qdrant, pgvector, Chroma, sentence-transformers** en local.
6. **Whisper/faster-whisper et PaddleOCR** local.
7. Les APIs hosted Gemini/Groq/OpenRouter nécessitent normalement clé, même si le quota est gratuit. « Sans clé » ne vaut pas « gratuit » pour les services opérés par des tiers.

---

## 6. Compatibilité Python / Django

**Excellente** : Ollama via `httpx`/SDK, PydanticAI, LangGraph, Haystack, LlamaIndex, sentence-transformers, Qdrant client, pgvector, Chroma, Crawl4AI, Whisper, PaddleOCR, Django REST Framework, Celery.

**API HTTP fournisseur** : utiliser `httpx` ou le SDK Python officiel derrière une interface interne `LLMProvider`, `SearchProvider`, `EmbeddingProvider`. Implémenter timeout, retries exponentiels avec jitter, limites de concurrence, idempotence, journalisation des coûts et fallback.

**Architecture Django** : requête web courte et contrôlée dans Django; agents longs exécutés dans Celery/RQ et suivis par tâche; stockage des traces et confirmations humaines; pas d'exécution Python arbitraire dans le processus web. Secret manager ou environnement protégé, jamais `settings.py` commité. Django seul n'est pas le runtime d'agent.

---

## 7. Les 10 technologies les plus prometteuses

1. **MCP** pour un contrat standard d'outils; autoriser les serveurs explicitement et filtrer outils/arguments.
2. **OpenAI-compatible provider adapters** pour passer d'un hébergeur à un autre, sans confondre compatibilité API et licence ouverte.
3. **LangGraph** pour workflows persistants, interruptions humaines et reprises déterministes.
4. **PydanticAI** pour sorties contrôlées, dépendances et outils typés dans les applications Python.
5. **Qwen3 / modèles à poids permissifs** en local, sous réserve de vérifier la licence exacte de la version, des quantifications et des dérivés.
6. **Ollama + llama.cpp** pour inference locale accessible et quantifiée, sans coûts de requête.
7. **pgvector / PostgreSQL** pour réunir données métier, contrôle d'accès et mémoire; Qdrant si recherche vectorielle devient dominante.
8. **RAG hybride** (BM25 + vecteurs + reranker) plutôt que recherche vectorielle seule.
9. **Crawl4AI + SearXNG** pour acquisition web contrôlable et auto-hébergée, sous respect des conditions des sites.
10. **Evals/observabilité + garde-fous** : jeux de tests, traces locales OpenTelemetry, métriques d'appels, human approval, budget maximal et sandbox. Les garde-fous sont aussi importants que le modèle.

---

## 8. Tableau comparatif (résumé transversal)

| Solution | Catégorie | Open Source (code) | Gratuit | API URL | GitHub | Python | Commercial |
|---|---|---|---|---|---|---|---|
| Ollama | Inference locale | Oui, MIT | Oui local | `localhost:11434/api` | [ollama/ollama](https://github.com/ollama/ollama) | Oui | Runtime généralement oui; modèle séparé |
| Gemini API | LLM distant | Non | quota gratuit, variable | `generativelanguage.googleapis.com/v1beta` | SDK [googleapis/python-genai](https://github.com/googleapis/python-genai) | Oui | Conditions Google et modèle |
| Groq | Inférence hébergée | Non | palier limité | `api.groq.com/openai/v1` | [SDK](https://github.com/groq/groq-python) | Oui | Conditions service/modèle |
| OpenRouter | Gateway LLM | Non | certains `:free` | `openrouter.ai/api/v1` | [docs](https://openrouter.ai/docs) | Oui (OpenAI SDK) | fournisseur/modèle à vérifier |
| HF Inference | API modèle | Non pour service | crédits limités | `router.huggingface.co/v1` | [huggingface_hub](https://github.com/huggingface/huggingface_hub) | Oui | dépend du modèle/provider |
| Tavily | Recherche web | Non | quota mensuel limité | `api.tavily.com/search` | [SDK](https://github.com/tavily-ai/tavily-python) | Oui | Conditions SaaS |
| Brave Search | Recherche web | Non | crédits, vérifier carte | `api.search.brave.com/res/v1/web/search` | docs API | Oui, HTTP | Conditions SaaS |
| Exa | Recherche sémantique | Non | crédit selon offre | `api.exa.ai/search` | [exa-py](https://github.com/exa-labs/exa-py) | Oui | Conditions SaaS |
| SearXNG | Métarecherche | Oui, AGPL | Oui auto-hébergé | `/search` | [searxng/searxng](https://github.com/searxng/searxng) | HTTP | Oui, obligations AGPL à examiner |
| Crawl4AI | Crawler | Oui, Apache-2.0 | Oui local | lib locale / Cloud distinct | [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) | Natif | Oui, respecter sites |
| Firecrawl | Scraping | Oui, AGPL-3.0 principalement | local à héberger | `api.firecrawl.dev/v2` cloud | [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) | SDK | Oui sous AGPL/conditions |
| LangGraph | Agents | Oui, MIT | Oui | service optionnel | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | Natif | Oui |
| PydanticAI | Agents typés | Oui, MIT | Oui | service optionnel | [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) | Natif | Oui |
| CrewAI | Multi-agents | Oui, MIT | Oui local | cloud distinct | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | Natif | Oui |
| Qdrant | Vector DB | Oui, Apache-2.0 | Oui local | `localhost:6333` | [qdrant/qdrant](https://github.com/qdrant/qdrant) | SDK | Oui |
| pgvector | Vector SQL | Oui, PostgreSQL License | Oui local | PostgreSQL | [pgvector/pgvector](https://github.com/pgvector/pgvector) | psycopg/Django | Oui |
| Chroma | Vector DB | Oui, Apache-2.0 | Oui local | Python/HTTP | [chroma-core/chroma](https://github.com/chroma-core/chroma) | Natif | Oui |
| Whisper | STT | Oui, MIT | Oui local | pas d'API hébergée incluse | [openai/whisper](https://github.com/openai/whisper) | Natif | Code/poids MIT selon repo; dépendances |
| PaddleOCR | OCR | Oui, Apache-2.0 | Oui local | bibliothèque | [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | Natif | Vérifier poids |
| Playwright | Browser | Oui, Apache-2.0 | Oui local | bibliothèque | [microsoft/playwright](https://github.com/microsoft/playwright) | Natif | Oui; isoler navigateur |

**Classement qualitatif (1 = excellent)** — notes de sélection, pas benchmark indépendant, basées sur les compromis documentés et les licences ci-dessus.

| Solution | Puissance | Gratuité | Intégration | Docs | Potentiel commercial | Agent autonome |
|---|---:|---:|---:|---:|---:|---:|
| Ollama + Qwen local (selon matériel) | 3–4 | 5 | 5 | 4 | 4* | 4 |
| Gemini API (quota) | 5 | 3 | 5 | 5 | 3* | 5 |
| Groq (modèles disponibles) | 4 | 3 | 5 | 4 | 3* | 4 |
| LangGraph | 5 | 5 | 4 | 5 | 5 | 5 |
| PydanticAI | 4 | 5 | 5 | 4 | 5 | 4 |
| CrewAI | 4 | 5 | 4 | 4 | 5 | 4 |
| SearXNG | 3 | 5 | 3 | 4 | 4* | 3 |
| Tavily | 4 | 2 | 5 | 4 | 3* | 4 |
| Qdrant | 4 | 5 | 4 | 5 | 5 | 4 |
| pgvector | 4 | 5 | 5 | 5 | 5 | 4 |

`*` dépend de la licence du modèle, du contrat, de la juridiction et de l'usage des données. Les niveaux de gratuité des SaaS sont faibles à moyens parce qu'ils sont limités et non garantis.

---

## 9. Architecture technique recommandée

```text
Navigateur (HTML5 + Bootstrap + JS)
        │ HTTPS / session CSRF
Django + Django REST Framework
        ├── AuthN/AuthZ, validation, quota utilisateur, audit
        ├── Interface providers: LLM / Search / Embeddings / OCR / STT
        ├── Agent service: PydanticAI simple OU LangGraph workflow stateful
        ├── Policy engine: allowlist d'outils, approbation humaine, limites
        └── Celery worker + Redis (tâches longues, retries bornés)
              ├── LLM local Ollama OU adaptateur API hosted
              ├── Recherche: SearXNG local + fournisseur optionnel Tavily/Exa
              ├── Fetch: Crawl4AI/Playwright dans conteneur isolé
              ├── Documents: OCR PaddleOCR + extraction/PDF
              ├── STT/TTS: faster-whisper + moteur TTS à licence validée
              └── Exécution Python: worker éphémère isolé, sans réseau par défaut
        │
Stockage prototype: SQLite + fichiers locaux
Production: PostgreSQL + pgvector (ou Qdrant), stockage objet, Redis
```

### Principes d'implémentation
- **Modularité** : définissez des protocoles internes `ChatModel.complete()`, `Search.search()`, `Embed.encode()`, `VectorStore.upsert/query()`. Fournisseurs configurables par `.env`, sans imports fournisseur dans les vues Django.
- **Données** : `DATABASE_URL`, `LLM_BASE_URL`, `LLM_API_KEY`, `MODEL_ID`, `SEARCH_PROVIDER`, `SEARCH_API_KEY`, `VECTOR_BACKEND`, `MAX_AGENT_STEPS`, `MAX_TOOL_SECONDS`, `MAX_DAILY_TOKENS`; `.env` hors Git, fichier `.env.example` sans secret.
- **Mémoire** : court terme = état du workflow/conversation; long terme = PostgreSQL et vecteurs avec `user_id`/tenant filter obligatoire. Ajouter durée de rétention, suppression exportable, provenance et date d'ingestion.
- **Fiabilité** : tâches asynchrones idempotentes, timeouts, limites de tokens et d'étapes, retries plafonnés, cache avec TTL, journal d'audit, backoff, circuit breaker et déduplication des résultats.
- **Sécurité** : l'exécution Python arbitraire et le navigateur ne doivent jamais tourner dans le processus Django. Utiliser conteneur/VM à usage unique, non-root, limites CPU/RAM/temps, système de fichiers éphémère, réseau désactivé par défaut, secrets non montés. Le `subprocess` seul n'est pas un sandbox.
- **Prompt injection** : traiter pages, PDFs et résultats comme données hostiles; ne jamais leur conférer le droit de changer les règles système; séparer lecture/action et demander confirmation pour email, achat, suppression, publication ou écriture externe.
- **Production** : SQLite est prototype mono-instance; PostgreSQL dès que concurrence, tâches et mémoire comptent. Les coûts API/hébergement persistent même si les bibliothèques sont gratuites.

---

## 10. TOP 5 combinaisons technologiques

1. **Zéro SaaS / poste ou serveur modeste** : Django + PydanticAI + Ollama (Qwen3 quantifié) + sentence-transformers + pgvector + Whisper. Simple et local; qualité LLM variable et matériel limitant.
2. **Agent fiable à étapes et validation humaine** : Django + LangGraph + PostgreSQL checkpoint/pgvector + Ollama en dev, fallback Gemini/Groq configurable + SearXNG. Contrôle explicite et bon chemin d'évolution.
3. **RAG documentaire Django classique** : Django + Haystack + PostgreSQL/pgvector + PaddleOCR + faster-whisper + modèle local; add Qdrant si la recherche devient dominante.
4. **Recherche web efficace** : LangGraph/PydanticAI + Tavily (quota gratuit si actif) + Crawl4AI local pour pages autorisées + Qdrant + modèle local/API de secours. Ne pas dépendre d'un quota gratuit pour un service client.
5. **Prototype multimodal sans GPU serveur** : Django + Gemini API sur quota (si disponible dans la région et acceptable pour les données) + Tavily/Exa quota + pgvector + Playwright local. À convertir vers modèles locaux ou contrat payant avant mise en production.

## 11. Recommandation finale — construire à 0 €

Commencer avec une **boucle d'agent mono-agent** (pas une équipe multi-agent) sous PydanticAI ou fonctions Python simples : modèle local Ollama; modèle Qwen téléchargé après vérification de sa carte/licence exacte; Django; SQLite; `sentence-transformers` + pgvector lorsque PostgreSQL est installé; SearXNG/Crawl4AI local; Playwright avec allowlist; Whisper et PaddleOCR uniquement si nécessaires. Mettre une approbation humaine avant toute action irréversible.

Limiter à 3–5 étapes par tâche, 2–4 outils autorisés, taille maximale d'import, durée maximale, budget de tokens et journaliser toutes les actions. Comparer chaque version de prompt/modèle sur un petit jeu d'évaluation français reproductible (exactitude, citations, réussite d'outil, latence et coût). Ajouter LangGraph seulement si persistance, interruptions ou branches complexes le justifient.

**Pas d'infrastructure coûteuse** ne veut pas dire modèle frontier gratuit : une machine CPU peut exécuter un petit modèle, pas garantir une intelligence de niveau cloud. Pour meilleure qualité à coût de zéro au début, tester un quota gratuit distant mais isoler les données sensibles et garder le local comme repli. Avant toute vente, auditer la licence des poids, du TTS, des dépendances et des services; le code MIT/Apache ne donne aucun droit automatique sur les modèles ou données.

---

## Sources vérifiées / points d'appui

- Cadre modèle et API : [Ollama API](https://docs.ollama.com/api), [Gemini docs](https://ai.google.dev/gemini-api/docs), [Groq docs](https://console.groq.com/docs/quickstart), [OpenRouter docs](https://openrouter.ai/docs), [HF inference docs](https://huggingface.co/docs/inference-providers/index), [NVIDIA NIM](https://docs.nvidia.com/nim/), [Mistral docs](https://docs.mistral.ai/), [Cohere docs](https://docs.cohere.com/).
- Recherche/crawl : [Brave API](https://api.search.brave.com/app/documentation), [Tavily docs](https://docs.tavily.com/), [Exa docs](https://docs.exa.ai/), [SearXNG API](https://docs.searxng.org/dev/search_api.html), [Firecrawl API et licence](https://github.com/firecrawl/firecrawl), [Crawl4AI docs](https://docs.crawl4ai.com/).
- Orchestration : [LangGraph repo](https://github.com/langchain-ai/langgraph), [PydanticAI](https://github.com/pydantic/pydantic-ai), [CrewAI](https://github.com/crewAIInc/crewAI), [Google ADK](https://github.com/google/adk-python), [Haystack](https://github.com/deepset-ai/haystack), [LlamaIndex](https://github.com/run-llama/llama_index), [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk).
- Mémoire/ML : [Qdrant](https://github.com/qdrant/qdrant), [Chroma](https://github.com/chroma-core/chroma), [pgvector](https://github.com/pgvector/pgvector), [Transformers](https://huggingface.co/docs/transformers), [Sentence Transformers](https://sbert.net/).
- Vision/audio/automation : [Whisper](https://github.com/openai/whisper), [faster-whisper](https://github.com/SYSTRAN/faster-whisper), [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR), [Playwright](https://playwright.dev/python/), [Django](https://docs.djangoproject.com/), [Celery](https://docs.celeryq.dev/).
- Recherches complémentaires : [licences des frameworks (analyse comparative, août 2026)](https://agentsindex.ai/blog/open-source-ai-agent-frameworks-licence-check); [comparatif de recherche web, novembre 2026](https://parallel.ai/articles/best-free-web-search-api); les pages officielles ci-dessus doivent faire autorité pour tarifs, quotas et licences avant implémentation.
