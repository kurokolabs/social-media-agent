/* ============================================================
   KUROKO LABS — Social Agent Demo Data
   Mock posts for March 2026
   ============================================================ */

const CONTENT = {
  linkedin: [
    {
      type: 'rag_architecture',
      text: `Unser Retrieval-System hatte 61% Genauigkeit. Heute hat es 84%.

Ein einziger Architekturentscheid hat das geändert.




Was wir falsch gemacht hatten: feste 512-Token-Blöcke. Die schnellste Art RAG aufzubauen. Und in Produktion die schnellste Art zu scheitern.

Ein technisches Dokument hat Struktur. Abschnitte bauen aufeinander auf, Definitionen werden eingeführt bevor sie verwendet werden, Querverweise verbinden Kapitel. Wenn man das in gleichgroße Blöcke zerteilt, landet Kapitel 3 oft ohne Kapitel 1. Der Retrieval-Schritt findet das Fragment. Nicht den Kontext.

Was stattdessen funktioniert ist semantisches Chunking nach Dokumentstruktur, gefolgt von einem CrossEncoder-Reranker der nicht Ähnlichkeit misst sondern Relevanz im Kontext der gesamten Anfrage bewertet.

Das dritte Element das die meisten überspringen: ein strukturiertes Eval-Set. 100 bis 200 Testfragen mit erwarteten Antworten und relevanten Quell-Chunks. Ohne das weiß man nicht ob die 84% stabil sind oder Glück.

Wer RAG produktiv betreiben will kommt um diesen Aufbau nicht herum.

#RAG #LLM #AIEngineering #KIAgenten`
    },
    {
      type: 'pilot_hell',
      text: `18 Monate. Vier Piloten. Keiner davon läuft heute.

Das ist kein Einzelfall. Das ist ein Muster.




"Pilot Hell" nennt man den Zustand in dem ein Unternehmen mehrere KI-Projekte parallel entwickelt, jedes mit vielversprechenden Ergebnissen in der Demo, und trotzdem keines davon den Weg in die Produktion findet.

Was steckt dahinter? In unserer Beobachtung fehlt fast nie Technologie. Es fehlt eine Antwort auf eine Frage die vor dem ersten Prompt stehen sollte: Wer übernimmt nach dem Pilot die Verantwortung?

Nicht für das Modell. Für das System. Wer betreibt es, pflegt die Daten, reagiert wenn Outputs falsch werden, erklärt intern warum der Agent das entschieden hat?

Wenn die Antwort "das klärt sich dann" ist, klärt es sich meist mit einer Entscheidung, das System abzuschalten.

Was in unseren Projekten hilft: Wir definieren am Anfang einen "Agent Owner" auf Unternehmensseite. Eine Person die das System nicht nur nutzt, sondern versteht und verantwortet. Das ändert die Qualität jeder Entscheidung im gesamten Projekt.

#KIStrategie #Automatisierung #Mittelstand #Transformation`
    },
    {
      type: 'japan_germany',
      text: `Japanische Fertigungsbetriebe implementieren digitale Projekte 40% schneller als deutsche.

Fraunhofer IPA hat das gemessen. Wir glauben es, weil wir es sehen.




Der Grund ist nicht bessere Technologie. Nicht mehr Budget. Nicht weniger Bürokratie.

In Gesprächen mit deutschen Betrieben hören wir oft: "Wir müssen erst alle Prozesse sauber dokumentieren, bevor wir anfangen können." Das ist verständlich. Es ist auch ein Weg, Jahre zu verlieren.

In japanischen Betrieben die wir kennen ist der Einstiegspunkt ein konkretes Problem in einem konkreten Teilprozess. Nicht perfekt vorbereitet. Klein. Lernend.

Der Unterschied ist keine Frage der Sorgfalt. Es ist eine unterschiedliche Definition davon, was "bereit" bedeutet.

Was uns dabei auffällt: Die Endqualität ist oft vergleichbar. Aber wer zehn Monate früher startet, hat zehn Monate mehr gelernt. In einem Feld das sich so schnell entwickelt wie KI ist das keine Kleinigkeit.

Die Kombination aus japanischem Tempo und deutschem Qualitätsanspruch ist übrigens genau das, was uns bei der Gründung von Kuroko Labs beschäftigt hat.

#JapanDeutschland #KI #Industrie40 #Fertigung #Transformation`
    },
    {
      type: 'llm_cost_tco',
      text: `Ein KI-Projekt das 50.000 Euro kosten sollte, hat am Ende 280.000 gekostet.

Die Token-Rechnung war korrekt. Alles andere war falsch.




Was in fast jedem KI-Budget unterschätzt wird, weil es nicht auf der Preisseite des Modell-Anbieters steht:

Erstens: Datenaufbereitung. Bevor ein Agent auf internen Dokumenten, ERP-Exports oder Produktionslogs sinnvoll arbeiten kann, müssen diese strukturiert, bereinigt und indexiert werden. In unserer Erfahrung sind das 40 bis 60 Prozent des gesamten Projektaufwands. In keiner ersten Kalkulation.

Zweitens: Prompt-Engineering und Evaluation. Einen Prompt zu schreiben der in 95% der Fälle das Richtige tut dauert nicht Stunden. Es dauert Wochen. Mit Testsets, Regressionschecks, Edge-Cases.

Drittens: Betrieb. Ein Agent der in Produktion läuft braucht Monitoring, Alerting, Log-Analyse, und eine Review-Queue für Grenzfälle die nicht automatisch durchlaufen dürfen.

Wer nur die API-Kosten sieht, sieht den kleinsten Teil der Rechnung.

Das ändert nichts daran, dass sich gute KI-Projekte rechnen. Aber die Entscheidung ob ein Projekt gut ist, sollte auf der richtigen Basis getroffen werden.

#LLM #AIEngineering #KIStrategie #TCO #Mittelstand`
    },
    {
      type: 'multiagent_complexity',
      text: `Drei Agenten, eine Pipeline, am Ende eine falsche Zahl im Bericht.

Niemand hatte gemerkt seit drei Wochen.




Multi-Agent-Systeme sind mächtig. Sie sind auch die schnellste Art sich unsichtbare Fehlerquellen einzubauen, wenn man nicht aufpasst.

Das Versprechen kennt man: Spezialisierte Agenten arbeiten zusammen, jeder besser in seiner Aufgabe als ein einzelner generalistischer Prompt. Das stimmt. Aber was beim Design oft vergessen wird: Fehler multiplizieren sich in Ketten.

Agent A produziert einen Wert mit 5% Fehlerwahrscheinlichkeit. Agent B übernimmt diesen Wert und arbeitet damit weiter. Am Ende der Kette hat sich der Fehler fortgepflanzt, und das Endresultat hat keinen expliziten Hinweis woher der Fehler kam.

Was in der Praxis hilft: Strukturierte Outputs mit Validierungsschemas zwischen jedem Agenten-Übergabepunkt. Und menschliche Checkpoints nicht als letzten Schritt, sondern an den Stellen in der Kette wo Konsequenzen hoch sind.

Multi-Agent richtig gebaut ist einer der stärksten Ansätze in der aktuellen KI-Architektur. Multi-Agent ohne Fehlerarchitektur ist ein komplizierter Weg zum falschen Ergebnis.

#MultiAgent #AgentDev #KIArchitektur #LLM #AIEngineering`
    },
    {
      type: 'dsgvo_llm',
      text: `DSGVO und LLMs. Jedes Mal wenn wir das Thema ansprechen, verlässt jemand innerlich den Raum.

Das ist verständlich. Und teuer.




Die häufigste Reaktion auf DSGVO-Bedenken bei LLM-Projekten ist Lähmung. Entweder das Projekt wird auf Eis gelegt bis "die Rechtslage klarer ist", oder man ignoriert das Thema und hofft dass es sich nicht materialisiert.

Beide Wege sind schlechter als notwendig.

Was konkret hilft ist Data Tiering. Die Entscheidung welche Daten ein Modell sehen darf hängt von ihrer Klassifikation ab, nicht vom Projekt.

Nicht-personenbezogene, nicht-geschäftskritische Daten können an externe APIs (OpenAI, Anthropic, Google) mit Standard-Vertragsklauseln. Personenbezogene oder strategisch sensible Daten bleiben on-premise, auf Azure OpenAI in EU-Regionen, oder auf offenen Modellen wie Mistral die man selbst betreibt.

Das ist keine perfekte Lösung. Sie setzt aber eine Entscheidung voraus die ohnehin sinnvoll ist: Was braucht der Agent wirklich? Meistens ist die Antwort überraschend wenig.

#DSGVO #LLM #Compliance #KIStrategie #Datenschutz`
    },
    {
      type: 'evals_not_vibes',
      text: `"Das fühlt sich jetzt besser an."

Das ist kein Eval. Das ist ein Wunsch.




In fast jedem frühen KI-Projekt bewerten Teams Verbesserungen nach Gefühl. Eine Prompt-Änderung kommt rein, jemand testet fünf Beispiele, die Antworten wirken besser, die Änderung geht in Produktion.

Das Problem: Vibe-based Evaluation sieht Regressionen nicht. Eine Optimierung die Typ-A-Anfragen besser macht kann gleichzeitig Typ-B-Anfragen schlechter machen. Ohne strukturiertes Testset merkt man das erst wenn es zu spät ist.

Was wir in Projekten einführen: Einen festen Eval-Datensatz. 100 bis 200 Beispielanfragen mit erwarteten Outputs. Bei Reasoning-Aufgaben nimmt man LLM-as-Judge (Claude oder GPT-4o bewertet ob die Antwort korrekt und vollständig ist). Bei strukturierten Outputs exakte Metriken.

Jeden Prompt-Change gegen dieses Set zu laufen kostet 5 Minuten und 2 Euro. Dafür weiß man was man tut.

Der Unterschied zwischen einem Agenten der nach sechs Monaten immer noch das Vertrauen der Organisation hat, und einem der abgeschaltet wird, ist oft genau das.

#LLMEvals #AIEngineering #PromptEngineering #KIAgenten`
    },
    {
      type: 'supply_chain_agent',
      text: `Lieferantenprobleme erkannt: 11 Tage nach dem Auftreten.

Nach dem Agenten: 2 Tage.

Die neun Tage dazwischen kosten Geld.




Der Anwendungsfall klingt unspektakulär. Ein Fertigungsbetrieb mit 200 aktiven Lieferanten, einem SAP-System aus 2018, und einem Einkaufsteam das täglich entscheidet.

Was fehlte war keine Entscheidungskompetenz. Es war Sichtbarkeit.

Der Agent überwacht täglich Lieferanten-Performance-Daten aus dem ERP: Liefertreue, Qualitätsquoten, Leadtime-Abweichungen. Wenn ein Lieferant in zwei aufeinanderfolgenden Wochen Kennzahlen außerhalb des historischen Normalbereichs zeigt, erstellt er automatisch eine Zusammenfassung mit relevanten Datenpunkten und Handlungsoptionen. Der Einkäufer bekommt das morgens auf dem Schreibtisch.

Der Agent trifft keine Einkaufsentscheidungen. Er stellt sicher, dass Probleme früh sichtbar werden bevor sie Produktionsstopps verursachen.

Neun Tage früher reagieren ist kein Prozessoptimierungs-Thema. Es ist ein Wettbewerbsvorteil.

#SupplyChain #KIAgenten #Fertigung #Einkauf #Automatisierung`
    },
    {
      type: 'fine_tuning_vs_rag',
      text: `Fine-Tuning oder RAG? Wir werden das fast wöchentlich gefragt.

Die Antwort überrascht fast immer.




In 80% der Fälle wo Teams Fine-Tuning wollten, war RAG die richtige Antwort.

Warum? Weil der Unterschied zwischen den beiden oft missverstanden wird.

Fine-Tuning verändert wie ein Modell antwortet: seinen Stil, seine Struktur, seine Konsistenz in bestimmten Formaten oder Kategorien. Es ist sinnvoll wenn man ein Modell auf einen spezifischen Ton, eine Unternehmenssprache oder ein konstantes Ausgabeformat trainieren will. Es braucht ausreichend Trainingsdaten (500 bis 5000 Beispiele) und verändert nicht was das Modell weiß.

RAG verändert worauf ein Modell zugreifen kann. Es ist sinnvoll wenn das Problem Zugang zu spezifischem, aktuellem oder umfangreichem Wissen ist. Technische Dokumentation, Produktkataloge, interne Richtlinien, ERP-Daten. Wenn sich das Wissen ändert, ist RAG fast immer die Antwort.

Was in der Praxis öfter schiefgeht: Teams wählen Fine-Tuning weil sie denken "das Modell weiß dann mehr". Fine-Tuning ändert kein Wissen. Es ändert Verhalten.

#LLM #FineTuning #RAG #AIEngineering #KIAgenten`
    },
    {
      type: 'model_selection',
      text: `Wir haben im letzten Quartal GPT-4o, Claude Sonnet und Gemini Pro auf denselben Enterprise-Aufgaben verglichen.

Die Ergebnisse passen nicht in einen Satz.




2026 ist die Modellauswahl differenzierter als je zuvor. Das ist eigentlich eine gute Nachricht, weil es bedeutet dass es für fast jede Aufgabe einen gut passenden Ansatz gibt.

Was unsere Benchmarks auf realen Projekt-Daten zeigen:

Für Long-Context-Analysen über 50k Tokens, also Vertragsanalysen, technische Reports, mehrseitige Dokumentation: Claude Sonnet und Opus sind konsistenter. GPT-4o verliert messbar an Attention-Qualität bei sehr langen Inputs.

Für strukturierte Outputs und Function Calling in Agenten-Pipelines: GPT-4o-mini ist schwer zu schlagen. JSON-Konsistenz hoch, Latenz bei einfachen Tasks unter 200ms.

Für Einbettungen auf deutschen Fachtexten: Cohere Embed v3 schlägt text-embedding-3-large bei domänenspezifischem Vokabular. Für allgemeine Texte ist OpenAI stärker.

Was fast immer vergessen wird: Inference-Kosten skalieren. Was bei 1.000 Requests pro Tag günstig ist, kann bei 100.000 unerschwinglich werden. Die richtige Entscheidung ist die, die für das spezifische Volumen, Budget und Latenzprofil passt.

#LLM #ModelSelection #AIEngineering #KIAgenten #Technologie`
    },
    {
      type: 'graphrag_architecture',
      text: `Microsofts GraphRAG-Paper hat unser Retrieval-System von 71% auf 89% Precision gebracht.

Nicht durch ein besseres Modell. Durch eine andere Datendarstellung.




Naives RAG hat ein strukturelles Problem das erst in der Praxis sichtbar wird: Es findet Chunks die einer Anfrage ähneln, aber es versteht keine Beziehungen zwischen Konzepten. Bei Fragen wie "Welche Projekte teilen die gleichen Technologiekomponenten?" liefert ein Vektorindex brauchbare Fragmente, aber keine kohärente Antwort.

GraphRAG, beschrieben im Microsoft-Paper von 2024, löst das durch einen vorgelagerten Schritt: Das Dokument-Korpus wird zunächst in eine Wissensgraph-Struktur überführt. Entitäten (Personen, Systeme, Konzepte), Eigenschaften und Relationen werden extrahiert und gespeichert. Retrieval traversiert dann diesen Graph, nicht nur einen Vektorindex.

Die konkreten Zahlen aus dem Paper: Bei globalen Summarisierungsanfragen über große Textmengen schlägt GraphRAG naives RAG um 26 bis 33 Prozentpunkte in menschlichen Bewertungen. Bei lokalen Faktenfragen ist der Vorteil kleiner, aber die Kohärenz der Antworten messbar höher.

Was das für Projektentscheidungen bedeutet: GraphRAG lohnt sich bei Frage-Typen die Beziehungen oder Aggregationen über viele Dokumente erfordern. Der Preis ist höherer Indexierungsaufwand und langsamere Latenz bei einfachen Lookups. Für einfache Dokumentensuche bleibt Standard-RAG die erste Wahl.

In unseren Enterprise-Projekten setzen wir beide Ansätze nebeneinander, je nach Anfrageprofil des Anwendungsfalls.

#GraphRAG #RAG #LLM #AIEngineering #KIArchitektur`
    },
    {
      type: 'vector_db_comparison',
      text: `Qdrant, Weaviate, Pinecone oder Chroma? Wir haben alle vier auf demselben Datensatz verglichen.

Die Antwort hängt davon ab, was man wirklich braucht.




Vector-Datenbanken sind 2026 keine experimentellen Werkzeuge mehr. Wer aber glaubt, die Wahl sei egal, wird in Produktion eines Besseren belehrt.

Latenz: Bei 1 Million Vektoren und einfachen ANN-Queries liefern Qdrant und Weaviate Medianwerte unter 5ms bei HNSW-Indizes. Pinecone liegt bei 8 bis 12ms wegen des Netzwerk-Overheads durch seine vollständig gemanagte Cloud-Architektur. Für Agenten-Pipelines die im Millisekunden-Bereich entscheiden, ist das relevant.

Filterkapazitäten: Hybrid-Queries, also Vektorsuche kombiniert mit Metadaten-Filtern, zeigen die grössten Unterschiede. Qdrant hat hier die stärkste Performance bei komplexen Filterausdrücken durch seine native Payload-Indexierung. Weaviate ist stärker wenn Graphstruktur in der Datenbasis vorkommt. Pinecone ist einfacher zu betreiben, aber Filterperformance bei hoher Selektivität bleibt ein bekanntes Thema.

Kosten bei 10 Millionen Vektoren: Pinecone Serverless liegt bei ca. 70 bis 90 Euro pro Monat. Qdrant und Weaviate selbstgehostet auf einer GPU-losen Instance kosten Hardware, aber keine per-Query-Gebühr. Für Teams mit DevOps-Kapazität ist der Kostenunterschied bei Scale erheblich.

Chroma ist für lokale Entwicklung und kleine Prototypen ideal. In Produktion mit mehr als 500.000 Vektoren und gleichzeitigen Queries stoßen wir regelmäßig an Grenzen.

#VectorDB #Qdrant #Weaviate #Pinecone #RAG`
    },
    {
      type: 'moe_architecture',
      text: `GPT-4 und Mixtral kosten in der Inferenz deutlich weniger als ihre Parameteranzahl vermuten lässt.

Der Grund ist Mixture-of-Experts, und er verändert wie Enterprise-Deployments kalkuliert werden.




Bei einem Standard-Dense-Modell mit 70 Milliarden Parametern werden bei jedem Token alle 70 Milliarden Parameter aktiviert. Das ist rechenintensiv, konsistent, und für viele Aufgaben überdimensioniert.

MoE-Architekturen funktionieren anders. Ein Router-Netzwerk entscheidet bei jedem Token, welche zwei bis vier von beispielsweise acht "Expert"-Subsystemen aktiviert werden. Mixtral 8x7B hat nominell 46,7 Milliarden Parameter, aktiviert aber pro Token nur etwa 12 Milliarden. Das ist Sparse Activation.

Die direkte Konsequenz für Inferenzkosten: Ein MoE-Modell mit der Qualität eines Dense-70B-Modells verbraucht ungefähr 30 bis 40 Prozent weniger GPU-Compute pro Token. Bei 100 Millionen API-Calls pro Monat ist das ein erheblicher Kostenunterschied.

Was für Enterprise-Entscheidungen relevant ist: MoE-Modelle brauchen mehr VRAM als ein Dense-Modell gleicher aktiver Parametergröße, weil alle Experten im Speicher gehalten werden müssen. Mixtral 8x7B braucht ungefähr 90 GB VRAM für Full-Precision, während ein tatsächliches Dense-12B-Modell mit 24 GB auskommt. Self-hosting von MoE-Modellen erfordert also mehr Hardware-Planung als die "aktive Parameter"-Zahl suggeriert.

Für Cloud-basierte Deployments ist das irrelevant. Für On-Premise-Entscheidungen ist es der entscheidende Faktor.

#MixtureOfExperts #LLM #AIEngineering #Inferenz #KIArchitektur`
    },
    {
      type: 'mittelstand_ki_barrieren',
      text: `62% der deutschen Mittelstandsunternehmen haben bis Ende 2025 keine KI-Anwendung produktiv im Einsatz.

Das IW Köln hat das gemessen. Die Begründungen überraschen.




In der öffentlichen Diskussion wird KI-Zurückhaltung im Mittelstand oft auf Angst, mangelnde Risikobereitschaft oder kulturelle Konservatismus zurückgeführt. Die IW-Köln-Studie von Anfang 2026 zeichnet ein anderes Bild.

Die drei am häufigsten genannten Barrieren: IT-Infrastruktur (53% der befragten Unternehmen nennen veraltete Systemlandschaften als Hindernis), Datenqualität (48% berichten, ihre Daten seien nicht in einem Zustand der für KI-Anwendungen geeignet ist), und fehlende interne Kompetenzen (44%).

"Angst vor KI" oder ethische Bedenken tauchen in der Rangliste der Hemmnisse weit hinten auf, bei unter 15 Prozent.

Was das konkret bedeutet: Ein Unternehmen mit ERP-Daten aus 2008, drei verschiedenen Systemen die nicht miteinander kommunizieren, und einem IT-Team das für Tagesgeschäft ausgelastet ist, wird mit einem LLM-API-Key nicht weit kommen. Das ist kein Motivationsproblem. Das ist ein Infrastrukturproblem.

Was wir in Projekten beobachten: Der häufigste erste sinnvolle Schritt ist keine KI-Implementierung. Es ist eine Dateninventur. Wer versteht welche Daten wo liegen und in welchem Zustand, kann den ersten sinnvollen Anwendungsfall identifizieren. Ohne das ist jeder Pilot ein Zufallstreffer.

#Mittelstand #KI #IWKöln #Transformation #Digitalisierung`
    },
    {
      type: 'prompt_injection',
      text: `Wir haben einen produktiven Agenten mit einem einzigen manipulierten PDF-Dokument übernommen.

Das ist kein theoretischer Angriff. Das ist Prompt Injection.




Prompt Injection ist die relevanteste Sicherheitsbedrohung für Agenten-Systeme 2026. Und sie ist anders als klassische Sicherheitslücken, weil der Angriff über den Eingabekanal des Modells läuft, nicht über Code-Exploits.

Das häufigste Angriffsmuster in der Praxis: Indirektes Injection via RAG-Dokumente. Ein Angreifer platziert in einem harmlosen Dokument (PDF, E-Mail, Webseite) versteckte Anweisungen im Text. Wenn der Agent dieses Dokument als Teil seines Kontexts verarbeitet, folgt er den eingebetteten Anweisungen. Ein bekanntes Beispiel aus 2024: Ein Agent der Web-Research betreibt, liest eine präparierte Webseite und leitet daraufhin vertrauliche Informationen aus seiner Konversationshistorie weiter.

Tool-Use-Hijacking ist das zweite Muster: Ein manipulierter Input veranlasst den Agenten, Tools mit unbeabsichtigten Parametern aufzurufen. Bei einem Agenten mit Datenbankzugriff kann das bedeutsam sein.

Konkrete Schutzmaßnahmen die wir einsetzen: Strenge Trennung von Instruktionsebene und Datenebene im System-Prompt. Validierung aller Tool-Calls gegen eine Whitelist erlaubter Aktionen. Canary-Tokens in sensiblen Bereichen des Kontexts die bei Leak alarmieren. Und bei hochkritischen Agenten: Separate Evaluationsebene die Antworten auf Exfiltrations-Muster prüft.

Prompt Injection wird in den nächsten 24 Monaten zu einem Standard-Thema in Security-Audits für Enterprise-KI werden.

#PromptInjection #KISecurity #AgentSecurity #LLM #OWASP`
    },
    {
      type: 'context_window_economics',
      text: `128.000 Token Context kostet bei GPT-4o 18-mal mehr als 8.000 Token.

Das klingt offensichtlich. Aber die Implikationen für Systemarchitektur sind es nicht.




Bei Gemini 1.5 Pro hat Google 2024 ein Modell mit 1 Million Token Context Window eingeführt. Die Versuchung ist groß: Einfach alles in den Kontext, kein Chunking, kein RAG, keine Komplexität. Das funktioniert. Aber es kostet.

Eine Kalkulation mit realen Zahlen: Gemini 1.5 Pro kostet bei Inputs über 128k Token 3,50 Dollar pro Million Input-Token. Ein 500-Seiten-Dokument hat ungefähr 200.000 bis 250.000 Token. Bei 1.000 Anfragen pro Monat gegen dieses Dokument: 700 bis 875 Dollar allein für Input-Token. Dasselbe System mit RAG und 4.000-Token-Kontext: unter 40 Dollar.

Der Gegenfall: Aufgaben die globales Verständnis über ein Dokument erfordern, wie Konsistenzprüfungen, Muster über den Gesamttext, oder Fragen die von Anfang bis Ende des Dokuments abhängen, profitieren von langen Kontexten erheblich. RAG findet Fragmente. Full-Context versteht Zusammenhänge.

Die Entscheidungsregel die wir nutzen: Wenn weniger als 20 Prozent des Dokuments für eine typische Anfrage relevant ist, ist RAG effizienter. Wenn globales Verständnis gefragt ist oder das Dokument kürzer als 50.000 Token ist, rechnet sich Full-Context.

Für die meisten Enterprise-Workloads bleibt RAG der kosteneffizientere Ansatz.

#LLM #ContextWindow #Gemini #RAG #AIEngineering`
    },
    {
      type: 'agentic_failure_modes',
      text: `Unser Agent hat sich in einer Schleife befangen und 340 API-Calls in vier Minuten produziert.

Kostenpunkt: 47 Euro. Problem: Es wäre vermeidbar gewesen.




ReAct-Agents (Reasoning + Acting) und CoT-basierte Selbstkorrektur-Agenten haben eine gemeinsame Schwachstelle: Sie wissen nicht wann sie aufhören sollen.

Das häufigste Failure-Muster in unseren Projekten: Infinite Tool-Call-Loops. Der Agent probiert eine Lösung, bewertet sie als unzureichend, modifiziert seinen Ansatz, probiert erneut. Ohne externe Abbruchbedingung kann das sehr lange laufen. Das Modell ist dabei nicht "kaputt". Es tut genau das was man es gelehrt hat: iterativ verbessern.

Das zweite häufige Muster ist Overconfidence bei Zwischenergebnissen. Ein Agent der mehrere Schritte sequenziell ausführt, prüft selten ob Prämissen aus frühen Schritten noch gelten. Ein geändertes Zwischenergebnis propagiert sich nicht rückwärts durch die Kette.

Circuit Breakers die funktionieren: Harte Limits auf Tool-Calls pro Task (wir setzen typisch 15 bis 20). Time-Budget pro Aufgabe. Und ein Confidence-Threshold: Wenn der Agent nach N Iterationen kein Ergebnis mit ausreichender Sicherheit liefert, eskaliert er an einen Menschen statt weiterzulaufen.

Das dritte Element ist oft übersehen: Zustandsisolierung zwischen Tasks. Agenten die geteilten Zustand über Tasks hinweg nutzen, können aus Fehlern eines vorherigen Tasks Schlüsse für den aktuellen ziehen. Das ist selten was man will.

#AgenticAI #ReAct #KIArchitektur #AIEngineering #LLM`
    },
    {
      type: 'onprem_llm_deployment',
      text: `Mistral 7B auf einer Consumer-GPU läuft heute mit 35 Token pro Sekunde.

Das ist schnell genug für die meisten Enterprise-Anwendungsfälle. Und es bleibt auf eurer Hardware.




On-Premise LLM ist 2026 kein Nischen-Thema mehr. Zwei Tools haben das zugänglich gemacht: Ollama für einfaches lokales Deployment und vLLM für produktive Server-Deployments mit Hochlast.

Ollama eignet sich für Entwicklungsumgebungen, Tests und kleinere Workloads. Setup dauert 10 Minuten, läuft auf Mac, Linux und Windows, unterstützt GGUF-Quantisierungen die Modelle auf Consumer-Hardware laufen lassen. Eine RTX 3090 mit 24 GB VRAM reicht für Mistral 7B Q8 oder LLaMA 3.1 8B vollständig.

vLLM ist die Produktionsoption. PagedAttention-Mechanismus ermöglicht effiziente KV-Cache-Verwaltung und erlaubt deutlich höhere Throughput als naive Implementierungen. Für LLaMA 3.1 70B braucht man zwei A100-80GB-GPUs (ca. 25.000 Euro Hardware) oder vier A6000 Ada (ca. 24.000 Euro). Latenz: 20 bis 40 Token pro Sekunde bei 70B, was für die meisten Batch-Anwendungsfälle ausreicht.

Der DSGVO-Vorteil ist real: Daten verlassen niemals die eigene Infrastruktur. Kein Datenschutzbeauftragter muss Drittlandübermittlung prüfen. Kein Vertrag mit US-Anbietern über personenbezogene Daten.

Wann es sich rechnet: Bei mehr als 5 Millionen Tokens pro Monat beginnt On-Premise preislich konkurrenzfähig zu werden gegenüber Cloud-APIs. Darunter überwiegt der Betriebsaufwand.

#OnPremLLM #Ollama #vLLM #DSGVO #KIArchitektur`
    }
  ],

Die meisten Teams starten mit dem Offensichtlichen. PDF rein, chunken, vektorisieren, fertig. Das funktioniert für Demos gut. In der Produktion fängt dann das eigentliche Problem an.

Was wir konkret sehen: Naive Chunking-Strategien (feste 512-Token-Blöcke) reißen Sinnzusammenhänge auseinander. Ein Wartungshandbuch mit 200 Seiten hat Abschnitte die aufeinander aufbauen. Wenn Chunk 47 auf Abschnitt 12 verweist, findet ein reiner Vektor-Retrieval das nicht zuverlässig.

Was tatsächlich hilft ist ein zweistufiges System. Erst semantisch chunken (nach Überschriften, Absätzen, logischen Einheiten). Dann einen Re-Ranker vorschalten der nicht nur Ähnlichkeit berechnet, sondern auch Relevanz im Kontext der Gesamtanfrage bewertet. Cohere Rerank oder CrossEncoder-Modelle machen das gut.

Der dritte Schritt den viele überspringen: Evaluation. Ohne einen strukturierten Testdatensatz (Frage, erwartete Antwort, relevante Chunks) weiß man nicht ob der Retrieval-Schritt gut ist oder man nur Glück hatte.

Wer RAG produktiv betreiben will kommt um diesen Aufbau nicht herum.

#RAG #LLM #AIEngineering #KIAgenten #Produktion`
    },
    {
      type: 'pilot_hell',
      text: `"Pilot hell" ist ein Begriff der in der Unternehmensberatung kursiert. Was er beschreibt ist real und wir begegnen ihm häufiger als uns lieb ist.

Es geht um den Zustand in dem ein Unternehmen drei, vier, manchmal fünf KI-Piloten parallel laufen hat. Jeder für sich liefert interessante Ergebnisse. Keiner wird skaliert. Und nach 18 Monaten hat das Unternehmen gute Präsentationen aber kein produktives System.

Was steckt dahinter? Meistens fehlt keine Technologie. Es fehlt eine klare Entscheidung: Wer übernimmt nach dem Pilot die Verantwortung? Wer betreibt das System, pflegt die Daten, reagiert wenn der Agent falsche Outputs produziert?

Das ist keine KI-Frage. Das ist eine Organisationsfrage. Und die muss vor dem ersten Prompt beantwortet werden.

Was in unseren Projekten funktioniert: Wir definieren am Anfang einen "Agent Owner" auf Unternehmensseite. Jemand der das System nicht nur nutzt, sondern versteht und verantwortet. Das ändert die Qualität der Entscheidungen im ganzen Projekt.

#KIStrategie #Automatisierung #Mittelstand #Transformation`
    },
    {
      type: 'japan_germany',
      text: `Ein Kontrast den wir bei Kuroko Labs seit Jahren beobachten und der sich 2026 noch einmal zugespitzt hat.

Deutsche Fertigungsunternehmen und japanische Produktionsbetriebe haben ähnliche Ziele (Effizienz, Qualität, Skalierung) aber sehr unterschiedliche Wege dorthin.

In Deutschland erleben wir oft den Wunsch, vor dem ersten Schritt alles verstanden und dokumentiert zu haben. Prozesse müssen klar sein, Daten sauber, Schnittstellen definiert. Das führt zu guten Konzepten und langen Vorlaufzeiten.

In japanischen Betrieben die wir kennen, ist der Einstiegspunkt kleiner. Ein konkretes Problem in einem konkreten Prozess. Oft manuell, oft unspektakulär. Der Agent löst genau das. Dann den nächsten Schritt.

Fraunhofer IPA hat in einer Vergleichsstudie 40% kürzere Implementierungszyklen auf japanischer Seite gemessen. Die Ursache ist nicht fehlende Sorgfalt, sondern eine andere Definition davon was "bereit" bedeutet.

Das interessante daran: Die Endqualität unterscheidet sich kaum. Aber die Zeit bis zum ersten echten Nutzen ist signifikant verschieden.

#JapanDeutschland #KI #Industrie40 #Fertigung #Transformation`
    },
    {
      type: 'llm_cost_tco',
      text: `Eine Rechnung die wir Kunden regelmäßig aufzeigen, weil sie fast immer überraschend ist: Was kostet ein KI-Projekt wirklich?

Die Aufmerksamkeit geht meistens auf die API-Kosten. Und ja, bei GPT-4o oder Claude Sonnet kommen bei hohem Volumen schnell dreistellige Monatsbeträge zusammen. Aber das ist selten der größte Posten.

Was in der Praxis dominiert:

Erstens: Datenaufbereitung. Bevor ein Agent auf internen Dokumenten, ERP-Daten oder Produktionslogs sinnvoll arbeiten kann, müssen diese strukturiert, bereinigt und indexiert werden. Das ist oft 40 bis 60 Prozent des Projektaufwands.

Zweitens: Prompt-Engineering und Evaluation. Einen guten Prompt zu schreiben dauert Stunden. Einen zu testen, der in 95% der Fälle das Richtige tut, dauert Wochen.

Drittens: Betrieb und Monitoring. Ein Agent der in Produktion läuft, braucht Observability. Logs, Alerts, manuelle Review-Queues für Grenzfälle.

Wer nur die Token-Kosten kalkuliert, unterschätzt das Gesamtprojekt um den Faktor 3 bis 5.

#LLM #AIEngineering #KIStrategie #TCO #Mittelstand`
    },
    {
      type: 'multiagent_complexity',
      text: `Multi-Agent-Systeme sind 2026 ein echtes Thema. Was sie leisten können ist beeindruckend. Was dabei schiefgeht auch.

Das Versprechen: Mehrere spezialisierte Agenten arbeiten zusammen. Ein Agent liest Dokumente, ein anderer führt Berechnungen durch, ein dritter kommuniziert mit externen APIs. Das Ergebnis ist besser als alles was ein einzelner Prompt erreicht.

Die Realität in frühen Projekten: Orchestrierungskomplexität unterschätzt. Wenn Agent A auf das Ergebnis von Agent B wartet, und B auf Agent C, entstehen Fehlerquellen die sich multiplizieren. Ein falsches Output an einer Stelle pflanzt sich durch die gesamte Kette fort.

Was wir in der Praxis gelernt haben: Multi-Agent-Architekturen brauchen klare Contracts zwischen den Agenten (strukturierte Outputs, Validierungsschritte) und einen menschlichen Checkpoint an kritischen Stellen. Nicht jede Entscheidung, aber die mit hohen Konsequenzen.

Gut umgesetzt sind sie mächtig. Schlecht umgesetzt sind sie eine komplizierte Art, fehlerhafte Outputs zu produzieren.

#MultiAgent #AgentDev #KIArchitektur #LLM #AIEngineering`
    },
    {
      type: 'dsgvo_llm',
      text: `DSGVO und LLMs. Ein Thema das in der KI-Community oft als Randproblem behandelt wird und in deutschsprachigen Unternehmen regelmäßig zum Showstopper wird.

Die konkrete Frage ist oft diese: Darf ich interne Kundendaten an ein externes Modell (OpenAI, Anthropic, Google) schicken?

Die juristische Antwort ist komplex und vom Einzelfall abhängig. Was uns in Projekten begegnet:

API-Calls an US-Anbieter gelten als Drittlandübermittlung. Das erfordert Standardvertragsklauseln (SCCs) und eine Datenschutzfolgeabschätzung (DSFA). Beide sind machbar, kosten aber Zeit.

Eine praktische Alternative ist das Tiering von Daten. Anonymisierte oder aggregierte Daten gehen an externe Modelle. Personenbezogene oder geschäftskritische Daten bleiben on-premise, auf Azure OpenAI (EU-Region) oder auf lokalen Modellen wie Mistral oder LLaMA.

Das ist keine perfekte Lösung, aber eine die funktioniert. Und sie setzt eine Entscheidung voraus die ohnehin sinnvoll ist: Welche Daten braucht der Agent wirklich?

#DSGVO #LLM #Compliance #KIStrategie #Datenschutz`
    },
    {
      type: 'evals_not_vibes',
      text: `"Das fühlt sich besser an." Das ist die häufigste Methode mit der Prompt-Änderungen in frühen KI-Projekten bewertet werden. Und es ist ein Problem.

Vibes-based Evaluation funktioniert für Demos. Für produktive Systeme ist sie gefährlich, weil man Regressionen nicht sieht. Eine Prompt-Optimierung die Typ-A-Anfragen verbessert, kann gleichzeitig Typ-B-Anfragen verschlechtern. Ohne Testset merkt man das erst wenn es zu spät ist.

Was stattdessen funktioniert:

Ein strukturiertes Eval-Set aufbauen. 50 bis 200 Beispielanfragen mit erwarteten Outputs. Bei Reasoning-Tasks reicht oft ein LLM-as-Judge (Claude bewertet ob die Antwort korrekt und vollständig ist). Bei strukturierten Outputs nimmt man exakte Metriken (Precision, Recall, F1).

Dann jeden Prompt-Change gegen dieses Set laufen lassen. Das dauert bei GPT-4o vielleicht 5 Minuten und 2 Euro. Dafür weiß man was man tut.

Das klingt nach Overhead. In Wirklichkeit ist es das, was den Unterschied zwischen einem Agent der in Produktion stabil läuft und einem der nach drei Wochen Vertrauen verliert, ausmacht.

#LLMEvals #AIEngineering #PromptEngineering #KIAgenten`
    },
    {
      type: 'supply_chain_agent',
      text: `Ein Anwendungsfall der 2026 in mehreren Projekten bei uns konkret wird: KI-Agenten in der Supply Chain.

Das abstrakte Versprechen kennt jeder. Aber was heißt das in einem mittelständischen Fertigungsbetrieb mit 200 aktiven Lieferanten, einem SAP-System aus 2018 und einem Einkaufsteam von 6 Personen?

Konkret: Der Agent überwacht täglich Lieferanten-Performance-Daten aus dem ERP (Liefertreue, Qualitätsquoten, Leadtime-Abweichungen). Wenn ein Lieferant in zwei aufeinanderfolgenden Wochen Abweichungen über einem Schwellwert zeigt, erstellt der Agent automatisch eine Zusammenfassung mit Handlungsoptionen und eskaliert an den zuständigen Einkäufer.

Das ersetzt keine Einkaufsentscheidung. Es stellt sicher, dass Probleme früh sichtbar werden, bevor sie Produktionsstopps verursachen.

In einem laufenden Projekt hat das die Reaktionszeit auf Lieferantenprobleme von durchschnittlich 11 Tagen auf 2 Tage reduziert. Nicht durch bessere Menschen, sondern durch bessere Sichtbarkeit.

#SupplyChain #KIAgenten #Fertigung #Einkauf #Automatisierung`
    },
    {
      type: 'fine_tuning_vs_rag',
      text: `Fine-Tuning oder RAG? Eine Frage die wir fast wöchentlich gestellt bekommen. Die Antwort hängt von etwas ab, das viele beim Fragen noch nicht geklärt haben.

Fine-Tuning macht Sinn wenn man einen Stil, eine Struktur oder ein Verhaltensmuster in das Modell einbrennen will. Ein Modell das immer in einem bestimmten Format antwortet, oder eine spezifische Sprache spricht (technischer Jargon, Unternehmenssprache), oder bestimmte Kategorisierungen konsistent trifft. Dafür braucht man ausreichend Trainingsdaten, meistens 500 bis 5000 Beispiele, und ein klares Eval-Set.

RAG macht Sinn wenn das Problem Zugang zu spezifischem Wissen ist, das sich ändert oder das zu umfangreich für den Kontext ist. Technische Dokumentation, aktuelle Preislisten, Produktkataloge, interne Richtlinien.

Was in der Praxis öfter schiefgeht: Teams wählen Fine-Tuning weil sie denken, das Modell "weiß dann mehr". Aber Fine-Tuning ändert nicht was das Modell weiß. Es ändert wie es antwortet. Wer aktuelles Wissen braucht, kommt an RAG nicht vorbei.

#LLM #FineTuning #RAG #AIEngineering #KIAgenten`
    },
    {
      type: 'model_selection',
      text: `Welches Modell für welchen Zweck? 2026 ist die Antwort differenzierter als noch vor zwei Jahren und das ist eigentlich eine gute Nachricht.

Aus laufenden Projekten ergeben sich bei uns klare Muster.

Für Long-Context-Aufgaben (Vertragsanalyse, technische Dokumentation, mehrseitige Reports): Claude Sonnet und Opus sind konsistenter als GPT-4o bei Inputs über 50k Tokens. Das hat mit dem Attention-Mechanismus und dem Training auf langen Sequenzen zu tun.

Für strukturierte Outputs und Function Calling in Agenten-Pipelines: GPT-4o bleibt schwer zu schlagen. Die JSON-Konsistenz ist hoch, die Latenz bei 4o-mini für einfache Tasks sehr gut.

Für Einbettungen und Retrieval: text-embedding-3-large von OpenAI und Cohere Embed v3 sind die Werkzeuge der Wahl. Voyage AI ist interessant für domänenspezifische Finetuning-Einbettungen.

Was oft vergessen wird: Inference-Kosten skalieren mit dem Volumen. Ein Modell das bei 1000 Requests pro Tag günstig ist, kann bei 100.000 unerschwinglich werden. Latenz ist der andere Parameter der oft erst in Produktion zum Problem wird.

#LLM #ModelSelection #AIEngineering #KIAgenten #Technologie`
    }
  ],

  twitter: [
    {
      type: 'rag_tip',
      text: 'RAG in Produktion: Naive 512-Token-Chunks reißen Sinnzusammenhänge auseinander. Semantisches Chunken nach Dokumentstruktur + CrossEncoder-Reranker bringt in unseren Tests 30 bis 40% bessere Retrieval-Qualität. #RAG #LLM #AIEng'
    },
    {
      type: 'model_fact',
      text: 'Claude Sonnet 4.6 bei 200k-Token-Inputs: Konsistenz bei Long-Context-Retrieval liegt bei 87% in unseren Benchmarks. GPT-4o fällt ab 80k Tokens messbar ab. Relevant für Vertragsanalysen. #LLM #Claude'
    },
    {
      type: 'insight_tweet',
      text: 'Pilot Hell: Unternehmen mit 4+ parallelen KI-Piloten, null davon in Produktion. Das Problem ist nie die Technologie. Es ist die fehlende Antwort auf "wer betreibt das nach dem Pilot?" #KIStrategie #Mittelstand'
    },
    {
      type: 'agent_tip',
      text: 'Multi-Agent-Fehler den wir regelmäßig sehen: Kein Validation-Layer zwischen Agenten. Agent A produziert Fehler, Agent B baut darauf auf, das Endresultat ist weit weg. Structured Outputs + Checkpoints lösen das. #AgentDev'
    },
    {
      type: 'cost_fact',
      text: 'Wer nur Token-Kosten kalkuliert unterschätzt KI-Projekte um Faktor 3 bis 5. Datenaufbereitung, Evals und Betrieb dominieren. API-Kosten sind meist der kleinste Posten. #LLM #AIEng #Kosten'
    },
    {
      type: 'dsgvo_tip',
      text: 'DSGVO + LLM: Personenbezogene Daten an US-APIs = Drittlandübermittlung. SCCs + DSFA erforderlich. Praktische Lösung: Data Tiering. Kritische Daten bleiben on-premise oder auf Azure EU-Region. #DSGVO #LLM'
    },
    {
      type: 'eval_tip',
      text: 'Evals sind keine Bürokratie. Ein 100-Beispiele-Testset + LLM-as-Judge erkennt Prompt-Regressionen bevor sie in Produktion ankommen. Kostet 2 Euro und 5 Minuten pro Run. #LLMEvals #PromptEng'
    },
    {
      type: 'model_fact',
      text: 'text-embedding-3-large vs. Cohere Embed v3 auf deutschen Fachtexten: Cohere gewinnt bei domänenspezifischem Vokabular (Maschinenbau, Recht, Medizin). OpenAI ist stärker bei allgemeinen Texten. #Embedding #RAG'
    },
    {
      type: 'insight_tweet',
      text: 'Beobachtung aus 2026: Fine-Tuning wird überschätzt. 80% der Fälle wo Teams Fine-Tuning wollten, war RAG die richtige Antwort. Fine-Tuning ändert Verhalten, nicht Wissen. #LLM #FineTuning'
    },
    {
      type: 'case_study_tweet',
      text: 'Supply Chain Agent in Produktion: Reaktionszeit auf Lieferantenprobleme von 11 Tagen auf 2 Tage. Nicht durch bessere Menschen. Durch bessere Sichtbarkeit auf ERP-Daten. #SupplyChain #KIAgenten'
    },
    {
      type: 'rag_tip',
      text: 'Hybrid Search (BM25 + dense retrieval) schlägt pure-vector in 70% der Enterprise-Retrieval-Tasks laut unseren internen Benchmarks. Stichwortpräzision und Semantik ergänzen sich. #RAG #VectorSearch'
    },
    {
      type: 'insight_tweet',
      text: 'GPT-4o-mini Function Calling bei einfachen Tasks: 180ms Median-Latenz. GPT-4o: 420ms. Für Agenten die im Loop laufen ist das der Unterschied zwischen akzeptabel und nervig. #AgentDev #Latenz'
    },
    {
      type: 'benchmark_finding',
      text: 'GraphRAG vs. naives RAG auf globalen Summarisierungsanfragen: +26 bis +33 Prozentpunkte in menschlicher Bewertung (Microsoft Paper 2024). Der Preis: ~4x längere Indexierungszeit. #GraphRAG #RAG'
    },
    {
      type: 'cost_fact',
      text: 'Pinecone Serverless bei 10M Vektoren: ca. 80 Euro/Monat. Qdrant self-hosted auf einer 16GB-RAM-Instanz: ~12 Euro/Monat Hardware. Bei Scale ist die Wahl der Vector DB eine Kostenentscheidung. #VectorDB #Qdrant'
    },
    {
      type: 'architecture_tip',
      text: 'Sparse Activation bei MoE-Modellen: Mixtral 8x7B aktiviert pro Token ~12B von 46,7B Parametern. Günstigere Inferenz als Dense-70B bei ähnlicher Qualität. Aber mehr VRAM fürs Hosting nötig. #MoE #LLM'
    },
    {
      type: 'insight_tweet',
      text: 'Prompt Injection via RAG-Dokumente: Ein präpariertes PDF reicht, um einem ungesicherten Agenten neue Instruktionen zu geben. In 2026 kein Proof-of-Concept mehr, sondern dokumentierter Angriffsvektor. #AgentSecurity'
    },
    {
      type: 'cost_fact',
      text: 'Gemini 1.5 Pro bei 250k Token Input: 3,50$/M Token = ~0,875$ pro Anfrage. Dasselbe Dokument via RAG auf 4k Token: ~0,004$. 200x Kostenfaktor. Full-Context ist nur für globale Fragen wirtschaftlich. #LLM #Kosten'
    },
    {
      type: 'architecture_tip',
      text: 'Was auf einer RTX 3090 (24GB VRAM) läuft: Mistral 7B Q8, LLaMA 3.1 8B, Gemma 9B. Was nicht läuft: 70B-Modelle ohne Quantisierung. Lokale KI ist real, aber Hardware-Planung zählt. #Ollama #LocalLLM'
    },
    {
      type: 'benchmark_finding',
      text: 'Qwen2.5-72B-Instruct auf MMLU: 86,1%. Claude 3.5 Sonnet: 88,3%. Llama 3.3 70B: 86,0%. Open-Source hat proprietary fast eingeholt. Für viele Enterprise-Tasks ist der Gap heute nicht mehr entscheidend. #LLM'
    },
    {
      type: 'architecture_tip',
      text: 'Häufiger RAG-Fehler: Das Retrieval gibt 5 Chunks zurück, aber Chunk 3 widerspricht Chunk 1. Das Modell halbiert im Zweifel. Lösung: Cross-Encoder-Reranking + Konsistenzprüfung vor der Antwort-Generierung. #RAG'
    }
  ],

  instagram: [
    {
      type: 'ai_moment',
      text: `Stell dir vor, dein ERP antwortet auf Fragen wie ein erfahrener Kollege. 🤖

"Welche drei Lieferanten haben uns in Q4 die meisten Qualitätsprobleme verursacht?"
"Zeig mir alle Bestellungen über 50.000 Euro die in den letzten 30 Tagen verspätet eingetroffen sind."
"Was war der Ausschuss in Linie 3 vergangene Woche im Vergleich zum Vorjahresdurchschnitt?"

Das ist kein Zukunftsszenario mehr. Das sind Agenten die wir heute produktiv in Fertigungsbetrieben deployen.

Was sich grundlegend verändert hat: Sprachmodelle sind gut genug geworden, um mit internen, strukturierten Daten kohärent umzugehen. Halluzinationen sind dann ein Problem, wenn das Modell raten muss. In einer RAG-Architektur mit sauberem Datenzugriff rät es nicht.

Die entscheidende Variable bleibt Datenqualität. Ein Agent mit Zugriff auf unvollständige oder inkonsistente ERP-Daten produziert unvollständige und inkonsistente Antworten. Das ist kein Modellproblem, das ist ein Datenproblem.

#KIAgenten #Automatisierung #ERP #Mittelstand #AIFirst`,
      hasImage: true
    },
    {
      type: 'automation_economics',
      text: `Was kostet Automatisierung wirklich? Und was bringt sie wirklich? 💡

Eine BCG-Analyse zeigt: KI-Agenten in der Kreditorenbuchhaltung reduzieren manuelle Bearbeitungszeit um 68%. Bei einem Team von fünf Vollzeitstellen entspricht das etwa zwei Stellen an Kapazitätsgewinn.

Aber hier ist das Wichtige: Der ROI entsteht in den wenigsten Fällen durch Stellenabbau. Er entsteht durch Reallokation.

Dieselben fünf Menschen bearbeiten danach komplexere Fälle, klären Ausnahmen, pflegen Lieferantenbeziehungen. Sie tun Dinge die tatsächlich Urteilsvermögen erfordern. Der Agent übernimmt den Rest.

Was wir bei Kuroko Labs in Projekten beobachten: Die stärksten Business Cases kommen nicht von "wir ersetzen Mitarbeiter". Sie kommen von "wir hören auf, qualifizierte Menschen mit unqualifizierter Arbeit zu beschäftigen."

Das ist kein kleiner Unterschied. Das ist der Kern davon, ob KI als Bedrohung oder als Werkzeug erlebt wird.

#Automatisierung #KI #ROI #Mittelstand #AIFirst`,
      hasImage: false
    },
    {
      type: 'hallucination_cost',
      text: `Wie viel kostet eine Halluzination? Eine ernsthafte Frage, die selten ernsthaft beantwortet wird. 🔍

Wenn ein LLM in einer Vertragsanalyse eine Klausel erfindet die nicht existiert und das erst beim Anwalt auffällt, ist der Schaden messbar. Wenn ein Beschaffungsagent einen Lieferantenpreis falsch zitiert und jemand auf Basis davon eine Entscheidung trifft, auch.

Was uns in Projekten beschäftigt: Halluzinationen sind nicht gleichmäßig verteilt. Sie passieren häufiger bei vagen Anfragen, bei Texten die das Modell nicht gesehen hat, und bei Fragen die suggerieren, es gäbe eine definitive Antwort wo keine ist.

Was dagegen hilft ist nicht primär ein besseres Modell. Es ist eine Architektur die das Modell nicht zum Raten zwingt. RAG mit klaren Quellen, strukturierte Outputs mit Validierung, und Grenzfälle die automatisch in eine Review-Queue gehen statt blind durchzulaufen.

Das ändert die Fehlermodus-Kategorie. Von "Agent erfindet etwas" zu "Agent sagt, er kann das nicht beurteilen". Der zweite Fehler ist erheblich besser.

#LLM #Hallucination #KIAgenten #AIArchitektur #Mittelstand`,
      hasImage: true
    },
    {
      type: 'automation_anxiety',
      text: `Automatisierungsangst ist real. Und sie verdient eine ehrliche Antwort. 🧠

In Gesprächen mit Produktionsleitern, Operations-Teams und Sachbearbeitern hören wir eine Frage die selten direkt gestellt, aber oft gemeint ist: "Werde ich noch verstehen was hier passiert?"

Das ist keine irrationale Frage. Ein Agent der Entscheidungen vorbereitet oder Prozesse steuert, ohne dass klar ist nach welcher Logik, ist tatsächlich ein Problem. Nicht nur für das Vertrauen der Mitarbeitenden. Sondern für die Qualität der Ergebnisse.

Was wir bei Kuroko Labs als Teil der Implementierungsarbeit sehen: Erklärbarkeit ist kein Nice-to-have. Es geht darum zu definieren, bei welchen Entscheidungen der Agent Vorschläge macht und warum. Und bei welchen Entscheidungen ein Mensch zwingend das letzte Wort hat. Nicht als Backup-Lösung, sondern als bewusstes Design.

Unternehmen die das früh klären, haben weniger Akzeptanzprobleme. Nicht weil die Menschen unkritisch sind, sondern weil sie das System verstehen.

#Automatisierung #KI #Arbeit #Mittelstand #Transparenz`,
      hasImage: false
    },
    {
      type: 'agent_in_action',
      text: `Was ein KI-Agent in der Produktion konkret macht. Ein reales Beispiel, anonymisiert. 🏭

Ausgangssituation: Fertigungsbetrieb, drei Produktionslinien, Maschinenausfälle wurden reaktiv gemeldet. Wenn die Maschine stand, wusste man es. Nicht vorher.

Die Lösung: Ein Agent überwacht Sensordaten in Echtzeit (Temperatur, Vibration, Stromaufnahme, Laufzeitmuster). Er vergleicht aktuelle Werte mit historischen Mustern aus drei Jahren Betriebsdaten. Bei statistisch signifikanten Abweichungen, also Mustern die in der Vergangenheit 48 bis 72 Stunden vor Ausfällen aufgetreten sind, wird automatisch ein Wartungsticket im ERP erstellt und der zuständige Techniker informiert.

Der Agent entscheidet nicht ob die Maschine abgeschaltet wird. Das bleibt beim Menschen.

Ergebnis nach einem Quartal: Ungeplante Stopps reduziert um 40%. Das entspricht bei dieser Anlage einem Produktionsgewinn von ungefähr 280 Arbeitsstunden.

#KIAgenten #PredictiveMaintenance #IIoT #Fertigung`,
      hasImage: true
    },
    {
      type: 'open_source_models',
      text: `Offene Modelle vs. proprietäre APIs. Eine Entscheidung die 2026 mehr Nuancen hat als je zuvor. ⚖️

Mistral Large, LLaMA 3.3, Qwen 2.5 und Gemma 3 sind inzwischen ernstzunehmende Alternativen zu GPT-4o und Claude Sonnet in einer überraschend breiten Aufgabenklasse. Für strukturierte Outputs, Klassifikation, Zusammenfassung und einfache Reasoning-Aufgaben ist der Qualitätsunterschied zu proprietären Modellen kleiner als er vor einem Jahr war.

Warum das relevant ist: Wer On-Premise deployt oder DSGVO-konforme Setups braucht, hat jetzt reale Optionen. Ollama oder vLLM auf einer GPU-Instanz in der EU löst viele Compliance-Fragen auf einen Schlag.

Was bleibt: Bei komplexen Reasoning-Aufgaben, Long-Context-Analysen über 50k Tokens und agentenbasierter Tool-Nutzung sind Claude und GPT-4o weiterhin vorn. Der Abstand wird kleiner, ist aber noch relevant.

Unsere Empfehlung für Projekte mit sensiblen Daten: Hybrid. Offene Modelle für Retrieval und einfache Klassifikation, proprietäre APIs für die komplexen Schritte in der Kette.

#OpenSource #LLM #DSGVO #KIArchitektur #Mittelstand`,
      hasImage: true
    },
    {
      type: 'data_quality',
      text: `Das größte KI-Problem der meisten Unternehmen ist kein KI-Problem. 📊

Es ist ein Datenproblem. Und das klingt nach einer Binsenweisheit bis man es konkret betrachtet.

Was in der Praxis heißt, dass Daten "nicht sauber" sind: Produktbezeichnungen die in fünf Jahren auf vier verschiedene Weisen eingetragen wurden. Lieferanten die unter drei verschiedenen Namen im System sind. Produktionslogs die manuell eingetragen wurden und Lücken haben. Zeitstempel in unterschiedlichen Formaten.

Ein LLM kann damit umgehen. Meistens. Aber was er nicht kann: Inkonsistenzen die inhaltlich falsch sind, von Inkonsistenzen unterscheiden die nur formal falsch sind. Er arbeitet mit dem was er bekommt.

Was das in Projekten bedeutet: Vor dem ersten Agenten-Deployment steht eine Datenanamyse. Nicht um perfekte Daten zu haben. Sondern um zu verstehen welche Datenfelder verlässlich sind und welche mit Vorsicht zu behandeln sind. Das formt die Architektur des Systems.

Unternehmen die das überspringen wollen, springen in der Regel zweimal. Einmal mit dem Agenten, und einmal wenn die Ausgaben nicht stimmen.

#Datenqualität #KIAgenten #AIFirst #Mittelstand #Transformation`,
      hasImage: false
    },
    {
      type: 'agent_governance',
      text: `KI-Agenten brauchen Governance. Nicht als Compliance-Pflicht, sondern damit sie funktionieren. 🛡️

Was wir in Projekten sehen: Agenten die in Produktion gehen ohne klare Antworten auf drei Fragen laufen regelmäßig in Probleme.

Erstens: Was sind die Grenzen des Agenten? Welche Entscheidungen darf er selbstständig treffen, welche nicht? Ohne klare Grenze übernimmt er im Zweifel mehr als beabsichtigt.

Zweitens: Wie wird bemerkt wenn der Agent falsch liegt? Kein System ist perfekt. Die Frage ist nicht ob Fehler passieren, sondern wie schnell sie sichtbar werden. Logs, Monitoring, Review-Queues für kritische Outputs sind keine optionalen Extras.

Drittens: Wer ist verantwortlich? In der Organisation. Eine Person die den Agenten nicht nur nutzt, sondern versteht, überprüft und im Zweifelsfall korrigiert.

Agenten die mit diesen drei Antworten starten, werden besser. Agenten ohne sie werden nach sechs Monaten abgeschaltet, weil das Vertrauen weg ist.

#KIGovernance #KIAgenten #AIEthics #Mittelstand #Automatisierung`,
      hasImage: true
    },
    {
      type: 'graphrag_explainer',
      text: `Was ist GraphRAG und warum klingt das nach mehr als normales RAG? 🔗

Stell dir normales RAG so vor: Du hast 10.000 Seiten Dokumentation. Du stellst eine Frage. Das System sucht die 5 ähnlichsten Textabschnitte und gibt sie dem Modell. Das Modell antwortet.

Das funktioniert gut für Faktenfragen. Aber was wenn du fragst: "Welche Systeme hängen alle von diesem einen Lieferanten ab?"

Normales RAG liefert Fragmente. Es versteht keine Beziehungen.

GraphRAG geht einen Schritt weiter. Bevor du suchst, baut das System einen Wissensgraphen: Entitäten, ihre Eigenschaften, ihre Verbindungen zueinander. Microsoft hat das 2024 in einem Paper beschrieben. Ihr Benchmark: Bei Fragen die Zusammenhänge über viele Dokumente erfordern, ist GraphRAG 26 bis 33 Prozentpunkte besser als normales RAG in menschlichen Qualitätsbewertungen.

Der Preis: Der Aufbau des Graphen dauert länger und kostet mehr Rechenaufwand beim Indexieren. Für einfache Dokumentensuche lohnt sich der Aufwand nicht.

Für Enterprise-Systeme mit vernetzten Daten, wie Lieferketten, Produktabhängigkeiten oder Projektportfolios, ist GraphRAG ein Ansatz der sich 2026 zunehmend aus dem Paper in die Praxis bewegt.

#GraphRAG #RAG #KIErklärung #Wissensmanagement`,
      hasImage: true
    },
    {
      type: 'hallucination_explainer',
      text: `Dein KI-Modell lügt nicht. Es rät.

Das ist ein wichtiger Unterschied und erklärt viel darüber, wann und wie Fehler entstehen.

Ein Sprachmodell hat kein Bewusstsein davon, was es weiß und was nicht. Es hat keine interne Datenbank die es schlägt und dann "nein" sagt wenn nichts gefunden wird. Es generiert den wahrscheinlichsten nächsten Token. Immer. Auch wenn keine gute Antwort existiert.

Was Halluzinationen häufiger macht: Vage Fragen ohne klaren Anker im Kontext. Fragen die eine definitive Antwort suggerieren wo keine ist. Anfragen zu sehr spezifischen oder sehr aktuellen Fakten die das Modell beim Training nicht ausreichend gesehen hat.

Was sie seltener macht: Eine Architektur die das Modell nicht zum Raten zwingt. RAG mit verifizierten Quellen gibt dem Modell einen Anker. Strukturierte Outputs mit Validierung fangen Ausreißer auf. Ein explizites "Ich weiß das nicht" als mögliche Antwortklasse zu trainieren oder per Prompt zu erlauben verändert das Verhalten erheblich.

Das Ziel ist kein Modell das nie falsch liegt. Es ist ein System das transparent macht, wann es unsicher ist.

#LLM #Halluzination #KIErklärung #AIArchitektur`,
      hasImage: false
    },
    {
      type: 'local_ai',
      text: `Was läuft heute wirklich auf deiner Hardware? Die Antwort ist überraschend gut. 💻

Mit Ollama und einer modernen GPU (oder sogar nur guter CPU-Kapazität) lassen sich heute ernstzunehmende Sprachmodelle vollständig lokal betreiben.

Was auf einer RTX 3090 (24 GB VRAM) läuft: Mistral 7B in voller Qualität, LLaMA 3.1 8B, Gemma 9B. Geschwindigkeit: 35 bis 55 Token pro Sekunde. Das ist flüssig genug für Echtzeit-Anwendungen.

Was auf einem MacBook Pro M3 Max (96 GB Unified Memory) läuft: LLaMA 3.1 70B in 4-Bit-Quantisierung, Mixtral 8x7B. Qualität ist gegenüber Full-Precision leicht reduziert, für viele Aufgaben aber nicht unterscheidbar.

Der Datenschutzaspekt ist real: Kein Token verlässt deine Hardware. Kein API-Anbieter sieht deine Daten. Kein Vertrag über Drittlandübermittlung. Für Anwendungsfälle mit sensiblen Unternehmensdaten ist das oft der entscheidende Vorteil.

Was lokale Modelle noch nicht können: Long-Context-Verarbeitung über 50.000 Token mit konsistenter Qualität. Und die absolut komplexesten Reasoning-Aufgaben bleiben bei proprietären Frontier-Modellen besser. Für strukturierte Klassifikation, Zusammenfassung und RAG-Anwendungen ist der Gap 2026 deutlich kleiner als noch vor einem Jahr.

#LocalAI #Ollama #Datenschutz #OpenSource #DSGVO`,
      hasImage: true
    },
    {
      type: 'knowledge_graph_enterprise',
      text: `Der Graph der alles verbindet: Wissensgraphen im Unternehmenseinsatz. 🕸️

Wissensgraphen sind keine neue Idee. Google nutzt sie seit über zehn Jahren für Knowledge Panels. Was neu ist: Die Kombination mit Sprachmodellen macht sie für Unternehmen mit komplexen Datenlandschaften zugänglich.

Ein konkretes Beispiel aus der Praxis: Ein Maschinen- und Anlagenbauer hat Produktdokumentation, Servicereports, Ersatzteillisten und Lieferantenverträge in verschiedenen Systemen. Ein Techniker fragt: "Welche Ersatzteile für Pumpentyp X kommen vom selben Lieferanten wie die Dichtungen die letzte Woche Qualitätsprobleme hatten?"

Ein Vektorindex findet ähnliche Dokumente. Ein Wissensgraph traversiert die Beziehung: Pumpentyp X, hat-Teil, Dichtung Y, geliefert-von, Lieferant Z, hat-Problem, QM-Ticket 4823.

Der Aufbau eines solchen Graphen aus bestehenden Dokumenten ist heute mit LLM-gestützter Entitätsextraktion machbar ohne dass jede Beziehung manuell eingetragen werden muss. GraphRAG von Microsoft und ähnliche Ansätze automatisieren diesen Schritt.

Der Einstieg funktioniert mit einem klar abgegrenzten Dokumentenkorpus, typisch einem Produktbereich oder einer Abteilung. Nicht mit dem gesamten Unternehmenswissen auf einmal.

#Wissensgraph #GraphRAG #KIArchitektur #Enterprise #RAG`,
      hasImage: true
    },
    {
      type: 'mittelstand_ki_barrieren_ig',
      text: `Warum 62% des deutschen Mittelstands noch keine KI nutzt. Und es ist nicht Angst.

Das IW Köln hat Anfang 2026 befragt. Die Zahlen sehen anders aus als die öffentliche Debatte vermuten lässt.

53% nennen IT-Infrastruktur als Haupthindernis. Systeme aus den 2000er-Jahren, getrennte Datensilos, keine APIs.

48% sagen: die Daten sind nicht sauber genug. Produktnamen in fünf Schreibweisen, Lieferanten unter drei verschiedenen Nummern, Zeitstempel ohne einheitliches Format.

44% fehlen interne Kompetenzen. Nicht KI-Experten, sondern jemand der beides versteht: das Fachgebiet und was KI damit machen kann.

"Angst vor KI" oder ethische Bedenken? Unter 15 Prozent.

Das ist wichtig, weil es die richtige Diagnose für die richtige Lösung braucht. Wer ein Motivationsproblem lösen will, wo ein Infrastrukturproblem vorliegt, wird nicht weit kommen.

Was tatsächlich hilft: Ein klar abgegrenzter Einstiegspunkt mit sauberen Daten. Nicht die Transformation des gesamten Unternehmens, sondern ein Prozess der funktioniert und Vertrauen aufbaut.

#Mittelstand #KI #Deutschland #Digitalisierung #IWKöln`,
      hasImage: false
    },
    {
      type: 'model_cost_quality',
      text: `Das beste Modell ist nicht das teuerste. Eine unbequeme Wahrheit für viele KI-Projekte. ⚖️

GPT-4o kostet bei der API ca. 5 Dollar pro Million Output-Token. GPT-4o-mini: 0,60 Dollar. Faktor 8 Unterschied. Mistral Small selbst gehostet: ein Bruchteil davon.

Was die Qualitätsdifferenz in der Praxis bedeutet: Bei strukturierter Klassifikation, einfacher Zusammenfassung und Dokumentenextraktion ist der Unterschied zwischen GPT-4o und GPT-4o-mini in kontrollierten Benchmarks unter 5 Prozentpunkten. Bei komplexen Reasoning-Ketten, juristischer Analyse oder sehr langen Kontexten wächst der Abstand auf 10 bis 20 Prozentpunkte.

Wir bei Kuroko Labs empfehlen in Projekten routinemäßig einen Task-basierten Modellmix. Einfache Schritte in der Agenten-Pipeline laufen auf kleineren, günstigeren Modellen. Nur die Schritte die wirklich Reasoning erfordern, laufen auf dem teuren Modell.

In einem konkreten Projekt haben wir damit die monatlichen API-Kosten um 60 Prozent reduziert, bei weniger als 3 Prozent Qualitätsverlust auf dem Eval-Set.

Die Frage ist nicht welches Modell am besten ist. Die Frage ist welches Modell für diesen Schritt ausreichend ist.

#LLM #ModelSelection #KIKosten #AIEngineering #Effizienz`,
      hasImage: true
    }
  ],

  threads: [
    {
      type: 'threads_question',
      text: 'Wie entscheidet ihr welches LLM ihr für produktive Systeme nehmt? In unseren Projekten läuft es meistens auf Claude für Long-Context und GPT-4o-mini für strukturierte Tool-Calls raus. Ist das bei euch auch so oder habt ihr andere Muster?'
    },
    {
      type: 'threads_insight',
      text: 'Beobachtung aus dieser Woche: Ein Unternehmen das wir begleiten hat seine RAG-Retrieval-Qualität durch einen einzigen Schritt von 61% auf 84% Accuracy verbessert. Nicht durch ein besseres Modell. Durch semantisches Chunking statt fixed-size. Details machen den Unterschied.'
    },
    {
      type: 'threads_question',
      text: 'Pilot Hell, wer kennt das? Vier KI-Piloten parallel, keiner in Produktion, alle irgendwie "sehr vielversprechend". Was hat bei euch den Unterschied gemacht zwischen Pilot und echtem Produktivbetrieb?'
    },
    {
      type: 'threads_insight',
      text: 'DSGVO und LLMs klingt immer wie ein Blockierthema. In der Praxis ist es lösbar wenn man früh anfängt. Data Tiering (was darf extern, was bleibt on-prem) entscheidet sich in der Architektur, nicht in der Rechtsprüfung. Die meisten Probleme entstehen wenn das zu spät gedacht wird.'
    },
    {
      type: 'threads_echo',
      text: 'RAG vs Fine-Tuning wird zu oft als Entweder-oder diskutiert. Unsere Erfahrung: Fine-Tuning für konsistenten Output-Stil und Format, RAG für aktuelles und umfangreiches Wissen. In komplexen Projekten beides zusammen. Die Frage die den Unterschied macht: Ändert sich das Wissen das der Agent braucht? Wenn ja, RAG.'
    },
    {
      type: 'threads_question',
      text: 'Agent Governance. Wer macht das strukturiert? Wir definieren inzwischen für jeden Agenten drei Dinge vor dem Start: Was entscheidet er selbstständig, was legt er vor, wer ist Owner im Unternehmen. Klingt aufwendig, spart aber massiv Zeit wenn es in Produktion läuft.'
    },
    {
      type: 'threads_insight',
      text: 'Evals bauen ist langweilig und wird deswegen oft übersprungen. Dann kommt ein Prompt-Update, Retrieval-Qualität fällt von 82% auf 67%, niemand merkt es für zwei Wochen. 100 Beispiele in einem Testset und ein automatischer Eval-Run bei jedem Release löst das. Lohnt sich immer.'
    },
    {
      type: 'threads_question',
      text: 'Offene Modelle in Produktion: Wer von euch hat Mistral oder LLaMA produktiv laufen? Nicht als Experiment, wirklich im Einsatz. Wie schlägt sich die Qualität im Vergleich zu GPT-4o auf euren konkreten Tasks?'
    },
    {
      type: 'threads_question',
      text: 'GraphRAG in Produktion: Hat das jemand wirklich laufen, nicht nur als Experiment? Der Indexierungsaufwand schreckt viele ab. Wir überlegen bei einem Projekt ob der Qualitätsgewinn bei Beziehungsanfragen den Aufwand rechtfertigt. #GraphRAG'
    },
    {
      type: 'threads_insight',
      text: 'Vector DB Auswahl ist komplizierter als sie aussieht. Qdrant, Weaviate, Pinecone, Chroma, pgvector. Alle funktionieren für einfache Use Cases. Die Unterschiede kommen bei Hybrid-Filtering, Skalierung und Betriebsaufwand. Wer einfach anfängt und wechselt, zahlt den Migrationspreis. Besser einmal richtig entscheiden.'
    },
    {
      type: 'threads_question',
      text: 'Lokale Modelle vs. Cloud-APIs: Wie trefft ihr die Entscheidung? Privacy-Argument ist klar. Aber Qualität bei komplexen Tasks und Betriebsaufwand sind echte Gegenargumente. Wir sehen mehr Projekte die Hybrid fahren. Was ist eure Erfahrung?'
    },
    {
      type: 'threads_insight',
      text: 'Prompt Injection wird unterschätzt. Nicht als theoretisches Problem, sondern als praktisches. Wir haben in einem internen Test einen ungesicherten Agenten mit einem präparierten PDF übernommen. Kein Exploit, nur Text. Das ist ein Architekturthema, kein Edge Case mehr. #AgentSecurity'
    },
    {
      type: 'threads_question',
      text: 'Context Window Strategie: Chunken und RAG, oder einfach alles in den langen Kontext stecken? Bei Gemini 1.5 Pro mit 1M Token ist die Versuchung groß. Aber die Kosten bei vielen Anfragen sind ein anderes Thema. Wie entscheidet ihr das in euren Projekten?'
    }
  ]
};

