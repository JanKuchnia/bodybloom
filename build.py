#!/usr/bin/env python3
"""Static page generator. Run: python3 build.py

Header, drawer, footer and head are taken from index.html (the shell), so edit those
there. Subpage content lives in PAGES below. Output is plain HTML: <slug>/index.html,
sitemap.xml, robots.txt, 404.html. No server code.
"""
import json, re, datetime, pathlib

ROOT = pathlib.Path(__file__).parent
SITE = "https://bodybloom.pl"  # shortcut: domain not confirmed, change here before launch
TEL, TELS = "+48533620733", "533 620 733"
TODAY = datetime.date.today().isoformat()

# ---------- helpers ----------
def esc(s): return s.replace("&", "&amp;")
def p(t): return f'<p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">{t}</p>'
def sec(h, inner, eyebrow=None):
    e = f'<span class="font-label-sm text-label-sm uppercase tracking-widest text-primary font-semibold">{eyebrow}</span>' if eyebrow else ""
    return (f'<section class="py-space-lg border-t border-surface-variant grid gap-space-sm lg:grid-cols-[minmax(0,1fr)_minmax(0,2.2fr)] lg:gap-space-lg">'
            f'<div class="flex flex-col gap-2 lg:sticky lg:top-28 lg:self-start">{e}<h2 class="font-headline-md text-headline-md text-on-surface tracking-tight">{h}</h2></div>'
            f'<div class="flex flex-col gap-space-sm min-w-0 max-w-3xl">{inner}</div></section>')
def ul(items):
    li = "".join(f'<li class="flex items-start gap-3 bg-surface-container-lowest rounded-2xl p-4 shadow-sm"><span class="w-7 h-7 rounded-full bg-primary-fixed text-on-primary-fixed flex items-center justify-center shrink-0"><i data-lucide="check" class="w-4 h-4"></i></span><span class="pt-0.5">{i}</span></li>' for i in items)
    return f'<ul class="grid grid-cols-1 sm:grid-cols-2 gap-space-xs font-body-md text-body-md text-on-surface-variant">{li}</ul>'
def cards(items, cols="md:grid-cols-3"):
    c = "".join(f'<div class="bg-surface-container-lowest rounded-2xl p-space-md shadow-sm flex flex-col gap-2"><div class="w-12 h-12 rounded-xl bg-primary-fixed text-on-primary-fixed flex items-center justify-center"><i data-lucide="{i}" class="w-6 h-6"></i></div><h3 class="font-headline-sm text-headline-sm font-semibold">{t}</h3><p class="font-body-sm text-body-sm text-on-surface-variant">{d}</p></div>' for i, t, d in items)
    return f'<div class="grid grid-cols-1 {cols} gap-gutter">{c}</div>'
def faq(items):
    d = "".join(f'<details class="bg-surface-container-lowest rounded-2xl shadow-sm group"><summary class="cursor-pointer list-none flex items-center justify-between gap-3 p-space-md font-headline-sm text-base font-semibold">{q}<i data-lucide="chevron-down" class="w-5 h-5 shrink-0 text-primary transition-transform duration-200 group-open:rotate-180"></i></summary><div class="px-space-md pb-space-md font-body-md text-body-md text-on-surface-variant">{a}</div></details>' for q, a in items)
    return f'<div class="flex flex-col gap-space-xs">{d}</div>'
def table(head, rows, note=None):
    th = "".join(f'<th class="text-left py-2 pr-4 font-label-md uppercase tracking-wider">{h}</th>' for h in head)
    tr = "".join("<tr class=\"border-t border-surface-variant\">" + "".join(f'<td class="py-3 pr-4 align-top">{c}</td>' for c in r) + "</tr>" for r in rows)
    n = f'<p class="font-body-sm text-body-sm text-on-surface-variant mt-2">{note}</p>' if note else ""
    return f'<div class="overflow-x-auto bg-surface-container-lowest rounded-2xl p-space-md shadow-sm"><table class="w-full font-body-md text-body-md"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>{n}</div>'
HOURS = [("Poniedziałek", "07:00 – 20:00"), ("Wtorek", "07:30 – 20:00"), ("Środa", "07:30 – 20:00"),
         ("Czwartek", "07:30 – 20:00"), ("Piątek", "07:30 – 19:00"), ("Sobota", "08:00 – 11:00"), ("Niedziela", "Zamknięte")]
def btn(href, icon, label, ghost=False, ext=False):
    cls = "bg-primary-fixed text-primary-container hover:bg-primary-fixed-dim" if ghost else "bg-primary text-on-primary hover:bg-primary-container"
    x = ' rel="noopener noreferrer" target="_blank"' if ext else ""
    return f'<a class="inline-flex items-center justify-center gap-2 {cls} font-label-lg text-label-lg px-7 py-3.5 rounded-full transition-colors" href="{href}"{x}><i data-lucide="{icon}" class="w-5 h-5 shrink-0"></i>{label}</a>'
MAPS = "https://maps.google.com/?q=ul.+Ignacego+Daszy%C5%84skiego+9,+My%C5%9Blenice"
def cta(text="Zadzwoń, a dobierzemy termin i formę zajęć."):
    return (f'<section class="py-space-lg"><div class="bg-primary-container text-on-primary-container rounded-3xl p-space-lg flex flex-col md:flex-row md:items-center justify-between gap-space-md">'
            f'<p class="font-headline-sm text-headline-sm font-semibold max-w-xl">{text}</p>'
            f'<div class="flex flex-wrap gap-space-sm">{btn("tel:" + TEL, "phone", "Zadzwoń: " + TELS).replace("bg-primary text-on-primary hover:bg-primary-container", "bg-surface text-on-surface hover:bg-surface-bright")}{btn(MAPS, "navigation", "Dojazd", True, True)}</div></div></section>')
def related(*links):
    a = "".join(f'<a class="group flex items-center justify-between gap-3 bg-surface-container-lowest rounded-2xl p-space-md shadow-sm hover:shadow-md transition-shadow font-headline-sm text-base font-semibold text-on-surface" href="{u}">{t}<i data-lucide="arrow-right" class="w-5 h-5 text-primary shrink-0 transition-transform group-hover:translate-x-1"></i></a>' for u, t in links)
    return f'<section class="py-space-md"><h2 class="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant mb-space-xs">Zobacz też</h2><div class="grid grid-cols-1 sm:grid-cols-3 gap-gutter">{a}</div></section>'
DISCLAIMER = p("<em>Informacje na tej stronie mają charakter ogólny i nie zastępują porady lekarza.</em>")

# ---------- pages ----------
# slug: (title<=60, description 120-155, h1, lead, body, service_schema_name|None, breadcrumb label)
PAGES = {}
def page(slug, title, desc, h1, lead, body, svc=None, crumb=None, noindex=False, pic=None):
    PAGES[slug] = dict(title=title, desc=desc, h1=h1, lead=lead, body=body, svc=svc, crumb=crumb or h1, noindex=noindex, pic=pic)

