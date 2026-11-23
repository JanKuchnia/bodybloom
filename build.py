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
    return (f'<section class="py-space-lg max-w-4xl flex flex-col gap-space-sm">{e}'
            f'<h2 class="font-headline-md text-headline-md text-on-surface tracking-tight">{h}</h2>{inner}</section>')
def ul(items):
    li = "".join(f'<li class="flex items-start gap-3"><i data-lucide="check" class="w-5 h-5 text-primary shrink-0 mt-0.5"></i><span>{i}</span></li>' for i in items)
    return f'<ul class="flex flex-col gap-2 font-body-md text-body-md text-on-surface-variant">{li}</ul>'
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
    a = "".join(f'<a class="inline-flex items-center gap-1 text-primary font-label-md font-semibold hover:underline" href="{u}">{t}<i data-lucide="arrow-right" class="w-4 h-4"></i></a>' for u, t in links)
    return f'<section class="py-space-md max-w-4xl"><h2 class="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant mb-2">Zobacz też</h2><div class="flex flex-wrap gap-x-6 gap-y-2">{a}</div></section>'
DISCLAIMER = p("<em>Informacje na tej stronie mają charakter ogólny i nie zastępują porady lekarza.</em>")

# ---------- pages ----------
# slug: (title<=60, description 120-155, h1, lead, body, service_schema_name|None, breadcrumb label)
PAGES = {}
def page(slug, title, desc, h1, lead, body, svc=None, crumb=None, noindex=False):
    PAGES[slug] = dict(title=title, desc=desc, h1=h1, lead=lead, body=body, svc=svc, crumb=crumb or h1, noindex=noindex)

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

page("cennik", "Cennik | BODY BLOOM Myślenice",
     "Cennik BODY BLOOM w Myślenicach: treningi, fizjoterapia, masaż. Aktualne ceny i zasady rezerwacji, tel. 533 620 733.",
     "Cennik", "Ceny usług BODY BLOOM. Pytaj o pakiety i zasady MultiSport.",
     # TODO(client): replace with real prices (HTML text, not an image) and add a "ważny od" date
     sec("Ceny", table(["Usługa", "Cena"], [["Trening personalny", "zadzwoń po aktualną cenę"], ["Treningi grupowe", "zadzwoń po aktualną cenę"], ["Fizjoterapia", "zadzwoń po aktualną cenę"], ["Masaż", "zadzwoń po aktualną cenę"]], 'Cennik jest w trakcie aktualizacji. Telefon: <a class="text-primary font-semibold hover:underline" href="tel:' + TEL + '">' + TELS + '</a>.')) +
     sec("MultiSport", p('Zasady korzystania z karty opisaliśmy na stronie <a class="text-primary font-semibold hover:underline" href="/multisport/">MultiSport</a>.')) +
     sec("Bony podarunkowe", p('Szczegóły: <a class="text-primary font-semibold hover:underline" href="/bon-podarunkowy/">bon podarunkowy</a>.')) +
     cta("Zapytaj o ceny i pakiety."), crumb="Cennik")

