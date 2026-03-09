SELECT * FROM "usertable";
DROP TABLE users;

CREATE TABLE cultivation_guidelines (
    id SERIAL PRIMARY KEY, 
	cultivation_size VARCHAR(20),
    climate_type VARCHAR(20),              
    activity VARCHAR(100),      
    notes TEXT,                
    image_url VARCHAR(255)      
);
INSERT INTO cultivation_guidelines (climate_type, cultivation_size, activity, notes, image_url) VALUES
('wet','small','Seed Selection','Local Wet, Black Beauty; fresh and disease-free','images/guideline/seeds.jpg'),
('wet','medium','Seed Selection','Local Wet, Black Beauty; fresh and disease-free','images/guideline/seeds.jpg'),

('wet','small','Seed Treatment','Soak 12-24 hrs; use fungicide or neem extract','images/guideline/seeds.jpg'),
('wet','medium','Seed Treatment','Soak 12-24 hrs; use fungicide or neem extract','images/guideline/seeds.jpg'),

('wet','small','Nursery Preparation','Well-drained soil; mix topsoil, compost, sand (2:1:1)','images/guideline/Nursery Preparation.jpg'),
('wet','medium','Nursery Preparation','Well-drained soil; mix topsoil, compost, sand (2:1:1)','images/guideline/Nursery Preparation.jpg'),

('wet','small','Sowing','0.5-1 cm deep; germination 7-14 days; faster due to humidity','images/guideline/Nursery Preparation.jpg'),
('wet','medium','Sowing','0.5-1 cm deep; germination 7-14 days; faster due to humidity','images/guideline/Nursery Preparation.jpg');

INSERT INTO cultivation_guidelines (climate_type, cultivation_size, activity, notes, image_url) VALUES
('wet','small','Pruning','Remove lower leaves and weak branches','images/guideline/Pruning.jpg'),
('wet','medium','Pruning','Remove lower leaves and weak branches','images/guideline/Pruning.jpg'),

('wet','small','Disease Management','Bacterial wilt, leaf spot; crop rotation and proper spacing','images/guideline/disease_management.jpg'),
('wet','medium','Disease Management','Bacterial wilt, leaf spot; crop rotation and proper spacing','images/guideline/disease_management.jpg'),



('wet','small','Flowering','Occurs 4–6 weeks after transplanting','images/guideline/flowers.jpg'),
('wet','medium','Flowering','Occurs 4–6 weeks after transplanting','images/guideline/flowers.jpg'),

('wet','small','Pollination','Mostly self-pollinated; bees improve yield','images/guideline/Pollination.jpg'),
('wet','medium','Pollination','Mostly self-pollinated; bees improve yield','images/guideline/Pollination.jpg'),

('wet','small','Harvesting','60–90 days after planting; harvest early for tenderness','images/guideline/Harvesting.jpg'),
('wet','medium','Harvesting','60–90 days after planting; harvest early for tenderness','images/guideline/Harvesting.jpg'),

('wet','small','Post-Harvest Handling','Store in cool shaded area; handle gently','images/guideline/Post-Harvest_Handling.jpg'),
('wet','medium','Post-Harvest Handling','Store in cool shaded area; handle gently','images/guideline/Post-Harvest_Handling.jpg');

INSERT INTO cultivation_guidelines (climate_type, cultivation_size, activity, notes, image_url) VALUES
('dry','small','Seed Selection','Dwarf Hybrid, Violet Long; heat tolerant varieties','images/guideline/seeds.jpg'),
('dry','medium','Seed Selection','Dwarf Hybrid, Violet Long; heat tolerant varieties','images/guideline/seeds.jpg'),

('dry','small','Sowing','Maintain moisture; use shade net if sunlight is intense','images/guideline/Nursery Preparation.jpg'),
('dry','medium','Sowing','Maintain moisture; use shade net if sunlight is intense','images/guideline/Nursery Preparation.jpg'),

('dry','small','Mulching','Essential to reduce evaporation and retain moisture','images/guideline/Mulching.jpg'),
('dry','medium','Mulching','Essential to reduce evaporation and retain moisture','images/guideline/Mulching.jpg'),

('dry','small','Irrigation','Water 3–4 times per week; drip irrigation recommended','images/guideline/Irrigation.jpg'),
('dry','medium','Irrigation','Water 3–4 times per week; drip irrigation recommended','images/guideline/Irrigation.jpg'),

('dry','small','Harvesting','Fruits may take slightly longer; maintain irrigation','images/guideline/Harvesting.jpg'),
('dry','medium','Harvesting','Fruits may take slightly longer; maintain irrigation','images/guideline/Harvesting.jpg');