page("treningi-personalne", "Trening personalny w Myślenicach | BODY BLOOM",
     "Trening personalny w Myślenicach: indywidualny plan, bezpieczny powrót po kontuzji i wsparcie trenerki. Umów się: 533 620 733.",
     "Trening personalny w Myślenicach", "Indywidualny plan, uwaga trenerki tylko dla Ciebie i tempo dopasowane do Twoich możliwości. Bez presji i bez oceniania.",
     sec("Dla kogo", ul(["osoby zaczynające od zera, które nie wiedzą, jak się za to zabrać", "osoby wracające do ruchu po przerwie lub kontuzji", "osoby z konkretnym celem: siła, sylwetka, kondycja, ruchomość", "wszyscy, którzy wolą pracować 1 na 1 niż w grupie"])) +
     sec("Jak to wygląda", ul(["rozmowa o celu, zdrowiu i dotychczasowej aktywności", "plan treningowy dopasowany do Ciebie i do sprzętu w studiu", "regularne sesje z korektą techniki i omówieniem postępów", "w razie potrzeby współpraca z fizjoterapeutką z naszego studia"]) ) +
     sec("Pierwszy trening", p("Pierwsze spotkanie służy poznaniu. Opowiadasz o celach i ewentualnych dolegliwościach, wspólnie robicie spokojną próbę ruchu, a na koniec ustalacie, jak mogą wyglądać kolejne sesje. Nie musisz się wcześniej przygotowywać. Wystarczą wygodny strój i obuwie sportowe.")) +
     sec("Cena", p('Aktualne ceny sesji i pakietów znajdziesz w <a class="text-primary font-semibold hover:underline" href="/cennik/">cenniku</a>.')) +
     sec("Najczęstsze pytania", faq([("Czy muszę mieć kondycję?", "Nie. Plan zaczynamy od Twojego poziomu, nie od cudzego."), ("Czy mogę ćwiczyć po kontuzji?", "Tak, po rozmowie o tym, co się wydarzyło. Jeśli to potrzebne, zalecimy wcześniej konsultację u lekarza lub fizjoterapeuty."), ("Czy mogę zapłacić kartą MultiSport?", 'Zasady dotyczące MultiSport opisaliśmy <a class="text-primary font-semibold hover:underline" href="/multisport/">tutaj</a>.')])) +
     cta("Umów pierwszy trening personalny.") + related(("/fizjoterapia/", "Fizjoterapia po kontuzji"), ("/treningi-grupowe/", "Treningi grupowe"), ("/cennik/", "Cennik")),
     svc="Trening personalny")

page("treningi-grupowe", "Treningi grupowe w Myślenicach | Zumba | BODY BLOOM",
     "Kameralne treningi grupowe w Myślenicach: zajęcia wzmacniające, mobility i zumba dla każdego poziomu. Sprawdź grafik i zapisz się.",
     "Treningi grupowe w Myślenicach", "Małe grupy, życzliwa atmosfera i zajęcia dla każdego poziomu. Przychodzisz we własnym tempie.",
     sec("Rodzaje zajęć", cards([("dumbbell", "Wzmacnianie", "Ćwiczenia siłowe i funkcjonalne, które budują siłę i dbają o stawy."), ("activity", "Mobility", "Ruchomość, rozciąganie i praca nad kręgosłupem."), ("music", "Zumba", "Energetyczny taniec i dobra zabawa, bez wcześniejszego przygotowania.")])) +
     sec("Mała grupa, brak presji", p("Zajęcia prowadzimy w kameralnych grupach, dzięki czemu trenerka widzi, jak ćwiczysz, i może podpowiedzieć modyfikację. Nikt nie porównuje się z innymi, a osoby początkujące czują się u nas swobodnie.")) +
     sec("Grafik i zapisy", p('Aktualne godziny zajęć znajdziesz w <a class="text-primary font-semibold hover:underline" href="/grafik/">grafiku</a>. Na zajęcia zapisujesz się telefonicznie: <a class="text-primary font-semibold hover:underline" href="tel:' + TEL + '">' + TELS + '</a>.') + p('Karty MultiSport: <a class="text-primary font-semibold hover:underline" href="/multisport/">zobacz zasady</a>.')) +
     sec("Najczęstsze pytania", faq([("Czy to dla początkujących?", "Tak. Zajęcia są otwarte dla każdego poziomu, a ćwiczenia można zmodyfikować."), ("Co zabrać?", "Wygodny strój, obuwie sportowe i wodę."), ("Czy trzeba się zapisać?", "Grupy są małe, więc zapisz się wcześniej telefonicznie.")])) +
     cta("Zapisz się na zajęcia grupowe.") + related(("/grafik/", "Grafik zajęć"), ("/treningi-personalne/", "Trening personalny"), ("/multisport/", "MultiSport")),
     svc="Treningi grupowe")

page("fizjoterapia", "Fizjoterapia w Myślenicach | BODY BLOOM",
     "Fizjoterapia w Myślenicach: diagnostyka, terapia manualna i praca z bólem kręgosłupa oraz stawów. Umów wizytę: 533 620 733.",
     "Fizjoterapia w Myślenicach", "Diagnostyka, terapia manualna i spokojna rozmowa o tym, co dolega. Trening i regeneracja w jednym miejscu.",
     sec("W czym pomagamy", ul(["dolegliwości bólowe kręgosłupa i stawów", "napięcia mięśniowe i ograniczona ruchomość", "powrót do aktywności po kontuzji", "zalecenia ruchowe do wykonywania w domu"]) ) +
     sec("Jak przebiega wizyta", ul(["wywiad: opowiadasz o dolegliwościach i trybie życia", "badanie i ocena ruchu", "terapia dobrana do tego, co wykazało badanie", "wskazówki i ćwiczenia na kolejne dni"])) +
     sec("Fizjoterapia i trening razem", p('Dzięki temu, że w jednym studiu działają fizjoterapeutki i trenerki, powrót do formy może być spójny: terapia łagodzi problem, a <a class="text-primary font-semibold hover:underline" href="/treningi-personalne/">trening personalny</a> pomaga utrwalić efekt.')) +
     sec("Umawianie i cena", p('Wizyty ustalamy telefonicznie. Ceny: <a class="text-primary font-semibold hover:underline" href="/cennik/">cennik</a>.')) +
     sec("Najczęstsze pytania", faq([("Czy potrzebuję skierowania?", "Zadzwoń i zapytaj, powiemy, jak wygląda umawianie wizyty."), ("Co zabrać na wizytę?", "Wygodny strój. Jeśli masz wyniki badań, zdjęcia lub opis diagnozy, zabierz je ze sobą.")])) + DISCLAIMER +
     cta("Umów wizytę u fizjoterapeutki.") + related(("/masaz/", "Masaż"), ("/treningi-personalne/", "Trening personalny"), ("/cennik/", "Cennik")),
     svc="Fizjoterapia")

