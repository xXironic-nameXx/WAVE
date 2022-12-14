from libtorrent import *
from pygame import mixer
from tinytag import TinyTag
import time
import datetime
import os
import climage

p = print
r = input
m = "./music/"


# получает информации о аудио-файле
def audio_get(a, b):
    return TinyTag.get(a + "/" + b[sum(i in b for i in [".txt", ".cue", ".m3u", ".jpg", ".png", ".DS_Store"]) + 1])


# смотрит, если музыка играет
def skip():
    if not mixer.music.get_busy():
        return 1


# возвращает на главное меню
def back(a):
    if a == "вернуться" or a == "<=":
        menu()


# получает файлы в dir'e
def d_getter(g):
    d = []
    try:
        for f in os.listdir(g):
            if os.path.isfile(os.path.join(g, f)):
                d.append(f)
    finally:
        return sorted(d)


# получает обложку пени
def song_cover(d, s):
    c = d[:d.find(".")]
    x = "ETC/"
    o = ".jpg"
    if c + o in os.listdir(m + x):
        p(climage.convert(m + x + c + o, is_unicode=1, is_truecolor=1, is_256color=0, is_16color=0, is_8color=0,
                          width=s), end="")


# получает обложку альбома
def cover(j, k, s):
    p(climage.convert(str(j) + "/art.jpg", is_truecolor=1, is_256color=0, is_16color=0, is_8color=0, is_unicode=1,
                      width=s) if "art.jpg" in k else "", end="")


# спрашивает о размере обложки
def dimens():
    x = r("большая картика? (да/нет): ")
    back(x)
    return [50, 100][x == "да"]


# смотрит на файлы и альбомы любого  dir'a
def z(path=m):
    f_list = []
    d_list = []

    try:
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)):
                f_list.append(f)
            else:
                if os.path.isdir(os.path.join(path, f)):
                    d_list.append(f)
    finally:
        p("""
████─████─████─█──█─█──█────██─
█──█─█▄▄▄─█────█▄▄█─█─▄█────█─█
█──█─█────█────█──█─█▀─█──███──
█──█─████─████─█──█─█──█──███──
        """)
        f_list = sorted(f_list)
        song_cover(f_list[1], 30)
        for i, j in enumerate(f_list):
            if j != ".DS_Store":
                p(j, end=[", ", "\n"][len(f_list[:i]) % 3 != 0])
        if len(d_list) != 0:
            p("""
████──████─████──████──█──█─█────█────█████
█──█──█──█─█────█────█─████─█────█────█───█
█▀▀█──█──█─█▀▀█─█────█─█▐─█─█▀▀█─█──███─███
█──█─██──█─████──████──█──█─████─█──███─███
            """)
            a = d_list[0]
            cover((m + a), d_getter(m + a), 30)
            for i, j in enumerate(d_list):
                if j != "ETC":
                    p(j, end=[", ", "\n"][len(d_list[:i]) % 2 != 0])


