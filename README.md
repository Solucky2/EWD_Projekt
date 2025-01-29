# EWD final project - Otomoto scrapper

Projekt zaliczeniowy mający na celu przeprowadzenie analizy oraz predykcji cen samochodów osobowych z serwisu   

https://www.otomoto.pl/

W celu pobrania potrzebnych paczek: pip install -r requirements.txt  

Opis struktury projektu:  
**\services** - folder zawierający klasę scrapy.Spider oraz klasy pomocnicze  
**\notebooks\cleaned** - folder zawierający dane zapisane w formie .csv po czyszczeniu oraz zakodowaniu za pomocą  
TargetEncoder  
**\notebooks\cleaner** - notatnik do czyszczenia danych oraz ich transformacji  
**\notebooks\models** - folder z modelami: Regresja Liniowa, Drzewo Decyzyjne, SVM, Ensemble
**\notebooks\raw** - docelowy folder do danych pobranych na sucho z serwisu internetowego  
**\notebooks\visuals** - notantik z wykrasami przedstawiającymi wstępne zależności między danymi  
**\helpers\plotters** - funkcje pomocnicze do tworzenia wykresów w określonym stylu graficznym