page("masaz", "Masaż w Myślenicach | leczniczy, relaksacyjny | BODY BLOOM",
     "Masaż w Myślenicach: leczniczy, relaksacyjny i drenaż w spokojnej atmosferze studia BODY BLOOM. Umów termin: 533 620 733.",
     "Masaż w Myślenicach", "Masaż leczniczy, relaksacyjny oraz drenaż, w ciszy i spokoju. Dla regeneracji ciała i głowy.",
     sec("Rodzaje masażu", cards([("heart-pulse", "Masaż leczniczy", "Praca z napięciami i bolesnymi miejscami, często w połączeniu z fizjoterapią."), ("flower-2", "Masaż relaksacyjny", "Spokojne tempo, które pomaga się wyciszyć i odpocząć."), ("droplets", "Drenaż", "Delikatna technika wspierająca uczucie lekkości.")])) +
     sec("Dla kogo", p("Dla osób, które dużo siedzą, ciężko pracują, trenują albo po prostu chcą się zregenerować. Jeśli masz wątpliwości, który masaż wybrać, doradzimy przy umawianiu terminu.")) +
     sec("Zanim przyjdziesz", p("Powiedz nam o przeciwwskazaniach, takich jak ciąża, stan zapalny, świeże urazy, choroby skóry czy zakrzepy. W razie wątpliwości skonsultuj się z lekarzem.")) +
     sec("Prezent", p('Masaż to dobry pomysł na prezent. <a class="text-primary font-semibold hover:underline" href="/bon-podarunkowy/">Zobacz bon podarunkowy</a>.')) +
     sec("Najczęstsze pytania", faq([("Ile trwa masaż?", "Czas zależy od rodzaju masażu. Podamy go przy umawianiu terminu."), ("Czy masaż boli?", "Masaż leczniczy bywa intensywny, ale zawsze możesz powiedzieć, żeby zmniejszyć nacisk.")])) + DISCLAIMER +
     cta("Umów masaż.") + related(("/fizjoterapia/", "Fizjoterapia"), ("/bon-podarunkowy/", "Bon podarunkowy"), ("/cennik/", "Cennik")),
     svc="Masaż")

# Source: Instagram post 2026-01-08 "grafik oraz cenniki obowiązujące od 2026", transcribed in docs/grafik-cennik-2026.md
# TODO(client): confirm the timetable is still current (no Zumba in it) and the Thursday 20:00 class vs 20:00 closing
WB, KH, KZ, ZB, MP, TZ = "Weronika Baran", "Karolina Hudaszek", "Karolina Ziemianin", "Zuza Bukowska", "Magda Płachta", "trener zmienny"
GRAFIK = [
    ("Poniedziałek", [("7:00", "Pilates", WB), ("8:00", "Trening funkcjonalny", WB), ("9:00", "Trening obwodowy", WB), ("11:30", "Pilates", KH),
                      ("17:00", "Trening funkcjonalny", KZ), ("18:00", "Chusty", KH), ("18:00", "Pilates", KZ), ("19:00", "Trening obwodowy", KZ)]),
    ("Wtorek", [("7:30", "Pilates", ZB), ("8:30", "Trening funkcjonalny", WB), ("9:30", "TRX", WB), ("17:00", "Obwodowy siłowy", KZ),
                ("17:00", "Zdrowy kręgosłup", MP), ("18:00", "Pilates", KZ), ("18:00", "Trening funkcjonalny", MP), ("19:00", "Trening obwodowy", MP)]),
    ("Środa", [("7:30", "Zdrowy kręgosłup", ZB), ("8:30", "Trening funkcjonalny", ZB), ("9:30", "Sztangi", ZB), ("12:00", "Pilates", KH),
               ("17:00", "Sztangi", ZB), ("18:00", "Trening siłowy", ZB), ("19:00", "Chusty", KH), ("19:00", "Pilates", ZB)]),
    ("Czwartek", [("7:45", "Trening funkcjonalny", WB), ("9:00", "Pilates", WB), ("17:00", "Zdrowy kręgosłup", MP), ("18:00", "Trening obwodowy", MP),
                  ("19:00", "Pilates", MP), ("19:00", "Trening obwodowy", KZ), ("20:00", "Trening funkcjonalny", KZ)]),
    ("Piątek", [("7:30", "Zdrowy kręgosłup", ZB), ("8:30", "Pilates", WB), ("9:30", "Pilates", WB), ("9:30", "Sztangi", ZB),
                ("10:30", "Trening funkcjonalny", WB), ("17:00", "Trening funkcjonalny", WB), ("18:00", "Pilates", WB)]),
    ("Sobota", [("8:00", "Trening funkcjonalny", TZ), ("9:00", "Pilates", TZ), ("10:00", "Obwodowy siłowy", TZ)]),
]
def day_card(day, rows):
    li = "".join(f'<li class="flex gap-3 py-2.5 border-t border-surface-variant first:border-0"><span class="font-headline-sm text-base font-bold text-primary w-12 shrink-0 tabular-nums">{t}</span><span class="flex flex-col"><span class="font-semibold text-on-surface">{n}</span><span class="font-body-sm text-body-sm text-on-surface-variant">{who}</span></span></li>' for t, n, who in rows)
    return f'<div class="bg-surface-container-lowest rounded-2xl p-space-md shadow-sm"><h3 class="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant mb-1">{day}</h3><ul class="font-body-md text-body-md">{li}</ul></div>'
GRAFIK_NOTE = 'Grafik obowiązuje od stycznia 2026 i może się zmienić. Przed pierwszą wizytą zadzwoń: <a class="text-primary font-semibold hover:underline" href="tel:' + TEL + '">' + TELS + '</a>.'

def price_cards(items):
    c = "".join(f'<div class="bg-surface-container-lowest rounded-2xl p-space-md shadow-sm flex flex-col gap-1"><span class="font-body-md text-body-md text-on-surface-variant">{n}</span><span class="font-headline-md text-headline-md font-bold text-on-surface tabular-nums">{v}</span></div>' for n, v in items)
    return f'<div class="grid grid-cols-2 lg:grid-cols-4 gap-gutter">{c}</div>'
