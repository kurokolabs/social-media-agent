"""Mock Claude client — returns realistic German posts without API calls."""

MOCK_POSTS = {
    "trend": """Eine Beobachtung, die uns bei Kuroko Labs in letzter Zeit häufiger begegnet: Fertigungsbetriebe haben die Diskussion über KI-Einführung längst hinter sich gelassen. Die Frage ist nicht mehr ob, sondern wie — und vor allem wie schnell.

Was wir dabei wahrnehmen: Der Druck kommt seltener von der Geschäftsführung als von den Operations-Teams selbst. Schichtleiter und Produktionsleiter, die konkrete Probleme haben und konkrete Lösungen suchen. Keine Strategie-Workshops. Keine Digitaliserungsoffensiven. Sondern: Diese eine Maschine fällt uns zu oft aus. Können wir das vorhersagen?

Das ist eigentlich eine gute Ausgangslage. Projekte mit einem klar definierten Ausgangsproblem haben eine deutlich höhere Umsetzungsrate als solche, die aus einer vagen „wir müssen jetzt KI machen"-Logik entstehen.

Was wir als Hindernis erleben: Die Daten sind oft da. Sensoren laufen. Maschinenprotokolle existieren. Aber sie liegen in Systemen, die nicht miteinander sprechen, und werden von niemandem systematisch ausgewertet.

Das ist kein Technologieproblem. Es ist meistens ein Prioritätenproblem — und manchmal ein Ressourcenproblem.

#KIAgenten #Fertigung #Mittelstand #Automatisierung""",

    "japan_germany": """BCG hat kürzlich einen Vergleich zwischen japanischen und deutschen Fertigungsunternehmen bei der KI-Einführung veröffentlicht. Das Ergebnis ist weniger überraschend als die Begründung dahinter.

Beide Länder erzielen ähnliche Produktivitätssteigerungen — der Unterschied liegt im Weg dorthin. Japanische Unternehmen tendieren zu kleinschrittiger, mitarbeitergetriebener Integration. Deutsche Unternehmen zu größeren Transformationsprojekten mit klaren Businesscases vorab.

Was uns bei Kuroko Labs auffällt: Die Projekte die bei deutschen Mittelständlern am besten laufen, ähneln strukturell eher dem japanischen Ansatz — obwohl das niemand so nennt. Ein abgegrenztes Problem, ein kleines Team, ein messbares Ziel. Dann Erweiterung.

Die Kaizen-Logik — kontinuierliche Verbesserung statt Einmalumstellung — ist eigentlich keine japanische Besonderheit. Sie ist einfach pragmatisch.

Was dabei verloren geht: Viele Mittelständler warten auf den richtigen Moment für das große Projekt. Der kommt selten. Der Einstieg mit einem kleinen, gut definierten Problem ist kein Kompromiss — er ist oft der direktere Weg.

#JapanDeutschland #Fertigung #KIAgenten #Industrie40""",

    "manufacturing_iot": """Laut einer aktuellen IoT-Analytics-Auswertung laufen in einem Großteil der analysierten Fertigungsanlagen bereits Sensoren — Temperatur, Vibration, Stromaufnahme. Die Daten werden gesammelt. Sie werden nur selten systematisch ausgewertet.

Das ist ein Befund, den wir bei Kuroko Labs aus Gesprächen mit Produktionsbetrieben kennen. Nicht weil die Unternehmen das nicht wollen, sondern weil der Schritt von „Daten vorhanden" zu „Daten nutzbar" unterschätzt wird. Verschiedene Systeme, verschiedene Formate, kein einheitliches Bild.

Predictive Maintenance ist als Konzept längst angekommen. Die Lücke liegt zwischen dem Konzept und der tatsächlichen Umsetzung auf Basis vorhandener Infrastruktur.

Was wir dabei beobachten: Unternehmen, die mit einer einzigen Anlage oder einer einzigen Maschinenklasse starten, kommen deutlich weiter als die, die direkt flächendeckend einführen wollen. Nicht weil die Technologie das erfordern würde — sondern weil die Organisation es tut.

Der technische Teil ist lösbar. Die Frage ist meistens: Wer im Unternehmen nimmt das in die Hand?

#IoT #PredictiveMaintenance #Industrie40 #Fertigung""",

    "thought_leadership": """Eine Frage, die uns bei Kuroko Labs regelmäßig in Gesprächen mit Fertigungsbetrieben begegnet: "Wir wollen KI einführen — aber wir wissen nicht, womit wir anfangen sollen."

Das klingt nach einem Technologieproblem. Es ist keins.

Meistens fehlt nicht das Wissen über verfügbare Tools. Es fehlt die Einigkeit darüber, welches Problem zuerst gelöst werden soll. KI-Projekte die ohne diese Einigkeit starten, enden häufig in Piloten, die niemand weiterführt — nicht weil das System schlecht war, sondern weil kein klarer Eigentümer definiert war.

Was wir aus unserer Praxis mitnehmen: Der erste und wichtigste Schritt ist nicht die Technologieauswahl. Es ist die Frage: Was kostet uns am meisten — in Zeit, in Fehlern, in manueller Arbeit? Und wer im Unternehmen hat das Problem täglich auf dem Tisch?

Wenn diese Frage beantwortet ist, wird die Technologieentscheidung fast zweitrangig. Dann gibt es selten zehn Optionen, sondern zwei oder drei.

#KIAgenten #Mittelstand #Prozessoptimierung #Fertigung""",

    "behind_scenes": """Was uns bei der Arbeit an KI-Projekten für Fertigungsbetriebe immer wieder auffällt: Die technische Umsetzung ist selten der schwierigste Teil.

Was häufiger zum Problem wird: Das System läuft, aber der Alltag ändert sich nicht. Warnmeldungen werden erzeugt und ignoriert. Dashboards existieren und werden nicht geöffnet. Nicht aus Desinteresse, sondern weil niemand im Tagesablauf explizit Zeit dafür vorgesehen hat.

Das ist keine Kritik an den Betrieben — es ist ein Planungsproblem, das wir als Dienstleister mitverantworten. Ein KI-System das Daten auswertet ist kein fertiges Produkt. Es ist der Ausgangspunkt für eine veränderte Arbeitsweise.

Bei Kuroko Labs haben wir gelernt, dieses Gespräch früher zu führen: Wer schaut täglich auf welche Information? Was ändert sich in der Entscheidung wenn das System einen Alarm ausgibt? Wer ist zuständig?

Diese Fragen klingen unspektakulär. Sie entscheiden darüber ob ein Projekt im Betrieb ankommt oder im Reporting bleibt.

#KurokoLabs #KIAgenten #Fertigung #Mittelstand""",
}


class MockClaudeClient:
    """Mock Claude client — returns realistic posts without API calls."""

    def generate_post(self, system: str, user: str, post_type: str) -> dict:
        content = MOCK_POSTS.get(post_type, MOCK_POSTS["trend"])
        return {
            "content": content,
            "post_type": post_type,
            "tokens_in": 450,
            "tokens_out": 280,
            "cost_usd": 0.0,
        }

    def evaluate_post(self, post: str) -> dict:
        return {"score": 8, "reason": "Mock: observation-based company voice, no invented results"}

    def generate_image_prompt(self, post: str) -> str:
        return (
            "Minimalist black and white photograph of industrial machinery gears and sensors, "
            "Japanese-German aesthetic, no people, no text, high contrast, clean composition"
        )
