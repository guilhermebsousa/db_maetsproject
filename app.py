from flask import Flask, render_template, request, redirect, flash
import mysql.connector


#Conectando ao Banco de Dados
db = mysql.connector.connect(
        host='',
        user='',
        password='', 
        database='maets_store')  
if db.is_connected():
    print(f"Conectado ao banco de dados maets_store")
    


# Funções para obter dados do banco de dados MySQL

#Métodos Tabela Games
    
#Método para listar itens da tabela Games
def getGames():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM games')  
    dados = cursor.fetchall()
    db.commit()
    cursor.close()
    return dados

def getGamesByCategory(genre):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {genre}")  
    dados = cursor.fetchall()
    db.commit()
    cursor.close()
    return dados

#Método para adicionar jogos à tabela Games
def setGames(title, genre, price):
    cursor = db.cursor()
    cursor.callproc('GameAdd', (title, genre, price))
    db.commit()
    cursor.close()

#Método para remover jogos à tabela Games
def delGame(idGame):
    cursor = db.cursor()
    cursor.callproc('GameRemove', (idGame,))
    db.commit()
    cursor.close()

#Método para alterar preço dos jogos
def gamePrice(idGame, newPrice):
    cursor = db.cursor()
    cursor.callproc('GamePriceChange', (idGame, newPrice))
    db.commit()
    cursor.close()

#Método para procurar jogo pelo título
def searchGame(title):
    cursor = db.cursor()
    query = "SELECT * FROM games WHERE title LIKE %s"
    cursor.execute(query, ('%' + title + '%',))
    games = cursor.fetchall()
    db.commit()
    cursor.close()
    return games


#Métodos Tabela Sales

#Método para listar itens da tabela Sales
def getSales():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM sales')  
    dados = cursor.fetchall()
    db.commit()
    cursor.close()
    return dados
 
 #Método para adicionar uma venda
def setSales(idUser, IdGame, total):
    cursor = db.cursor()
    cursor.callproc('SaleAdd', (idUser, IdGame, total))
    db.commit()
    cursor.close()

#Método para deletar uma venda
def delSale(idSale):
    cursor = db.cursor()
    cursor.callproc('SaleRemove', (idSale,))
    db.commit()
    cursor.close()

#Método para pesquisar venda por ID
def searchSale(idSale):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Sales WHERE saleId = %s', (idSale,))
    dados = cursor.fetchall()
    cursor.close()
    return dados


#Métodos Tabela Users 

#Método para listar itens da tabela Users
def getUsers():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users')  
    dados = cursor.fetchall()
    db.commit()
    cursor.close()
    return dados

#Método para adicionar Usuário
def setUsers(nickname, email):
    cursor = db.cursor()
    cursor.callproc('UserAdd', (nickname, email))
    db.commit()
    cursor.close()

#Método para remover Usuário
def delUsers(idUser):
    cursor = db.cursor()
    cursor.callproc('UserRemove', (idUser,))
    db.commit()
    cursor.close()

#Método para pesquisar Usuário pelo nickname
def searchUser(nickname):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Users WHERE nickname LIKE %s', ('%' + nickname + '%',))
    dados = cursor.fetchall()
    cursor.close()
    return dados

#Método para mudar e-mail do usuário
def changeEmail(idUser,email):
    cursor = db.cursor()
    cursor.callproc('ChangeEmail', (idUser, email))
    db.commit()
    cursor.close()

#Método para alterar nickname do usuário
def changeNickname(idUser, nickname):
    cursor = db.cursor()
    cursor.callproc('ChangeNick', (idUser, nickname))
    db.commit()
    cursor.close()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'GUIZAO'



#Rota para o Menu Principal
@app.route("/", methods=['GET','POST'])
def home():
    return render_template('home.html')

#Rota para o Menu Games
@app.route('/gamemenu', methods=["GET","POST"])
def gamemenu():
    return render_template("gamemenu.html")

#Rota para adicionar jogo
@app.route('/addgame', methods=["POST"])
def addGame():
    cursor=db.cursor()
    if request.method == 'POST':
        title = request.form.get('title')
        genre = request.form.get('genre')
        price = request.form.get('price')
        if price is not None:
            price = float(price)
        if title and genre and price:
            setGames(title, genre, price)
            db.commit()
            cursor.close()
            return redirect('/')
        return render_template('addgame.html')

#Rota para listar jogos e pesquisar por nome
@app.route('/games', methods=["GET", "POST"])
def games():
    if request.method == "POST":
        game = request.form.get('sch')
        if not game:
            games = getGames() 
            return render_template("tgames.html", dados=games)
        else:
            game = searchGame(game)
            return render_template("tgames.html", dados=game)

#Rota para o menu das tabelas de jogos
@app.route('/games_tables', methods=["GET", "POST"])
def gamesTables():
    return render_template("gamestables.html")

@app.route('/genre', methods=["GET", "POST"])
def genre():
    return render_template("gamegenre.html")

@app.route('/adventure_games', methods=["GET", "POST"])
def adventureGames():
    if request.method == "POST":
        game = request.form.get('sch')
        if not game:
            games = getGamesByCategory('aventura')
            return render_template("tgames.html", dados=games)
        else:
            game = searchGame(game)
            return render_template("tgames.html", dados=game)