page("cennik", "Cennik | BODY BLOOM Myślenice",
     "Cennik BODY BLOOM w Myślenicach: treningi grupowe od 50 zł, karnety, treningi personalne, fizjoterapia i masaże. Tel. 533 620 733.",
     "Cennik", "Ceny obowiązują od stycznia 2026. Pierwszy trening próbny jest bezpłatny.",
     sec("Treningi grupowe", price_cards([("Wejście jednorazowe", "50 zł"), ("Karnet 4 wejść", "180 zł"), ("Karnet 8 wejść", "320 zł"), ("Karnet OPEN", "420 zł")]) +
         p('Godziny zajęć: <a class="text-primary font-semibold hover:underline" href="/grafik/">grafik</a>. Karty MultiSport: <a class="text-primary font-semibold hover:underline" href="/multisport/">zasady</a>.')) +
     sec("Treningi personalne", price_cards([("Karnet 4 wejść", "600 zł"), ("Karnet 8 wejść", "1080 zł"), ("Karnet 12 wejść", "1440 zł")]) +
         p("Pierwszy trening próbny jest bezpłatny. Każdy karnet jest ważny 5 tygodni.")) +
     sec("Fizjoterapia i masaże", table(["Zabieg", "Czas", "1 zabieg", "Pakiet 5", "Pakiet 10"], [
         ["Fizjoterapia", "50 min", "180 zł", "160 zł", "140 zł"],
         ["Masaż relaksacyjny", "50 / 90 min", "200 / 240 zł", "180 / 220 zł", "170 / 210 zł"],
         ["Masaż leczniczy", "50 / 120 min", "180 / 300 zł", "160 / 280 zł", "150 / 270 zł"],
         ["Masaż gorącymi kamieniami", "50 min", "180 zł", "170 zł", "160 zł"],
         ["Masaż Hot Stone", "90 min", "260 zł", "250 zł", "240 zł"],
         ["Tajski rytuał stóp", "90 min", "200 zł", "190 zł", "180 zł"],
         ["Kobido", "50 / 120 min", "200 / 300 zł", "180 / 280 zł", "170 / 270 zł"],
         ["Autorski masaż DEFKA", "50 min", "200 zł", "190 zł", "180 zł"],
         ["Facemodeling", "120 min", "350 zł", "340 zł", "330 zł"],
         ["Masaż antycellulitowy", "50 min", "220 zł", "210 zł", "200 zł"],
         ["Masaż Touch Balance", "50 min", "250 zł", "240 zł", "230 zł"],
         ["Masaż Access Bars", "50 min", "250 zł", "240 zł", "230 zł"],
         ["Masaż Access Face Lift", "50 min", "250 zł", "240 zł", "230 zł"]],
         "Ceny w pakietach podano za jeden zabieg. Na masaż umówisz się telefonicznie: " + f'<a class="text-primary font-semibold hover:underline" href="tel:{TEL}">{TELS}</a>' + " lub w wiadomości na Instagramie.")) +
     sec("Bony podarunkowe", p('Szczegóły: <a class="text-primary font-semibold hover:underline" href="/bon-podarunkowy/">bon podarunkowy</a>.')) +
     cta("Zapytaj o wolny termin."), crumb="Cennik")

page("grafik", "Grafik zajęć | BODY BLOOM Myślenice",
     "Grafik zajęć grupowych BODY BLOOM w Myślenicach: pilates, trening funkcjonalny, obwodowy, zdrowy kręgosłup, TRX. Zapisy: 533 620 733.",
     "Grafik zajęć", "Zajęcia grupowe od poniedziałku do soboty. Zapisy telefoniczne, pierwszy trening próbny bezpłatny.",
     '<section class="py-space-lg flex flex-col gap-space-sm"><div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-gutter items-start">' + "".join(day_card(d, r) for d, r in GRAFIK) + '</div>' + p(GRAFIK_NOTE) + '</section>' +
     sec("Zapisy", p('Liczba miejsc jest ograniczona. Więcej o zajęciach: <a class="text-primary font-semibold hover:underline" href="/treningi-grupowe/">treningi grupowe</a>. Ceny karnetów: <a class="text-primary font-semibold hover:underline" href="/cennik/">cennik</a>. Zasady MultiSport: <a class="text-primary font-semibold hover:underline" href="/multisport/">tutaj</a>.')) +
     cta("Zapisz się na zajęcia."))

page("multisport", "MultiSport w Myślenicach | BODY BLOOM",
     "MultiSport w Myślenicach: honorujemy karty na wybrane zajęcia grupowe w BODY BLOOM. Sprawdź zasady i zapisz się.",
     "MultiSport w Myślenicach", "Honorujemy karty MultiSport na wybrane zajęcia grupowe.",
     sec("Jak to działa", ul(["karta obowiązuje na wybrane zajęcia grupowe, nie na wszystkie usługi", "grupy są małe, więc miejsce rezerwujesz wcześniej telefonicznie", "szczegóły i limity sprawdzisz dzwoniąc: " + TELS])) +
     sec("Zapisy", p('Wybierz zajęcia w <a class="text-primary font-semibold hover:underline" href="/grafik/">grafiku</a> i zadzwoń.')) + cta("Zapytaj o MultiSport."))

page("bon-podarunkowy", "Bon podarunkowy | BODY BLOOM Myślenice",
     "Bon podarunkowy BODY BLOOM w Myślenicach: masaż, konsultacja fizjoterapeutyczna lub pakiet treningów. Zamów: 533 620 733.",
     "Bon podarunkowy", "Podaruj chwilę wytchnienia: masaż, konsultację fizjoterapeutyczną lub pakiet treningów.",
     sec("Co możesz podarować", ul(["masaż relaksacyjny lub leczniczy", "konsultację fizjoterapeutyczną", "pakiet treningów"])) +
     sec("Jak zamówić", p("Zadzwoń lub napisz do nas na Instagramie. Ustalimy wartość lub usługę i formę vouchera. Warunki ważności podamy przy zamówieniu.")) +
     cta("Zamów bon podarunkowy.") + related(("/masaz/", "Masaż"), ("/cennik/", "Cennik")))

# ---------- wydarzenia: blog-style index + one page per event ----------
# TODO(client): add real dates, times and prices per event; use Event schema only for upcoming dated events
TONES = {"secondary": ("bg-secondary-container text-on-secondary-container", "text-secondary"),
         "tertiary": ("bg-tertiary-fixed text-on-tertiary-fixed", "text-tertiary"),
         "primary": ("bg-primary-fixed text-on-primary-fixed", "text-primary")}
