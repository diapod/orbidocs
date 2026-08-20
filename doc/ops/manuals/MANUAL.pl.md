---
render_macros: true
---

# Podręczniki operatorskie

Podręcznik operatorski jest **dokumentacją referencyjną komponentu**. Wyjaśnia,
do czego komponent służy, jak działa i z czym się komunikuje. Zbiera również jego
kontrakty danych, ustawienia, limity, możliwe odmowy oraz stan zapisywany na dysku.

Rozgraniczenie rodzin dokumentacji operacyjnej:

- **Podręcznik** — opis komponentu i jego kontraktów. *Czym jest, jak go
  skonfigurować i jakie dane udostępnia.*
- **Instrukcja awaryjna (runbook)** — procedura. *Co zrobić, gdy
  wystąpi określona sytuacja.*
- **[HOWTO](../howto/HOWTO.pl.md)** — instrukcja przeprowadzenia konkretnego
  zadania.
- **[FAQ](../faq/FAQ.pl.md)** — odpowiedź na pytanie.

Podręcznik odsyła do instrukcji awaryjnej zamiast powtarzać jej procedurę.
Nazwy typów, pól konfiguracji, tras i kodów błędów pozostają w oryginalnej
postaci `code`. Tekst objaśniający używa zwykłego języka i wprowadza termin
techniczny przy jego pierwszym użyciu.

## Struktura podręcznika

Nagłówek dokumentu zawiera **nazwę komponentu**. Akapit otwierający krótko
wyjaśnia jego rolę i odsyła do FAQ oraz HOWTO. Dalsze sekcje mają stałą
numerację i kolejność:

1. Cel i funkcje
2. Zasada działania
3. Umiejscowienie w architekturze i kanały komunikacji (z uzasadnieniem każdego kanału)
4. Kontrakty danych — schematy, cel użycia, kanał przepływu
5. Limity i zachowanie po ich przekroczeniu
6. Słowniki niepowodzeń i statusów (kod, znaczenie, ponawialność)
7. Autorytet i jego cofnięcie
8. Granice zaufania — co komponent weryfikuje sam, a co przyjmuje od wołającego
9. Zależności i tryby zdegradowane
10. Stan trwały i restart
11. Konfiguracja — składanie warstw, źródła, wartości domyślne
12. Obserwowalność — status, ślady, liczniki
13. Koszt i zasoby
14. Wersje kontraktów i kompatybilność
15. Znane ograniczenia
16. Powiązanie z implementacją

Sekcja 16 jest obowiązkowa. Wskazuje odpowiadający komponentowi wpis w rejestrze
implementacji, skrzynie Rust, schematy, zdolności i trasy. Dzięki temu można
wykryć rozbieżność między podręcznikiem a kodem. Zasadę opisuje
[TRACEABILITY.md](../../../TRACEABILITY.md).

## Dostępne podręczniki

{{ list_matching_pages("*-manual.pl.md", page=page) }}
