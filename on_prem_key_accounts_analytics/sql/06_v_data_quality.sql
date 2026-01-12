CREATE OR REPLACE VIEW v_data_quality_issues AS

-- 1) Null / blank key fields
SELECT
  'null_key_field' AS issue_type,
  invoice_item_id,
  sale_date,
  store_id,
  store_name,
  county,
  item_id,
  item_description,
  volume_liters,
  sale_dollars,
  CASE
    WHEN store_id IS NULL THEN 'store_id'
    WHEN county IS NULL OR TRIM(county) = '' THEN 'county'
    WHEN item_id IS NULL THEN 'item_id'
    WHEN sale_date IS NULL THEN 'sale_date'
    ELSE 'unknown'
  END AS issue_detail
FROM v_sales_clean
WHERE store_id IS NULL
   OR sale_date IS NULL
   OR item_id IS NULL
   OR county IS NULL
   OR TRIM(county) = ''

UNION ALL

-- 2) Duplicate store_name mapped to multiple store_ids (common real-world issue)
SELECT
  'duplicate_store_name_multiple_ids' AS issue_type,
  NULL AS invoice_item_id,
  NULL AS sale_date,
  NULL AS store_id,
  store_name,
  NULL AS county,
  NULL AS item_id,
  NULL AS item_description,
  NULL AS volume_liters,
  NULL AS sale_dollars,
  CAST(COUNT(DISTINCT store_id) AS VARCHAR) AS issue_detail
FROM (
  SELECT DISTINCT store_id, store_name
  FROM v_sales_clean
)
GROUP BY store_name
HAVING COUNT(DISTINCT store_id) > 1

UNION ALL

-- 3) Negative or zero volumes (should be filtered, but this confirms)
SELECT
  'non_positive_volume' AS issue_type,
  invoice_item_id,
  sale_date,
  store_id,
  store_name,
  county,
  item_id,
  item_description,
  volume_liters,
  sale_dollars,
  'volume_liters <= 0' AS issue_detail
FROM v_sales_clean
WHERE volume_liters <= 0

UNION ALL

-- 4) Outlier transactions by volume (top 0.1% approx via percentile)
SELECT
  'volume_outlier' AS issue_type,
  s.invoice_item_id,
  s.sale_date,
  s.store_id,
  s.store_name,
  s.county,
  s.item_id,
  s.item_description,
  s.volume_liters,
  s.sale_dollars,
  'above_p999_volume' AS issue_detail
FROM v_sales_clean s
CROSS JOIN (
  SELECT quantile_cont(volume_liters, 0.999) AS p999_vol
  FROM v_sales_clean
) q
WHERE s.volume_liters > q.p999_vol