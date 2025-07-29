-- ==============================================
-- SCRIPT DE SEED - SISTEMA CONCIERGE IA
-- Gerado automaticamente (fictício)
-- ==============================================

-- Limpeza opcional
-- DELETE FROM interactions;
-- DELETE FROM suggestions;
-- DELETE FROM transactions;
-- DELETE FROM profiles;
-- DELETE FROM users;

-- ==============================================
-- 1. USERS
-- ==============================================
INSERT INTO users (id,username,email,hashed_password,is_active,created_at,updated_at) VALUES
('3bf747e7-0ecb-4c5d-be3d-ba6c0f1f8745','carlos_santos','carlos.santos@email.com','$2b$12$hashseed',true,'2025-01-22 22:43:57','2025-06-29 21:48:55'),
('4f9a8adf-3039-4540-b2d3-81d59ae1a6fd','ana_silva','ana.silva@email.com','$2b$12$hashseed',true,'2025-01-15 15:49:18','2025-07-05 20:31:10'),
('5186e17d-565b-4a9a-b188-162cbb5141c8','pedro_oliveira','pedro.oliveira@email.com','$2b$12$hashseed',true,'2025-01-24 21:18:50','2025-07-19 11:01:52'),
('2768534b-6c39-48d1-a39e-2a4e694210be','juliana_costa','juliana.costa@email.com','$2b$12$hashseed',true,'2025-01-28 00:03:14','2025-07-01 18:24:13');
-- ==============================================
-- 2. PROFILES
-- ==============================================
INSERT INTO profiles (id, user_id, name, phone, birth_date, spouse_name, spouse_birth_date, preferences_json, created_at, updated_at) VALUES
('ad1f354e-9911-403b-b747-c163a84f9ed2', '3bf747e7-0ecb-4c5d-be3d-ba6c0f1f8745', 'Carlos Eduardo Santos', '(11) 99876-5432', '1985-03-15', 'Marina Santos', '1987-07-22',
'{"notifications": {"email": true, "push": true, "sms": false}, "suggestion_categories": {"anniversary": true, "purchase": true, "routine": true, "seasonal": true}, "quiet_hours": {"enabled": false, "start": "22:00", "end": "08:00"}, "suggestion_frequency": "high", "max_daily_suggestions": 7, "categories_of_interest": ["finance", "entertainment"], "preferred_times": {"morning": true, "afternoon": true, "evening": true, "night": true}}',
'2025-01-22 22:43:57', '2025-06-29 21:48:55'),
('b076969b-da3b-4374-8f80-63c6e335a3bc', '4f9a8adf-3039-4540-b2d3-81d59ae1a6fd', 'Ana Paula Silva', '(21) 98765-4321', '1990-11-08', 'Roberto Silva', '1988-12-03',
'{"notifications": {"email": true, "push": true, "sms": true}, "suggestion_categories": {"anniversary": true, "purchase": true, "routine": true, "seasonal": false}, "quiet_hours": {"enabled": true, "start": "22:00", "end": "08:00"}, "suggestion_frequency": "normal", "max_daily_suggestions": 5, "categories_of_interest": ["shopping", "food"], "preferred_times": {"morning": true, "afternoon": true, "evening": true, "night": false}}',
'2025-01-15 15:49:18', '2025-07-05 20:31:10'),
('e4aae7a5-15d2-4eaf-a5d5-7f1a6cc4e0c0', '5186e17d-565b-4a9a-b188-162cbb5141c8', 'Pedro Luis Oliveira', '(31) 97654-3210', '1982-06-20', NULL, NULL,
'{"notifications": {"email": true, "push": true, "sms": true}, "suggestion_categories": {"anniversary": true, "purchase": true, "routine": true, "seasonal": true}, "quiet_hours": {"enabled": false, "start": "22:00", "end": "08:00"}, "suggestion_frequency": "low", "max_daily_suggestions": 3, "categories_of_interest": ["health", "finance"], "preferred_times": {"morning": true, "afternoon": true, "evening": true, "night": false}}',
'2025-01-24 21:18:50', '2025-07-19 11:01:52'),
('9092d021-9671-4cdc-8a90-0c35b329540f', '2768534b-6c39-48d1-a39e-2a4e694210be', 'Juliana Rodrigues Costa', '(51) 96543-2109', '1986-09-14', 'Fernando Costa', '1984-02-28',
'{"notifications": {"email": true, "push": true, "sms": false}, "suggestion_categories": {"anniversary": true, "purchase": true, "routine": true, "seasonal": false}, "quiet_hours": {"enabled": false, "start": "22:00", "end": "08:00"}, "suggestion_frequency": "normal", "max_daily_suggestions": 5, "categories_of_interest": ["entertainment", "food"], "preferred_times": {"morning": true, "afternoon": true, "evening": true, "night": true}}',
'2025-01-28 00:03:14', '2025-07-01 18:24:13');
-- ==============================================
-- 3. TRANSACTIONS (exemplo das primeiras linhas)
-- ==============================================
INSERT INTO transactions (id, user_id, amount, category, description, date, recurring, recurrence_pattern, created_at, updated_at) VALUES
('f45b1809-8a48-40a9-8b5c-5fab913ee1eb', '3bf747e7-0ecb-4c5d-be3d-ba6c0f1f8745', 328.19, 'supermarket', 'Carrefour - Compras do mês', '2025-07-19 19:34:02', false, NULL, '2025-07-19 19:39:02', '2025-07-19 19:39:02'),
('3fd97509-f950-40f4-b346-642ef58f2e64', '3bf747e7-0ecb-4c5d-be3d-ba6c0f1f8745', 215.25, 'supermarket', 'Pão de Açúcar - Compras do mês', '2025-06-21 16:55:10', false, NULL, '2025-06-21 17:00:10', '2025-06-21 17:00:10'),
('e586d127-f93f-4a43-98e3-aa6f506b0901', '3bf747e7-0ecb-4c5d-be3d-ba6c0f1f8745', 182.74, 'supermarket', 'Extra - Compras do mês', '2025-05-24 15:13:11', false, NULL, '2025-05-24 15:18:11', '2025-05-24 15:18:11'),
('0d8e5b62-ab25-4835-84ea-0d505a2583c8', '3bf747e7-0ecb-4c5d-be3d-ba6c0f1f8745', 98.27, 'pharmacy', 'Drogasil - Medicamentos', '2025-05-10 12:53:07', false, NULL, '2025-05-10 12:58:07', '2025-05-10 12:58:07'),
('abbf4bd6-7c6d-4049-9e01-428b1734d29f', '3bf747e7-0ecb-4c5d-be3d-ba6c0f1f8745', 115.50, 'gas_station', 'Posto Ipiranga - Combustível', '2025-04-12 09:47:02', false, NULL, '2025-04-12 09:52:02', '2025-04-12 09:52:02'),
('9be01259-c1e7-4b90-90d6-bc09e680d24c', '3bf747e7-0ecb-4c5d-be3d-ba6c0f1f8745', 240.75, 'restaurant', 'La Bella Italia - Aniversário', '2025-07-22 19:00:00', false, NULL, '2025-07-22 19:05:00', '2025-07-22 19:05:00'),
-- (Mais de 200 linhas semelhantes distribuídas para todos os usuários e meses)
;
-- Bloco cont. TRANSACTIONS (variação de categorias e usuários)
INSERT INTO transactions (id, user_id, amount, category, description, date, recurring, recurrence_pattern, created_at, updated_at) VALUES
('b2eb8d8c-ba62-48ef-9180-1c130669a245', '4f9a8adf-3039-4540-b2d3-81d59ae1a6fd', 183.49, 'supermarket', 'Assaí Atacadista - Compras do mês', '2025-07-15 18:46:55', false, NULL, '2025-07-15 18:51:55', '2025-07-15 18:51:55'),
('33eeae01-39ad-44be-bbd0-37a251f63aec', '5186e17d-565b-4a9a-b188-162cbb5141c8', 340.21, 'supermarket', 'Walmart - Compras do mês', '2025-06-20 15:20:11', false, NULL, '2025-06-20 15:25:11', '2025-06-20 15:25:11'),
('ecc4ea9e-8a04-4962-a6d0-f1b5fde7e76e', '2768534b-6c39-48d1-a39e-2a4e694210be', 98.00, 'pharmacy', 'Raia - Medicamentos e produtos', '2025-06-08 10:22:00', false, NULL, '2025-06-08 10:27:00', '2025-06-08 10:27:00'),
('5f4a2b2e-2103-45e3-9959-a260a7d6afea', '3bf747e7-0ecb-4c5d-be3d-ba6c0f1f8745', 125.37, 'gas_station', 'Shell Select - Combustível', '2025-05-21 15:43:32', false, NULL, '2025-05-21 15:48:32', '2025-05-21 15:48:32'),
('9bc388d1-4fae-4810-8617-3160c369f8e4', '4f9a8adf-3039-4540-b2d3-81d59ae1a6fd', 265.00, 'restaurant', 'Sushi House - Jantar especial', '2025-05-02 20:30:00', false, NULL, '2025-05-02 20:35:00', '2025-05-02 20:35:00'),
('73019552-bad2-4cff-b4c9-1d2fb23dff7f', '5186e17d-565b-4a9a-b188-162cbb5141c8', 84.75, 'flowers', 'Floricultura Bela Vista - Buquê de rosas', '2025-07-20 09:15:00', false, NULL, '2025-07-20 09:20:00', '2025-07-20 09:20:00'),
('2158f029-7b0b-4f11-bf27-743d70571683', '3bf747e7-0ecb-4c5d-be3d-ba6c0f1f8745', 540.20, 'gifts', 'Magazine Luiza - Presente aniversário', '2025-07-21 15:17:00', false, NULL, '2025-07-21 15:22:00', '2025-07-21 15:22:00'),
('7434d175-a376-4dbb-ab00-2b97922e2cd9', '2768534b-6c39-48d1-a39e-2a4e694210be', 120.00, 'subscription', 'Spotify – Assinatura mensal', '2025-04-02 09:00:00', true, 'monthly', '2025-04-02 09:05:00', '2025-04-02 09:05:00'),
('4e97f5ec-2673-439c-b34e-9099051a8106', 'b076969b-da3b-4374-8f80-63c6e335a3bc', 175.42, 'supermarket', 'Big Bompreço - Compras do mês', '2025-03-15 15:15:10', false, NULL, '2025-03-15 15:20:10', '2025-03-15 15:20:10'),
('4d060a2f-06a9-44d9-9537-b3a2048633c4', 'e4aae7a5-15d2-4eaf-a5d5-7f1a6cc4e0c0', 205.00, 'restaurant', 'Villa Toscana - Jantar especial', '2025-07-04 20:00:00', false, NULL, '2025-07-04 20:05:00', '2025-07-04 20:05:00');
-- ==============================================
-- 4. SUGGESTIONS
-- ==============================================
INSERT INTO suggestions (id, user_id, type, content, category, priority, status, scheduled_date, metadata_json, transaction_id, created_at, updated_at) VALUES
('a5601d16-2bb6-4abe-b17d-43d169b746fd', '3bf747e7-0ecb-4c5d-be3d-ba6c0f1f8745', 'anniversary',
'Vi que 22/07 é aniversário de Marina Santos. Deseja reservar o La Bella Italia?', 'restaurant', 'high', 'pending', '2025-07-15',
'{"establishment": "La Bella Italia", "confidence_score": 0.95, "reasoning": "Padrão: restaurante italiano em aniversários"}',
NULL, '2025-07-05 10:00:00', '2025-07-05 10:01:00'),

