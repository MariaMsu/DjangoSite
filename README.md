# DjangoSite
> оставь одежду, всяк сюда смотрящий.
>> пути .md неисповедимы

сайт, который умеет падать и считать кол-во постов на странице ВК. Состоит из 3 частей:

+  сервер сайта на django
+ сервер-калькулятор на pure python
+  сервер-парсер на pure python


как завести:

1. ```python3 manage.py runserver``` из папки DjangoSite  

2. если вы словили ошибку  
```File "manage.py", line 14, in <module>  
) from exc  
ImportError: Couldn't import Django```
, то уставновить django:
    ```sudo apt install python3-pip```
    ```pip3 install django```  
3. перейти по адресу http://127.0.0.1:8000/    
  
> теперь можно регистрироваться, но если вам этого мало, то запустите сервера, выполняющие обработку запросов:  

4. ```python3 calculator.py``` из папки DjangoSite/side_servers  

5. ```python3 parser.py``` из папки DjangoSite/side_servers

пример ввода:
    link to vk profile: https://vk.com/elyaishere
    any expression (only "+" and "-"): 2-1