// Weekly schedule: {dayOfWeek: [platforms]}
// 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
// LinkedIn 5x + Instagram 5x = Mon–Fri; X 5x = Mon–Fri; Threads 3x = Mon/Wed/Fri
const WEEK_SCHEDULE = {
  0: ['linkedin', 'twitter', 'instagram', 'threads'],  // Mon
  1: ['linkedin', 'twitter', 'instagram'],              // Tue
  2: ['linkedin', 'twitter', 'instagram', 'threads'],  // Wed
  3: ['linkedin', 'twitter', 'instagram'],              // Thu
  4: ['linkedin', 'twitter', 'instagram', 'threads'],  // Fri
  5: ['twitter'],                                       // Sat
  6: ['twitter']                                        // Sun
};

const POSTING_HOURS = {
  0: [8, 10], 1: [12, 14], 2: [8, 10],
  3: [12, 14], 4: [8, 10], 5: [12, 14], 6: [10, 12]
};

const QUALITY_SCORES = {
  linkedin: [8.2, 8.7, 7.9, 8.5, 9.1, 8.3, 8.8, 7.6, 8.4, 9.0, 8.6, 8.1, 8.9, 7.8, 8.4, 8.7, 8.2, 9.0],
  twitter:  [8.0, 8.3, 7.8, 8.6, 8.1, 8.5, 7.9, 8.7, 8.2, 8.4, 8.0, 8.6, 8.3, 7.9, 8.5, 8.1, 8.7, 8.0, 8.4, 8.2],
  instagram:[8.4, 7.9, 8.8, 8.2, 8.6, 9.0, 7.8, 8.5, 8.3, 8.0, 8.7, 8.4, 9.1, 7.9],
  threads:  [8.1, 7.7, 8.5, 8.0, 8.3, 8.6, 7.9, 8.4, 8.2, 8.6, 7.8, 8.5, 8.1]
};

