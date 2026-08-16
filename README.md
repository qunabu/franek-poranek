# Poranek Franka 🕷️

Ośmiobitowa gra 2D dla 5–6 latków. Franek wstaje, ubiera się, je śniadanko,
myje ząbki i jedzie z tatą do przedszkola. **Sterowanie: same strzałki.**

▶ **Zagraj: https://qunabu.github.io/franek-poranek/**

Franek nie umie jeszcze czytać, więc **wszystko czyta narrator** — każde zadanie
jest wypowiadane na głos po polsku.

## Sterowanie

| Klawisz | Co robi |
|---|---|
| ◀ ▶ | chodzenie (w aucie: wolniej / szybciej) |
| ▲ | skok (w aucie: pas wyżej), a także „zacznij / dalej" |
| ▼ | w aucie: pas niżej |

Na telefonie i tablecie pojawiają się przyciski dotykowe. Telefon trzymany
pionowo prosi o obrócenie na poziomo (dotknięcie ekranu włącza pełny ekran).
Na ekranach menu wystarczy dotknąć/kliknąć.

Przedmioty zbiera się samym dotknięciem. Świecąca rzecz ze strzałką to ta,
po którą trzeba iść teraz. **Nie da się przegrać** — po spadnięciu Franek
wraca w bezpieczne miejsce.

## Poziomy

1. **Wstawaj, Franek!** — majtki → spodnie → skarpetki → koszulka
2. **Śniadanko** — schody na dół, potem miska → łódeczki → mleko → łyżka → jedzenie
3. **Myjemy ząbki** — pasta → szczoteczka → minigra szorowania
4. **Wychodzimy!** — czapka → kurtka → buty
5. **Do samochodu!** — spacer z tatą
6. **Jedziemy do przedszkola** — omijanie przeszkód na ulicy

Franek **ubiera się na oczach gracza** — każda zebrana rzecz pojawia się na postaci.

## Jak to zrobione

- Wszystko renderowane na kanwie **480×270 px**, skalowanej bez wygładzania —
  stąd wygląd 8-bitowy. Własna czcionka bitmapowa 5×7 z polskimi znakami.
- Twarze Franka i taty to **prawdziwe zdjęcia przerobione na piksele**
  (macOS Vision wycina sylwetkę, potem redukcja do kilkunastu pikseli).
- Postacie mają 4-klatkowy cykl chodu i osobną klatkę skoku.
- **Narrator, efekty i muzyka wygenerowane przez ElevenLabs** (`audio/*.mp3`):
  35 kwestii narratora po polsku, 6 efektów chiptune i 4 utwory.
  Gdyby plików zabrakło, gra sama piszczy przez WebAudio.

## Uruchomienie lokalnie

Otwórz `index.html` w przeglądarce (dwuklik). Wymaga tylko plików z tego repo.

Chcesz podmienić głos narratora? W `tools/gen_audio.py` zmień `GLOS`
na inne ID głosu ElevenLabs i uruchom ponownie (potrzebny własny klucz w `.env`).

## Ustawienia do zmiany

Na górze `index.html`:

```js
const CZAS_MYCIA_ZEBOW = 35;        // ile SEKUND naprawdę trwa szczotkowanie
const DROGA_DO_PRZEDSZKOLA = 7000;  // długość trasy samochodem
```

Zegar mycia zębów zawsze pokazuje odliczanie od `2:00` (bo tyle trzeba myć zęby
naprawdę), ale realnie trwa tyle sekund, ile ustawisz. Domyślne 35 s — dla
5-latka pełne dwie minuty klikania bywają za długie. Ustaw `120`, jeśli chcesz
prawdziwe dwie minuty.