EVENTS = [
    dict(slug="krag-kobiet", title="Krąg Kobiet: Spokojny Oddech i Relaks", tag="Warsztaty", meta="Kameralna grupa", icon="heart-handshake", tone="secondary",
         excerpt="Spotkanie regenerujące układ nerwowy poprzez techniki somatyczne, automasaż i uważność.",
         body=sec("Co nas czeka", p("Spokojne spotkanie w kameralnym gronie. Pracujemy z oddechem, poznajemy proste techniki somatyczne i automasażu, które pomagają rozluźnić napięcie i wyciszyć głowę. Bez pośpiechu i bez oceniania.")) +
              sec("Dla kogo", ul(["dla kobiet, które chcą na chwilę zwolnić", "nie potrzebujesz żadnego doświadczenia", "ćwiczenia są łagodne i dopasowane do Twoich możliwości"])) +
              sec("Co zabrać", ul(["wygodny strój", "ciepłe skarpetki", "butelkę wody"]))),
    dict(slug="wieczor-relaksacyjny", title="Wieczór Andrzejkowy / Relaksacyjny", tag="Spotkanie", meta="Limit 8 miejsc", icon="moon", tone="tertiary",
         excerpt="Aromaterapeutyczna sesja rozciągania przy świecach z ziołowym naparem i relaksacją dźwiękiem.",
         body=sec("Co nas czeka", p("Wieczór przy świecach: spokojne rozciąganie, ziołowy napar i relaksacja dźwiękiem na zakończenie. To dobry sposób, żeby odpocząć po dniu i spędzić czas w miłej atmosferze.")) +
              sec("Dla kogo", ul(["dla każdego, kto potrzebuje odpoczynku", "rozciąganie jest łagodne, bez wymagań kondycyjnych", "liczba miejsc jest ograniczona do 8 osób"])) +
              sec("Co zabrać", ul(["wygodny strój", "ciepłe skarpetki lub sweter"]))),
    dict(slug="zumba-i-wzmacnianie", title="Nowy cykl Zumba &amp; Wzmacnianie", tag="Nowa grupa", meta="Start od poniedziałku", icon="dumbbell", tone="primary",
         excerpt="Energetyczne, bezstresowe zajęcia ruchowe dla każdego, bez konieczności wcześniejszego przygotowania.",
         body=sec("Co nas czeka", p("Nowa grupa, w której łączymy taniec z ćwiczeniami wzmacniającymi. Dużo energii, dobra muzyka i ruch, który daje radość, a przy okazji buduje siłę i kondycję.")) +
              sec("Dla kogo", ul(["dla osób początkujących i średniozaawansowanych", "nie musisz umieć tańczyć", "tempo i intensywność dopasujesz do siebie"])) +
              sec("Co zabrać", ul(["wygodny strój i obuwie sportowe", "butelkę wody", "ręcznik"])) +
              sec("MultiSport", p('Zasady korzystania z karty: <a class="text-primary font-semibold hover:underline" href="/multisport/">MultiSport</a>.'))),
]
def tile(e, cls=""):
    bg, _ = TONES[e["tone"]]
    return f'<div class="{bg} {cls} flex items-center justify-center"><i data-lucide="{e["icon"]}" class="w-1/4 h-1/4 max-w-24 max-h-24" aria-hidden="true"></i></div>'
def post_card(e):
    _, fg = TONES[e["tone"]]
    return (f'<a href="/wydarzenia/{e["slug"]}/" class="group flex flex-col bg-surface-container-lowest rounded-3xl overflow-hidden shadow-sm hover:shadow-md transition-shadow">'
            f'{tile(e, "aspect-[16/9] transition-transform duration-300 group-hover:scale-[1.02]")}'
            f'<div class="flex flex-col gap-2 p-space-md flex-1"><div class="flex items-center justify-between gap-2 font-label-sm text-label-sm"><span class="font-semibold uppercase tracking-wider {fg}">{e["tag"]}</span><span class="text-on-surface-variant">{e["meta"]}</span></div>'
            f'<h2 class="font-headline-sm text-headline-sm font-semibold text-on-surface">{e["title"]}</h2>'
            f'<p class="font-body-sm text-body-sm text-on-surface-variant flex-1">{e["excerpt"]}</p>'
            f'<span class="inline-flex items-center gap-1 pt-2 text-primary font-label-md font-semibold">Czytaj więcej<i data-lucide="arrow-right" class="w-4 h-4 transition-transform group-hover:translate-x-1"></i></span></div></a>')

page("wydarzenia", "Wydarzenia w studiu | BODY BLOOM Myślenice",
     "Wydarzenia w BODY BLOOM w Myślenicach: Krąg Kobiet, wieczory relaksacyjne i nowe grupy zajęć. Sprawdź, co się dzieje.",
     "Wydarzenia w studiu", "Warsztaty, spotkania i nowe grupy. Szczegóły i zapisy telefonicznie.",
     '<section class="py-space-lg"><div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-gutter">' + "".join(post_card(e) for e in EVENTS) + '</div></section>' +
     sec("Aktualności", p('Najnowsze informacje publikujemy na <a class="text-primary font-semibold hover:underline" href="https://www.instagram.com/bodybloom_studio_treningowe/" rel="noopener" target="_blank">Instagramie</a> i <a class="text-primary font-semibold hover:underline" href="https://www.facebook.com/p/BodyBloom-61577916802764/" rel="noopener" target="_blank">Facebooku</a>.')) +
     cta("Zapytaj o wolne miejsca."))

for e in EVENTS:
    others = [o for o in EVENTS if o is not e]
    page("wydarzenia/" + e["slug"], f'{e["title"]} | BODY BLOOM Myślenice'.replace("&amp;", "&"),
         f'{e["excerpt"]} Wydarzenie w studiu BODY BLOOM w Myślenicach. Zapisy: {TELS}.',
         e["title"], e["excerpt"],
         e["body"] + sec("Termin i zapisy", p('Termin, godzinę i cenę podamy przy zapisie. Liczba miejsc jest ograniczona, więc zadzwoń wcześniej: <a class="text-primary font-semibold hover:underline" href="tel:' + TEL + '">' + TELS + '</a>.')) +
         cta("Zarezerwuj miejsce.") +
         '<section class="py-space-md"><h2 class="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant mb-space-xs">Inne wydarzenia</h2><div class="grid grid-cols-1 md:grid-cols-2 gap-gutter">' + "".join(post_card(o) for o in others) + '</div></section>',
         pic=tile(e, "hidden md:flex rounded-2xl aspect-[4/3]"), crumb=e["title"])

page("o-nas", "O nas | BODY BLOOM Myślenice",
     "BODY BLOOM to kameralne studio w Myślenicach: treningi, fizjoterapia i masaż w jednym miejscu, bez presji i bez oceniania.",
     "O studiu BODY BLOOM", "Kameralna, ciepła przestrzeń dla ruchu, fizjoterapii i regeneracji.",
     sec("Nasze podejście", p("Chcemy, żeby w studiu było spokojnie. Stawiamy na małe grupy, uważność i Twoje własne tempo. Bez tłumów, bez oceniania, bez presji.")) +
     sec("Wszystko pod jednym dachem", p('W jednym miejscu możesz potrenować, zadbać o ciało u fizjoterapeutki i odpocząć na masażu. Dzięki temu łatwiej o spójny plan: ból leczymy, ruch wzmacniamy, regenerację planujemy. Zobacz: <a class="text-primary font-semibold hover:underline" href="/treningi-grupowe/">treningi grupowe</a>, <a class="text-primary font-semibold hover:underline" href="/treningi-personalne/">trening personalny</a>, <a class="text-primary font-semibold hover:underline" href="/fizjoterapia/">fizjoterapia</a>, <a class="text-primary font-semibold hover:underline" href="/masaz/">masaż</a>.')) +
     sec("Gdzie jesteśmy", p("ul. Ignacego Daszyńskiego 9, Myślenice. Obsługujemy klientki i klientów z Myślenic, Dobczyc, Sułkowic i okolic.")) + cta("Przyjdź i się rozejrzyj."))

