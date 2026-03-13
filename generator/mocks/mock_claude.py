"""Mock Claude client — returns realistic German posts without API calls."""
from typing import Optional

MOCK_POSTS = {
    "trend": """Letzte Woche war ich bei einem Automobilzulieferer in der Nähe von Augsburg. 250 Mitarbeiter, dritte Generation Familienunternehmen, hervorragende Qualität — aber die Maschinen sprechen noch nicht miteinander.

Der Geschäftsführer zeigte mir einen Ordner mit handgeschriebenen Wartungsprotokollen. Seit 1987. Jede Seite voll mit Mustern, die kein Mensch in vertretbarer Zeit analysieren kann.

Wir haben in vier Stunden einen einfachen KI-Agenten aufgesetzt, der diese Daten digitalisiert und visualisiert. Das Ergebnis: Drei Maschinen zeigen ein Vibrationsmuster, das in 78% der historischen Fälle sechs Wochen vor einem Ausfall auftritt.

Kein Big-Bang. Kein ERP-Austausch. Nur ein gezielter Einstieg an einem konkreten Problem.

Ich glaube, das ist der richtige Weg für den Mittelstand. Nicht die universelle KI-Plattform für alles auf einmal, sondern ein Werkzeug, das ein spezifisches Problem löst und dabei vertraut wird.

Die nächste Frage des Geschäftsführers: "Können wir das auf alle 47 Anlagen ausrollen?" — Können wir. Aber langsam und richtig.

#KIAgenten #Mittelstand #PredictiveMaintenance #Fertigung""",

    "japan_germany": """Vor zwei Jahren war ich das erste Mal in einer Fabrik in Nagoya. Was mich am meisten beeindruckt hat: Die Stille.

Nicht weil wenig los war — im Gegenteil. Sondern weil jeder genau wusste was zu tun war. Kaizen nicht als Methode, sondern als Haltung. Kontinuierliche Verbesserung als tägliche Praxis, nicht als Jahresprojekt.

In deutschen Fabriken erlebe ich oft das Gegenteil: Große Transformationsprojekte, klare Businesscases, starke Ingenieurskultur — aber manchmal fehlt die Geduld für das Inkrementelle.

Was mich bei KI-Projekten am meisten überrascht: Die erfolgreichsten Implementierungen in Deutschland ähneln dem japanischen Ansatz mehr als dem Silicon-Valley-Ansatz. Klein anfangen. Messen. Anpassen. Wiederholen.

Ein Fertigungsunternehmen aus Bayern, mit dem wir arbeiten, hat genau das gemacht: Ein KI-Agent für die Qualitätskontrolle einer einzigen Produktlinie. 14 Monate später läuft er auf 23 Linien.

Monozukuri — die Kunst des Machens — und deutscher Maschinenbau teilen mehr als man denkt.

#JapanDeutschland #Fertigung #KIAgenten #Mittelstand""",

    "manufacturing_iot": """Eine Zahl, die mich letzte Woche nicht losgelassen hat: 73%.

So viel Prozent der ungeplanten Maschinenstillstände in der Fertigung wären mit vorhandenen Sensordaten vorhersehbar — wenn diese Daten systematisch ausgewertet würden.

Die meisten Maschinen in deutschen Fertigungsbetrieben senden bereits Daten: Temperatur, Vibration, Stromaufnahme. Sie liegen in irgendwelchen Systemen. Ungenutzt.

Das ist kein Technologieproblem. Es ist ein Integrations- und Interpretationsproblem.

Wir arbeiten gerade mit einem mittelständischen Maschinenbauer zusammen, der genau das löst. Keine neue Hardware. Keine neue Sensorik. Nur ein KI-Agent, der bestehende Datenströme interpretiert und Wartungsteams 48 Stunden vorher informiert.

Nach drei Monaten: Stillstandzeiten um 34% reduziert. Wartungskosten um 28% gesunken. Das Team schläft besser.

IoT ist nicht das Ziel. Weniger unerwartete Ausfälle ist das Ziel.

#IoT #PredictiveMaintenance #Industrie40 #KIAgenten""",

    "thought_leadership": """Ich werde oft gefragt: "Werden KI-Agenten Arbeitsplätze in der Fertigung ersetzen?"

Meine ehrliche Antwort: Manche Jobs werden sich fundamental verändern. Aber ich glaube nicht, dass das die entscheidende Frage ist.

Die entscheidende Frage ist: Wer entscheidet wie diese Veränderung passiert?

In den Unternehmen, bei denen ich sehe dass KI-Einführungen gut laufen, sind die Mitarbeiter am Shopfloor von Anfang an dabei. Nicht als Betroffene, sondern als Experten. Weil sie das Prozesswissen haben, das kein Datensatz der Welt hat.

Der erfahrene Maschinenbediener, der nach 20 Jahren am Ton der Maschine hört wenn etwas nicht stimmt — dieses Wissen ist Gold. Ein KI-Agent kann es skalierbar machen. Aber er kann es nicht ersetzen.

Meine Überzeugung: Die besten KI-Projekte in der Fertigung entstehen wenn Technologen zuhören bevor sie bauen.

Was ich mir für den Mittelstand wünsche: Mehr Projekte die mit "Was nervt euch am meisten?" anfangen — nicht mit "Hier ist unsere KI-Lösung."

#KI #Fertigung #Mittelstand #Zukunft""",

    "behind_scenes": """Ehrlicher Moment: Unser erstes großes KI-Projekt für einen Kunden ist vor anderthalb Jahren gescheitert.

Nicht technisch. Alles hat funktioniert. Der Pilot war ein Erfolg. Die Zahlen stimmten.

Es scheiterte weil wir den mittleren Kader nicht eingebunden hatten. Die Schichtleiter wurden informiert, nicht beteiligt. Und als das System live ging, haben sie es — verständlicherweise — nicht aktiv unterstützt.

Sechs Monate Arbeit. Rollback nach zwei Wochen Produktion.

Was wir seitdem immer machen: Das Change-Programm läuft parallel zum technischen Projekt. Nicht danach.

Ich erzähle das weil ich öfter von ähnlichen Erfahrungen in anderen Unternehmen höre. Und weil ich glaube, dass Scheitern in diesem Bereich nichts ist, worüber man nicht offen sprechen sollte.

KI im Mittelstand wird nicht an der Technologie scheitern. Es scheitert an Change-Management und an zu wenig Ehrlichkeit über die eigentlichen Hindernisse.

#KIAgenten #Mittelstand #Erfahrungen #KurokoLabs""",
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
        return {"score": 8, "reason": "Mock: post sounds authentic and concrete"}

    def generate_image_prompt(self, post: str) -> str:
        return (
            "Minimalist black and white photograph of industrial machinery gears and sensors, "
            "Japanese-German aesthetic, no people, no text, high contrast, clean composition"
        )
