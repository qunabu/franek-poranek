# Poranek Franka i Poli 🕷️

Ośmiobitowa gra 2D dla 5–6 latków. Na pierwszym ekranie wybierasz, kim grasz:
**Frankiem** (z tatą) albo **Polą** (z mamą). Każde ma własne etapy poranka.
**Sterowanie: same strzałki.**

▶ **Zagraj: https://qunabu.github.io/franek-poranek/**

Franek nie umie jeszcze czytać, więc **wszystko czyta narrator** — każde zadanie
jest wypowiadane na głos po polsku.

## Sterowanie

| Klawisz | Co robi |
|---|---|
| ◀ ▶ | chodzenie (w aucie: wolniej / szybciej) |
| ▲ | skok (w aucie: pas wyżej), a także „zacznij / dalej" |
| ▼ | w aucie: pas niżej (przycisk dotykowy pokazuje się tylko w aucie) |

Na telefonie i tablecie pojawiają się przyciski dotykowe. Telefon trzymany
pionowo prosi o obrócenie na poziomo. Na ekranie wyboru wystarczy **dotknąć
portretu** — to od razu wybiera postać, zaczyna grę i **włącza pełny ekran**.
Na pozostałych ekranach menu też wystarczy dotknąć/kliknąć.

Przedmioty zbiera się samym dotknięciem. Świecąca rzecz ze strzałką to ta,
po którą trzeba iść teraz. **Nie da się przegrać** — po spadnięciu Franek
wraca w bezpieczne miejsce.

## Poziomy Franka (9)

1. **Wstawaj, Franek!** — majtki → spodnie → skarpetki → koszulka
2. **Śniadanko** — schody na dół, potem miska → łódeczki → mleko → łyżka → jedzenie
3. **Myjemy ząbki** — pasta → szczoteczka → minigra szorowania
4. **Wychodzimy!** — czapka → kurtka → buty
5. **Do samochodu!** — spacer z tatą
6. **Jedziemy do przedszkola** — omijanie przeszkód na ulicy; w oknach auta
   widać Franka i tatę, a gdy tata wlecze się wolno, Franek go popędza
7. **Wyścig do furtki** — naciskaj ◀ ▶ na zmianę; Franek zawsze wygrywa z tatą
8. **Szatnia** — zdejmij buty, powieś kurtkę, zdejmij czapkę i **przytul tatę**
   na do widzenia (tata staje i czeka, na jego piersi świeci serduszko)
9. **Wyścig do okna** — korytarzem do okna, a tata idzie tą samą drogą za szybą;
   na mecie Franek macha mu przez okno „pa pa" (◀ ▶ na zmianę, jak przy furtce)

## Poziomy Poli (6)

1. **Wstawaj, Pola!** — kapcie → miś
2. **Łazienka** — pasta → szczoteczka → mycie ząbków → grzebień
3. **Rybka** — znajdź karmę i nakarm rybkę w akwarium
4. **Ubieramy się** — majtki → legginsy → skarpetki → bluza
5. **Śniadanko** — miska → płatki → mleko → łyżka
6. **Wychodzimy!** — czapka → kurtka → buty, mama czeka

Franek **ubiera się na oczach gracza** — każda zebrana rzecz pojawia się na postaci.

## Jak to zrobione

- Wszystko renderowane na kanwie **480×270 px**, skalowanej bez wygładzania —
  stąd wygląd 8-bitowy. Własna czcionka bitmapowa 5×7 z polskimi znakami.
- Twarze Franka, Poli, taty i mamy to **prawdziwe zdjęcia przerobione na piksele**
  (macOS Vision wycina sylwetkę, potem redukcja do kilkudziesięciu pikseli).
- Postacie mają 4-klatkowy cykl chodu i osobną klatkę skoku.
- **Narrator, efekty i muzyka wygenerowane przez ElevenLabs** (`audio/*.mp3`):
  82 kwestie narratora po polsku, 6 efektów chiptune i 4 utwory.
  Gdyby plików zabrakło, gra sama piszczy przez WebAudio.

## Instalacja na pulpicie (PWA)