page("grafik", "Grafik zajęć | BODY BLOOM Myślenice",
     "Grafik zajęć grupowych BODY BLOOM w Myślenicach: dni, godziny i rodzaje zajęć. Zapisz się telefonicznie: 533 620 733.",
     "Grafik zajęć", "Najbliższe zajęcia grupowe. Zapisy telefoniczne.",
     # TODO(client): sample rows copied from the home page design; replace with the real timetable
     sec("Zajęcia grupowe", table(["Dzień", "Godzina", "Zajęcia", "Czas"], [["Poniedziałek", "18:00", "Zdrowy Kręgosłup &amp; Mobility", "50 min"], ["Wtorek", "09:00", "Poranny Pilates &amp; Oddech", "55 min"], ["Czwartek", "19:15", "Wzmacnianie Funkcjonalne", "50 min"]], 'Grafik może ulec zmianie. Przed przyjściem zadzwoń: <a class="text-primary font-semibold hover:underline" href="tel:' + TEL + '">' + TELS + '</a>.')) +
     sec("Zapisy", p('Liczba miejsc jest ograniczona. Więcej o zajęciach: <a class="text-primary font-semibold hover:underline" href="/treningi-grupowe/">treningi grupowe</a>. Zasady MultiSport: <a class="text-primary font-semibold hover:underline" href="/multisport/">tutaj</a>.')) +
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

page("wydarzenia", "Wydarzenia w studiu | BODY BLOOM Myślenice",
     "Wydarzenia w BODY BLOOM w Myślenicach: Krąg Kobiet, wieczory relaksacyjne i nowe grupy zajęć. Sprawdź, co się dzieje.",
     "Wydarzenia w studiu", "Warsztaty, spotkania i nowe grupy. Szczegóły i zapisy telefonicznie.",
     # TODO(client): add dates; use Event schema only for upcoming events
     sec("Najbliższe", cards([("heart-handshake", "Krąg Kobiet: Spokojny Oddech i Relaks", "Warsztaty dla kameralnej grupy: techniki somatyczne, automasaż i uważność."), ("moon", "Wieczór Andrzejkowy / Relaksacyjny", "Rozciąganie przy świecach, napar ziołowy i relaksacja dźwiękiem. Limit 8 miejsc."), ("dumbbell", "Nowy cykl Zumba &amp; Wzmacnianie", "Energetyczne zajęcia dla każdego. Start od poniedziałku.")])) +
     sec("Aktualności", p('Najnowsze informacje publikujemy na <a class="text-primary font-semibold hover:underline" href="https://www.instagram.com/bodybloom_studio_treningowe/" rel="noopener" target="_blank">Instagramie</a> i <a class="text-primary font-semibold hover:underline" href="https://www.facebook.com/p/BodyBloom-61577916802764/" rel="noopener" target="_blank">Facebooku</a>.')) +
     cta("Zapytaj o wolne miejsca."))

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

page("kontakt", "Kontakt i dojazd | BODY BLOOM Myślenice",
     "Kontakt BODY BLOOM: ul. Ignacego Daszyńskiego 9, 32-400 Myślenice. Tel. 533 620 733. Godziny otwarcia i dojazd.",
     "Kontakt", "Zadzwoń lub wpadnij do studia.",
     sec("Dane kontaktowe", ul(["ul. Ignacego Daszyńskiego 9, 32-400 Myślenice", 'Telefon: <a class="text-primary font-semibold hover:underline" href="tel:' + TEL + '">' + TELS + '</a>', 'Instagram: <a class="text-primary font-semibold hover:underline" href="https://www.instagram.com/bodybloom_studio_treningowe/" rel="noopener" target="_blank">@bodybloom_studio_treningowe</a>', 'Facebook: <a class="text-primary font-semibold hover:underline" href="https://www.facebook.com/p/BodyBloom-61577916802764/" rel="noopener" target="_blank">BodyBloom</a>'])) +
     sec("Godziny otwarcia", table(["Dzień", "Godziny"], [[d, h] for d, h in HOURS])) +
     sec("Dojazd", p("Obsługujemy klientki i klientów z Myślenic, Dobczyc, Sułkowic i okolic.") + f'<div>{btn(MAPS, "navigation", "Otwórz w Mapach Google", False, True)}</div>') + cta())

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

# ---------- assembly ----------
index = (ROOT / "index.html").read_text(encoding="utf-8")
pre, rest = index.split("<main", 1)
_, post = rest.split("</main>", 1)
main_open = '<main class="flex-1 pt-20 w-full max-w-7xl mx-auto px-gutter-mobile sm:px-margin bg-surface">'

def head_meta(url, title, desc, ld):
    blocks = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return (f'<!--seo--><meta name="description" content="{desc}"><link rel="canonical" href="{url}">'
            f'<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:locale" content="pl_PL">'
            f'{blocks}<!--/seo-->')

def with_meta(html, title, meta):
    html = re.sub(r"<!--seo-->.*?<!--/seo-->", "", html, flags=re.S)
    html = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", html, count=1)
    return html.replace("</head>", meta + "</head>", 1)

ADDR = {"@type": "PostalAddress", "streetAddress": "ul. Ignacego Daszyńskiego 9", "postalCode": "32-400", "addressLocality": "Myślenice", "addressCountry": "PL"}
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
HRS = [("07:00", "20:00")] + [("07:30", "20:00")] * 3 + [("07:30", "19:00"), ("08:00", "11:00")]
BIZ = {"@context": "https://schema.org", "@type": "HealthClub", "name": "BODY BLOOM", "url": SITE + "/", "telephone": TEL, "address": ADDR,
       "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": d, "opens": o, "closes": c} for d, (o, c) in zip(DAYS, HRS)],
       "sameAs": ["https://www.instagram.com/bodybloom_studio_treningowe/", "https://www.facebook.com/p/BodyBloom-61577916802764/"]}

