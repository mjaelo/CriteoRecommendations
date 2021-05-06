# CriteoRecommendations
Program służy do polecania produktów użytkownikom na dany dzień, baując na wyświetlonych produktach z poprzednich dni kampanii.
- Przed uruchomieniem, należy pobrać zbiór danych CPS (Criteo Predictive Search) i przetworzyć go na format .csv w folderze dane. Można również odhashować dane.
- Plik partner_data_splitter rozdzieli plik na osobne dla partnerów w folderze partners. Występują tam również funkcje do odkodowania i sprawdzenia poprawności hashowania danych.
- plik simulation_core przetwarza dane i zbiera informacje na dany dzień. Wylicza również informacje o rentowności kampanii i tworzy odpowiednie wykresy.
- plik optimizer wyznacza listę produktów wykluczonych na dany dzień
