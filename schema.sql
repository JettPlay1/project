DROP TABLE IF EXISTS date_factory_order CASCADE;
DROP TABLE IF EXISTS factory_order CASCADE;
DROP TABLE IF EXISTS material CASCADE;
DROP TABLE IF EXISTS material_order CASCADE;
DROP TABLE IF EXISTS material_supply CASCADE;
DROP TABLE IF EXISTS material_using CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS provider CASCADE;

CREATE TABLE IF NOT EXISTS date_factory_order
(
    id_order integer NOT NULL,
    date_order date NOT NULL,
    CONSTRAINT date_factory_order_pkey PRIMARY KEY (id_order)
);
INSERT INTO date_factory_order(id_order, date_order) VALUES (1, '2023-10-31');
INSERT INTO date_factory_order(id_order, date_order) VALUES (2, '2023-11-01');
INSERT INTO date_factory_order(id_order, date_order) VALUES (3, '2023-11-02');
CREATE TABLE IF NOT EXISTS product
(
    id_product integer NOT NULL,
    name_product character varying(100) NOT NULL,
    cost_product integer NOT NULL,
    volume integer NOT NULL,
    CONSTRAINT product_pkey PRIMARY KEY (id_product),
    CONSTRAINT product_cost_product_check CHECK (cost_product >= 0),
    CONSTRAINT product_volume_check CHECK (volume >= 0)
);
INSERT INTO product(id_product, name_product, cost_product, volume) VALUES (1, 'Паллеты', 500, 100);
INSERT INTO product(id_product, name_product, cost_product, volume) VALUES (2, 'Брус', 1200, 30);
INSERT INTO product(id_product, name_product, cost_product, volume) VALUES (3, 'Доска', 600, 231);
INSERT INTO product(id_product, name_product, cost_product, volume) VALUES (4, 'Леса', 1200, 100);
CREATE TABLE IF NOT EXISTS provider
(
    id_provider integer NOT NULL,
    name_provider character varying(100) COLLATE pg_catalog."default" NOT NULL,
    city character varying(100) COLLATE pg_catalog."default" NOT NULL,
    phone_number character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT provider_pkey PRIMARY KEY (id_provider)
);
INSERT INTO provider(id_provider, name_provider, city, phone_number) VALUES (1, 'ООО ""МатериалТОРГ""', 'Ишим', '88009001000');
INSERT INTO provider(id_provider, name_provider, city, phone_number) VALUES (2, 'ООО ""ПривезуДаром""', 'Тюмень', '89987654321');
INSERT INTO provider(id_provider, name_provider, city, phone_number) VALUES (3, 'ООО ""МатериалТОРГ""', 'Тюмень', '89123456789');
CREATE TABLE factory_order
(
    id_factory_order integer NOT NULL,
    id_product integer NOT NULL,
    count_product integer NOT NULL,
    summa integer NOT NULL,
    CONSTRAINT factory_order_pkey PRIMARY KEY (id_factory_order, id_product),
    CONSTRAINT factory_order_id_factory_order_fkey FOREIGN KEY (id_factory_order)
        REFERENCES date_factory_order (id_order) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT factory_order_id_product_fkey FOREIGN KEY (id_product)
        REFERENCES product (id_product) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT factory_order_count_product_check CHECK (count_product >= 0),
    CONSTRAINT factory_order_summa_check CHECK (summa >= 0)
);
INSERT INTO factory_order(id_factory_order, id_product, count_product, summa) VALUES (2, 3, 14, 8400);
INSERT INTO factory_order(id_factory_order, id_product, count_product, summa) VALUES (2, 1, 30, 15000);
INSERT INTO factory_order(id_factory_order, id_product, count_product, summa) VALUES (1, 2, 12, 14400);
INSERT INTO factory_order(id_factory_order, id_product, count_product, summa) VALUES (1, 1, 13, 6500);
CREATE TABLE material
(
    id_material integer NOT NULL,
    name_material character varying(100) COLLATE pg_catalog."default" NOT NULL,
    count_stock integer NOT NULL,
    cost_material integer NOT NULL,
    description character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT material_pkey PRIMARY KEY (id_material),
    CONSTRAINT material_count_stock_check CHECK (count_stock >= 0),
    CONSTRAINT material_cost_material_check CHECK (cost_material >= 0)
);
INSERT INTO material(id_material, name_material, count_stock, cost_material, description) VALUES (1, 'Бревно', 1012, 20, 'Обычное дерево');
INSERT INTO material(id_material, name_material, count_stock, cost_material, description) VALUES (2, 'Железный лист', 312, 100, 'Кусок металла');
INSERT INTO material(id_material, name_material, count_stock, cost_material, description) VALUES (3, 'Инструмент', 10, 200, 'Необходим для производства');
CREATE TABLE IF NOT EXISTS material_supply
(
    id_supply integer NOT NULL,
    id_material integer NOT NULL,
    date_supplly date NOT NULL,
    volume integer NOT NULL,
    CONSTRAINT material_supply_pkey PRIMARY KEY (id_supply),
    CONSTRAINT material_supply_id_material_fkey FOREIGN KEY (id_material)
        REFERENCES material (id_material) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT material_supply_volume_check CHECK (volume >= 0)
);
INSERT INTO material_supply(id_supply, id_material, date_supplly, volume) VALUES (1, 2, '2023-11-21', 100);
INSERT INTO material_supply(id_supply, id_material, date_supplly, volume) VALUES (2, 3, '2023-11-21', 23);
INSERT INTO material_supply(id_supply, id_material, date_supplly, volume) VALUES (3, 1, '2023-11-25', 11);
INSERT INTO material_supply(id_supply, id_material, date_supplly, volume) VALUES (4, 2, '2023-11-22', 50);
INSERT INTO material_supply(id_supply, id_material, date_supplly, volume) VALUES (5, 2, '2023-11-21', 32);
CREATE TABLE IF NOT EXISTS material_order
(
    id_order integer NOT NULL,
    id_provider integer NOT NULL,
    id_supply integer NOT NULL,
    date_order date NOT NULL,
    cost_order integer NOT NULL,
    CONSTRAINT material_order_pkey PRIMARY KEY (id_order),
    CONSTRAINT material_order_id_provider_fkey FOREIGN KEY (id_provider)
        REFERENCES provider (id_provider) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT material_order_id_supply_fkey FOREIGN KEY (id_supply)
        REFERENCES material_supply (id_supply) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT material_order_cost_order_check CHECK (cost_order >= 0)
);
INSERT INTO material_order( id_order, id_provider, id_supply, date_order, cost_order) VALUES (1, 1, 1, '2023-11-15', 10000);
INSERT INTO material_order( id_order, id_provider, id_supply, date_order, cost_order) VALUES (2, 2, 2, '2023-11-15', 11000);
INSERT INTO material_order( id_order, id_provider, id_supply, date_order, cost_order) VALUES (3, 1, 3, '2023-11-17', 9000);
CREATE TABLE IF NOT EXISTS material_using
(
    id_using integer NOT NULL,
    id_material integer NOT NULL,
    id_factory_order integer NOT NULL,
    volume integer NOT NULL,
    CONSTRAINT material_using_pkey PRIMARY KEY (id_using),
    CONSTRAINT material_using_id_factory_order_fkey FOREIGN KEY (id_factory_order)
        REFERENCES date_factory_order (id_order) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT material_using_id_material_fkey FOREIGN KEY (id_material)
        REFERENCES material (id_material) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT material_using_volume_check CHECK (volume >= 0)
);
INSERT INTO material_using(id_using, id_material, id_factory_order, volume) VALUES (1, 1, 1, 100);
INSERT INTO material_using(id_using, id_material, id_factory_order, volume) VALUES (2, 2, 2, 13);
INSERT INTO material_using(id_using, id_material, id_factory_order, volume) VALUES (3, 3, 3, 64);
INSERT INTO material_using(id_using, id_material, id_factory_order, volume) VALUES (4, 3, 3, 200);
