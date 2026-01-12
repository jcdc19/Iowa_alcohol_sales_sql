CREATE OR REPLACE VIEW v_sales_clean AS
SELECT
  invoice_and_item_number AS invoice_item_id,

  CAST(date AS DATE) AS sale_date,
  DATE_TRUNC('month', CAST(date AS DATE)) AS sale_month,
  CAST(year AS INTEGER) AS sale_year,
  CAST(month AS INTEGER) AS sale_month_num,
  CAST(day AS INTEGER) AS sale_day,

  CAST(store_number AS INTEGER) AS store_id,
  store_name,
  address,
  city,
  zip_code,
  store_location,
  CAST(county_number AS INTEGER) AS county_id,
  county,

  CAST(category AS BIGINT) AS category_id,
  category_name,
  CAST(vendor_number AS INTEGER) AS vendor_id,
  vendor_name,
  CAST(item_number AS BIGINT) AS item_id,
  item_description,

  CAST(pack AS INTEGER) AS pack,
  CAST(bottle_volume_ml AS INTEGER) AS bottle_volume_ml,
  CAST(state_bottle_cost AS DOUBLE) AS state_bottle_cost,
  CAST(state_bottle_retail AS DOUBLE) AS state_bottle_retail,

  CAST(bottles_sold AS DOUBLE) AS bottles_sold,
  CAST(sale_dollars AS DOUBLE) AS sale_dollars,
  CAST(volume_sold_liters AS DOUBLE) AS volume_liters,
  CAST(volume_sold_gallons AS DOUBLE) AS volume_gallons

FROM raw_sales
WHERE date IS NOT NULL
  AND CAST(volume_sold_liters AS DOUBLE) > 0
  AND CAST(sale_dollars AS DOUBLE) >= 0;