page("faq", "Najczęstsze pytania | BODY BLOOM Myślenice",
     "Odpowiedzi na najczęstsze pytania o BODY BLOOM w Myślenicach: zapisy, MultiSport, treningi, fizjoterapia, masaż, bony.",
     "Najczęstsze pytania", "Nie znalazłaś lub nie znalazłeś odpowiedzi? Zadzwoń: " + TELS + ".",
     sec("Ogólne", faq([("Jak się zapisać?", "Telefonicznie: " + TELS + ". Zapisy przyjmujemy w godzinach otwarcia studia."), ("Gdzie jesteście?", "ul. Ignacego Daszyńskiego 9, 32-400 Myślenice."), ("Czy honorujecie MultiSport?", 'Tak, na wybrane zajęcia grupowe. <a class="text-primary font-semibold hover:underline" href="/multisport/">Szczegóły</a>.')])) +
     sec("Treningi", faq([("Czy zajęcia są dla początkujących?", "Tak, zajęcia są dla każdego poziomu."), ("Co zabrać?", "Wygodny strój, obuwie sportowe, wodę.")])) +
     sec("Fizjoterapia i masaż", faq([("Czy mogę umówić fizjoterapię i trening?", "Tak. Połączenie obu jest naszym atutem."), ("Czy mogę kupić bon?", 'Tak. <a class="text-primary font-semibold hover:underline" href="/bon-podarunkowy/">Szczegóły</a>.')])) + cta())

IG, FB = "https://www.instagram.com/bodybloom_studio_treningowe/", "https://www.facebook.com/p/BodyBloom-61577916802764/"
def contact_card(href, icon, label, value, ext=False):
    x = ' rel="noopener noreferrer" target="_blank"' if ext else ""
    return (f'<a href="{href}"{x} class="group flex items-center gap-space-sm bg-surface-container-lowest rounded-2xl p-space-md shadow-sm hover:shadow-md transition-shadow min-w-0">'
            f'<span class="w-12 h-12 rounded-xl bg-primary-fixed text-on-primary-fixed flex items-center justify-center shrink-0"><i data-lucide="{icon}" class="w-6 h-6"></i></span>'
            f'<span class="flex flex-col min-w-0"><span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant">{label}</span>'
            f'<span class="font-headline-sm text-base font-semibold text-on-surface [overflow-wrap:anywhere] group-hover:text-primary transition-colors">{value}</span></span></a>')
page("kontakt", "Kontakt i dojazd | BODY BLOOM Myślenice",
     "Kontakt BODY BLOOM: ul. Ignacego Daszyńskiego 9, 32-400 Myślenice. Tel. 533 620 733. Godziny otwarcia i dojazd.",
     "Kontakt", "Zadzwoń, napisz na Instagramie albo wpadnij do studia. Zapisy na zajęcia i wizyty przyjmujemy telefonicznie.",
     "{HOME_KONTAKT}" +
     cta("Masz pytanie? Zadzwoń, chętnie pomożemy."),
     pic='<div class="flex flex-col gap-space-xs"><span class="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant">Napisz do nas</span>' +
         contact_card(IG, "instagram", "Instagram", "@bodybloom_studio_treningowe", True) + contact_card(FB, "facebook", "Facebook", "BodyBloom", True) + '</div>')

# Placeholder: noindex and out of the sitemap until real reviews exist.
# TODO(client): add reviews (text + permission) and the Google review link, then drop noindex=True
page("opinie", "Opinie klientów | BODY BLOOM Myślenice",
     "Opinie o BODY BLOOM w Myślenicach. Wkrótce opublikujemy tu opinie naszych klientów.",
     "Opinie klientów", "Opinie pojawią się tutaj wkrótce.",
     sec("Wkrótce", p("Zbieramy opinie klientów i opublikujemy je za ich zgodą. Wcześniej zajrzyj na nasz " + '<a class="text-primary font-semibold hover:underline" href="https://www.instagram.com/bodybloom_studio_treningowe/" rel="noopener" target="_blank">Instagram</a> lub <a class="text-primary font-semibold hover:underline" href="https://www.facebook.com/p/BodyBloom-61577916802764/" rel="noopener" target="_blank">Facebook</a>.')) + cta(), noindex=True)

LEGAL = "Dokument roboczy. Przed publikacją wymaga weryfikacji przez prawnika i uzupełnienia danych administratora."
page("polityka-prywatnosci", "Polityka prywatności | BODY BLOOM Myślenice",
     "Polityka prywatności serwisu BODY BLOOM w Myślenicach: jakie dane przetwarzamy, w jakim celu i jakie masz prawa.",
     "Polityka prywatności", LEGAL,
     # TODO(legal): fill administrator data (name, address, e-mail) once confirmed
     sec("Jakie dane zbieramy", p("Ta strona nie ma formularzy, kont ani systemu analitycznego i nie używa plików cookie do śledzenia. Dane przekazujesz nam tylko wtedy, gdy zadzwonisz lub napiszesz do nas na Instagramie lub Facebooku. Wtedy używamy ich wyłącznie do odpowiedzi i umówienia usługi.")) +
     sec("Zasoby zewnętrzne", p("Strona ładuje czcionki z Google Fonts oraz skrypty z serwerów cdn.tailwindcss.com i unpkg.com. Ich operatorzy mogą widzieć Twój adres IP podczas ładowania strony.")) +
     sec("Twoje prawa", p("Masz prawo dostępu do danych, ich sprostowania, usunięcia, ograniczenia przetwarzania oraz wniesienia skargi do Prezesa UODO.")) +
     sec("Kontakt", p("Telefon: " + TELS + ".")), crumb="Polityka prywatności")

page("regulamin", "Regulamin | BODY BLOOM Myślenice",
     "Regulamin korzystania z usług studia BODY BLOOM w Myślenicach: zapisy, odwoływanie terminów, zasady na zajęciach.",
     "Regulamin", LEGAL,
     # TODO(client): replace with the studio's real rules (payments, cancellations, vouchers)
     sec("Zapisy", p("Zapisy na zajęcia i wizyty przyjmujemy telefonicznie w godzinach otwarcia.")) +
     sec("Zasady", ul(["przychodź w stroju sportowym i obuwiu na zajęcia", "poinformuj nas o przeciwwskazaniach zdrowotnych", "jeśli nie możesz przyjść, odwołaj termin telefonicznie jak najwcześniej"])) +
     sec("Kontakt", p("Pytania: " + TELS + ".")))