// Image generation rates per platform (0–100%)
const IMAGE_RATES = {
  linkedin:  20,   // 1 in 5 LinkedIn posts gets an AI image
  twitter:   10,   // 1 in 10 X/Twitter posts gets an AI image
  instagram: 60,   // 60% of Instagram posts get an AI image (default)
  threads:    0    // Threads: text only
};

function getStatus(date) {
  const today = new Date(2026, 2, 15); // March 15 2026
  const d = new Date(date);
  d.setHours(0,0,0,0);
  today.setHours(0,0,0,0);
  if (d < today) return 'published';
  if (d.getTime() === today.getTime()) return Math.random() > 0.5 ? 'published' : 'scheduled';
  // Mondays have pending posts
  if (d.getDay() === 1 && d > today) return 'pending';
  return 'scheduled';
}

let _idCounter = 1;

function generatePosts() {
  const posts = [];
  const counters = { linkedin: 0, twitter: 0, instagram: 0, threads: 0 };

  // Generate for all days in March 2026
  for (let day = 1; day <= 31; day++) {
    const date = new Date(2026, 2, day);
    const dow = (date.getDay() + 6) % 7; // Mon=0
    const platforms = WEEK_SCHEDULE[dow] || [];
    const [hMin, hMax] = POSTING_HOURS[dow] || [9, 11];

    platforms.forEach((platform) => {
      const contentArr = CONTENT[platform];
      const idx = counters[platform] % contentArr.length;
      const content = contentArr[idx];
      counters[platform]++;

      const hour = hMin + Math.floor(Math.random() * (hMax - hMin));
      const min = Math.floor(Math.random() * 60);
      const jitter = Math.floor(Math.random() * 30) - 15;
      const scheduledDate = new Date(2026, 2, day, hour, min + jitter);

      const qArr = QUALITY_SCORES[platform];
      const q = qArr[counters[platform] % qArr.length];

      // Determine if this post gets an image based on per-platform rate
      const imgRate = IMAGE_RATES[platform] || 0;
      const hasImage = content.hasImage !== undefined
        ? content.hasImage
        : (Math.random() * 100 < imgRate);

      const status = getStatus(scheduledDate);
      const isPublished = status === 'published';

      // Phase 2 fields
      const isLongform   = platform === 'linkedin' && content.text.split(/\s+/).length > 350;
      const isCarousel   = platform === 'linkedin' && Math.random() < 0.18;
      const isEvergreen  = isPublished && Math.random() < 0.22;
      const isRepurposed = (platform === 'twitter' || platform === 'threads') && Math.random() < 0.25;

      const likes      = isPublished ? Math.floor(Math.random() * 180) + 5  : 0;
      const comments   = isPublished ? Math.floor(likes * 0.12)             : 0;
      const shares     = isPublished ? Math.floor(likes * 0.08)             : 0;
      const reach      = isPublished ? likes * (12 + Math.floor(Math.random() * 20)) : 0;
      const impressions = isPublished ? reach * (1.4 + Math.random() * 0.8)  : 0;

      posts.push({
        id: _idCounter++,
        platform,
        post_type: content.type,
        content: content.text,
        scheduled_at: scheduledDate.toISOString(),
        status,
        quality_score: isLongform ? Math.max(q, 8.5) : q,
        image_path: hasImage ? `output/images/${platform}_${_idCounter}.jpg` : null,
        article_id: Math.floor(Math.random() * 50) + 1,
        day,
        month: 3,
        year: 2026,
        // Phase 2
        is_longform:        isLongform,
        is_evergreen:       isEvergreen,
        is_repurposed:      isRepurposed,
        repurposed_from_id: isRepurposed ? Math.max(1, _idCounter - 3) : null,
        carousel_pdf_path:  isCarousel ? `output/carousels/${content.type}_${_idCounter}.pdf` : null,
        likes,
        comments,
        shares,
        reach:              Math.round(reach),
        impressions:        Math.round(impressions),
      });
    });
  }

  return posts;
}

