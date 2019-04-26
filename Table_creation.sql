----
-- phpLiteAdmin database dump (http://www.phpliteadmin.org/)
-- phpLiteAdmin version: 1.9.7.1
-- Exported: 6:33am on April 26, 2019 (UTC)
-- database file: /home/ubuntu/workspace/pset7/finance/finance.db
----
BEGIN TRANSACTION;

----
-- Table structure for users
----
CREATE TABLE 'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' TEXT NOT NULL, 'hash' TEXT NOT NULL, 'cash' NUMERIC NOT NULL DEFAULT 10000.00 , 'email' varchar(20));

----
-- Data dump for users, a total of 9 rows
----
INSERT INTO "users" ("id","username","hash","cash","email") VALUES ('1','skfist','pbkdf2:sha256:50000$VworTddV$415dd083ca830cb3146bd15d3f933e4915d6250e189a4b356989000d2702bdbf','9988.0391',NULL);
INSERT INTO "users" ("id","username","hash","cash","email") VALUES ('2','skfist1','pbkdf2:sha256:50000$bM8c5hjb$a84b8760fcea5ce7833d42d867747fe3742bddd8f566ccc7d0211b5cb0ca207c','10000',NULL);
INSERT INTO "users" ("id","username","hash","cash","email") VALUES ('3','skfist2','pbkdf2:sha256:50000$GQM7FPMz$84de1989c17c0756058c92d0aecbac12a20a3adc5c45e1d3c61137d976d477c1','10000',NULL);
INSERT INTO "users" ("id","username","hash","cash","email") VALUES ('4','skfist3','pbkdf2:sha256:50000$KTK138qf$8cc78dae306671fb32709d4183bb30c55364130f3e3e45a28eba732b294b1e8f','10000',NULL);
INSERT INTO "users" ("id","username","hash","cash","email") VALUES ('5','HelloTry','pbkdf2:sha256:50000$hiiB1QFf$bc7d5163962eea221168d903fb3c6b906b6f048e1539a6fd284f658c463b8a21','6349.715','ap37@iitbbs.ac.in');
INSERT INTO "users" ("id","username","hash","cash","email") VALUES ('6','HelloTry2','pbkdf2:sha256:50000$lXi87sHY$35219b239f4847d11439fa82662f42ac3853b8142815704f3e4a2b830ae7743a','10000','aditi525@gmail.com');
INSERT INTO "users" ("id","username","hash","cash","email") VALUES ('7','Ok','pbkdf2:sha256:50000$QuH3cz7v$10546c08fe15e09c9cce4f725ce0b9ae28cec2b6a711e1ca39ce0f21b99082c1','9669.76','sa26@iitbbs.ac.in');
INSERT INTO "users" ("id","username","hash","cash","email") VALUES ('8','Ab','pbkdf2:sha256:50000$h5g2P9qg$11b4efe52a49f674b943d297144503a93a52edb9ea52c370ae6bf2c4d9156a59','9999.93','Cd');
INSERT INTO "users" ("id","username","hash","cash","email") VALUES ('9','a','pbkdf2:sha256:50000$XyneKGHK$1b4aedf4991f17e4f732ac88bd2b8db5d3d1ddf21c4729e9175c84257a898c0d','6559.06','adityapal.nghss@gmail.com');

----
-- Table structure for transactions
----
CREATE TABLE 'transactions' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'user_id' INTEGER NOT NULL, 'symbol' TEXT NOT NULL, 'shares' INTEGER NOT NULL, 'price_per_share' REAL NOT NULL, 'created_at'  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP  );

