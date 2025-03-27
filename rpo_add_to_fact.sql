INSERT INTO sample_fact (
    supplier_id, 
    part_id, 
    inspect_id, 
    desc_id, 
    stats_id, 
    sample_value
)
SELECT 
sd.supplier_id,
pd.part_id,
id.inspect_id,
dd.desc_id,
std.stats_id,
ft.sample_value
FROM fact_temp ft
LEFT JOIN 
suppliers_dimension sd 
ON (ft.supplier_codeand_name = sd.supplier_codeand_name OR (ft.supplier_codeand_name IS NULL AND sd.supplier_codeand_name IS NULL))
AND (ft.supplier_factory_location = sd.supplier_factory_location OR (ft.supplier_factory_location IS NULL AND sd.supplier_factory_location IS NULL))
LEFT JOIN 
parts_dimension pd 
ON (ft.wd_part_number = pd.wd_part_number OR (ft.wd_part_number IS NULL AND pd.wd_part_number IS NULL))
AND (ft.commodity_codeand_name = pd.commodity_codeand_name OR (ft.commodity_codeand_name IS NULL AND pd.commodity_codeand_name IS NULL))
AND (ft.supplier_part_numberand_revision = pd.supplier_part_numberand_revision OR (ft.supplier_part_numberand_revision IS NULL AND pd.supplier_part_numberand_revision IS NULL))
AND (ft.wdsqe = pd.wdsqe OR (ft.wdsqe IS NULL AND pd.wdsqe IS NULL))
LEFT JOIN 
inspection_dimension id 
ON (ft.qa_supervisor = id.qa_supervisor OR (ft.qa_supervisor IS NULL AND id.qa_supervisor IS NULL))
AND (ft.qa_inspector = id.qa_inspector OR (ft.qa_inspector IS NULL AND id.qa_inspector IS NULL))
AND (ft.date_inspected = id.date_inspected OR (ft.date_inspected IS NULL AND id.date_inspected IS NULL))
AND (ft.submit_date = id.submit_date OR (ft.submit_date IS NULL AND id.submit_date IS NULL))
AND (ft.wd_program_name = id.wd_program_name OR (ft.wd_program_name IS NULL AND id.wd_program_name IS NULL))
AND (ft.build_phase = id.build_phase OR (ft.build_phase IS NULL AND id.build_phase IS NULL))
LEFT JOIN 
descriptions_dimension dd 
ON (ft.critical_parameter_numbers = dd.critical_parameter_numbers OR (ft.critical_parameter_numbers IS NULL AND dd.critical_parameter_numbers IS NULL))
AND (ft.descriptions = dd.descriptions OR (ft.descriptions IS NULL AND dd.descriptions IS NULL))
LEFT JOIN 
statistic_dimension std 
ON (ft.cp_type = std.cp_type OR (ft.cp_type IS NULL AND std.cp_type IS NULL))
AND (ft.nominal = std.nominal OR (ft.nominal IS NULL AND std.nominal IS NULL))
AND (ft.tolerance = std.tolerance OR (ft.tolerance IS NULL AND std.tolerance IS NULL))
AND (ft.usl = std.usl OR (ft.usl IS NULL AND std.usl IS NULL))
AND (ft.lsl = std.lsl OR (ft.lsl IS NULL AND std.lsl IS NULL))
AND (ft.mc_upper_limit = std.mc_upper_limit OR (ft.mc_upper_limit IS NULL AND std.mc_upper_limit IS NULL))
AND (ft.mc_lower_limit = std.mc_lower_limit OR (ft.mc_lower_limit IS NULL AND std.mc_lower_limit IS NULL))
AND (ft.mean_stats = std.mean_stats OR (ft.mean_stats IS NULL AND std.mean_stats IS NULL))
AND (ft.mc_percent_error = std.mc_percent_error OR (ft.mc_percent_error IS NULL AND std.mc_percent_error IS NULL))
AND (ft.stdev = std.stdev OR (ft.stdev IS NULL AND std.stdev IS NULL))
AND (ft.uc_lof_hvm_cpk_estimate = std.uc_lof_hvm_cpk_estimate OR (ft.uc_lof_hvm_cpk_estimate IS NULL AND std.uc_lof_hvm_cpk_estimate IS NULL))
AND (ft.hvm_cpk_point_estimate = std.hvm_cpk_point_estimate OR (ft.hvm_cpk_point_estimate IS NULL AND std.hvm_cpk_point_estimate IS NULL))
AND (ft.lc_lof_hvm_cpk_estimate = std.lc_lof_hvm_cpk_estimate OR (ft.lc_lof_hvm_cpk_estimate IS NULL AND std.lc_lof_hvm_cpk_estimate IS NULL))
AND (ft.min_stats = std.min_stats OR (ft.min_stats IS NULL AND std.min_stats IS NULL))
AND (ft.max_stats = std.max_stats OR (ft.max_stats IS NULL AND std.max_stats IS NULL))
AND (ft.range_stats = std.range_stats OR (ft.range_stats IS NULL AND std.range_stats IS NULL))
AND (ft.count_stats = std.count_stats OR (ft.count_stats IS NULL AND std.count_stats IS NULL));