('b6704e26-7b69-4fee-8353-ad1bc6028fb4', '3bf747e7-0ecb-4c5d-be3d-ba6c0f1f8745', 'purchase',
'Você costuma enviar flores. Posso providenciar um buquê?', 'flowers', 'medium', 'pending', '2025-07-17',
'{"product": "Buquê de rosas vermelhas", "confidence_score": 0.88, "reasoning": "Flores enviadas nos últimos aniversários"}',
NULL, '2025-07-05 10:10:00', '2025-07-05 10:11:00'),

('6d976b0f-e00e-42bb-ab15-9556b884b7e2', '3bf747e7-0ecb-4c5d-be3d-ba6c0f1f8745', 'routine',
'01/08 é a primeira sexta. Reservo sua mesa no Sushi House?', 'restaurant', 'medium', 'pending', '2025-07-29',
'{"establishment": "Sushi House", "confidence_score": 0.82, "reasoning": "Jantar na primeira sexta do mês"}',
NULL, '2025-07-05 10:12:00', '2025-07-05 10:13:00'),

('b11022b7-1e70-4af7-b3f4-9ab055b12462', '4f9a8adf-3039-4540-b2d3-81d59ae1a6fd', 'anniversary',
'Vi que 03/12 é aniversário de Roberto Silva. Deseja reservar o La Bella Italia?', 'restaurant', 'high', 'pending', '2025-11-26',
'{"establishment": "La Bella Italia", "confidence_score": 0.95, "reasoning": "Padrão: restaurante italiano em aniversários"}',
NULL, '2025-11-15 09:00:00', '2025-11-15 09:02:00'),

('ec93171e-2c0e-43ea-b595-cc55c8ff272c', '4f9a8adf-3039-4540-b2d3-81d59ae1a6fd', 'purchase',
'Você costuma enviar flores para Roberto Silva. Posso providenciar um buquê?', 'flowers', 'medium', 'pending', '2025-11-28',
'{"product": "Buquê de rosas vermelhas", "confidence_score": 0.87, "reasoning": "Flores enviadas nos últimos aniversários"}',
NULL, '2025-11-15 09:10:00', '2025-11-15 09:11:00'),

('bda67ed8-9a2c-4486-855e-c50b9cd23e56', '4f9a8adf-3039-4540-b2d3-81d59ae1a6fd', 'routine',
'05/09 é a primeira sexta. Reservo sua mesa no Sushi House?', 'restaurant', 'medium', 'pending', '2025-09-02',
'{"establishment": "Sushi House", "confidence_score": 0.83, "reasoning": "Jantar na primeira sexta do mês"}',
NULL, '2025-09-01 09:15:00', '2025-09-01 09:16:00')

-- (segue no mesmo padrão para outros usuários e datas especiais)
;
