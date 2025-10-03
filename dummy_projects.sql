INSERT INTO Projects (project_id, project_name) VALUES (1, 'Yksinäisyyden linnake');
INSERT INTO Projects (project_id, project_name) VALUES (2, 'Lepakkoluola');
INSERT INTO Projects (project_id, project_name) VALUES (3, 'Megacity One');
INSERT INTO Projects (project_id, project_name) VALUES (4, 'Baxter Tower');
INSERT INTO Projects (project_id, project_name) VALUES (5, 'Stark Tower');
INSERT INTO Projects (project_id, project_name) VALUES (6, 'Kostajien avaruusasema');
INSERT INTO Projects (project_id, project_name) VALUES (7, 'Sanctum Sanctorum');
INSERT INTO Projects (project_id, project_name) VALUES (8, 'The Fulcrum');
INSERT INTO Projects (project_id, project_name) VALUES (9, 'East-Meg One');
INSERT INTO Projects (project_id, project_name) VALUES (10, 'Daily Planet Building');

INSERT INTO Project_definitions (project_id, title, value) VALUES (1, 'Projektityyppi', 'Korjaus');
INSERT INTO Project_definitions (project_id, title, value) VALUES (1, 'Poistomenetelmä', 'Tasapoisto 30 vuotta');

INSERT INTO Project_definitions (project_id, title, value) VALUES (2, 'Projektityyppi', 'Uudisrakennus');
INSERT INTO Project_definitions (project_id, title, value) VALUES (2, 'Poistomenetelmä', 'Tasapoisto 10 vuotta');

INSERT INTO Project_definitions (project_id, title, value) VALUES (3, 'Projektityyppi', 'Muutostyö');
INSERT INTO Project_definitions (project_id, title, value) VALUES (3, 'Poistomenetelmä', 'Menojäännös 20 %');

INSERT INTO Project_definitions (project_id, title, value) VALUES (4, 'Projektityyppi', 'Korjaus');
INSERT INTO Project_definitions (project_id, title, value) VALUES (4, 'Poistomenetelmä', 'Tasapoisto 10 vuotta');

INSERT INTO Project_definitions (project_id, title, value) VALUES (5, 'Projektityyppi', 'Uudisrakennus');
INSERT INTO Project_definitions (project_id, title, value) VALUES (5, 'Poistomenetelmä', 'Menojäännös 20 %');

INSERT INTO Project_definitions (project_id, title, value) VALUES (6, 'Projektityyppi', 'Muutostyö');
INSERT INTO Project_definitions (project_id, title, value) VALUES (6, 'Poistomenetelmä', 'Tasapoisto 30 vuotta');

INSERT INTO Project_definitions (project_id, title, value) VALUES (7, 'Projektityyppi', 'Korjaus');
INSERT INTO Project_definitions (project_id, title, value) VALUES (7, 'Poistomenetelmä', 'Tasapoisto 10 vuotta');

INSERT INTO Project_definitions (project_id, title, value) VALUES (8, 'Projektityyppi', 'Uudisrakennus');
INSERT INTO Project_definitions (project_id, title, value) VALUES (8, 'Poistomenetelmä', 'Tasapoisto 30 vuotta');

INSERT INTO Project_definitions (project_id, title, value) VALUES (9, 'Projektityyppi', 'Muutostyö');
INSERT INTO Project_definitions (project_id, title, value) VALUES (9, 'Poistomenetelmä', 'Menojäännös 20 %');

INSERT INTO Project_definitions (project_id, title, value) VALUES (10, 'Projektityyppi', 'Muutostyö');
INSERT INTO Project_definitions (project_id, title, value) VALUES (10, 'Poistomenetelmä', 'Menojäännös 20 %');

INSERT INTO Inserted (inserting_user, project_id, inserted_at) 
VALUES (1, 1, '2025-09-21 23:59:59');

INSERT INTO Inserted (inserting_user, project_id, inserted_at) 
VALUES (1, 2, '2025-09-21 23:59:59');

INSERT INTO Inserted (inserting_user, project_id, inserted_at) 
VALUES (1, 3, '2025-09-21 23:59:59');

INSERT INTO Inserted (inserting_user, project_id, inserted_at) 
VALUES (1, 4, '2025-09-21 23:59:59');

INSERT INTO Inserted (inserting_user, project_id, inserted_at) 
VALUES (1, 5, '2025-09-21 23:59:59');

INSERT INTO Inserted (inserting_user, project_id, inserted_at) 
VALUES (1, 6, '2025-09-21 23:59:59');

INSERT INTO Inserted (inserting_user, project_id, inserted_at) 
VALUES (1, 7, '2025-09-21 23:59:59');

INSERT INTO Inserted (inserting_user, project_id, inserted_at) 
VALUES (1, 8, '2025-09-21 23:59:59');

INSERT INTO Inserted (inserting_user, project_id, inserted_at) 
VALUES (1, 9, '2025-09-21 23:59:59');

INSERT INTO Inserted (inserting_user, project_id, inserted_at) 
VALUES (1, 10, '2025-09-21 23:59:59');

INSERT INTO ProjectPermissions (project_id, user_id, can_modify, granted_by) VALUES (1, 1, 1, 1);
INSERT INTO ProjectPermissions (project_id, user_id, can_modify, granted_by) VALUES (2, 1, 1, 1);
INSERT INTO ProjectPermissions (project_id, user_id, can_modify, granted_by) VALUES (3, 1, 1, 1);
INSERT INTO ProjectPermissions (project_id, user_id, can_modify, granted_by) VALUES (4, 1, 1, 1);
INSERT INTO ProjectPermissions (project_id, user_id, can_modify, granted_by) VALUES (5, 1, 1, 1);
INSERT INTO ProjectPermissions (project_id, user_id, can_modify, granted_by) VALUES (6, 1, 1, 1);
INSERT INTO ProjectPermissions (project_id, user_id, can_modify, granted_by) VALUES (7, 1, 1, 1);
INSERT INTO ProjectPermissions (project_id, user_id, can_modify, granted_by) VALUES (8, 1, 1, 1);
INSERT INTO ProjectPermissions (project_id, user_id, can_modify, granted_by) VALUES (9, 1, 1, 1);
INSERT INTO ProjectPermissions (project_id, user_id, can_modify, granted_by) VALUES (10, 1, 1, 1);