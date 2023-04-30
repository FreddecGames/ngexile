SET SEARCH_PATH TO s03;

INSERT INTO s03.db_buildings VALUES (310, 80, 'send_energy_satellite', 'Satellite émetteur d''énergie', 'Ce satellite permet de créer un lien avec un satellite de réception d''une autre planète située dans la même galaxie et de lui envoyer de l''énergie.<br/>

Un satellite émetteur ne peut envoyer qu''un seul flux à la fois.', 120000, 80000, 0, 25000, 200, 0, 0, 1, 0, 0, 0, 0, 0, 100, 100000, true, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, false, true, 0, 0, 5, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, true, 0, false, 50, 0, true, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, true, 0, 0);

INSERT INTO s03.db_buildings VALUES (210, 80, 'receive_energy_satellite', 'Satellite de réception d''énergie', 'Ce satellite permet de recevoir un flux d''énergie provenant d''une autre planète située dans la même galaxie envoyé par un satellite émetteur.<br/>

L''énergie reçue est redirigée vers la rectenna et est ensuite utilisable par la colonie.', 9000, 6000, 0, 5000, 0, 0, 0, 1, 0, 0, 0, 0, 0, 200, 28000, true, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, false, false, 0, 0, 5, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, true, 0, false, 20, 0, true, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, true, 0, 0);

INSERT INTO s03.db_buildings_req_building VALUES (210, 207);
INSERT INTO s03.db_buildings_req_building VALUES (310, 207);
INSERT INTO s03.db_buildings_req_building VALUES (310, 302);
INSERT INTO s03.db_buildings_req_research VALUES (210, 420, 1);
INSERT INTO s03.db_buildings_req_research VALUES (310, 420, 1);