----
-- Data dump for transactions, a total of 38 rows
----
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('2','1','EURUSD','10','1.196','2018-05-03 15:24:52');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('3','1','EURUSD','-1','1.1989','2018-05-03 20:12:05');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('4','1','EURUSD','11','1.1988','2018-05-03 20:46:31');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('5','1','EURUSD','-10','1.1987','2018-05-03 20:51:23');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('6','5','MSFT','8','116.96','2019-03-18 14:06:57');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('7','5','MSFT','-3','116.94','2019-03-18 14:07:45');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('8','5','NFLX','2','358.14','2019-03-20 14:00:06');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('9','5','AAPL','2','194.62','2019-03-21 17:14:28');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('10','5','AAPL','-1','195.91','2019-03-21 18:07:05');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('11','5','AAPL','2','195.91','2019-03-21 18:07:25');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('12','5','MSFT','1','119.0','2019-03-21 18:09:18');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('13','5','MSFT','2','119.065','2019-03-21 18:14:58');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('14','5','AMZN','2','1818.4','2019-03-22 04:48:17');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('15','5','AMZN','-1','1818.89','2019-03-22 05:00:39');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('16','5','MSFT','-3','120.64','2019-03-22 05:04:24');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('17','5','AAPL','-1','195.01','2019-03-22 05:09:49');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('18','5','NFLX','-1','377.92','2019-03-22 06:14:35');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('19','5','MSFT','1','120.64','2019-03-22 13:24:04');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('20','5','MSFT','-1','120.62','2019-03-22 13:25:33');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('21','5','MSFT','-1','120.64','2019-03-22 13:26:16');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('22','5','FB','2','166.74','2019-03-22 14:39:58');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('23','5','NFLX','1','366.315','2019-03-22 15:27:12');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('24','5','FB','1','165.51','2019-03-22 15:32:04');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('25','7','FB','2','165.12','2019-03-22 15:37:28');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('26','8','Nflx','1','361.02','2019-03-24 16:05:38');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('27','8','Nflx','-1','360.95','2019-03-24 16:06:22');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('28','5','MSFT','1','119.74','2019-04-05 18:01:02');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('29','5','MSFT','1','119.88','2019-04-07 14:30:21');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('30','9','MSFT','2','119.88','2019-04-08 04:33:04');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('31','9','AAPL','2','197.01','2019-04-08 04:34:45');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('32','9','FB','1','175.7','2019-04-08 04:34:59');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('33','9','NFLX','6','365.47','2019-04-08 04:40:09');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('34','9','AAPL','-1','197.01','2019-04-08 04:43:26');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('35','9','AAPL','1','198.95','2019-04-12 04:11:16');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('36','9','FB','1','178.32','2019-04-20 17:14:43');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('38','9','AAPL','1','203.86','2019-04-21 19:23:49');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('39','9','AAPL','-1','203.86','2019-04-21 19:24:17');
INSERT INTO "transactions" ("id","user_id","symbol","shares","price_per_share","created_at") VALUES ('40','9','AAPL','1','203.86','2019-04-22 03:57:52');

----
-- Table structure for friends
----
CREATE TABLE friends (uid INTEGER PRIMARY KEY, f1 INTEGER, f2 INTEGER, f3 INTEGER, f4 INTEGER, f5 INTEGER);

----
-- Data dump for friends, a total of 2 rows
----
INSERT INTO "friends" ("uid","f1","f2","f3","f4","f5") VALUES ('5','3','2','4','1','6');
INSERT INTO "friends" ("uid","f1","f2","f3","f4","f5") VALUES ('9',NULL,'5',NULL,NULL,NULL);

----
-- Table structure for predictions
----
CREATE TABLE 'predictions' ('symbol' varchar(10) PRIMARY KEY NOT NULL,'price' real);

----
-- Data dump for predictions, a total of 5 rows
----
INSERT INTO "predictions" ("symbol","price") VALUES ('EURUSD','1.125');
INSERT INTO "predictions" ("symbol","price") VALUES ('MSFT','120.3');
INSERT INTO "predictions" ("symbol","price") VALUES ('NFLX','347.4');
INSERT INTO "predictions" ("symbol","price") VALUES ('AAPL','198.9');
INSERT INTO "predictions" ("symbol","price") VALUES ('AMZN','1844.0');

----
-- Table structure for advertisement
----
CREATE TABLE 'advertisement' ('symbol' varchar(10) PRIMARY KEY NOT NULL, 'imagesource' varchar(25), 'alttext' varchar(25), 'description' varchar(1000), 'link' varchar(100), 'priority' integer, 'duration' integer, 'created'  datetime DEFAULT CURRENT_TIMESTAMP  );

