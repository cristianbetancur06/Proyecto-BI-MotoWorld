-- =========================================================
-- CLIENTES
-- =========================================================
 
INSERT INTO mt_clientes (tipo_doc, num_doc, nombre, telefono, email, estado)
VALUES ('CC', '1020304050', 'Sebastián Mora Ríos', '3101234567', 'sebasmora@gmail.com', 'ACTIVO');
 
INSERT INTO mt_clientes (tipo_doc, num_doc, nombre, telefono, email, estado)
VALUES ('CC', '1045678901', 'Valentina Castro Gil', '3157654321', 'valecastro@gmail.com', 'ACTIVO');
 
INSERT INTO mt_clientes (tipo_doc, num_doc, nombre, telefono, email, estado)
VALUES ('CE', '987123456', 'Andrés Rojas Peña', '3209876543', 'andresrojas@hotmail.com', 'ACTIVO');
 
INSERT INTO mt_clientes (tipo_doc, num_doc, nombre, telefono, email, estado)
VALUES ('CC', '3301122334', 'Camila Herrera López', '3004561234', 'camilaherrera@gmail.com', 'ACTIVO');
 
INSERT INTO mt_clientes (tipo_doc, num_doc, nombre, telefono, email, estado)
VALUES ('NIT', '900456789', 'ABC Transport SAS', '6014789632', 'cotizacaciones@abctranspport.com', 'ACTIVO');



-- =========================================================
-- MOTOS
-- =========================================================
 
-- KTM 

INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('ABC-12D', 'KTM', 'Duke 200 NG', 2024, 200, 'Naranja', 19690000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('XYZ-34M', 'KTM', 'Duke 250', 2025, 250, 'Negro', 23990000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('EFG-56N', 'KTM', 'RC 390', 2025, 373, 'Blanco/Naranja', 27400000, 'VENDIDA');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('HIJ-78O', 'KTM', '390 Adventure', 2026, 373, 'Naranja/Negro', 36990000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('KLM-90P', 'KTM', '1390 Super Duke R', 2026, 1350, 'Negro', 119990000, 'DISPONIBLE');
 

-- HONDA 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('MNO-12Q', 'Honda', 'CB 100', 2024, 99, 'Negro', 5700000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('PQR-34R', 'Honda', 'Navi 110', 2025, 110, 'Rojo', 7250000, 'VENDIDA');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('STU-56S', 'Honda', 'XR 150 L', 2024, 150, 'Blanco', 10850000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('VWX-78T', 'Honda', 'CB 190 R', 2026, 184, 'Negro/Rojo', 11900000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('YZA-90U', 'Honda', 'XR 190L', 2025, 184, 'Rojo', 13400000, 'DISPONIBLE');
 

-- SUZUKI 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('BCD-12V', 'Suzuki', 'AX4', 2024, 113, 'Negro', 5960000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('EFG-34W', 'Suzuki', 'GN 125', 2024, 124, 'Negro/Azul', 7399000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('HIJ-56X', 'Suzuki', 'Gixxer 150 FI', 2025, 155, 'Azul', 11390000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('KLM-78Y', 'Suzuki', 'DR 160 X', 2026, 149, 'Gris/Verde', 12999000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('NOP-90Z', 'Suzuki', 'GSX-R150 ABS', 2026, 147, 'Azul GP', 14990000, 'DISPONIBLE');
 
 
-- YAMAHA
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('QRS-12A', 'Yamaha', 'Crypton Finn', 2024, 114, 'Negro', 9100000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('TUV-34B', 'Yamaha', 'XTZ 150', 2025, 149, 'Azul/Gris', 14400000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('WXY-56C', 'Yamaha', 'MT 15', 2025, 155, 'Azul/Negro', 15500000, 'VENDIDA');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('ZAB-78D', 'Yamaha', 'NMAX Connected', 2026, 155, 'Gris Mate', 16100000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('CDE-90E', 'Yamaha', 'R15', 2026, 155, 'Negro Mate', 15800000, 'DISPONIBLE');
 
 
-- TVS 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('FGH-12F', 'TVS', 'Radeon 110', 2024, 110, 'Negro', 5500000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('IJK-34G', 'TVS', 'Raider 125', 2025, 124, 'Amarillo/Negro', 7450000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('LMN-56H', 'TVS', 'Apache RTR 160 4V', 2025, 160, 'Rojo/Gris', 9800000, 'VENDIDA');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('OPQ-78I', 'TVS', 'Apache RTR 200 4V', 2026, 198, 'Negro Mate', 11700000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('RST-90J', 'TVS', 'Ronin 225', 2026, 226, 'Naranja', 12500000, 'DISPONIBLE');
 
 
-- AKT 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('UVW-12K', 'AKT', 'NKD 125', 2024, 124, 'Negro', 5390000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('XYZ-34L', 'AKT', 'Dynamic Pro 125', 2025, 124, 'Gris', 7500000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('ABC-56M', 'AKT', 'CR5 180', 2024, 181, 'Rojo', 8400000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('DEF-78N', 'AKT', 'TT Dual Sport 200', 2026, 197, 'Verde', 8900000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('GHI-90O', 'AKT', 'AK 150 CR4', 2025, 161, 'Azul', 6300000, 'DISPONIBLE');
 
 
-- BAJAJ 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('JKL-12P', 'Bajaj', 'Boxer CT100 ES', 2024, 102, 'Negro/Azul', 5499000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('MNO-34Q', 'Bajaj', 'Discover 125 ST', 2025, 125, 'Rojo', 6800000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('PQR-56R', 'Bajaj', 'Pulsar NS 160 FI ABS', 2025, 160, 'Blanco/Gris', 10200000, 'DISPONIBLE');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('STU-78S', 'Bajaj', 'Pulsar NS 200 FI ABS', 2026, 200, 'Negro', 12400000, 'VENDIDA');
 
INSERT INTO mt_motos (placa, marca, modelo, año_fabricacion, cilindraje, color, precio, estado)
VALUES ('VWX-90T', 'Bajaj', 'Dominar 400', 2026, 373, 'Verde Aurora', 17500000, 'DISPONIBLE');




-- =========================================================
-- COMPRAS
-- =========================================================

INSERT INTO mt_compras (cliente_id, moto_id, fecha_compra, monto_total, tipo_venta, estado)
VALUES (1, 23, TRUNC(SYSDATE) - 30, 9800000, 'FINANCIADO', 'ACTIVA');

INSERT INTO mt_compras (cliente_id, moto_id, fecha_compra, monto_total, tipo_venta, estado)
VALUES (2, 18, TRUNC(SYSDATE) - 20, 15500000, 'CONTADO', 'PAGO');

INSERT INTO mt_compras (cliente_id, moto_id, fecha_compra, monto_total, tipo_venta, estado)
VALUES (3, 3, TRUNC(SYSDATE) - 45, 27400000, 'FINANCIADO', 'ACTIVA');

INSERT INTO mt_compras (cliente_id, moto_id, fecha_compra, monto_total, tipo_venta, estado)
VALUES (4, 7, TRUNC(SYSDATE) - 10, 7250000, 'CONTADO', 'PAGO');

INSERT INTO mt_compras (cliente_id, moto_id, fecha_compra, monto_total, tipo_venta, estado)
VALUES (5, 34, TRUNC(SYSDATE) - 60, 12400000, 'FINANCIADO', 'ACTIVA');



-- =========================================================
-- PAGOS
-- =========================================================

INSERT INTO mt_pagos (compra_id, fecha_pago, monto_pago, canal_pago, referencia)
VALUES (1, TRUNC(SYSDATE) - 25, 2000000, 'PSE', 'PSE-001');

INSERT INTO mt_pagos (compra_id, fecha_pago, monto_pago, canal_pago, referencia)
VALUES (2, TRUNC(SYSDATE) - 20, 15500000, 'TRANSFERENCIA', 'TF-001');

INSERT INTO mt_pagos (compra_id, fecha_pago, monto_pago, canal_pago, referencia)
VALUES (3, TRUNC(SYSDATE) - 10, 5000000, 'TC', 'TC-001');

INSERT INTO mt_pagos (compra_id, fecha_pago, monto_pago, canal_pago, referencia)
VALUES (3, TRUNC(SYSDATE) - 5, 10000000, 'TC', 'TC-002');
 
INSERT INTO mt_pagos (compra_id, fecha_pago, monto_pago, canal_pago, referencia)
VALUES (4, TRUNC(SYSDATE) - 10, 7250000, 'EFECTIVO', 'EF-001');

INSERT INTO mt_pagos (compra_id, fecha_pago, monto_pago, canal_pago, referencia)
VALUES (5, TRUNC(SYSDATE) - 60, 3500000, 'TRANSFERENCIA', 'TF-002');

INSERT INTO mt_pagos (compra_id, fecha_pago, monto_pago, canal_pago, referencia)
VALUES (5, TRUNC(SYSDATE) - 25, 3500000, 'PSE', 'PSE-002');
 