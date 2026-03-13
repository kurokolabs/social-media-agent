"""Mock scraper returning realistic articles — used when USE_MOCK_APIS=true."""


class MockScraper:
    """Returns 8 hardcoded realistic mock articles for development and testing."""

    def scrape(self) -> list[dict]:
        return [
            {
                "url": "https://www.mckinsey.com/industries/manufacturing/insights/ai-manufacturing-2024",
                "title": "KI in der Fertigung: Wie Mittelstand-Unternehmen Produktionskosten um 23% senken",
                "summary": (
                    "Eine neue McKinsey-Analyse von 450 deutschen Fertigungsunternehmen zeigt, "
                    "dass KI-gestützte Predictive Maintenance die ungeplanten Stillstandzeiten um "
                    "durchschnittlich 37% reduziert. Besonders bemerkenswert: Unternehmen mit 200-500 "
                    "Mitarbeitern erzielen die höchsten ROI-Werte, da sie flexibler bei der Implementierung "
                    "sind. Die Studie identifiziert drei kritische Erfolgsfaktoren: Datenqualität der "
                    "Maschinensensoren, Change-Management bei Shopfloor-Mitarbeitern und schrittweise "
                    "Integration statt Big-Bang-Ansatz. Unternehmen, die KI-Agenten für die "
                    "Qualitätskontrolle einsetzen, berichten von 41% weniger Ausschuss und einer "
                    "Amortisationszeit von unter 18 Monaten."
                ),
                "source": "McKinsey",
                "relevance_score": 8.5,
            },
            {
                "url": "https://www.mckinsey.com/capabilities/operations/insights/automation-mittelstand",
                "title": "Automatisierung im Mittelstand: Warum 67% der Projekte scheitern — und wie die 33% es richtig machen",
                "summary": (
                    "McKinsey Operations hat 200 Automatisierungsprojekte in deutschen KMU analysiert. "
                    "Das Hauptproblem: Unternehmen kaufen Technologie, bevor sie ihre Prozesse verstehen. "
                    "Erfolgreiche Projekte starten mit einer 4-Wochen-Prozessanalyse, identifizieren "
                    "3-5 hochvolumige repetitive Prozesse und pilotieren mit einem kleinen Team. "
                    "RPA allein reicht nicht — die Kombination aus KI-Agenten, RPA und menschlicher "
                    "Oversight schafft resiliente Systeme. Durchschnittliche Kosteneinsparung in "
                    "erfolgreichen Projekten: 340.000 Euro pro Jahr bei Vollkostenbetrachtung."
                ),
                "source": "McKinsey",
                "relevance_score": 7.8,
            },
            {
                "url": "https://www.bcg.com/publications/2024/japan-germany-industry40-comparison",
                "title": "Japan und Deutschland im Industrie 4.0-Vergleich: Zwei Wege zur smarten Fabrik",
                "summary": (
                    "Eine BCG-Studie vergleicht die Digitalisierungsstrategien japanischer und deutscher "
                    "Fertigungsunternehmen. Japan setzt auf Kaizen-getriebene inkrementelle KI-Integration "
                    "— kleinere Teams, kontinuierliche Verbesserung, hohe Mitarbeitereinbindung. "
                    "Deutschland bevorzugt größere Transformationsprojekte mit klaren ROI-Kennzahlen. "
                    "Interessant: In der Produktivitätssteigerung liegen beide gleichauf (15-18% in 3 "
                    "Jahren), aber japanische Mitarbeiter berichten höhere Zufriedenheit mit der "
                    "KI-Einführung. Monozukuri-Prinzipien und deutsche Ingenieurskultur ergänzen sich "
                    "in hybriden Ansätzen besonders gut."
                ),
                "source": "BCG",
                "relevance_score": 9.2,
            },
            {
                "url": "https://www.bcg.com/publications/2024/german-japanese-manufacturing-partnership",
                "title": "Deutsch-japanische Fertigungspartnerschaften als Blaupause für KI-Adoption",
                "summary": (
                    "BCG dokumentiert fünf erfolgreiche Kooperationen zwischen deutschen Mittelständlern "
                    "und japanischen Produktionsunternehmen. Das gemeinsame Merkmal: Beide Kulturen "
                    "priorisieren Qualität und Langfristigkeit über kurzfristige Gewinne. In diesen "
                    "Partnerschaften werden KI-Systeme gemeinsam entwickelt, was Implementierungszeiten "
                    "um 40% verkürzt. Die Studie zeigt, wie Lean-Methoden aus Japan mit deutschen "
                    "Engineering-Standards kombiniert werden, um Predictive Maintenance-Systeme zu "
                    "schaffen, die in beiden Märkten funktionieren. Deutschland exportiert dabei "
                    "Maschinenbau-Know-how, Japan die Prozessphilosophie."
                ),
                "source": "BCG",
                "relevance_score": 8.9,
            },
            {
                "url": "https://www.iot-analytics.com/predictive-maintenance-manufacturing-2024",
                "title": "Predictive Maintenance 2024: IoT-Sensoren reduzieren Wartungskosten um 31%",
                "summary": (
                    "IoT Analytics hat 780 Fertigungsanlagen weltweit analysiert. Maschinen mit "
                    "Vibrations-, Temperatur- und Stromsensoren erreichen eine Fehlervorhersage-Genauigkeit "
                    "von 89% bei 48-Stunden-Vorlaufzeit. Die Implementierungskosten sind in den letzten "
                    "zwei Jahren um 45% gesunken. Kritischer Erfolgsfaktor: Saubere Basisdaten der ersten "
                    "6 Monate. Unternehmen, die mit 5-10 kritischen Maschinen starten und graduell "
                    "skalieren, zeigen dreifach höhere Erfolgsquoten als solche, die flächendeckend "
                    "starten. Edge-Computing ermöglicht dabei Reaktionszeiten unter 100ms ohne Cloud-Abhängigkeit."
                ),
                "source": "IoT Analytics",
                "relevance_score": 8.1,
            },
            {
                "url": "https://www.vdi.de/news/detail/industrie40-ki-integration-2024",
                "title": "VDI-Studie: KI-Integration in deutschen Fertigungsbetrieben — Status 2024",
                "summary": (
                    "Der VDI hat 1.200 deutsche Fertigungsunternehmen zum KI-Einsatz befragt. "
                    "Ergebnis: 34% nutzen bereits KI-Systeme produktiv, 41% planen Einführung in "
                    "den nächsten 24 Monaten. Größtes Hemmnis: Fachkräftemangel (67%), gefolgt von "
                    "Datenschutzbedenken (54%) und unklarem ROI (48%). Positive Überraschung: "
                    "Unternehmen aus dem Maschinenbau und der Elektrotechnik führen mit 52% "
                    "Adoptionsrate. Die Mitarbeiterakzeptanz steigt wenn KI als Unterstützung, "
                    "nicht als Ersatz positioniert wird. Drei von vier KI-Projekten im Mittelstand "
                    "starten mit weniger als 5 Personen im Kernteam."
                ),
                "source": "VDI",
                "relevance_score": 7.5,
            },
            {
                "url": "https://www.fraunhofer.de/de/presse/presseinformationen/2024/ki-mittelstand-automatisierung.html",
                "title": "Fraunhofer IPA: Modulare KI-Agenten für Mittelstand — Ergebnisse aus 3 Jahren Praxisforschung",
                "summary": (
                    "Das Fraunhofer IPA Stuttgart veröffentlicht Ergebnisse aus dem Forschungsprojekt "
                    "KI-Flex: 47 mittelständische Fertigungsunternehmen haben modulare KI-Agenten-Systeme "
                    "implementiert. Kernbefund: Standardisierte Schnittstellen (OPC-UA, MQTT) sind "
                    "entscheidend für schnelle Integration. Unternehmen mit vorhandener MES-Infrastruktur "
                    "benötigen im Schnitt 8 Wochen bis zum produktiven Betrieb. Die Forschungsgruppe "
                    "entwickelt derzeit KI-Agenten, die Produktionsparameter autonom optimieren — "
                    "erste Pilotunternehmen berichten von 12-18% Energieeinsparung ohne "
                    "Qualitätsverlust."
                ),
                "source": "Fraunhofer",
                "relevance_score": 8.3,
            },
            {
                "url": "https://www.meti.go.jp/english/press/2024/industrial-ai-strategy-2030.html",
                "title": "METI Japan: Industrial AI Strategy 2030 — Implikationen für deutsch-japanische Kooperationen",
                "summary": (
                    "Japans Wirtschaftsministerium METI hat die Industrial AI Strategy 2030 "
                    "veröffentlicht. Kern: 10 Billionen Yen Investitionen in industrielle KI bis "
                    "2030, Fokus auf Fertigung, Energie und Logistik. Für deutsche Unternehmen "
                    "besonders relevant: METI fördert explizit internationale Technologiepartnerschaften, "
                    "besonders mit EU-Unternehmen. Das Monozukuri-Framework wird mit KI-Agenten "
                    "kombiniert — Qualitätssicherung, Prozessoptimierung und Wissensweitergabe "
                    "sollen automatisiert werden. Erste Pilotprojekte mit deutschen Maschinenherstellern "
                    "zeigen Effizienzsteigerungen von 25-30% in der Qualitätskontrolle."
                ),
                "source": "METI",
                "relevance_score": 9.0,
            },
        ]