HOME_TITLE = "BODY BLOOM Myślenice | Studio treningowe, fizjoterapia i masaż"
HOME_DESC = "Treningi grupowe i personalne, fizjoterapia, masaż i MultiSport w Myślenicach. Ignacego Daszyńskiego 9. Zadzwoń: 533 620 733."
(ROOT / "index.html").write_text(with_meta(index, HOME_TITLE, head_meta(SITE + "/", HOME_TITLE, HOME_DESC, [BIZ])), encoding="utf-8")

# shell for subpages: no "current page" mark on Start
pre_sub = pre.replace('aria-current="page" class="transition-colors py-2 text-primary font-bold inline-flex items-center gap-1.5"',
                      'class="font-label-lg text-label-lg text-on-surface-variant hover:text-on-surface transition-colors py-2 inline-flex items-center gap-1.5"')
pre_sub = re.sub(r"<!--seo-->.*?<!--/seo-->", "", pre_sub, flags=re.S)

def render(slug, d):
    url = f"{SITE}/{slug}/"
    crumbs = [("Start", SITE + "/"), (d["crumb"], url)]
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}]
    if d["svc"]:
        ld.append({"@context": "https://schema.org", "@type": "Service", "name": d["svc"], "areaServed": "Myślenice", "provider": {"@type": "HealthClub", "name": "BODY BLOOM", "telephone": TEL, "address": ADDR}})
    if slug == "kontakt": ld.append(BIZ)
    bc = f'<nav aria-label="Breadcrumb" class="font-label-md text-label-md text-on-surface-variant"><a class="hover:text-primary" href="/">Start</a> <span aria-hidden="true">/</span> <span aria-current="page">{d["crumb"]}</span></nav>'
    head = (f'<header class="pt-space-lg pb-space-sm max-w-4xl flex flex-col gap-space-sm">{bc}'
            f'<h1 class="font-display-lg-mobile text-display-lg-mobile md:font-display-lg md:text-display-lg tracking-tight break-words">{d["h1"]}</h1>'
            f'<p class="font-body-lg text-body-lg text-on-surface-variant">{d["lead"]}</p></header>')
    html = pre_sub + main_open + '<div class="flex flex-col w-full">' + head + d["body"] + "</div></main>" + post
    html = with_meta(html, d["title"], head_meta(url, d["title"], d["desc"], ld))
    return html.replace("<head>", '<head><meta name="robots" content="noindex">', 1) if d.get("noindex") else html

for slug, d in PAGES.items():
    out = ROOT / slug / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(render(slug, d), encoding="utf-8")

# 404 (noindex, absolute asset paths so it works at any depth)
nf = {"title": "Nie znaleziono strony | BODY BLOOM", "desc": "Nie znaleziono strony.", "h1": "Nie znaleziono strony", "crumb": "404", "svc": None, "noindex": True,
      "lead": "Tej strony nie ma lub została przeniesiona.", "body": cta("Wróć na stronę główną lub zadzwoń.")}
(ROOT / "404.html").write_text(render("404", nf), encoding="utf-8")

urls = [""] + [s + "/" for s, d in PAGES.items() if not d["noindex"]]
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{SITE}/{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
print(len(PAGES), "pages built")
