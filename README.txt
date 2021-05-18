#Running the server

#In cmd admin mode, navigate to
C:\Users\Triinu Tasa\Kool\MuusikaAndmeteadus\django\chord_master>

#Run the server
C:\Users\Triinu Tasa\Kool\MuusikaAndmeteadus\django\chord_master>python .\manage.py runserver

#Running frontend
C:\Users\Triinu Tasa\Kool\MuusikaAndmeteadus\django\chord_master\frontend>npm run dev


#When updating DB schema:
C:\Users\Triinu Tasa\Kool\MuusikaAndmeteadus\django\chord_master>python ./manage.py makemigrations
C:\Users\Triinu Tasa\Kool\MuusikaAndmeteadus\django\chord_master>python ./manage.py migrate

#To view the DB state:
http://127.0.0.1:8000/api/list-videos

#To populate the UG Chord table from csv
http://127.0.0.1:8000/api/upload-chords

#To flush the DB
C:\Users\Triinu Tasa\Kool\MuusikaAndmeteadus\django\chord_master>python ./manage.py flush

#To install FFmpeg
https://www.wikihow.com/Install-FFmpeg-on-Windows