SELECT *
FROM cultivation_guidelines
;
DROP TABLE cultivation_guidelines;

UPDATE cultivation_guidelines
SET image_url = 'images/guideline/flowers.jpg'
WHERE id = 14;

DROP TABLE eggplant_disease_management;

CREATE TABLE eggplant_disease_management (
    disease_id SERIAL PRIMARY KEY,
    disease VARCHAR(150) NOT NULL,
    treatment TEXT NOT NULL,
    prevention_tips TEXT NOT NULL
);

INSERT INTO eggplant_disease_management (disease, treatment, prevention_tips) VALUES
(
    'Eggplant Cercosporin Leaf Disease',
    'Mancozeb 2 g/L; Chlorothalonil 2 ml/L; Neem oil 3 ml/L',
    'Use disease-free seeds; Avoid overhead irrigation'
),
(
    'Eggplant Healthy Leaf Disease',
    'Balanced NPK fertilizer; Compost or organic manure',
    'Proper watering; Weed control'
),
(
    'Eggplant Insect Pest Disease',
    'Neem oil 3–5 ml/L; Emamectin benzoate 0.4 g/L; Spinosad 0.3 ml/L',
    'Pheromone traps; Remove infested parts'
),
(
    'Eggplant Leaf Spot Disease',
    'Mancozeb 2 g/L; Copper oxychloride 2.5 g/L; Trichoderma',
    'Avoid water splash; Destroy crop residue'
),
(
    'Eggplant Powdery Mildew Disease',
    'Sulfur fungicide 2 g/L; Carbendazim 1 g/L; Neem oil',
    'Improve air circulation; Avoid excess nitrogen'
),
(
    'Eggplant Wilt Disease',
    'Streptomycin 0.5 g/10 L; Carbendazim 1 g/L; Neem cake',
    'Crop rotation; Well-drained soil treatment'
);
UPDATE eggplant_disease_management
SET disease = 'Eggplant Cercospora Leaf Disease'
WHERE disease = 'Eggplant Cercosporin Leaf Disease';

UPDATE eggplant_disease_management
SET disease = 'Eggplant Powdery mildew Disease'
WHERE disease = 'Eggplant Powdery Mildew Disease';
SELECT disease_name, treatment, prevention_tips
FROM eggplant_disease_management
WHERE disease_name = 'Eggplant Leaf Spot Disease';

SELECT * FROM "eggplant_disease_management";

CREATE TABLE weather_guidelines (
    weather_id SERIAL PRIMARY KEY,
    min_temp FLOAT,
    max_temp FLOAT,
    min_humidity FLOAT,
    max_humidity FLOAT,
    risk VARCHAR(150),
    system_recommendation TEXT
);

INSERT INTO weather_guidelines
(min_temp, max_temp, min_humidity, max_humidity, risk, system_recommendation)
VALUES

-- > 32°C  AND  > 80%
(32, 100, 80, 100,
 'Heat stress + fungal disease risk',
 'Increase irrigation, apply mulch, spray neem oil or copper-based fungicide'),

-- > 32°C  AND  < 40%
(32, 100, 0, 40,
 'Water stress, mite infestation',
 'Light frequent irrigation, neem oil spray'),

-- 25 – 32°C  AND 60 – 80%
(25, 32, 60, 80,
 'Optimal growth, moderate disease risk',
 'Normal irrigation, routine crop monitoring'),

-- 20 – 25°C  AND  > 80%
(20, 25, 80, 100,
 'Leaf spot and fungal infection risk',
 'Reduce watering, ensure proper drainage, apply organic fungicide'),

-- < 20°C AND > 70%
(0, 20, 70, 100,
 'Slow growth, root diseases',
 'Avoid over-watering, improve soil aeration'),

-- 25 – 30°C AND < 50%
(25, 30, 0, 50,
 'Pest attack (thrips, mites)',
 'Maintain soil moisture, apply neem-based pest control'),

-- > 30°C AND > 85%
(30, 100, 85, 100,
 'Severe fungal disease risk',
 'Avoid overhead irrigation, apply preventive fungicide'),

-- 22 – 28°C AND 70 – 80%
(22, 28, 70, 80,
 'Healthy growth with mild risk',
 'Monitor crop weekly, maintain balanced nutrition'),

-- > 35°C AND Any humidity
(35, 100, 0, 100,
 'Extreme heat stress',
 'Use shade nets, increase watering intervals'),

-- Any temp AND > 90% humidity
(0, 100, 90, 100,
 'High fungal & bacterial disease risk',
 'Improve airflow, avoid spraying, monitor leaves daily');

SELECT * FROM weather_guidelines;

DROP TABLE weather_guidelines;

SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
