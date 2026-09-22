#!/usr/bin/env python3
"""Generuje narratora, efekty i muzykę przez ElevenLabs do katalogu audio/."""
import json, os, subprocess, sys, time

KLUCZ = None
for linia in open('/Users/mateuszwojczal/Desktop/localhost/gra-franek/.env'):
    if linia.startswith('ELEVEN_LABS_API_KEY='):
        KLUCZ = linia.split('=', 1)[1].strip()
assert KLUCZ, 'brak klucza'

KAT = '/Users/mateuszwojczal/Desktop/localhost/gra-franek/audio'
os.makedirs(KAT, exist_ok=True)

GLOS = os.environ.get('GLOS', 'FGY2WhTYpPnrIDTdsKH5')   # Laura
MODEL = 'eleven_multilingual_v2'

def poslij(url, dane, plik, proby=3):
    """Wysyła przez curl – Pythonowy urllib nie ma tu certyfikatów SSL."""
    sciezka = os.path.join(KAT, plik)
    if os.path.exists(sciezka) and os.path.getsize(sciezka) > 2000:
        return 'pominięto (jest)'
    for p in range(proby):
        wynik = subprocess.run(
            ['curl', '-s', '-o', sciezka, '-w', '%{http_code}', '--max-time', '300',
             '-X', 'POST', url,
             '-H', 'xi-api-key: ' + KLUCZ,
             '-H', 'Content-Type: application/json',
             '-d', json.dumps(dane)],
            capture_output=True, text=True)
        kod = wynik.stdout.strip()
        rozmiar = os.path.getsize(sciezka) if os.path.exists(sciezka) else 0
        if kod == '200' and rozmiar > 1000:
            return 'OK %.0f KB' % (rozmiar / 1024)
        tresc = ''
        if os.path.exists(sciezka):
            tresc = open(sciezka, 'rb').read()[:200].decode('utf-8', 'replace')
            os.remove(sciezka)
        if p == proby - 1:
            return 'BŁĄD HTTP %s %s' % (kod, tresc)
        time.sleep(3 * (p + 1))

def mowa(plik, tekst):
    return poslij('https://api.elevenlabs.io/v1/text-to-speech/' + GLOS,
                  {'text': tekst, 'model_id': MODEL,
                   'voice_settings': {'stability': 0.45, 'similarity_boost': 0.75,
                                      'style': 0.35, 'use_speaker_boost': True}},
                  plik)

def efekt(plik, opis, sek):
    return poslij('https://api.elevenlabs.io/v1/sound-generation',
                  {'text': opis, 'duration_seconds': sek, 'prompt_influence': 0.75}, plik)

def muzyka(plik, opis, ms):
    return poslij('https://api.elevenlabs.io/v1/music',
                  {'prompt': opis, 'music_length_ms': ms}, plik)

