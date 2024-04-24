CREATE DATABASE maets_store;
USE maets_store;

CREATE TABLE Games
(
    gameId INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) UNIQUE NOT NULL,
    mainGenre VARCHAR(100) NOT NULL,
    price FLOAT(10, 2) UNSIGNED NOT NULL DEFAULT 0
);

DELIMITER //

CREATE PROCEDURE GameAdd(IN pTitle VARCHAR(255), IN pGenre VARCHAR(100), IN pPrice FLOAT(10, 2))
BEGIN
    INSERT INTO Games(title, mainGenre, price) 
    VALUES(pTitle, pGenre, pPrice);
END//

CREATE PROCEDURE GamePriceChange(IN pGameId INT, IN pPrice FLOAT(10, 2))
BEGIN
    UPDATE Games
    SET price = pPrice
    WHERE gameId = pGameId;
END//

CREATE PROCEDURE GameRemove(IN pGameId INT)
BEGIN
    DELETE FROM Games
    WHERE gameId = pGameId;
END//

CREATE PROCEDURE GameNameSearch(IN pTitle VARCHAR(255))
BEGIN
    SELECT * FROM Games
    WHERE title LIKE CONCAT('%', pTitle ,'%');
END//

CREATE PROCEDURE GameList()
BEGIN
    SELECT * FROM Games;
END//

DELIMITER ;

CREATE TABLE Users
(
    userId INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nickname VARCHAR(30) UNIQUE NOT NULL DEFAULT 'Player',
    email VARCHAR(100) UNIQUE NOT NULL,
    registerDate DATE NOT NULL
);

DELIMITER //

CREATE PROCEDURE UserAdd(IN pNickname VARCHAR(255), IN pEmail VARCHAR(100))
BEGIN
    INSERT INTO Users(nickname, email, registerDate)
    VALUES(pNickname, pEmail, CURDATE());
END//

CREATE PROCEDURE UserRemove(IN pUserId INT)
BEGIN
    DELETE FROM Users
    WHERE userId = pUserId;
END//

CREATE PROCEDURE UserList()
BEGIN
    SELECT * FROM Users;
END//

CREATE PROCEDURE UserSearch(IN pNickname VARCHAR(255))
BEGIN
    SELECT * FROM Users
    WHERE nickname LIKE CONCAT('%', pNickname, '%');
END//

CREATE PROCEDURE ChangeEmail(IN pUserId INT, IN pEmail VARCHAR(100))
BEGIN
    UPDATE Users
    SET email = pEmail
    WHERE userId = pUserId;
END//

CREATE PROCEDURE ChangeNick(IN pUserId INT, IN pNickname VARCHAR(255))
BEGIN
    UPDATE Users
    SET nickname = pNickname
    WHERE userId = pUserId;
END//

DELIMITER ;

CREATE TABLE Sales
(
    saleId INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    idUser INT UNSIGNED NOT NULL,
    idGame INT UNSIGNED NOT NULL,
    FOREIGN KEY (idUser) REFERENCES Users(userId),
    FOREIGN KEY (idGame) REFERENCES Games(gameId),
    sellDate DATE NOT NULL,
    totalValue FLOAT(10, 2) UNSIGNED NOT NULL
);

DELIMITER //

CREATE PROCEDURE SaleAdd(IN pIdUser INT, IN pIdGame INT)
BEGIN
    SET @tPrice = (SELECT price FROM Games WHERE gameId = pIdGame);
    INSERT INTO Sales(idUser, idGame, sellDate, totalValue)
    VALUES(pIdUser, pIdGame, CURDATE(), @tPrice);
END//

CREATE PROCEDURE SaleSearch(IN pSaleId INT)
BEGIN
    SELECT * FROM Sales
    WHERE saleId = pSaleId;
END//

CREATE PROCEDURE SaleList()
BEGIN
    SELECT * FROM Sales;
END//

DELIMITER ;

-- Adicionando os jogos à tabela Games
CALL GameAdd('CS:GO', 'Ação', 29.99);
CALL GameAdd('Terraria', 'Aventura', 39.99);
CALL GameAdd('Age Of Empires', 'Estratégia', 19.99);
CALL GameAdd('Goat Simulator', 'Simulação', 49.99);
CALL GameAdd('The Witcher', 'RPG', 59.99);

-- Adicionando os usuários à tabela Users
CALL UserAdd('limaozinho', 'limonada@gmail.com');
CALL UserAdd('cabeçao', 'bighead@gmail.com');
CALL UserAdd('Noobmaster69', 'noob69@gmail.com');
CALL UserAdd('jesus_take_the_wheel', 'jesus@gmail.com');
CALL UserAdd('Mike_Drunkbeater', 'mike@gmail.com');

-- Adicionando vendas à tabela Sales
CALL SaleAdd(1, 1);  
CALL SaleAdd(2, 2);  
CALL SaleAdd(3, 3);  
CALL SaleAdd(4, 4);  
CALL SaleAdd(5, 5);