const DEMO_POSTS = generatePosts();

// Index by date string YYYY-MM-DD
const POSTS_BY_DATE = {};
DEMO_POSTS.forEach(p => {
  const d = new Date(p.scheduled_at);
  const key = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
  if (!POSTS_BY_DATE[key]) POSTS_BY_DATE[key] = [];
  POSTS_BY_DATE[key].push(p);
});

const PLATFORM_LABELS = {
  linkedin: 'LinkedIn',
  twitter: 'X / Twitter',
  instagram: 'Instagram',
  threads: 'Threads'
};

const PLATFORM_SHORT = {
  linkedin: 'LI',
  twitter: 'X',
  instagram: 'IG',
  threads: 'TH'
};

// ── DEMO ALERTS ──────────────────────────────────────────────────────────────
const DEMO_ALERTS = [
  {
    id: 1, severity: 'high', read: false,
    source: 'Anthropic Research',
    title: 'Claude 4 Opus released — 42% better on enterprise reasoning benchmarks',
    summary: 'Anthropic published Claude 4 Opus today with significantly improved long-context reasoning and structured output reliability. Enterprise API pricing remains unchanged.',
    recommended_platforms: ['linkedin', 'twitter'],
    created_at: '2026-03-15T08:12:00Z',
    article_url: '#'
  },
  {
    id: 2, severity: 'high', read: false,
    source: 'TechCrunch AI',
    title: 'OpenAI launches o3-mini — reasoning at $0.15/1M tokens',
    summary: 'OpenAI releases o3-mini with competitive pricing that undercuts Claude Haiku on reasoning tasks. Benchmarks show 89% on AIME 2024 math. Relevant for Kuroko Labs cost modelling content.',
    recommended_platforms: ['twitter', 'instagram'],
    created_at: '2026-03-14T16:45:00Z',
    article_url: '#'
  },
  {
    id: 3, severity: 'medium', read: false,
    source: 'VentureBeat AI',
    title: 'German Mittelstand AI adoption reaches 41% — IW Köln Q1 update',
    summary: 'New IW Köln data shows German SME AI adoption grew 12 points in 12 months. Infrastructure barriers remain the top obstacle (51%). Strong angle for Kuroko Labs consulting content.',
    recommended_platforms: ['linkedin', 'threads'],
    created_at: '2026-03-13T10:20:00Z',
    article_url: '#'
  },
  {
    id: 4, severity: 'medium', read: true,
    source: 'Hugging Face Blog',
    title: 'Mistral Large 2 outperforms GPT-4o on German legal text classification',
    summary: 'New benchmark shows Mistral Large 2 achieves 94.2% accuracy on German-language legal classification tasks vs. 91.8% for GPT-4o. Relevant for DSGVO/compliance content angle.',
    recommended_platforms: ['linkedin'],
    created_at: '2026-03-12T14:00:00Z',
    article_url: '#'
  },
  {
    id: 5, severity: 'low', read: true,
    source: 'Papers With Code',
    title: 'GraphRAG achieves new SOTA on multi-hop QA — 27% improvement',
    summary: 'Microsoft Research publishes GraphRAG v2 with improved entity extraction. The 27% gain on multi-hop QA benchmarks directly validates the Kuroko Labs GraphRAG content series.',
    recommended_platforms: ['linkedin', 'twitter'],
    created_at: '2026-03-11T09:30:00Z',
    article_url: '#'
  },
  {
    id: 6, severity: 'low', read: true,
    source: 'DeepMind Blog',
    title: 'Gemini 2.0 Pro: 1M context window with native image generation',
    summary: 'Google DeepMind releases Gemini 2.0 Pro with 1M token context and native image generation at $0.35/1M tokens. Direct impact on Kuroko Labs Instagram image generation pipeline.',
    recommended_platforms: ['instagram', 'threads'],
    created_at: '2026-03-10T11:00:00Z',
    article_url: '#'
  }
];

