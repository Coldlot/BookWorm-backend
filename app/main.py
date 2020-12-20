from flask import Flask, jsonify, send_file

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
            Book("Кодеры за работой", "Питер Сейбел", "Образование", "Программисты - люди не очень публичные, многие работают поодиночке или в небольших группах. Причем самая важная и интересная часть их работы никому не видна, потому что происходит у них в голове. Питер Сейбел, писатель-программист, снимает покров таинственности с этой профессии.", "http://127.0.0.1:5000/thumbs/kodery-za-rabotoy.png", "http://127.0.0.1:5000/files/kodery-za-rabotoy.pdf", False),
            Book("Простой Python", "Билл Любанович", "Образование", "Эта книга идеально подходит как для начинающих программистов, так и для тех, кто только собирается осваивать Python, но уже имеет опыт программирования на других языках. В ней подробно рассматриваются самые современные пакеты и библиотеки Python. Стилистически издание напоминает руководство с вкраплениями кода, подробно объясняя различные концепции Python 3.", "http://127.0.0.1:5000/thumbs/simple-python.png", "http://127.0.0.1:5000/files/simple-python.pdf", False),
            Book("Код: тайный язык информатики", "Чарльз Петцольд", "Образование", "Культовая книга, ставшая для многих первым уверенным шагом в программировании.", "http://127.0.0.1:5000/thumbs/code.png", "http://127.0.0.1:5000/files/code.pdf", False),
            Book("Идеальный программист", "Роберт Мартин", "Образование", "Всех программистов, которые добиваются успеха в мире разработки ПО, отличает один общий признак: они больше всего заботятся о качестве создаваемого программного обеспечения. Это – основа для них. Потому что они являются профессионалами своего дела.", "http://127.0.0.1:5000/thumbs/ideal-programmer.png", "http://127.0.0.1:5000/files/ideal-programmer.pdf", False),
            Book("Путь программиста: человек эпохи IT", "Джон Сонмез", "Образование", "Любой программист - прежде всего, человек со своими достоинствами и недостатками. Но в то же время программист - это интеллектуал, человек, постоянно занятый решением задач, анализом требований, исправлением ошибок, взаимодействием с коллегами и заказчиками.", "http://127.0.0.1:5000/thumbs/put-programmista.png", "http://127.0.0.1:5000/files/put-programmista.pdf", False),
            Book("Алгоритмы для чайников", "Джон Поль Мюллер, Лука Массарон", "Образование", "Не нужно иметь ученую степень, чтобы понять смысл алгоритмов. Это ясное и доступное руководство покажет вам, как алгоритмы влияют на нашу повседневную жизнь. Они вездесущи и сопровождают всю нашу жизнь - от общения с друзьями в сети до принятия важных решений. Если вы хотите знать, как использовать алгоритмы для решения реальных задач - эта книга для вас.", "http://127.0.0.1:5000/thumbs/algoritmy-dlya-chaynikov.png", "http://127.0.0.1:5000/files/algoritmy-dlya-chaynikov.pdf", False),
            Book("Программирование на Java для начинающих", "Алексей Васильев", "Образование", "Полный спектр сведений о языке Java с примерами и разбором задач от автора учебников-бестселлеров по языкам программирования Алексея Васильева. С помощью этой книги освоить язык Java сможет каждый желающий - от новичка до специалиста.", "http://127.0.0.1:5000/thumbs/java-prog.png", "http://127.0.0.1:5000/files/java-prog.pdf", False),
            Book("Олимпиадное программирование", "Антти Лааксонен", "Образование", "Эта замечательная книга представляет собой всестороннее введение в современное олимпиадное программирование. В книге приведено много приемов проектирования алгоритмов, которые известны опытным олимпиадникам, но до сих пор обсуждались лишь на различных сетевых форумах и в блогах.", "http://127.0.0.1:5000/thumbs/olimpiadnoe-programmirovanie.png", "http://127.0.0.1:5000/files/olimpiadnoe-programmirovanie.pdf", False),
        ]




#Flask
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run()