NARRACJA = {
    'start':        'Poranek Franka! Naciśnij strzałkę w górę, żeby zacząć.',
    'poziom1':      'Poziom pierwszy. Wstawaj Franek! Ubierz się po kolei.',
    'poziom2':      'Poziom drugi. Zejdź po schodach i zrób sobie śniadanko.',
    'poziom3':      'Poziom trzeci. Czas umyć ząbki!',
    'poziom4':      'Poziom czwarty. Ubieramy się i wychodzimy!',
    'poziom5':      'Poziom piąty. Idziemy do samochodu, tata już czeka.',
    'poziom6':      'Ostatni poziom! Jedziemy do przedszkola!',
    'zad_majtki':      'Znajdź majtki!',
    'zad_spodnie':     'Teraz spodnie!',
    'zad_skarpetki':   'Teraz skarpetki!',
    'zad_koszulka':    'Teraz koszulka!',
    'zad_miska':       'Znajdź miskę!',
    'zad_platki':      'Teraz łódeczki!',
    'zad_mleko':       'Teraz mleko!',
    'zad_lyzka':       'Znajdź łyżkę!',
    'zad_sniadanie':   'Zjedz śniadanko!',
    'zad_pasta':       'Znajdź pastę do zębów!',
    'zad_szczoteczka': 'Znajdź szczoteczkę!',
    'zad_zeby':        'Idź do umywalki!',
    'zad_czapka':      'Znajdź czapkę!',
    'zad_kurtka':      'Teraz kurtka!',
    'zad_buty':        'Teraz buty!',
    'zad_drzwi':       'Idź do drzwi!',
    'zad_samochod':    'Wsiadaj do samochodu!',
    'brawo1':       'Brawo!',
    'brawo2':       'Super!',
    'brawo3':       'Świetnie ci idzie!',
    'brawo4':       'Ekstra!',
    'zle':          'Jeszcze nie teraz. Weź to, co świeci!',
    'mycie':        'Myj ząbki! Naciskaj w lewo i w prawo.',
    'mycie_koniec': 'Ząbki czyściutkie! Brawo!',
    'jazda':        'Jedziemy! Strzałką w górę i w dół zmieniasz pas.',
    'jedzenie':     'Mniam mniam! Pyszne łódeczki z mleczkiem.',
    'ups':          'Ups! Ostrożnie!',
    'wybor':        'Kim chcesz grać? Strzałką w lewo wybierz Franka, w prawo Polę.',
    'poziom7':      'Poziom siódmy. Wyścig z tatą do furtki przedszkola!',
    'poziom8':      'Poziom ósmy. Szatnia! Rozbierz się i przytul tatę.',
    'poziom9':      'Ostatni poziom! Wyścig do okna. Zdąż pomachać tacie!',
    'zad_przytulas':'A teraz przytul tatę na do widzenia!',
    'przytulas':    'Ale super przytulas! Do widzenia tato, do zobaczenia!',
    'wyscig':       'Naciskaj strzałki w lewo i w prawo, żeby biec szybciej!',
    'wyscig_start': 'Trzy, dwa, jeden, start!',
    'wygrana':      'Wygrałeś! Brawo!',
    'pomachaj':     'Pomachaj tacie przez okno! Pa pa!',
    'zad_zdejmij_buty':   'Zdejmij buty!',
    'zad_zdejmij_kurtke': 'Powieś kurtkę!',
    'zad_zdejmij_czapke': 'Zdejmij czapkę!',
    'zad_okno':     'Biegnij do okna!',
    'zad_furtka':   'Biegnij do furtki!',
    'p_start':      'Poranek Poli! Naciśnij strzałkę w górę, żeby zacząć.',
    'p_koniec':     'Brawo Pola! Udało się! Jesteś w przedszkolu!',
    'p_poziom1':    'Poziom pierwszy. Wstawaj Pola! Czas wstać z łóżka.',
    'p_poziom2':    'Poziom drugi. Do łazienki! Umyj ząbki.',
    'p_poziom3':    'Poziom trzeci. Nakarm rybkę!',
    'p_poziom4':    'Poziom czwarty. Ubierz się!',
    'p_poziom5':    'Poziom piąty. Czas na śniadanko.',
    'p_poziom6':    'Poziom szósty. Wychodzimy do przedszkola!',
    'zad_kapcie':   'Znajdź kapcie!',
    'zad_mis':      'Zabierz misia!',
    'zad_grzebien': 'Uczesz się!',
    'zad_karma':    'Znajdź karmę dla rybki!',
    'zad_rybka':    'Nakarm rybkę!',
    'zad_legginsy': 'Teraz legginsy!',
    'zad_bluza':    'Teraz bluza!',
    'mama_czeka':   'Mama już czeka przy drzwiach!',
    'szybciej':     'Szybciej tata! Rura!',
    'mycie2':          'Szoruj w lewo i w prawo! Strzałka w górę i w dół zmienia ząbki.',
    'zeby_gora_przod': 'Górne ząbki z przodu!',
    'zeby_dol_przod':  'Dolne ząbki z przodu!',
    'zeby_gora_tyl':   'Teraz górne od środka!',
    'zeby_dol_tyl':    'Teraz dolne od środka!',
    'zeby_strefa_ok':  'Te ząbki już lśnią!',
    'zeby_minuta':  'Została jeszcze minuta mycia!',
    'zeby_pol':     'Została jeszcze pół minuty!',
    'zeby_20':      'Jeszcze dwadzieścia sekund!',
    'licz5':        'Pięć!',
    'licz4':        'Cztery!',
    'licz3':        'Trzy!',
    'licz2':        'Dwa!',
    'licz1':        'Jeden!',
    'szybciej2':    'Tata, jedź szybciej! Rura!',
    'koniec':       'Brawo Franek! Udało się! Jesteś w przedszkolu!',

    # --- nowe etapy poranka Franka: światło, wstawanie, siku ---
    'poziom_swiatlo':   'Poziom pierwszy. Ciemno! Zapal światło w pokoju.',
    'poziom_wstawanie': 'Poziom drugi. Wstawaj Franek! Wygrzeb się z łóżka.',
    'poziom_siku':      'Poziom trzeci. Lecimy do kibelka na siku!',
    'swiatlo_jak':      'Wyciągnij rączkę do ściany. Strzałki w lewo i w prawo, '
                        'a strzałka w górę naciska.',
    'swiatlo_ok':       'Jasno! Brawo Franek!',
    'swiatlo_zle':      'To nie to. Szukaj kontaktu na ścianie!',
    'wstawanie_jak':    'Naciskaj w lewo i w prawo na zmianę, żeby wstać z łóżka!',
    'wstawanie_ok':     'Wstałeś! Brawo! Teraz lecimy do kibelka.',
    'wstawanie_spij':   'Nie zasypiaj! Naciskaj szybciej!',
    'siku_jak':         'Sikaj do środka muszli. Strzałka w lewo bliżej, '
                        'w prawo dalej. Nie obsikaj deski!',
    'siku_deska':       'Ups! Celuj do wody w środku!',
    'siku_ok':          'Wszystko do środka i deska czysta! Brawo! Spłukujemy.',
    'siku_koniec':      'Spłukujemy. Teraz umyj rączki!',

    # --- wybór sposobu siku i sprzątanie po nietrafionym strumieniu ---
    'siku_wybor':       'Jak robimy siku? Strzałka w lewo, to na stojąco i trzeba '
                        'celować. Strzałka w prawo, to na siedząco i nic się nie obsika. '
                        'Strzałka w górę zaczyna.',
    'siku_siedzac':     'Siadasz na desce i siedzisz spokojnie. Wszystko leci prosto '
                        'do środka, więc nic się nie obsika.',
    'siku_splucz':      'Koniec siku! Naciśnij strzałkę w górę i spłucz wodę.',
    'siku_brudno':      'Ojej, obsikana deska i podłoga. Trzeba po sobie posprzątać.',
    'siku_sprzatanie':  'Jak się obsika deskę albo podłogę, to potem trzeba to umyć. '
                        'Naciskaj w lewo i w prawo na zmianę, żeby wycierać.',
    'siku_wytrzyj':     'Weź papier i wytrzyj deskę. Tam i z powrotem!',
    'siku_podloga':     'Teraz mop! Umyj kałużę na podłodze.',
    'siku_posprzatane': 'Wszystko czyściutkie! Brawo! Następnym razem celuj do środka.',

    # --- przenumerowane zapowiedzi poziomów Franka (po dodaniu trzech etapów) ---
    'f_poziom4':  'Poziom czwarty. Ubierz się po kolei.',
    'f_poziom5':  'Poziom piąty. Zejdź po schodach i zrób sobie śniadanko.',
    'f_poziom6':  'Poziom szósty. Czas umyć ząbki!',
    'f_poziom7':  'Poziom siódmy. Ubieramy się i wychodzimy!',
    'f_poziom8':  'Poziom ósmy. Idziemy do samochodu, tata już czeka.',
    'f_poziom9':  'Poziom dziewiąty. Jedziemy do przedszkola!',
    'f_poziom10': 'Poziom dziesiąty. Wyścig z tatą do furtki przedszkola!',
    'f_poziom11': 'Poziom jedenasty. Szatnia! Rozbierz się i przytul tatę.',
    'f_poziom12': 'Poziom dwunasty. Wyścig do okna. Zdąż pomachać tacie!',

    # --- dwanaście etapów Poli (tyle samo co u Franka) ---
    'p2_poziom1':  'Poziom pierwszy. Ciemno! Zapal światło w pokoju.',
    'p2_poziom2':  'Poziom drugi. Wstawaj Pola! Wygrzeb się z łóżka.',
    'p2_poziom3':  'Poziom trzeci. Znajdź kapcie i zabierz misia.',
    'p2_poziom4':  'Poziom czwarty. Do łazienki! Umyj ząbki i uczesz się.',
    'p2_poziom5':  'Poziom piąty. Nakarm rybkę!',
    'p2_poziom6':  'Poziom szósty. Ubierz się po kolei.',
    'p2_poziom7':  'Poziom siódmy. Czas na śniadanko.',
    'p2_poziom8':  'Poziom ósmy. Czapka, kurtka, buty. Mama już czeka!',
    'p2_poziom9':  'Poziom dziewiąty. Rowerem do przedszkola! Pedałuj strzałkami!',
    'p2_poziom10': 'Poziom dziesiąty. Wyścig z mamą do furtki przedszkola!',
    'p2_poziom11': 'Poziom jedenasty. Szatnia! Rozbierz się i przytul mamę.',
    'p2_poziom12': 'Ostatni poziom! Wyścig do okna. Zdąż pomachać mamie!',
    # kwestie w rodzaju żeńskim i z mamą zamiast taty
    'p_swiatlo_ok':    'Jasno! Brawo Pola!',
    'p_wstawanie_ok':  'Wstałaś! Brawo! Gdzie są kapcie?',
    'p_wygrana':       'Wygrałaś! Brawo!',
    'p_pomachaj':      'Pomachaj mamie przez okno! Pa pa!',
    'p_przytulas':     'Ale super przytulas! Do widzenia mamo, do zobaczenia!',
    'p_zad_przytulas': 'A teraz przytul mamę na do widzenia!',
    'p_szybciej':      'Szybciej mamo! Spóźnimy się!',
    'p_szybciej2':     'Mamo, jedź szybciej! Pędzimy!',
    # Pola jedzie rowerem, a mama biegnie za nią
    'p_rower_jak':       'Pola jedzie rowerem, a mama biegnie za nią! Naciskaj strzałki '
                         'w lewo i w prawo na zmianę, żeby pedałować.',
    'p_nie_tak_szybko':  'Pola, nie tak szybko! Poczekaj na mamę!',
    'p_nie_tak_szybko2': 'Pola, nie tak szybko! Mama nie nadąża!',

    # --- dalszy ciąg dnia Franka: przedszkole, powrót, wieczór w domu ---
    'f_poziom13': 'Poziom trzynasty. Kółko powitalne! Przywitaj się z dziećmi.',
    'f_poziom14': 'Poziom czternasty. Cały dzień w przedszkolu!',
    'f_poziom15': 'Poziom piętnasty. Tata przyszedł! Uciekaj, jeśli nie chcesz się myć!',
    'f_poziom16': 'Poziom szesnasty. Jedziemy do domu i słuchamy Kociej szajki.',
    'f_poziom17': 'Poziom siedemnasty. Tankujemy auto. Nie rozlej benzyny!',
    'f_poziom18': 'Poziom osiemnasty. Idziemy do domu. Przywitaj się z Igorem!',
    'f_poziom19': 'Poziom dziewiętnasty. Jesteśmy w domu, mama czeka w drzwiach.',
    'kolko_jak':  'Chodź dookoła kółka strzałkami, a strzałką w górę mów cześć.',
    'kolko_ok':   'Przywitałeś się ze wszystkimi dziećmi! Brawo!',
    'dzien_klocki': 'Budujemy wielką wieżę z klocków!',
    'dzien_farby':  'Malujemy farbami. Ale się ubrudziłeś!',
    'dzien_obiad':  'Obiadek! Zupka i kompot.',
    'dzien_lezak':  'Leżakowanie. Cichutko, sza!',
    'dzien_plac':   'Plac zabaw! Piasek i zjeżdżalnia!',
    'dzien_koniec': 'Koniec dnia w przedszkolu. Tata już idzie po ciebie!',
    'lapanie_jak':     'Tata pyta: idziemy się umyć? Uciekaj! Naciskaj strzałki na zmianę.',
    'lapanie_uciekl':  'Uciekłeś tacie! Dzisiaj się nie myjemy!',
    'lapanie_zlapany': 'Mam cię! Idziemy umyć rączki i buzię.',
    'mycie_rak':       'Myjemy rączki i buzię. Szoru, szoru!',
    'jazda_dom':   'Jedziemy do domu. W radiu leci Kocia szajka!',
    'tank_jak':     'Trzymaj strzałkę w górę i tankuj. Puść w zielonym polu, nie rozlej benzyny!',
    'tank_ok':      'Zatankowane! Ani kropli obok. Brawo!',
    'tank_rozlane': 'Ojej, benzyna się rozlewa! Puszczaj!',
    'zad_igor':    'Powiedz cześć Igorowi!',
    'czesc_igor':  'Cześć Igor! My już idziemy do domu.',
    'dom_czysty':  'Fajnie, że wróciliście chłopaki!',
    'dom_brudny':  'Ale brudas! Idziemy się myć i przebrać!',
    'dom_lapie':   'Mam cię! Do łazienki!',
    'dom_koniec':  'Umyty i przebrany w piżamkę. Brawo Franek!',
    'f_koniec2':   'Brawo Franek! Cały dzień za tobą. Umyty, przebrany, w domu!',

    # --- Pola wybiera: do przedszkola z mamą Olą albo z tatą Adamem ---
    'p_wybor_opiekuna': 'Z kim idziesz dziś do przedszkola? Strzałka w lewo to mama, '
                        'w prawo tata. Strzałka w górę zaczyna.',
    'pt_zad_przytulas': 'A teraz przytul tatę na do widzenia!',
    'pt_przytulas':     'Ale super przytulas! Do widzenia tato, do zobaczenia!',
    'pt_pomachaj':      'Pomachaj tacie przez okno! Pa pa!',
    'pt_szybciej':      'Szybciej tato! Spóźnimy się!',
    'pt_szybciej2':     'Tato, jedź szybciej! Pędzimy!',
    'pt_rower_jak':       'Pola jedzie rowerem, a tata biegnie za nią! Naciskaj strzałki '
                          'w lewo i w prawo na zmianę, żeby pedałować.',
    'pt_nie_tak_szybko':  'Pola, nie tak szybko! Poczekaj na tatę!',
    'pt_nie_tak_szybko2': 'Pola, nie tak szybko! Tata nie nadąża!',
    'pt2_poziom8':      'Poziom ósmy. Czapka, kurtka, buty. Tata już czeka!',
    'pt2_poziom10':     'Poziom dziesiąty. Wyścig z tatą do furtki przedszkola!',
    'pt2_poziom11':     'Poziom jedenasty. Szatnia! Rozbierz się i przytul tatę.',
    'pt2_poziom12':     'Ostatni poziom! Wyścig do okna. Zdąż pomachać tacie!',

    # --- wieczór Franka w domu: zabawa, Igor, kolacja, kąpiel, książka i sen ---
    'f_poziom20': 'Poziom dwudziesty. Zabawa w domu! Tory, lego i rebusy z gazetki.',
    'f_poziom21': 'Poziom dwudziesty pierwszy. Wspinaj się po ściance i przez płot do Igora!',
    'f_poziom22': 'Poziom dwudziesty drugi. Zabawa u Igora za płotem!',
    'f_poziom23': 'Poziom dwudziesty trzeci. Kolacja! Dzisiaj fish and chips.',
    'f_poziom24': 'Poziom dwudziesty czwarty. Kąpiel! Umyj się cały, część po części.',
    'f_poziom25': 'Poziom dwudziesty piąty. Jeszcze ząbki i piżamka.',
    'f_poziom26': 'Poziom dwudziesty szósty. Tata poczyta ci książkę na dobranoc.',
    'f_poziom27': 'Ostatni poziom! Franek śpi i śni o kotkach, co rzucały śnieżkami.',
    'zad_tory':      'Rozłóż tory z kolejką!',
    'zad_lego':      'Teraz klocki lego!',
    'zad_rebusy':    'Teraz rebusy z gazetki!',
    'zad_plot':      'Wspinaj się po ściance i idź przez płot do Igora!',
    'zad_ryba':      'Znajdź rybkę w panierce!',
    'zad_frytki':    'Teraz frytki!',
    'zad_kolacja':   'Zjedz kolację!',
    'kolacja_mniam': 'Mniam mniam! Pyszna rybka z frytkami.',
    'zad_pizama':    'Ubierz piżamkę!',
    'igor_pilka':    'Gramy z Igorem w piłkę!',
    'igor_autka':    'Ścigamy się autkami po trawie!',
    'igor_chowany':  'Gramy w chowanego. Gdzie jest Igor?',
    'igor_koniec':   'Pa pa Igor! Mama woła na kolację.',
    'kapiel_jak':     'Kąpiel! Szoruj gąbką w lewo i w prawo. Umyjemy się cały, po kolei.',
    'kapiel_szyja':   'Najpierw szyja!',
    'kapiel_glowa':   'Teraz głowa!',
    'kapiel_rece':    'Teraz rączki!',
    'kapiel_nogi':    'Teraz nóżki!',
    'kapiel_pupa':    'Teraz pupa!',
    'kapiel_stopy':   'I jeszcze stopy!',
    'kapiel_czysta':  'Ta część już czyściutka!',
    'kapiel_recznik': 'Cały umyty! Teraz wytrzyj się ręcznikiem.',
    'kapiel_koniec':  'Czysty i suchy! Brawo Franek.',
    'ksiazka_wybor':     'Którą książkę czyta dziś tata? Strzałkami w lewo i w prawo wybierasz, '
                         'a strzałka w górę zaczyna.',
    'ksiazka_muminki':   'Muminki! Dolina Muminków śpi pod śniegiem.',
    'ksiazka_kocia':     'Kocia szajka! Koty ruszają na wyprawę.',
    'ksiazka_pirat':     'Pirat Rabarbar! Płyniemy po skarb.',
    'ksiazka_autka':     'Auta! Zygzak McQueen pędzi po torze.',
    'ksiazka_przytulas': 'Koniec książki. Przytul mamę na dobranoc!',
    'ksiazka_dobranoc':  'Gasimy światło. Dobranoc Franek!',
    'sen_jak':    'Franek śpi. A we śnie kotki rzucają się śnieżkami! '
                  'Strzałka w górę rzuca śnieżkę.',
    'sen_koniec': 'Śpij słodko Franek. Kotki rzucają śnieżkami całą noc.',
    'f_koniec3':  'Brawo Franek! Cały dzień za tobą. Zabawa, kolacja, kąpiel, '
                  'książka i sen o kotkach.',

    # --- Franek wybiera opiekuna: z tatą autem, z mamą Magdą taksówką ---
    'f_wybor_opiekuna': 'Z kim jedziesz dziś do przedszkola? Strzałka w lewo to mama Magda '
                        'i taksówka, w prawo tata i auto. Strzałka w górę zaczyna.',
    'fm_poziom8':  'Poziom ósmy. Idziemy do taksówki, mama już czeka.',
    'fm_poziom9':  'Poziom dziewiąty. Jedziemy taksówką do przedszkola!',
    'fm_poziom10': 'Poziom dziesiąty. Wyścig z mamą do furtki przedszkola!',
    'fm_poziom11': 'Poziom jedenasty. Szatnia! Rozbierz się i przytul mamę.',
    'fm_poziom12': 'Poziom dwunasty. Wyścig do okna. Zdąż pomachać mamie!',
    'fm_poziom15': 'Poziom piętnasty. Mama przyszła! Uciekaj, jeśli nie chcesz się myć!',
    'fm_poziom16': 'Poziom szesnasty. Wracamy autobusem do domu.',
    'fm_poziom17': 'Poziom siedemnasty. Kasujemy bilet w autobusie. Nie zgnieć go!',
    'fm_poziom19': 'Poziom dziewiętnasty. Jesteśmy w domu, tata czeka w drzwiach.',
    'fm_zad_przytulas':  'A teraz przytul mamę na do widzenia!',
    'fm_przytulas':      'Ale super przytulas! Do widzenia mamo, do zobaczenia!',
    'fm_pomachaj':       'Pomachaj mamie przez okno! Pa pa!',
    'fm_szybciej':       'Szybciej mama! Rura!',
    'fm_szybciej2':      'Mamo, jedź szybciej! Rura!',
    'fm_lapanie_jak':    'Mama pyta: idziemy się umyć? Uciekaj! Naciskaj strzałki na zmianę.',
    'fm_lapanie_uciekl': 'Uciekłeś mamie! Dzisiaj się nie myjemy!',
    'fm_dom_czysty':     'Fajnie, że już jesteście!',
    'fm_jazda_dom':      'Wracamy autobusem do domu. Franek nuci Kocią szajkę!',
    'fm_zad_samochod':   'Wsiadaj do taksówki!',
    'bilet_jak': 'Wsuwaj bilet w kasownik. Trzymaj strzałkę w górę i puść w zielonym polu, '
                 'żeby go nie zgnieść!',
    'bilet_ok':  'Bilet skasowany, równiutko! Brawo.',
    'bilet_zle': 'Ojej, bilet się gniecie! Puszczaj!',

    # --- kto kładzie Franka spać ---
    'ksiazka_kto': 'Kto ma cię dziś położyć spać? Strzałka w lewo to mama, w prawo tata. '
                   'Drugie dostanie przytulasa.',
    'ksiazka_czyta_mama': 'Mama poczyta ci do snu.',
    'ksiazka_czyta_tata': 'Tata poczyta ci do snu.',
    'ksiazka_przytulas_mama': 'Koniec książki. Przytul mamę na dobranoc!',
    'ksiazka_przytulas_tata': 'Koniec książki. Przytul tatę na dobranoc!',

    # --- cztery kapsułki rybno-truskawkowe po śniadanku ---
    'zad_kapsulki':   'Po śniadanku czas na kapsułki. Zjedz cztery, rybno-truskawkowe!',
    'kaps_2':         'Druga kapsułka!',
    'kaps_3':         'Trzecia kapsułka!',
    'kaps_4':         'Ostatnia, czwarta kapsułka!',
    'kapsulki_mniam': 'Cztery kapsułki zjedzone! Rybka i truskawka. Brawo Franek!',

    # --- minigra: liczymy jabłuszka (dodawanie, wszystko mówione) ---
    'licz_poziom': 'Etap bonusowy! W przedszkolu liczymy jabłuszka.',
    'licz_jak':    'Pod jabłuszkami są trzy liczby. Strzałki w lewo i w prawo je pokazują, '
                   'strzałka w górę wybiera. A strzałka w dół policzy razem z tobą.',
    'licz_ile':    'Ile to jest',
    'licz_plus':   'plus',
    'licz_razem':  'Liczymy razem!',
    'licz_brawo':  'Brawo! Razem to jest',
    'licz_nie':    'To nie tyle. Policzmy jeszcze raz.',
    'licz_koniec': 'Wszystko policzone! Ale z ciebie matematyk, Franek!',
    'licz_1':  'jeden',
    'licz_2':  'dwa',
    'licz_3':  'trzy',
    'licz_4':  'cztery',
    'licz_5':  'pięć',
    'licz_6':  'sześć',
    'licz_7':  'siedem',
    'licz_8':  'osiem',
    'licz_9':  'dziewięć',
    'licz_10': 'dziesięć',

    # --- minigra: gra w grze, czyli Franek gra w Poranek Franka ---
    'gierka_poziom': 'Etap bonusowy! Franek dostaje tablet i gra w Poranek Franka. '
                     'Gra w grze!',
    'gierka_jak':    'W gierce chodzi malutki Franek. Strzałki w lewo i w prawo go '
                     'prowadzą, strzałka w górę skacze. Zbierz trzy rzeczy.',
    'gierka_1':      'Malutkie śniadanko!',
    'gierka_2':      'Malutka szczoteczka!',
    'gierka_3':      'Malutkie buciki!',
    'gierka_koniec': 'Koniec grania! Franek odkłada tablet. Lecimy dalej!',

    # --- minigra: tory dla pociągu ---
    'rail_poziom': 'Etap bonusowy! Franek układa tory dla pociągu.',
    'rail_jak':    'Tory leżą krzywo. Strzałki w lewo i w prawo wybierają tor, a strzałka '
                   'w górę go obraca. Ułóż całą drogę z dworca na dworzec!',
    'rail_pasuje': 'Ten tor pasuje!',
    'rail_jedzie': 'Tory gotowe! Jedzie pociąg! Ciuch, ciuch!',
    'rail_koniec': 'Pociąg dojechał na stację. Brawo Franek!',

    # --- minigra: raz, dwa, trzy, Baba Jaga patrzy ---
    'baba_poziom':  'Etap bonusowy! Na placu zabaw gramy w Raz, dwa, trzy, Baba Jaga patrzy.',
    'baba_jak':     'Kiedy Baba Jaga stoi tyłem i śpiewa, biegnij! Naciskaj strzałki w lewo '
                    'i w prawo na zmianę. Jak się odwróci, stój jak posąg!',
    'baba_raz':     'Raz, dwa, trzy, Baba Jaga patrzy!',
    'baba_stoj':    'Stój! Ani drgnij!',
    'baba_lapie':   'Widziała cię! Wracasz kawałek do tyłu.',
    'baba_wygrana': 'Dobiegłeś do Baby Jagi! Wygrałeś! Brawo Franek!',

    # --- minigra: podłoga to lawa ---
    'lawa_poziom': 'Etap bonusowy! Podłoga to lawa!',
    'lawa_jak':    'Cała podłoga to gorąca lawa! Skacz po meblach strzałką w górę i dojdź '
                   'aż na kanapę. Nie dotykaj podłogi!',
    'lawa_ups':    'Ups, lawa! Wracasz na ostatni mebel.',
    'lawa_polowa': 'Połowa za tobą! Skacz dalej!',
    'lawa_koniec': 'Jesteś na kanapie! Lawa cię nie dostała. Brawo Franek!',

    # --- etap: karmimy dwa koty i królika ---
    'zwierzaki_poziom': 'Etap bonusowy! Koty i królik też chcą śniadanko.',
    'zad_karma_kot':    'Weź karmę dla kotów!',
    'zad_kot1':         'Nakarm pierwszego kotka!',
    'zad_kot2':         'Teraz drugi kotek! Siedzi na półce.',
    'zad_marchewka':    'Weź marchewkę dla królika!',
    'zad_krolik':       'Nakarm królika!',
    'zwierzaki_koniec': 'Koty mruczą, królik chrupie marchewkę. Wszyscy najedzeni! Brawo Franek!',

    # --- minigra: ubieranie na pogodę ---
    'pog_poziom':  'Etap bonusowy! Zobacz, jaka jest pogoda, i ubierz się dobrze.',
    'pog_jak':     'Popatrz przez okno, jaka jest pogoda. Strzałki w lewo i w prawo wybierają '
                   'ubranko, strzałka w górę je zakłada.',
    'pog_deszcz':  'Pada deszcz! Co zakładamy?',
    'pog_snieg':   'Pada śnieg i jest mróz! Co zakładamy?',
    'pog_slonce':  'Świeci słonko i jest ciepło! Co zakładamy?',
    'pog_kalosze': 'Kalosze i parasol.',
    'pog_czapka':  'Ciepła czapka i szalik.',
    'pog_okulary': 'Kaszkiet i okulary przeciwsłoneczne.',
    'pog_dobrze':  'Dokładnie tak! W tym będzie ci wygodnie. Brawo!',
    'pog_zle':     'W tym byłoby ci niewygodnie. Popatrz jeszcze raz przez okno.',
    'pog_koniec':  'Na każdą pogodę wiesz, co założyć! Brawo Franek!',

    # --- minigra: zawiązywanie butów ---
    'szn_poziom':   'Etap bonusowy! Uczymy się zawiązywać buty.',
    'szn_jak':      'Przewlekaj sznurówkę przez dziurki. Naciskaj strzałki w lewo i w prawo '
                    'na zmianę.',
    'szn_kokardka': 'Wszystkie dziurki gotowe! Teraz kokardka. Naciskaj strzałkę w górę '
                    'i zaciągaj.',
    'szn_koniec':   'Sam zawiązałeś buty! Ale jesteś duży. Brawo Franek!',

    # --- minigra: nakrywanie do stołu ---
    'stol_poziom':   'Etap bonusowy! Nakrywamy do stołu.',
    'stol_jak':      'Przy stole siedzą trzy osoby. Strzałki w lewo i w prawo wybierają '
                     'miejsce, a strzałka w górę kładzie.',
    'stol_talerze':  'Najpierw talerze. Każdy dostaje jeden.',
    'stol_kubki':    'Teraz kubki. Znowu po jednym dla każdego.',
    'stol_widelce':  'I jeszcze widelce. Ostatnia rzecz!',
    'stol_juz_jest': 'Tutaj już to leży. Wybierz inne miejsce.',
    'stol_koniec':   'Stół nakryty jak w restauracji! Można siadać do kolacji. Brawo!',

    # --- minigra: porządki w pokoju ---
    'porz_poziom':     'Etap bonusowy! Po zabawie trzeba posprzątać pokój.',
    'porz_jak':        'Klocki idą do pudełka, a misie na półkę. Chodź strzałkami w lewo '
                       'i w prawo, a strzałką w górę podnieś i odłóż.',
    'porz_klocek':     'Masz klocek. Nieś go do pudełka!',
    'porz_mis':        'Masz misia. Nieś go na półkę!',
    'porz_zle_klocek': 'Klocki idą do pudełka, nie na półkę.',
    'porz_zle_mis':    'Misie siadają na półce, nie w pudełku.',
    'porz_koniec':     'Wszystko na swoim miejscu! Ale porządek. Brawo Franek!',

    # --- minigra: kolory i kształty ---
    'ksz_poziom':      'Etap bonusowy! Bawimy się w kolory i kształty.',
    'ksz_jak':         'Strzałki w lewo i w prawo pokazują figury, a strzałka w górę wybiera.',
    'ksz_ktory_kolor': 'Który jest',
    'ksz_gdzie':       'Gdzie jest',
    'ksz_czerwony':    'czerwony',
    'ksz_niebieski':   'niebieski',
    'ksz_zielony':     'zielony',
    'ksz_zolty':       'żółty',
    'ksz_kolko':       'kółko',
    'ksz_kwadrat':     'kwadrat',
    'ksz_trojkat':     'trójkąt',
    'ksz_brawo':       'Dokładnie! To jest',
    'ksz_nie':         'To nie ten. Popatrz jeszcze raz.',
    'ksz_koniec':      'Wszystkie kolory i kształty zgadnięte! Brawo Franek!',

    # --- minigra: rytm i klaskanie ---
    'rytm_poziom':  'Etap bonusowy! Pani pokazuje rytm, a ty go powtarzasz.',
    'rytm_jak':     'Pani klaszcze rytm strzałkami. Popatrz, posłuchaj i powtórz go dokładnie '
                    'tak samo.',
    'rytm_sluchaj': 'Słuchaj i patrz!',
    'rytm_powtorz': 'Teraz ty! Powtórz rytm.',
    'rytm_dobrze':  'Idealnie, ten sam rytm! Brawo!',
    'rytm_zle':     'Ojej, to inny rytm. Popatrz jeszcze raz.',
    'rytm_koniec':  'Wszystkie rytmy powtórzone! Ale z ciebie muzyk!',

    # --- minigra: zupka na obiad ---
    'zupa_poziom':  'Etap bonusowy! Obiadek w przedszkolu. Dzisiaj zupka.',
    'zupa_jak':     'Zupka jest za gorąca! Trzymaj strzałkę w górę i dmuchaj, aż przestanie '
                    'parować.',
    'zupa_ostygla': 'Już dobra, nie parzy! Teraz jedz łyżka po łyżce. Naciskaj strzałki '
                    'w lewo i w prawo na zmianę.',
    'zupa_koniec':  'Pusty talerz! Cała zupka zjedzona. Brawo Franek!',

    # --- minigra: szukanie kurtki w szatni ---
    'szuk_poziom': 'Etap bonusowy! W szatni wisi mnóstwo kurtek. Która jest twoja?',
    'szuk_jak':    'Popatrz dobrze, to jest twoja kurtka. Zapamiętaj ją! Potem strzałki '
                   'w lewo i w prawo szukają, a strzałka w górę zdejmuje.',
    'szuk_patrz':  'Nowa kurtka do zapamiętania. Patrz uważnie!',
    'szuk_szukaj': 'A teraz znajdź ją na wieszaku!',
    'szuk_ok':     'To ta! Brawo, dobra pamięć!',
    'szuk_zle':    'To nie twoja kurtka. Szukaj dalej!',
    'szuk_koniec': 'Znalazłeś swoją kurtkę za każdym razem! Brawo Franek!',

    # --- minigra: bańki mydlane w kąpieli ---
    'banki_poziom': 'Etap bonusowy! W kąpieli lecą bańki mydlane.',
    'banki_jak':    'Łap bańki rączką! Strzałki w lewo i w prawo przesuwają rączkę, a bańka '
                    'pęka od samego dotknięcia.',
    'banki_koniec': 'Wszystkie bańki pyk! Ale zabawa. Brawo Franek!',


    # --- minigra: liczymy owieczki ---
    'owce_poziom': 'Etap bonusowy! Przed snem liczymy owieczki.',
    'owce_jak':    'Owieczka podchodzi do płotu i czeka. Naciśnij strzałkę w górę, żeby '
                   'przeskoczyła, a ja będę liczyć.',
    'owce_koniec': 'Dziesięć owieczek przeskoczyło płot. Franek zasypia. Dobranoc!',

    # --- minigra: kotki budują igloo ---
    'igloo_poziom':  'Etap bonusowy! We śnie kotki budują igloo ze śniegu.',
    'igloo_jak':     'Kotek macha łapką, kiedy czeka na śnieżkę. Naciśnij wtedy strzałkę '
                     'w górę i rzuć mu ją.',
    'igloo_czekaj':  'Poczekaj, aż kotek machnie łapką!',
    'igloo_rosnie':  'Igloo rośnie! Rzucaj dalej!',
    'igloo_koniec':  'Igloo gotowe! Kotki idą spać do środka. Dobranoc Franek!',

    # --- ekran ustawień: język i tryb ---
    'menu_jak':    'Poranek Franka! Strzałka w lewo albo w prawo zmienia język, strzałka '
                   'w dół zmienia tryb, a strzałka w górę zaczyna grę.',
    'menu_jezyk':  'Polski.',
    'menu_prosty': 'Tryb prosty. Krótsze etapy i nic się nie powtarza.',
    'menu_pelny':  'Tryb pełny. Wszystkie etapy i cały długi dzień.',

    # --- minigra: alfabet ---
    'alf_poziom':  'Literki! Na jaką literę zaczyna się słowo?',
    'alf_jak':     'Popatrz na obrazek i posłuchaj. Potem strzałki w lewo i w prawo pokazują '
                   'litery, a strzałka w górę wybiera.',
    'alf_pytanie': 'Na jaką literę się zaczyna?',
    'alf_brawo':   'Tak! Zaczyna się na',
    'alf_nie':     'To nie ta litera. Powiedz słowo powoli i posłuchaj początku.',
    'alf_koniec':  'Znasz literki! Brawo Franek!',
    'alf_kot':       'Kot.',
    'alf_rybka':     'Rybka.',
    'alf_czapka':    'Czapka.',
    'alf_mleko':     'Mleko.',
    'alf_buty':      'Buty.',
    'alf_lyzka':     'Łyżka.',
    'alf_krolik':    'Królik.',
    'alf_marchewka': 'Marchewka.',

    # --- minigra: pary obrazków ---
    'mem_poziom': 'Pary obrazków. Znajdź dwa takie same.',
    'mem_jak':    'Karty leżą obrazkiem do dołu. Strzałki w lewo i w prawo przesuwają rączkę, '
                  'a strzałka w górę odwraca kartę. Znajdź dwie takie same.',
    'mem_para':   'Para! Brawo!',
    'mem_nie':    'To nie para. Zapamiętaj, gdzie leżą, i spróbuj jeszcze raz.',
    'mem_koniec': 'Znalazłeś wszystkie pary! Ale pamięć!',

    # --- minigra: co będzie dalej ---
    'wzor_poziom':   'Wzory! Zgadnij, co będzie dalej.',
    'wzor_jak':      'Figury układają się we wzór, który się powtarza. Zgadnij, co będzie dalej. '
                     'Strzałki w lewo i w prawo wybierają, strzałka w górę zatwierdza.',
    'wzor_co_dalej': 'Co będzie dalej?',
    'wzor_brawo':    'Tak! Taki jest wzór. Brawo!',
    'wzor_nie':      'To nie to. Popatrz na wzór od początku.',
    'wzor_koniec':   'Wszystkie wzory zgadnięte! Ale z ciebie detektyw!',

    # --- minigra: co nie pasuje ---
    'nie_poziom': 'Które nie pasuje do reszty?',
    'nie_jak':    'Trzy obrazki są z jednej rodziny, a jeden nie. Strzałki w lewo i w prawo '
                  'wybierają, strzałka w górę zatwierdza.',
    'nie_ktore':  'Które nie pasuje?',
    'nie_brawo':  'Tak, to nie pasuje!',
    'nie_nie':    'To akurat pasuje. Popatrz jeszcze raz.',
    'nie_koniec': 'Wszystko posortowane! Ale z ciebie mądrala!',
    'nie_zwierzeta': 'Reszta to zwierzątka.',
    'nie_jedzenie':  'Reszta to jedzenie.',
    'nie_ubrania':   'Reszta to ubranka.',
    'nie_zabawki':   'Reszta to zabawki.',
    'nie_kuchnia':   'Reszta jest z kuchni.',

    # --- minigra: wyższa karta ---
    'karty_poziom': 'Która karta jest większa?',
    'karty_jak':    'Są dwie karty. Wybierz tę z większą liczbą. Strzałki w lewo i w prawo '
                    'wybierają, strzałka w górę zatwierdza.',
    'karty_ktora':  'Która karta jest większa?',
    'karty_brawo':  'Tak! Większa liczba to',
    'karty_nie':    'Nie, ta druga jest większa. Policz serduszka.',
    'karty_koniec': 'Znasz liczby! Zawsze wiesz, która jest większa!',

    # --- minigra: zgadywanie literek ze słuchu ---
    'zgad_poziom':  'Zgadujemy literki! Posłuchaj i znajdź tę, którą mówię.',
    'zgad_jak':     'Powiem literę, a ty ją znajdź. Strzałki w lewo i w prawo wybierają, '
                    'strzałka w górę zatwierdza, a strzałka w dół powtarza literę.',
    'zgad_szukamy': 'Szukamy litery',
    'zgad_brawo':   'Tak, to ta litera! Brawo!',
    'zgad_nie':     'To nie ta. Wybrałeś literę',
    'zgad_a_szukamy': 'A my szukamy litery',
    'zgad_koniec':  'Znasz wszystkie literki! Brawo!',

    # --- minigra: układanie słów z liter ---
    'pisz_poziom': 'Piszemy słowa! Ułóż słowo z literek.',
    'pisz_jak':    'Popatrz na obrazek i ułóż słowo. Strzałki w lewo i w prawo wybierają '
                   'literę, strzałka w górę ją dokłada, a strzałka w dół powtarza słowo.',
    'pisz_slowo':  'Ułóż słowo:',
    'pisz_brawo':  'Całe słowo gotowe! Brawo!',
    'pisz_nie':    'To nie ta litera. Posłuchaj słowa jeszcze raz.',
    'pisz_koniec': 'Wszystkie słowa napisane! Ale z ciebie pisarz!',
}