@app.route('/action_games', methods=["GET", "POST"])
def actionGames():
    if request.method == "POST":
        game = request.form.get('sch')
        if not game:
            games = getGamesByCategory('acao')
            return render_template("tgames.html", dados=games)
        else:
            game = searchGame(game)
            return render_template("tgames.html", dados=game)


@app.route('/survival_games', methods=["GET", "POST"])
def survivalGames():
    if request.method == "POST":
        game = request.form.get('sch')
        if not game:
            games = getGamesByCategory('sobrevivencia')
            return render_template("tgames.html", dados=games)
        else:
            game = searchGame(game)
            return render_template("tgames.html", dados=game)


@app.route('/rpg_games', methods=["GET", "POST"])
def rpgGames():
    if request.method == "POST":
        game = request.form.get('sch')
        if not game:
            games = getGamesByCategory('rpg')
            return render_template("tgames.html", dados=games)
        else:
            game = searchGame(game)
            return render_template("tgames.html", dados=game)


@app.route('/strategy_games', methods=["GET", "POST"])
def strategyGames():
    if request.method == "POST":
        game = request.form.get('sch')
        if not game:
            games = getGamesByCategory('estrategia')
            return render_template("tgames.html", dados=games)
        else:
            game = searchGame(game)
            return render_template("tgames.html", dados=game)


#Rota para remover jogo
@app.route('/removegame', methods=["GET", "POST"])
def removegame():
    cursor=db.cursor()
    if request.method == 'POST':
        gameid = request.form.get('gameid')
        if gameid is not None:
            gameid = int(gameid)
            delGame(gameid)
            db.commit()
            cursor.close()
            return redirect('/')
        return render_template('removegame.html')

#Rota para alterar valor de um jogo
@app.route('/gameprice', methods=["POST"])
def gPrice():
    cursor=db.cursor()
    if request.method == 'POST':
        gameid = request.form.get('gameid')
        nprice = request.form.get('nprice')
        if nprice is not None:
            nprice = float(nprice)
        if gameid and nprice:
            gamePrice(gameid, nprice)
            db.commit()
            cursor.close()
            return redirect('/')
        return render_template('gameprice.html')

#Rota para o Menu Users
@app.route('/usermenu', methods=["GET","POST"])
def usermenu():
    return render_template("usermenu.html")

#Rota para listar usuárioss e pesquisar por nome
@app.route('/users', methods=["GET","POST"])
def users():
    if request.method == "POST":
        user = request.form.get('sch')
        if not user:
            users = getUsers() 
            return render_template("tusers.html", dados=users)
        else:
            user = searchUser(user)
            return render_template("tusers.html", dados=user)

#Rota para adicionar usuário
@app.route('/adduser', methods=["POST"])
def addUser():
    cursor=db.cursor()
    if request.method == 'POST':
        nick = request.form.get('nickname')
        email = request.form.get('email')
        if nick and email:
            setUsers(nick, email)
            db.commit()
            cursor.close()
            return redirect('/')
        return render_template('adduser.html')

#Rota para remover usuário
@app.route('/removeuser', methods=["GET", "POST"])
def removeuser():
    cursor=db.cursor()
    if request.method == 'POST':
        userid = request.form.get('userid')
        if userid is not None:
            delUsers(userid)
            db.commit()
            cursor.close()
            return redirect('/')
        return render_template('removeuser.html')

#Rota para alterar nickname
@app.route('/changenickname', methods=["POST"])  #OK
def nNick():
    cursor=db.cursor()
    if request.method == 'POST':
        userid = request.form.get('userid')
        nnick = request.form.get('nnick')
        if userid and nnick:
            changeNickname(userid, nnick)
            db.commit()
            cursor.close()
            return redirect('/')
        return render_template('changenickname.html')

#Rota para alterar e-mail
@app.route('/changeemail', methods=["POST"])
def nEmail():
    cursor=db.cursor()
    if request.method == 'POST':
        userid = request.form.get('userid')
        nemail = request.form.get('nEmail')
        if userid and nemail:
            changeEmail(userid, nemail)
            db.commit()
            cursor.close()
            return redirect('/')
        return render_template('changeemail.html')

#Rota para o Menu Sales
@app.route('/salesmenu', methods=["GET","POST"])
def salesmenu():
    return render_template("salesmenu.html")

#Rota para adicionar venda
@app.route('/addsale', methods=["POST"])
def addSale():
    cursor=db.cursor()
    if request.method == 'POST':
        idUser = request.form.get('iduser')
        idGame = request.form.get('idGame')
        value = request.form.get('value')
        if value is not None:
            value = float(value)
        if idUser and idGame and value:
            setSales(idUser, idGame, value)
            db.commit()
            cursor.close()
            return redirect('/')
        return render_template('addsale.html')

#Rota para remover venda
@app.route('/removesale', methods=["GET", "POST"])
def removesale():
    cursor=db.cursor()
    if request.method == 'POST':
        saleid = request.form.get('saleid')
        if saleid is not None:
            delSale(saleid)
            db.commit()
            cursor.close()
            return redirect('/')
        return render_template('removesale.html')

#Rota para listar vendas e pesquisar por ID
@app.route('/sales', methods=["GET","POST"])
def sales():
    if request.method == "POST":
        sale = request.form.get('sch')
        if not sale:
            sales = getSales() 
            return render_template("tsales.html", dados=sales)
        else:
            sale=int(sale)
            sale = searchSale(sale)
            return render_template("tsales.html", dados=sale)

if __name__=="__main__":
    app.run(debug=True)