Gra jest aplikacją PWA, więc da się ją **zainstalować jak zwykły program**
i uruchamiać na pełnym ekranie, bez paska adresu.

Najprościej: na ekranie wyboru postaci (a na telefonie trzymanym pionowo — pod
prośbą o obrót) jest przycisk **📲 ZAINSTALUJ GRĘ**. Na Androidzie i na
komputerze otwiera prawdziwe okienko instalacji, a na iPhonie tłumaczy krok po
kroku, gdzie kliknąć. Przycisk chowa się na czas gry, żeby nie zasłaniał planszy.

Ręcznie, gdyby ktoś wolał:

- **Komputer (Chrome / Edge):** ikona instalacji po prawej w pasku adresu
  (albo menu ⋮ → *Zainstaluj*). Gra dostaje własną ikonę i osobne okno.
- **Android (Chrome):** menu ⋮ → *Zainstaluj aplikację* / *Dodaj do ekranu głównego*.
- **iPhone / iPad (Safari):** przycisk *Udostępnij* → *Do ekranu początkowego*.
  Safari **nigdy** nie proponuje instalacji sam — na iPhonie zawsze robi się to ręcznie.

Po instalacji gra:

- startuje **na pełnym ekranie i w poziomie** (`display: fullscreen`,
  `orientation: landscape`),
- **zawsze pokazuje najnowszą wersję** — `sw.js` bierze `index.html` najpierw
  z sieci, a gdy w tle pojawi się nowa wersja, okno samo się przeładowuje,
- **działa bez internetu** — ikony, twarze i strona są zapisane od razu,
  a dźwięki dogrywają się do zapasu przy pierwszym graniu (potem gra chodzi
  offline; przy okazji każdy plik po cichu odświeża się na nowszy).

Ikony na pulpit robi `tools/gen_ikony.py` z pikselowego portretu Franka
(czysty Python, bez bibliotek).

## Uruchomienie lokalnie

Otwórz `index.html` w przeglądarce (dwuklik). Wymaga tylko plików z tego repo.
Service worker działa jednak dopiero po `http://`, więc żeby sprawdzić PWA,
odpal `python3 -m http.server` w katalogu gry.

Chcesz podmienić głos narratora? W `tools/gen_audio.py` zmień `GLOS`
na inne ID głosu ElevenLabs i uruchom ponownie (potrzebny własny klucz w `.env`).

## Ustawienia do zmiany

Na górze `index.html`:

```js
const CZAS_MYCIA_ZEBOW = 35;        // ile SEKUND naprawdę trwa szczotkowanie
const DROGA_DO_PRZEDSZKOLA = 7000;  // długość trasy samochodem
```

### Mycie ząbków

Minigra prowadzi przez **cztery strefy jak przy prawdziwym myciu**: górne
i dolne ząbki, najpierw z przodu, potem od środka. Na zębach widać **brud**,
który schodzi dopiero od **szorowania tam i z powrotem** — samo trzymanie
strzałki prawie nic nie daje, więc ruch w grze odpowiada ruchowi szczoteczką.
Strzałki ◀ ▶ szorują, ▲ ▼ przełączają strefę, a gdy strefa jest czysta,
gra sama przechodzi do następnej. Cztery kwadraciki u góry pokazują postęp
każdej strefy.

Narrator zapowiada, ile zostało („została jeszcze minuta mycia"),
a na finiszu odlicza **5, 4, 3, 2, 1** — cyfra pokazuje się też na ekranie.
Na koniec gra podaje, w ilu procentach ząbki zostały umyte.

Zegar mycia zębów zawsze pokazuje odliczanie od `2:00` (bo tyle trzeba myć zęby
naprawdę). Realnie leci szybciej, bo **ruch skraca czas**: trzymanie strzałki
przyspiesza zegar 2×, a szorowanie ◀ ▶ na zmianę 3×. Przy żwawym szorowaniu
mycie zajmuje około 14 sekund. Ustaw `CZAS_MYCIA_ZEBOW = 240`, jeśli chcesz
prawdziwe dwie minuty przy szorowaniu.