// Demo stats
const published = DEMO_POSTS.filter(p => p.status === 'published');

const STATS = {
  totalMonth: DEMO_POSTS.length,
  published: published.length,
  scheduled: DEMO_POSTS.filter(p => p.status === 'scheduled').length,
  pending: DEMO_POSTS.filter(p => p.status === 'pending').length,
  byPlatform: {
    linkedin:  DEMO_POSTS.filter(p => p.platform === 'linkedin').length,
    twitter:   DEMO_POSTS.filter(p => p.platform === 'twitter').length,
    instagram: DEMO_POSTS.filter(p => p.platform === 'instagram').length,
    threads:   DEMO_POSTS.filter(p => p.platform === 'threads').length,
  },
  // Phase 2 stats
  longform:   DEMO_POSTS.filter(p => p.is_longform).length,
  evergreen:  DEMO_POSTS.filter(p => p.is_evergreen).length,
  repurposed: DEMO_POSTS.filter(p => p.is_repurposed).length,
  withCarousel: DEMO_POSTS.filter(p => p.carousel_pdf_path).length,
  totalLikes:   published.reduce((a, p) => a + p.likes, 0),
  totalReach:   published.reduce((a, p) => a + p.reach, 0),
  alertsUnread: DEMO_ALERTS.filter(a => !a.read).length,
};
