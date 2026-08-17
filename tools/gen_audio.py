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
    'poziom8':      'Ostatni poziom. Szatnia! Rozbierz się i pobiegnij do okna.',
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
}

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

def main():
    wynik = {}
    print('=== NARRATOR (glos %s) ===' % GLOS, flush=True)
    for k, t in NARRACJA.items():
        wynik[k] = mowa(k + '.mp3', t)
        print('%-16s %s  "%s"' % (k, wynik[k], t), flush=True)
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
