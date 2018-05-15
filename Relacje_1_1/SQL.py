"""
ALTER TABLE CLIENT ADD PRIMARY KEY(id);

CREATE TABLE UserAddress(
	client_id int,
	city varchar(255),
	street varchar(255),
	house_nr varchar(255),
	PRIMARY KEY (client_id),
	FOREIGN KEY (client_id)
	REFERENCES client(id)
);

INSERT INTO UserAddress(client_id, city, street, house_nr)
VALUES (1, 'Pruszków', 'Ciemna', '667'),
(2, 'Warszawa', 'Obozowa', '231'),
(3, 'Piaseczno', 'Żeromskiego', '301');

SELECT * FROM client
JOIN UserAddress ON client.id = UserAddress.client_id;

SELECT * FROM client
LEFT JOIN UserAddress ON client.id = UserAddress.client_id;
"""