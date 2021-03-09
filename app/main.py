from flask import Flask, jsonify, send_file, request
import os
import csv
import uuid

#Models
class Book:
    def __init__(self, title: str, author: str, genre: str, desc: str, thumbUrl: str, fileUrl: str, isExternal: bool):
        self.title = title
        self.author = author
        self.genre = genre
        self.desc = desc
        self.thumbUrl = thumbUrl
        self.fileUrl = fileUrl
        self.isExternal = isExternal
    def toJson(self):
        book_dict = {
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'description': self.desc,
            'thumb_url': self.thumbUrl,
            'file_url': self.fileUrl,
            'is_external': self.isExternal
        }
        return book_dict

books = [
            Book("Кодеры за работой", "Питер Сейбел", "Образование", "Программисты - люди не очень публичные, многие работают поодиночке или в небольших группах. Причем самая важная и интересная часть их работы никому не видна, потому что происходит у них в голове. Питер Сейбел, писатель-программист, снимает покров таинственности с этой профессии.", "https://spbstu-books-api.herokuapp.com/thumbs/kodery-za-rabotoy.png", "https://spbstu-books-api.herokuapp.com/files/kodery-za-rabotoy.pdf", False),
            Book("Простой Python", "Билл Любанович", "Образование", "Эта книга идеально подходит как для начинающих программистов, так и для тех, кто только собирается осваивать Python, но уже имеет опыт программирования на других языках. В ней подробно рассматриваются самые современные пакеты и библиотеки Python. Стилистически издание напоминает руководство с вкраплениями кода, подробно объясняя различные концепции Python 3.", "https://spbstu-books-api.herokuapp.com/thumbs/simple-python.png", "https://spbstu-books-api.herokuapp.com/files/simple-python.pdf", False),
            Book("Код: тайный язык информатики", "Чарльз Петцольд", "Образование", "Культовая книга, ставшая для многих первым уверенным шагом в программировании.", "https://spbstu-books-api.herokuapp.com/thumbs/code.png", "https://spbstu-books-api.herokuapp.com/files/code.pdf", False),
            Book("Идеальный программист", "Роберт Мартин", "Образование", "Всех программистов, которые добиваются успеха в мире разработки ПО, отличает один общий признак: они больше всего заботятся о качестве создаваемого программного обеспечения. Это – основа для них. Потому что они являются профессионалами своего дела.", "https://spbstu-books-api.herokuapp.com/thumbs/ideal-programmer.png", "https://spbstu-books-api.herokuapp.com/files/ideal-programmer.pdf", False),
            Book("Путь программиста: человек эпохи IT", "Джон Сонмез", "Образование", "Любой программист - прежде всего, человек со своими достоинствами и недостатками. Но в то же время программист - это интеллектуал, человек, постоянно занятый решением задач, анализом требований, исправлением ошибок, взаимодействием с коллегами и заказчиками.", "https://spbstu-books-api.herokuapp.com/thumbs/put-programmista.png", "https://spbstu-books-api.herokuapp.com/files/put-programmista.pdf", False),
            Book("Алгоритмы для чайников", "Джон Поль Мюллер, Лука Массарон", "Образование", "Не нужно иметь ученую степень, чтобы понять смысл алгоритмов. Это ясное и доступное руководство покажет вам, как алгоритмы влияют на нашу повседневную жизнь. Они вездесущи и сопровождают всю нашу жизнь - от общения с друзьями в сети до принятия важных решений. Если вы хотите знать, как использовать алгоритмы для решения реальных задач - эта книга для вас.", "https://spbstu-books-api.herokuapp.com/thumbs/algoritmy-dlya-chaynikov.png", "https://spbstu-books-api.herokuapp.com/files/algoritmy-dlya-chaynikov.pdf", False),
            Book("Программирование на Java для начинающих", "Алексей Васильев", "Образование", "Полный спектр сведений о языке Java с примерами и разбором задач от автора учебников-бестселлеров по языкам программирования Алексея Васильева. С помощью этой книги освоить язык Java сможет каждый желающий - от новичка до специалиста.", "https://spbstu-books-api.herokuapp.com/thumbs/java-prog.png", "https://spbstu-books-api.herokuapp.com/files/java-prog.pdf", False),
            Book("Олимпиадное программирование", "Антти Лааксонен", "Образование", "Эта замечательная книга представляет собой всестороннее введение в современное олимпиадное программирование. В книге приведено много приемов проектирования алгоритмов, которые известны опытным олимпиадникам, но до сих пор обсуждались лишь на различных сетевых форумах и в блогах.", "https://spbstu-books-api.herokuapp.com/thumbs/olimpiadnoe-programmirovanie.png", "https://spbstu-books-api.herokuapp.com/files/olimpiadnoe-programmirovanie.pdf", False),
        ]

class User:
    def __init__(self, email: str, password: str, token: str):
        self.email = email
        self.password = password
        self.token = token

def jsonTokenWithMessage(token: str, message: str):
        json = {
            'message': message,
            'token': token
        }
        return json


#Flask
app = Flask(__name__)
users = []

@app.route('/getBooks', methods= ['GET'])
def getBooks():
    return jsonify([book.toJson() for book in books])

@app.route('/filterBooks/<predicate>', methods= ['GET'])
def filterBooks(predicate: str):
    return jsonify([book.toJson() for book in books if book.title == predicate])

@app.route('/files/<fileUrl>', methods= ['GET'])
def getBook(fileUrl: str):
    return send_file('../files/' + fileUrl, mimetype='application/pdf')

@app.route('/thumbs/<thumbUrl>', methods= ['GET'])
def getThumb(thumbUrl: str):
    return send_file('../thumbs/' + thumbUrl, mimetype='image/png')

@app.route('/registration', methods= ['POST'])
def registration():
    email = str(request.json['email'])
    password = str(request.json['password'])
    for user in users:
        if user.email == email:
            return jsonify(jsonTokenWithMessage('', 'User with the same email has been already registered!'))
    new_user = User(email, password, uuid.uuid4())
    #with open('../config/users.csv', mode='a') as users_csv:
        #csv_writer = csv.writer(users_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #csv_writer.writerow([new_user.email, new_user.password, new_user.token])
    users.append(new_user)
    return jsonify(jsonTokenWithMessage(new_user.token, 'Registered!'))
    

@app.route('/login', methods= ['POST'])
def login():
    email = str(request.json['email'])
    password = str(request.json['password'])
    for user in users:
        print(user.email, ' ', email)
        print(user.password, ' ', password)
        if user.email == email:
            if user.password == password:
                return jsonify(jsonTokenWithMessage(user.token, 'Logged In!'))
            else:
                return jsonify(jsonTokenWithMessage('', 'Invalid creds!'))
    return jsonify(jsonTokenWithMessage('', 'User does not exists!'))

if __name__ == '__main__':
    #if os.path.exists('../config/users.csv'):
       # with open('../config/users.csv', 'r') as users_csv:
           # csv_reader = csv.reader(users_csv, delimiter=',')
           # for row in csv_reader:
            #    email, password, token = row
            #    users.append(User(email, password, token))
    #else:
        #os.mkdir('../config')
       # f = open('../config/users.csv', 'w+')
        #f.close()

    port = int(os.environ.get("PORT", 5000))
    app.run(host= '0.0.0.0', port=port, debug=True)
