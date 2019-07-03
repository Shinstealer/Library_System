DELETE FROM book_manager_category;

INSERT INTO book_manager_category(code, name) values('0', '総記');
INSERT INTO book_manager_category(code, name) values('1', '哲学');
INSERT INTO book_manager_category(code, name) values('2', '歴史');
INSERT INTO book_manager_category(code, name) values('3', '社会科学');
INSERT INTO book_manager_category(code, name) values('4', '自然科学');
INSERT INTO book_manager_category(code, name) values('5', '技術');
INSERT INTO book_manager_category(code, name) values('6', '産業');
INSERT INTO book_manager_category(code, name) values('7', '芸術');
INSERT INTO book_manager_category(code, name) values('8', '言語');
INSERT INTO book_manager_category(code, name) values('9', '文学');

DELETE FROM book_manager_status;

INSERT INTO book_manager_status(code, name) values(0, '貸出可');
INSERT INTO book_manager_status(code, name) values(1, '貸出中');
INSERT INTO book_manager_status(code, name) values(2, '確保中');