# --- nazwy liter: po polsku „be, ce, ka", po angielsku „bee, see, kay" ---
LITERY_PL = {'a':'a', 'b':'be', 'c':'ce', 'd':'de', 'e':'e', 'f':'ef', 'g':'gie', 'h':'ha',
             'i':'i', 'j':'jot', 'k':'ka', 'l':'el', 'm':'em', 'n':'en', 'o':'o', 'p':'pe',
             'r':'er', 's':'es', 't':'te', 'u':'u', 'w':'wu', 'y':'igrek', 'z':'zet', 'ł':'eł'}
LITERY_EN = {'a':'ay', 'b':'bee', 'c':'see', 'd':'dee', 'e':'ee', 'f':'eff', 'g':'jee',
             'h':'aitch', 'i':'eye', 'j':'jay', 'k':'kay', 'l':'ell', 'm':'em', 'n':'en',
             'o':'oh', 'p':'pee', 'r':'arr', 's':'ess', 't':'tee', 'u':'you', 'w':'double you',
             'y':'why', 'z':'zed', 'ł':'ell'}
for _l, _n in LITERY_PL.items():
    NARRACJA['lit_' + _l] = _n

EFEKTY = {
    'sfx_skok':   ('8-bit chiptune jump sound effect, retro NES video game, short rising square wave blip', 0.6),
    'sfx_zbierz': ('8-bit chiptune coin pickup sound, retro NES video game, two quick high square wave notes', 0.7),
    'sfx_sukces': ('8-bit chiptune level complete fanfare, retro NES video game, cheerful ascending arpeggio', 2.0),
    'sfx_zle':    ('8-bit chiptune error buzz, retro NES video game, short low descending blip', 0.6),
    'sfx_bum':    ('8-bit chiptune crash bump, retro NES video game, short noise thud', 0.7),
    'sfx_drzwi':  ('8-bit chiptune door opening chime, retro NES video game, short bright arpeggio', 1.0),
}