# ---------- relative links (site also runs under /bodybloom/ on GitHub Pages) ----------
IDX = "index.html"  # shortcut: explicit index.html so links also work from file://; set "" once only served over HTTP

def absolutize(html):
    """undo relativize so rebuilding from an already-built index.html is idempotent"""
    slugs = "|".join(re.escape(k) for k in PAGES)
    html = re.sub(r'href="(?:\./|\.\./)(?=(?:#oferta)?")', 'href="/', html)
    html = re.sub(r'href="(?:\./|\.\./)?(?=index\.html(?:#oferta)?")', 'href="/', html)
    html = re.sub(r'href="(?:\./|\.\./)?(?=(?:' + slugs + r')/(?:index\.html)?")', 'href="/', html)
    return re.sub(r'(href="/(?:(?:' + slugs + r')/)?)index\.html', r'\1', html)

def relativize(html, depth):
    up = "../" * depth
    html = re.sub(r'href="/(?=(?:#oferta)?")', f'href="{up}{IDX}', html)
    html = re.sub(r'href="/(?!/)([^"#]*/)(?=")', lambda m: f'href="{up}{m.group(1)}{IDX}', html)
    return html

# ---------- assembly ----------
index = absolutize((ROOT / "index.html").read_text(encoding="utf-8"))
pre, rest = index.split("<main", 1)
_, post = rest.split("</main>", 1)
def _img(word):
    m = re.search(r'data-alt="([^"]*' + word + r'[^"]*)" src="([^"]+)"', index)
    return (m.group(2), "") if m else None  # decorative: the h1 already names the service
IMGS = {k: v for k, v in {"treningi-grupowe": _img("group"), "treningi-personalne": _img("personal trainer"), "fizjoterapia": _img("physiotherapist"), "masaz": _img("massage")}.items() if v}
def _sub(html, pat, rep):
    out, n = re.subn(pat, lambda m: rep, html, count=1, flags=re.S)
    if not n: raise SystemExit(f"kontakt: homepage contact markup changed, pattern not found: {pat[:60]}")
    return out
def hours_rows():
    li = ""
    for i, (d, h) in enumerate(HOURS):
        o, c = h.split(" – ") if "–" in h else ("", "")
        mins = lambda t: int(t[:2]) * 60 + int(t[3:]) if t else -1
        li += (f'<li data-day="{(i + 1) % 7}" data-o="{mins(o)}" data-c="{mins(c)}" class="flex justify-between py-1 px-2 -mx-2 rounded-lg border-b border-surface-variant last:border-0">'
               f'<span class="text-on-surface font-medium">{d}</span><span class="text-on-surface-variant tabular-nums">{h}</span></li>')
    # highlights today's row and says whether the studio is open now (visitor's local time; fine for a local studio)
    js = ("<script>(()=>{const d=new Date(),n=d.getHours()*60+d.getMinutes(),r=document.querySelector('#hours li[data-day=\"'+d.getDay()+'\"]');if(!r)return;"
          "r.classList.add('bg-primary-fixed','text-on-primary-fixed');const open=n>=+r.dataset.o&&n<+r.dataset.c,b=document.getElementById('open-now');"
          "b.textContent=open?'Teraz otwarte':'Teraz zamknięte';b.className+=open?' bg-primary-fixed text-on-primary-fixed':' bg-surface-container-high text-on-surface-variant';b.hidden=false})()</script>")
    return (f'<ul id="hours" class="flex flex-col gap-1 font-body-sm text-body-sm">{li}</ul>{js}'
            '<p class="font-body-sm text-body-sm text-on-surface-variant mt-space-xs">Zajęcia grupowe odbywają się według <a class="text-primary font-semibold hover:underline" href="/grafik/">grafiku</a>.</p>')
_k = re.search(r'<section class="py-space-xl" id="kontakt">.*?</section>', index, flags=re.S).group(0)
_k = _k.replace(' id="kontakt"', "").replace("py-space-xl", "py-space-lg", 1)
_k = _sub(_k, r'<div class="flex flex-col gap-2 font-body-sm text-body-sm">.*?Zamknięte</span>\s*</div>\s*</div>', hours_rows())
_k = _sub(_k, r'<h3 class="[^"]*">\s*Godziny otwarcia\s*</h3>',
          '<div class="flex items-center justify-between gap-2 mb-space-xs"><h3 class="font-label-md text-label-md font-semibold text-on-surface uppercase tracking-wider">Godziny otwarcia</h3>'
          '<span id="open-now" hidden class="font-label-sm text-label-sm font-semibold px-3 py-1 rounded-full"></span></div>')
_k = _sub(_k, r'<p class="font-label-lg text-label-lg font-semibold text-on-surface">ul\. Ignacego',
          '<p class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant font-semibold">BODY BLOOM Studio Treningowe</p><p class="font-label-lg text-label-lg font-semibold text-on-surface">ul. Ignacego')
PAGES["kontakt"]["body"] = PAGES["kontakt"]["body"].replace("{HOME_KONTAKT}", _k)
main_open = '<main class="flex-1 pt-20 w-full max-w-[1600px] mx-auto px-gutter-mobile sm:px-margin bg-surface">'

def head_meta(url, title, desc, ld):
    blocks = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return (f'<!--seo--><meta name="description" content="{desc}"><link rel="canonical" href="{url}">'
            f'<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:locale" content="pl_PL">'
            f'{blocks}<!--/seo-->')

def with_meta(html, title, meta):
    html = re.sub(r"<!--seo-->.*?<!--/seo-->", "", html, flags=re.S)
    html = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", html, count=1)
    # whole site kept out of search engines for now; remove NOINDEX to allow indexing
    return html.replace("</head>", meta.replace("<!--/seo-->", NOINDEX + "<!--/seo-->", 1) + "</head>", 1)

NOINDEX = '<meta name="robots" content="noindex, nofollow">'

ADDR = {"@type": "PostalAddress", "streetAddress": "ul. Ignacego Daszyńskiego 9", "postalCode": "32-400", "addressLocality": "Myślenice", "addressCountry": "PL"}
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
HRS = [("07:00", "20:00")] + [("07:30", "20:00")] * 3 + [("07:30", "19:00"), ("08:00", "11:00")]
BIZ = {"@context": "https://schema.org", "@type": "HealthClub", "name": "BODY BLOOM", "url": SITE + "/", "telephone": TEL, "address": ADDR,
       "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": d, "opens": o, "closes": c} for d, (o, c) in zip(DAYS, HRS)],
       "sameAs": ["https://www.instagram.com/bodybloom_studio_treningowe/", "https://www.facebook.com/p/BodyBloom-61577916802764/"]}

