# Anime2You (Inoffiziell)

Dies ist eine **INOFFIZIELLE** Bibliothek speziell für die Website [Anime2You](https://www.anime2you.de/) um aktuelle
Artikel zu empfangen.

Der Client nutzt die Möglichkeit der RSS-Feed funktion von Anime2You, um die aktuellen Artikel abzurufen.

# Nutzung

Die Library eignet sich hervorragend, um aktuelle Anime2You Artikel bei sich im Programm einzubinden z.B. in form eines
Discord Bots oder auf der eigenen Website.

Bitte gebe immer den Urheber (Anime2You) an und verkaufe die Artikel nicht als die eigenen. Die Möglichkeit geben
den Artikel direkt bei Anime2You aufzurufen wäre ebenfalls nicht schlecht, um Anime2You damit zu unterstützen. 

# Installation

Mit pip installieren

``pip install anime2you``

pip + github

``pip install git+https://github.com/princessmiku/anime2you``

# Einrichtung

Die Einrichtung ist einfach und unkompliziert, nach erfolgreicher Installation kann man wie folgt den RSSManager nutzen.

`````python
from anime2you import RSSManager

manager = RSSManager()
`````

nun ist das System in der Grundfunktion bereits verfügbar.

## RSSManager
Der RSSManager ist der Verwalter des Feeds, dieser ist dafür zuständig den Feed zu empfangen.

Der RSSManager hat folgende Optionen:

- ``feed_type`` > hier kann man auswählen welchen feed man möchte. Anime2You gibt da 3 Möglichkeiten, `ganzer Feed`, `nur Artikel` oder `nur Streams`
- ``use_cache`` > das ist eine Option um das Caching zu aktiveren, was die Funktion nutzbar macht, um sich nur die neusten News Einträge anzeigen zu lassen, da er dann den Timestamp des letzten Feeds speichert.
- ``cache_path`` > hier kann man einen custom path für den caching Ordner setzen. Andernfalls wird im ausführenden verzeichnis ein ordner namens `cache` erstellt für das Caching.

### feed_type
Standardmäßig wird der komplette Feed geladen. Möchte man nun etwas filtern, so kann man die Variablen in der RSSManager Klasse nutzen.

- ``RSSManager.FEED_COMPLETE`` für den gesamten Feed
- ``RSSManager.FEED_ARTICLES`` damit nur News geladen werden
- ``RSSManager.FEED_STREAMS`` damit nur Streams geladen werden

**Beispielhafte Nutzung**

`````python
from anime2you import RSSManager

manager = RSSManager(RSSManager.FEED_COMPLETE)
`````

### use_cache und cache_path

``use_cach`` ist ein boolean der entweder auf `True` oder `False` sein kann. True = An, False = Aus

``cache_path`` dort kann man einen eigenen Ordner setzen für den Cache

**Beispielhafte Nutzung**

`````python
from anime2you import RSSManager

manager = RSSManager(
    feed_type=RSSManager.FEED_COMPLETE,
    use_cache=True,
    cache_path="./cache"
)
`````

### Abrufen des Feeds

Um einen Feed abzurufen stehen ``get_feed()`` und ``get_new_feed()`` zur verfügung.
Beim ``get_new_feed()`` ist zu beachten das Caching aktiviert ist für das Ordnungsgemäße funktionieren.
Es wird eine Liste aus ``Feed`` klassen zurückgegeben.

`````python
from anime2you import RSSManager, Feed

manager = RSSManager()
feeds: list[Feed] = manager.get_feed() # für den gesamten
new_feeds: list[Feed] = manager.get_new_feed() # für die neuen
`````

## Feed

Der Feed ist der Artikel von Anime2You in einer Klasse zum Nutzen. Er wird Feed genannt, da man im RSS System einen Feed empfängt.

Der Feed beinhaltet folgenden informationen 

- ``id`` > `str` | Ist die ID wie angegeben, sie besteht aus einer URL mit der ID
- ``short_id`` > `str` | Ist die ID extrahiert ohne die URL dafür
- ``link`` > `str` | Ist die Url wie sie im Browser in der URL Leiste zu finden ist
- ``title`` > `str` | Ist der Titel des Artikels
- ``description`` > `str` | Ist die Beschreibung vom Artikel
- ``published`` > `datetime` | Ist das Datum der veröffentlichung
- ``image_url`` > `str` | Ist der Link zu der Bild ressource
- ``authors`` > `list str` | Ist eine Liste mit den Autoren von dem Artikel
- ``tags`` > `list str` | Ist eine Liste mit den genutzten Tags
- ``raw_rss_item`` > `dict` | Ist das dictionary wie der Artikel empfangen wird unverarbeitet, dort man z.B. direkten HTML code

außerdem bietet die Klasse noch die funktion über ``to_dict()`` oder direkt per ``dict(feed)`` in ein dictionary umwandeln lassen zu lassen.


# Weiteres

Für fortgeschrittenere Entwickler ist es auch möglich das Caching für den RSSManager anpassen um es durch z.B. eine Datenbank zu ersetzen. Man muss diesen nur in eine neue Klasse vererben und folgende funktionen umschreiben

``def set_cache_feed_published(self, date: datetime):`` und ``def get_cache_feed_published(self) -> datetime:``

dabei ist zu beachten, das die funktionen das datetime format annehmen und das datetime format zurückgeben.