MUZYKA = {
    'muz_menu':   ('Cheerful 8-bit chiptune title theme for a children video game, NES style, square wave melody, '
                   'simple bassline, upbeat and friendly, seamless loop, no vocals', 22000),
    'muz_gra':    ('Happy bouncy 8-bit chiptune platformer level music, NES style like classic Mario, '
                   'square wave melody, walking bassline, playful, seamless loop, no vocals', 32000),
    'muz_jazda':  ('Fast energetic 8-bit chiptune driving music, NES style racing level, '
                   'driving bassline, exciting, seamless loop, no vocals', 24000),
    'muz_koniec': ('Triumphant 8-bit chiptune victory fanfare, NES style, celebratory, short, no vocals', 12000),
}

import re as _re
from narracja_en import NARRACJA_EN
for _l, _n in LITERY_EN.items():
    NARRACJA_EN['lit_' + _l] = _n

# --- wersje bez numeru poziomu (n_...) dla trybu uproszczonego ---
# W trybie prostym etapy są przetasowane, więc nagrane „Poziom siódmy" by kłamało.
BEZ_NUMERU = [
    (_re.compile(r'^Poziom [\w ]+?\.\s*'), ''),
    (_re.compile(r'^Ostatni poziom!\s*'), ''),
    (_re.compile(r'^Etap bonusowy!\s*'), ''),
]
def bezNumeru(tekst):
    nowy = tekst
    for wzor, czym in BEZ_NUMERU:
        nowy = wzor.sub(czym, nowy)
    return nowy if nowy != tekst and nowy else None

