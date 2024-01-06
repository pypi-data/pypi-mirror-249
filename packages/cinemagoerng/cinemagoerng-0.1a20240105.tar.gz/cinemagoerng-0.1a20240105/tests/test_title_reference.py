import pytest

from cinemagoerng import web


@pytest.mark.parametrize(("imdb_id", "primary_image"), [
    ("tt0133093", "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX101_CR0,0,101,150_.jpg"),  # The Matrix
    ("tt3629794", None),  # Aslan
])
def test_title_parser_should_set_primary_image_from_thumbnail(imdb_id, primary_image):
    parsed = web.get_title(imdb_id=imdb_id, page="reference")
    assert parsed.primary_image == primary_image


@pytest.mark.parametrize(("imdb_id", "n", "cast"), [
    ("tt7045440", 1, [  # David Bowie: Ziggy Stardust
        ("nm0000309", "David Bowie", "David Bowie", []),
    ]),
    ("tt0101597", 2, [  # Closet Land
        ("nm0000614", "Alan Rickman", "Interrogator", []),
        ("nm0000656", "Madeleine Stowe", "Victim", []),
    ]),
    ("tt1000252", 12, [  # Blink
        ("nm0855039", "David Tennant", "The Doctor", []),
        ("nm1303956", "Freema Agyeman", "Martha Jones", []),
        ("nm1659547", "Carey Mulligan", "Sally Sparrow", []),
        ("nm1164725", "Lucy Gaskell", "Kathy Nightingale", []),
        ("nm1015511", "Finlay Robertson", "Larry Nightingale", []),
        ("nm0134458", "Richard Cant", "Malcolm Wainwright", []),
        ("nm0643394", "Michael Obiora", "Billy Shipton", []),
        ("nm0537158", "Louis Mahoney", "Old Billy", []),
        ("nm1631281", "Thomas Nelstrop", "Ben Wainwright", []),
        ("nm2286323", "Ian Boldsworth", "Banto", []),
        ("nm0768205", "Raymond Sawyer", "Desk Sergeant", ["as Ray Sawyer"]),
        ("nm4495179", "Elen Thomas", "Weeping Angel", ["uncredited"]),
    ]),
    ("tt0133093", 41, []),  # The Matrix
    ("tt3629794", 0, []),  # Aslan
])
def test_title_reference_parser_should_set_all_cast(imdb_id, n, cast):
    parsed = web.get_title(imdb_id=imdb_id, page="reference")
    assert len(parsed.cast) == n
    if len(cast) > 0:
        assert [(credit.imdb_id, credit.name, credit.role, credit.notes)
                for credit in parsed.cast] == cast


@pytest.mark.parametrize(("imdb_id", "n", "directors"), [
    ("tt1000252", 1, [  # Blink
        ("nm0531751", "Hettie Macdonald", None, [])
    ]),
    ("tt0133093", 2, [  # The Matrix
        ("nm0905154", "Lana Wachowski", None, ["as The Wachowski Brothers"]),
        ("nm0905152", "Lilly Wachowski", None, ["as The Wachowski Brothers"]),
    ]),
    ("tt0092580", 10, [  # Aria
        ("nm0000265", "Robert Altman", None, ['segment "Les Boréades"']),
        ("nm0000915", "Bruce Beresford", None, ['segment "Die tote Stadt"']),
        ("nm0117317", "Bill Bryden", None, ['segment "I pagliacci"']),
        ("nm0000419", "Jean-Luc Godard", None, ['segment "Armide"']),
        ("nm0418746", "Derek Jarman", None, ['segment "Depuis le jour"']),
        ("nm0734466", "Franc Roddam", None, ['segment "Liebestod"']),
        ("nm0001676", "Nicolas Roeg", None, ['segment "Un ballo in maschera"']),
        ("nm0001692", "Ken Russell", None, ['segment "Nessun dorma"']),
        ("nm0836430", "Charles Sturridge", None, ['segment "La virgine degli angeli"']),
        ("nm0854697", "Julien Temple", None, ['segment "Rigoletto"']),
    ]),
    ("tt3629794", 0, []),  # Aslan
])
def test_title_reference_parser_should_set_all_directors(imdb_id, n, directors):
    parsed = web.get_title(imdb_id=imdb_id, page="reference")
    assert len(parsed.directors) == n
    if len(directors) > 0:
        assert [(credit.imdb_id, credit.name, credit.role, credit.notes)
                for credit in parsed.directors] == directors


@pytest.mark.parametrize(("imdb_id", "n", "writers"), [
    ("tt7045440", 1, [  # David Bowie: Ziggy Stardust
        ("nm0000309", "David Bowie", None, [])
    ]),
    ("tt0133093", 2, [  # The Matrix
        ("nm0905152", "Lilly Wachowski", None, ["written by", "as The Wachowski Brothers"]),
        ("nm0905154", "Lana Wachowski", None, ["written by", "as The Wachowski Brothers"]),
    ]),
    ("tt0076786", 3, [  # Suspiria
        ("nm0000783", "Dario Argento", None, ["screenplay"]),
        ("nm0630453", "Daria Nicolodi", None, ["screenplay"]),
        ("nm0211063", "Thomas De Quincey", None, ['book "Suspiria de Profundis"', "uncredited"]),
    ]),
    ("tt0092580", 10, []),  # Aria
    ("tt0365467", 0, []),  # Making 'The Matrix'
])
def test_title_reference_parser_should_set_all_writers(imdb_id, n, writers):
    parsed = web.get_title(imdb_id=imdb_id, page="reference")
    assert len(parsed.writers) == n
    if len(writers) > 0:
        assert [(credit.imdb_id, credit.name, credit.role, credit.notes)
                for credit in parsed.writers] == writers


@pytest.mark.parametrize(("imdb_id", "n", "crew"), [
    ("tt1000252", 4, [  # Blink
        ("nm2289913", "Charlotte Mitchell", "costume supervisor", []),
        ("nm2939651", "Sara Morgan", "costume assistant", []),
        ("nm1574636", "Bobbie Peach", "costume assistant", ["as Bobby Peach"]),
        ("nm1834907", "Stephen Kill", "costume prop maker", ["uncredited"]),
    ]),
])
def test_title_reference_parser_should_set_all_crew(imdb_id, n, crew):
    parsed = web.get_title(imdb_id=imdb_id, page="reference")
    parsed_crew = parsed.costume_department
    assert len(parsed_crew) == n
    if len(crew) > 0:
        assert [(credit.imdb_id, credit.name, credit.role, credit.notes)
                for credit in parsed_crew] == crew
