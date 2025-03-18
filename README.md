# iMAP4
Protocol IMAP4 for Gmail

 Projekt zakłada utworzenie serwisu który cyklicznie monitoruje ruch na skrzynce 
email (IMAP) i filtruje wiadomości, które mają w tytule frazę [RED] i zawierają załącznik. 
Następnie wiadomość ta powinna zostać przeniesiona na skrzynce do folderu OLD-RED, a 
tytuł oraz załącznik powinny zostać zapisane lokalnie. 

Architektura Projektu 
1. Logowanie do Skrzynki Email: Skrypt loguje się do skrzynki email za pomocą 
protokołu IMAP.  
2. Tworzenie Folderu: Sprawdza, czy folder OLD-RED istnieje, a jeśli nie, tworzy go.  
3. Filtrowanie Wiadomości: Wyszukuje wiadomości z frazą [RED] w tytule.  
4. Przetwarzanie Wiadomości: Pobiera zawartość wiadomości oraz załączniki, 
zapisuje je lokalnie i przenosi wiadomość do folderu OLD-RED.  