# спрашивает о выбранном альбоме
def album():
    f = r("песню из альбома или целый альбом (песню/ целый): ")
    back(f)
    if f == "песню":
        h = m + r("напишите названия альбома сюда: ")
        f_list = d_getter(h)
        p()
        z(h)
        d = dimens()
        cover(h, f_list, d)
        audio = audio_get(h, f_list)
        a = str(audio.artist) + " - " + str(audio.album)
        p(" " * (d // 2 - len(a) // 2) + a)
        c = r("напишите название песни сюда: ")
        back(c)
        p("Играю: " + c, end=" ")
        play(h, c)
        menu()
    else:
        c = r("напишите его названия сюда: ")
        back(c)
        g = m + c
        f_list = []
        p()
        try:
            for f in os.listdir(g):
                if os.path.isfile(os.path.join(g, f)):
                    f_list.append(f)
        finally:
            if r("размешать (да/нет): ") == "нет":
                f_list = sorted(f_list)
            else:
                f_list = f_list
            for i in f_list:
                p(i)
            time.sleep(3)
            d = dimens()
            cover(g, f_list, d)
            audio = audio_get(g, f_list)
            a = str(audio.artist) + " - " + str(audio.album)
            p(" " * (d//2 - len(a)//2) + a)
            x = r("сначала/ с какой-то песни (1 - сначало/ любая другая цифра): ")
            back(x)
            for i in f_list[int(x) - 1 * (".DS_Store" not in f_list):]:
                p("Играю: " + i, end=" ")
                play(g, i)


# выдаёт информацию о музыкальной группе                
def band():
    f_list = []
    bands = set()
    albums = []
    try:
        for f in os.listdir(m):
            if os.path.isdir(os.path.join(m, f)):
                if f != "ETC":
                    f_list.append(f)
    finally:
        f_list = sorted(f_list)
    for j in f_list:
        b = 0
        for i in d_getter(m + j):
            if ".flac" in i:
                b = i
        audio = TinyTag.get(m + j + "/" + b)
        bands.add(str(audio.artist))
        albums.append([j, str(audio.artist)])
    return [list(bands), sorted(albums)]


# проигрывает песню
def play(h, y):
    mixer.init()
    f = False in [i not in y for i in [".cue", ".txt", ".m3u", ".jpg", ".png", ".DS_Store"]]
    if f == 0:
        dur = audio_get(h, [0, y]).duration
    else:
        dur = 0
    i = round(dur % 60)
    p(str(int(dur // 60)) + ":" + "0" * (i < 10) + str(i))
    while f == 0:
        mixer.music.load(h + "/" + y)
        mixer.music.play()
        p()
        a = r("остановить/ следующий: ")
        back(a)
        if a == "остановить":
            mixer.music.pause()
            v = r("начать(начнёт сначала, никак по-другому на данной момент)? (да): ")
            back(v)
            while v != "да":
                continue
            else:
                mixer.music.unpause()
                pause = 1
        else:
            mixer.music.unload()
            f = skip()
            pause = 0
        if pause != 1:
            f = skip()
    else:
        p("закончил играть")


# главная страница        
def home():
    z()
    p()
    p("используйте 'вернуться' или '<=', чтобы выйти из проигрывателя")
    a = r("альбом/ песня/ группы: ")
    p()
    back(a)
    if a == "альбом":
        album()
        menu()
    elif a == "песня":
        d = r("напишите название песни сюда: ")
        back(d)
        di = dimens()
        song_cover(d, di)
        p("Играю: " + d, end=" ")
        play(m, d)
    else:
        bands = band()[0]
        albums = band()[1]
        for i in range(len(bands)):
            p(bands[i], end=["\n", ", "][i % 3 == 0])
        p()
        y = r("кого сегодня послушаем: ")
        back(y)
        e = "ETC/bands"
        p(climage.convert(m + e + "/" + y + ".jpg", is_truecolor=1, is_256color=0, is_16color=0, is_8color=0, is_unicode=1,
                          width=50) if y + ".jpg" in d_getter(m + e) else "", end="")
        p("""
████──████─████──████──█──█─█────█
█──█──█──█─█────█────█─████─█────█
█▀▀█──█──█─█▀▀█─█────█─█▐─█─█▀▀█─█
█──█─██──█─████──████──█──█─████─█
        """)
        for i in albums:
            if y in i:
                print(i[0], end=["\n", ", "][albums.index(i) % 3 == 0])
        p()
        album()
    menu()


# торрент    
def torrent():
    p("""
────────────────────────
█████───███─███────█████
──█─────█─█─█─█──────█──
──█─────███─███▐▀─▌▐─█──
──█─█▀█─█───█──▐▀─██─█──
──█─███─█───█──▐█─▌▐─█──
────────────────────────
    """)

    ses = session()
    c = r("магнитик: ")
    back(c)
    handle = add_magnet_uri(ses, c, {"save_path": m, "storage_mode": storage_mode_t(2)})
    ses.start_dht()

    p(datetime.datetime.now())

    p("скачиваю метадату...")
    while not handle.has_metadata():
        time.sleep(1)
    p("метадату у нас!")

    p("Поехали", handle.name())
    state_str = ["жду", "проверяю", "скачиваю метадату", "торрентю", "закончил"]
    s = handle.status()
    p('(down: %.1f kb/s up: %.1f kB/s дорогие сидеры: %d) %s ' % (
        s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state]))
    if r("стримить торрент(если высокая скорость)? да/нет: ") == "нет":
        while handle.status().state != torrent_status.seeding:
            p('%.2f%% скачено (down: %.1f kb/s up: %.1f kB/s дорогие сидеры: %d) %s ' % (
                s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state]))
            time.sleep(5)
        p(handle.name(), "закончил!")
        p(datetime.datetime.now())
        p("переименуйте картинку альбома на art.jpg")
        time.sleep(5)
        menu()
    else:
        menu()


# главное меню        
def menu():
    if r("торрент/ дом: ") == "дом":
        home()
    else:
        torrent()


# что вас встречает        
p("""
▄▄▄▄▄────▄▄▄───────██████──────▄───▄──▄▄▄▄▄
██──█───█───█─────█▒▒▒▒▒▒█─────█───█──█──██
██─█────█───█────█▒▒▒▒▒▒▒▒█────█████──█████
██████──█───█───█▒▒▒▒▒▒▒▒▒▒█───█───█──█──██
██───█──█───█──█▒▒▒▒▒▒▒▒▒▒▒▒█──█───█──█──██
███████████████████████████████████████████
█▒▒▒▒▒▒▒▒▒▒▒▒█───────────────█▒▒▒▒▒▒▒▒▒▒▒▒█
─█▒▒▒▒▒▒▒▒▒▒█─────────────────█▒▒▒▒▒▒▒▒▒▒█─
──█▒▒▒▒▒▒▒▒█───────────────────█▒▒▒▒▒▒▒▒█──
───█▒▒▒▒▒▒█─────────────────────█▒▒▒▒▒▒█───
────██████───────────────────────██████────

                Н а ч а т ь ?
            да / нет / инструкция
""")
n = r()
if n == "да":
    menu()
elif n == "инструкция":
    p("""
    █▀▀█──█▀█──────█████───
    █▄█▀──█─█─────█▒▒▒▒▒█──
    █▀▀█──█─█────█▒▒▒▒▒▒▒█─
    █▄▄█──███───█▒▒▒▒▒▒▒▒▒█
    ░░░░░░░░░░░█░░░░░░░░░░░
    █▒▒▒▒▒▒▒▒▒█──▐▌─█─████─
    ─█▒▒▒▒▒▒▒█───▐███─█──█─
    ──█▒▒▒▒▒█────▐▌─█─█▀▀█─
    ───█████─────▐▌─█─█──█─
    Волна - это музыкальный
    проигрыватель с функци-
    оналом торрента. 
    Это инструкция по этой 
    терминальной программе.

    1) Вводить нужно опции 
    нужно чётко, как напи-
    сано 

    2) постройте папки сле-
    дующим образом:

    |волна
        |music
            ETC*
            {ваши альбомы}
            {ваши песни}

    * ETC всегда
    должен стоят на 1ом 
    месте, альбомы и песни
    могут быть вразброс

    3) Используем обычные 
    формаиты: .mp3, .FLAC,
    .wav, и.т.д

    4) Картинки песен дол-
    жды быть, как название.
    Картинки ставьте в пап-
    ку "ETC":

    *если в название песни
    имеются точки, уберите 
    их

    пр файл: звезда.jpg

    пр* : вол.на => волна

    5) Картинки альбомов
    должны быть в папке
    альбома и назваться
    "art.jpg"

    пр: /music/чёрный аль-
    бом/art.jpg

    6) Чтобы вернутся из лю-
    бого откуда-либов меню
    напишите "вернуться" или
    "<="

    """)
    if r("я прочитал(да/нет) ") == "да":
        menu()
else:
    exit()
