---
render_macros: true
---

# Indeks rozwiązań

Ten katalog definiuje komponenty warstwy rozwiązań, które spinają wymagania projektowe z późniejszymi repozytoriami implementacyjnymi.

Opisuje on, czego architektura rozwiązania oczekuje od bazowych komponentów takich jak Orbiplex Node, cienkie klienty kontrolne oraz opcjonalne narzędzia deweloperskie, bez przeciekania do szczegółowego układu modułów konkretnego repo.

Role związane z Node mogą pojawiać się tu później jako osobne komponenty, nawet jeśli operacyjnie są podpięte do Node. Przykładowo archivist, provider memarium albo provider sensorium mogą być osobnym programem lub procesem z własnym API i runtime'em, a nadal należeć do powierzchni rozwiązania Node.

## Bieżące komponenty rozwiązania

{{ list_matching_pages("*.md", page=page, exclude="SOLUTIONS*.md", summaries=true) }}

## Widoki generowane

- [Macierz zdolności rozwiązań](CAPABILITY-MATRIX.pl.md)

## Rejestry i mapy kontraktów

- [Rejestr capability IDs](CAPABILITY-REGISTRY.pl.md)