----
-- Data dump for advertisement, a total of 9 rows
----
INSERT INTO "advertisement" ("symbol","imagesource","alttext","description","link","priority","duration","created") VALUES ('NFLX','/static/images/NFLX.png','Netflix','Netflix, Inc. is an American media-services provider headquartered in Los Gatos, California, founded in 1997 by Reed Hastings and Marc Randolph in Scotts Valley, California. The company''s primary business is its subscription-based streaming OTT service which offers online streaming of a library of films and television programs, including those produced in-house.','https://www.netflix.com/in/','5','10','2019-03-21 12:46:15');
INSERT INTO "advertisement" ("symbol","imagesource","alttext","description","link","priority","duration","created") VALUES ('MSFT','/static/images/msft.jpg','Microsoft','Microsoft Corporation is an American multinational technology company with headquarters in Redmond, Washington. It develops, manufactures, licenses, supports and sells computer software, consumer electronics, personal computers, and related services.','https://www.microsoft.com/en-in/','5','1','2019-03-21 14:54:40');
INSERT INTO "advertisement" ("symbol","imagesource","alttext","description","link","priority","duration","created") VALUES ('AAPL','/static/images/apple.jpg','Apple','Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services. It is considered one of the Big Four of technology along with Amazon, Google, and Facebook','https://www.apple.com/in/','5','6','2019-03-21 16:39:26');
INSERT INTO "advertisement" ("symbol","imagesource","alttext","description","link","priority","duration","created") VALUES ('FB','/static/images/fb.png','Facebook','Facebook, Inc. is an American online social media and social networking service company. It is based in Menlo Park, California. It was founded by Mark Zuckerberg, along with fellow Harvard College students and roommates Eduardo Saverin, Andrew McCollum, Dustin Moskovitz and Chris Hughes. It is considered one of the Big Four technology companies along with Amazon, Apple, and Google.','www.facebook.com','6','8','2019-04-08 04:56:00');
INSERT INTO "advertisement" ("symbol","imagesource","alttext","description","link","priority","duration","created") VALUES ('AMZN','/static/images/amzn.png','Amazon','Amazon is the largest e-commerce marketplace and cloud computing platform in the world as measured by revenue and market capitalization.[7] Amazon.com was founded by Jeff Bezos on July 5, 1994, and started as an online bookstore but later diversified to sell video downloads/streaming, MP3 downloads/streaming, audiobook downloads/streaming, software, video games, electronics, apparel, furniture, food, toys, and jewelry.','www.amazon.com','10','4','2019-04-08 05:02:28');
INSERT INTO "advertisement" ("symbol","imagesource","alttext","description","link","priority","duration","created") VALUES ('GOOGL','/static/images/googl.png','Google','Google LLC[5] is an American multinational technology company that specializes in Internet-related services and products, which include online advertising technologies, search engine, cloud computing, software, and hardware. It is considered one of the Big Four technology companies, alongside Amazon, Apple and Facebook.The company''s rapid growth since incorporation has triggered a chain of products, acquisitions, and partnerships beyond Google''s core search engine (Google Search). It offers services designed for work and productivity (Google Docs, Google Sheets, and Google Slides), email (Gmail/Inbox), scheduling and time management (Google Calendar), cloud storage (Google Drive), instant messaging and video chat (Google Allo, Duo, Hangouts), language translation (Google Translate), mapping and navigation (Google Maps, Waze, Google Earth, Street View), video sharing (YouTube), note-taking (Google Keep), and photo organizing and editing (Google Photos). The company leads the development of the Android mobile operating system, the Google Chrome web browser, and Chrome OS, a lightweight operating system based on the Chrome browser.','www.google.com','9','34','2019-04-08 05:14:22');
INSERT INTO "advertisement" ("symbol","imagesource","alttext","description","link","priority","duration","created") VALUES ('ADBE','/static/images/adbe.png','Adobe','Adobe Inc. (/əˈdoʊbiː/ ə-DOH-bee) is an American multinational computer software company headquartered in San Jose, California. It has historically focused upon the creation of multimedia and creativity software products, with a more recent foray towards digital marketing software. Adobe is best known for its deprecated Adobe Flash web software ecosystem, Photoshop image editing software, Acrobat Reader, the Portable Document Format (PDF), and Adobe Creative Suite, as well as its successor Adobe Creative Cloud.','www.adobe.com','8','4','2019-04-08 05:28:17');
INSERT INTO "advertisement" ("symbol","imagesource","alttext","description","link","priority","duration","created") VALUES ('ORCL','/static/images/orcl.jpg','Oracle','Oracle Corporation is an American multinational computer technology corporation headquartered in Redwood Shores, California. The company specializes primarily in developing and marketing database software and technology, cloud engineered systems, and enterprise software products — particularly its own brands of database management systems. In 2018, Oracle was the third-largest software maker by revenue, after Microsoft and Alphabet.','www.oracle.com','4','8','2019-04-08 05:32:51');
INSERT INTO "advertisement" ("symbol","imagesource","alttext","description","link","priority","duration","created") VALUES ('ACN','/static/images/acn.png','Accenture','Accenture is a global management consulting and professional services firm that provides strategy, consulting, digital, technology and operations services. A Fortune Global 500 company,[5] it has been incorporated in Dublin, Ireland, since 1 September 2009. In 2018, the company reported net revenues of $39.6 billion, with more than 459,000 employees[3] serving clients in more than 200 cities in 120 countries.[6] In 2015, the company had about 150,000 employees in India,[7] about 48,000 in the US,[8] and about 50,000 in the Philippines','www.accenture.com','5','7','2019-04-08 05:37:20');

----
-- structure for index username on table users
----
CREATE UNIQUE INDEX 'username' ON "users" ("username");

----
-- structure for index idx_user_id_and_symbol on table transactions
----
CREATE INDEX 'idx_user_id_and_symbol' ON "transactions" ("user_id" ASC, "symbol" ASC);

----
-- structure for index sqlite_autoindex_predictions_1 on table predictions
----
;

----
-- structure for index sqlite_autoindex_advertisement_1 on table advertisement
----
;
COMMIT;