def home_grafik():
    rows = []
    for di, (day, items) in enumerate(GRAFIK):
        for t, n, who in items:
            h, m = map(int, t.split(":"))
            rows.append(f'<div data-t="{di * 1440 + h * 60 + m}" class="{"" if len(rows) < 3 else "hidden "}bg-surface-container-lowest p-space-md rounded-2xl shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-space-sm hover:shadow-md transition-shadow">'
                        f'<div class="flex items-center gap-space-md min-w-0"><div class="bg-surface-container px-3.5 py-2 rounded-xl text-center shrink-0 min-w-28"><span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant block">{day}</span><span class="font-headline-sm text-headline-sm font-bold text-on-surface block tabular-nums">{t}</span></div>'
                        f'<div class="flex flex-col min-w-0"><h3 class="font-headline-sm text-base sm:text-headline-sm font-semibold text-on-surface">{n}</h3><p class="font-body-sm text-body-sm text-on-surface-variant mt-0.5">{who}</p></div></div>'
                        f'<a class="inline-flex items-center justify-center bg-primary text-on-primary font-label-md text-label-md px-5 py-2.5 rounded-full hover:bg-primary-container transition-colors shrink-0" href="tel:{TEL}">Zapisz się</a></div>')
    # shows the next 3 classes from now (Mon=0, minutes of week); without JS the first 3 of the week stay visible
    js = ("<script>(()=>{const l=document.getElementById('grafik-next'),r=[...l.children],d=new Date(),n=((d.getDay()+6)%7)*1440+d.getHours()*60+d.getMinutes();"
          "const s=[...r.filter(e=>+e.dataset.t>n),...r.filter(e=>+e.dataset.t<=n)].slice(0,3);r.forEach(e=>e.classList.toggle('hidden',!s.includes(e)));s.forEach(e=>l.append(e))})()</script>")
    return '<!--grafik--><div id="grafik-next" class="flex flex-col gap-space-xs">' + "".join(rows) + "</div>" + js + "<!--/grafik-->"
if "<!--grafik-->" not in index:
    a = index.index('<div class="flex flex-col gap-space-xs">\n<!-- Timetable Row 1 -->')
    b = index.index("</div>\n</div>\n<!-- Right Column")
    index = index[:a] + "<!--grafik--><!--/grafik-->" + index[b:]
index = re.sub(r"<!--grafik-->.*?<!--/grafik-->", lambda m: home_grafik(), index, flags=re.S)

HOME_TITLE = "BODY BLOOM Myślenice | Studio treningowe, fizjoterapia i masaż"
HOME_DESC = "Treningi grupowe i personalne, fizjoterapia, masaż i MultiSport w Myślenicach. Ignacego Daszyńskiego 9. Zadzwoń: 533 620 733."
(ROOT / "index.html").write_text(relativize(with_meta(index, HOME_TITLE, head_meta(SITE + "/", HOME_TITLE, HOME_DESC, [BIZ])), 0), encoding="utf-8")

# shell for subpages: no "current page" mark on Start
pre_sub = pre.replace('aria-current="page" class="transition-colors py-2 text-primary font-bold inline-flex items-center gap-1.5"',
                      'class="font-label-lg text-label-lg text-on-surface-variant hover:text-on-surface transition-colors py-2 inline-flex items-center gap-1.5"')
pre_sub = re.sub(r"<!--seo-->.*?<!--/seo-->", "", pre_sub, flags=re.S)

def render(slug, d, depth=1):
    url = f"{SITE}/{slug}/"
    parent = PAGES.get(slug.rsplit("/", 1)[0]) if "/" in slug else None
    crumbs = [("Start", SITE + "/")] + ([(parent["crumb"], f'{SITE}/{slug.rsplit("/", 1)[0]}/')] if parent else []) + [(d["crumb"], url)]
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}]
    if d["svc"]:
        ld.append({"@context": "https://schema.org", "@type": "Service", "name": d["svc"], "areaServed": "Myślenice", "provider": {"@type": "HealthClub", "name": "BODY BLOOM", "telephone": TEL, "address": ADDR}})
    if slug == "kontakt": ld.append(BIZ)
    bc = f'<nav aria-label="Breadcrumb" class="font-label-md text-label-md text-on-surface-variant"><a class="hover:text-primary" href="/">Start</a> <span aria-hidden="true">/</span> {"".join(f'<a class="hover:text-primary" href="{u[len(SITE):]}">{n}</a> <span aria-hidden="true">/</span> ' for n, u in crumbs[1:-1])}<span aria-current="page">{d["crumb"]}</span></nav>'
    img = IMGS.get(slug)
    pic = d.get("pic") or (f'<div class="hidden md:block rounded-2xl overflow-hidden aspect-[4/3] shadow-sm"><img class="w-full h-full object-cover" src="{img[0]}" alt="{img[1]}" loading="eager"></div>' if img else "")
    acts = (f'<div class="flex flex-wrap gap-space-xs pt-2">{btn("tel:" + TEL, "phone", "Zadzwoń: " + TELS)}{btn("/wydarzenia/", "arrow-left", "Wszystkie wydarzenia", True) if parent else btn(MAPS, "navigation", "Dojazd", True, True) if slug == "kontakt" else btn("/cennik/", "receipt-text", "Cennik", True)}</div>' if d["svc"] or d.get("pic") or slug == "kontakt" else "")
    head = (f'<header class="mt-space-md bg-surface-container-low rounded-3xl p-space-md md:p-space-lg grid grid-cols-1 gap-space-md {"md:grid-cols-[1.3fr_1fr] md:items-center" if pic else ""}">'
            f'<div class="flex flex-col gap-space-sm max-w-3xl">{bc}'
            f'<h1 class="font-display-lg-mobile text-display-lg-mobile md:font-display-lg md:text-display-lg tracking-tight break-words">{d["h1"]}</h1>'
            f'<p class="font-body-lg text-body-lg text-on-surface-variant">{d["lead"]}</p>{acts}</div>{pic}</header>')
    html = pre_sub + main_open + '<div class="flex flex-col w-full">' + head + d["body"] + "</div></main>" + post
    html = with_meta(html, d["title"], head_meta(url, d["title"], d["desc"], ld))
    return relativize(html, depth) if depth is not None else html

for slug, d in PAGES.items():
    out = ROOT / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(slug, d, slug.count("/") + 1), encoding="utf-8")

# 404 (noindex, absolute asset paths so it works at any depth)
nf = {"title": "Nie znaleziono strony | BODY BLOOM", "desc": "Nie znaleziono strony.", "h1": "Nie znaleziono strony", "crumb": "404", "svc": None, "noindex": True,
      "lead": "Tej strony nie ma lub została przeniesiona.", "body": cta("Wróć na stronę główną lub zadzwoń.")}
(ROOT / "404.html").write_text(render("404", nf, None), encoding="utf-8")

urls = [""] + [s + "/" for s, d in PAGES.items() if not d["noindex"]]
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{SITE}/{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
print(len(PAGES), "pages built")
