<h2>Первичная настройка проекта</h2>

<p>Не забудьте создать виртуальное окружения и установить необходимые библиотеки для работы проекта из фаила requirements.txt.</p><br>

<p>Перед тем как запустить проект вам необходимо настроить подключения к DB указать данные, хост и имя DB. 
Настроить это можно в файле config.py, поля SQLALCHEMY_DATABASE_URI.

mysql+pymysql://{username}:{password}@{host:port}/{dbname}</p>

При возникновении каких либо ошибок они будут записываться в лог фаил в папке logs/demo.log<br>
После настройки, проект можно запустить через файл runserver.py
  
  <h2> Правила для передачи JWT TOKEN</h2>
  <p>JWT Token необходимо передать в HEADER в формате:</p>
    Authorization: Bearer {$JWT}<br>
    также в качестве тестового JWT Token можете использовать ниже указаны токен
    
      eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1Mjg1NDY1MywianRpIjoiZDM5ZGY2NDItMTU3ZC00MGU0LWI3YTAtZDBiZTAzNDljNGRiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJyb2xlIjoiYWRtaW4iLCJwdWJsaWNfaWQiOiIwZjdjMjg4OS01YTk5LTRhMDAtOWE3Ni03NDcwM2E2NDc5ODcifSwibmJmIjoxNjUyODU0NjUzfQ.3Uw_iBYr7XO2Nl8BYAtlwBSXQpyWSCMgfnEbRYR4uo4
  
  <h2>Роутинг</h2>
  
  <h3>v1/user/get/{user_id}</h3>
  Endpoint для получения данных о пользователе по его public_id.<hr>
  <li>Метод: GET</li>
  <li>В качестве параметров необходимо передать user_id в url.</li>
  <li>Также в header необходимо передать JWT токен.</li>
  <li>Ответ от сервера data с информацией о пользователе.</li>
  
  
  <h3>v1/user/registration</h3>
  Endpoint для регистрации нового пользователя.<hr>
  <li>метод: POST.</li>
  
  <li>Параметры необходимо передать в формате JSON:</li>
  <h5>Обязательные параметры</h5>
  email, 
  username, 
  password
  
  <h5>Необязательные параметры:</h5>
  role для указания роли пользователя. Можно указать admin, по умолчанию будет установлено role user.
  <br><li>Ответ от сервера при успешной регистрации пользователя user unique_id.</li>
   
  
  
  <h3>v1/user/status</h3>
  endpoint для изменения статуса пользователя.<hr>
  <li>Метод: POST</li>
  <li>В качестве обязательных параметров необходимо передать в формате JSON user_id и status.</li>
  <li>Также в header необходимо передать JWT токен с role admin.</li>
  <li>Ответ от сервера unique_id, old_status и new_status.</li>
  
  
  <h3>v1/user/authorization</h3>
  endpoint для авторизации.<hr>
  <li>Метод: POST</li>
  <li>В качестве обязательных параметров необходимо передать в формате JSON email и password.</li>
  <li>Ответ от сервера JWT Token.</li>
  
  
  