def main():
    wynik = {}
    print('=== NARRATOR PL (glos %s) ===' % GLOS, flush=True)
    for k, t in NARRACJA.items():
        wynik[k] = mowa(k + '.mp3', t)
        print('%-16s %s  "%s"' % (k, wynik[k], t), flush=True)

    print('=== NARRATOR PL bez numerów poziomów ===', flush=True)
    for k, t in NARRACJA.items():
        t2 = bezNumeru(t)
        if not t2:
            continue
        wynik['n_' + k] = mowa('n_' + k + '.mp3', t2)
        print('%-18s %s  "%s"' % ('n_' + k, wynik['n_' + k], t2), flush=True)

    print('=== NARRATOR EN ===', flush=True)
    os.makedirs(os.path.join(KAT, 'en'), exist_ok=True)
    brak = [k for k in NARRACJA if k not in NARRACJA_EN]
    if brak:
        print('BRAK TŁUMACZENIA: ' + ', '.join(sorted(brak)), flush=True)
    for k, t in NARRACJA_EN.items():
        wynik['en/' + k] = mowa(os.path.join('en', k + '.mp3'), t)
        print('%-18s %s  "%s"' % ('en/' + k, wynik['en/' + k], t), flush=True)
    print('=== EFEKTY ===', flush=True)
    for k, (opis, sek) in EFEKTY.items():
        wynik[k] = efekt(k + '.mp3', opis, sek)
        print('%-16s %s' % (k, wynik[k]), flush=True)
    print('=== MUZYKA ===', flush=True)
    for k, (opis, ms) in MUZYKA.items():
        wynik[k] = muzyka(k + '.mp3', opis, ms)
        print('%-16s %s' % (k, wynik[k]), flush=True)

    bledy = {k: v for k, v in wynik.items() if v and v.startswith('BŁĄD')}
    json.dump({'narracja': NARRACJA, 'wynik': wynik},
              open(os.path.join(KAT, 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
    print('\nGOTOWE. plików: %d, błędów: %d' % (len(wynik), len(bledy)), flush=True)
    if bledy:
        print('BŁĘDY:', json.dumps(bledy, ensure_ascii=False, indent=1), flush=True)

main()
