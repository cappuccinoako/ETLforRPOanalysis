CREATE TABLE IF NOT EXISTS suppliers_dimension(
    supplier_id SERIAL PRIMARY KEY,
    supplier_codeand_name VARCHAR(200),
    supplier_factory_location VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS parts_dimension(
    part_id SERIAL PRIMARY KEY,
    wd_part_number VARCHAR(200),
    commodity_codeand_name VARCHAR(200),
    supplier_part_numberand_revision VARCHAR(200),
    wdsqe VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS inspection_dimension(
    inspect_id SERIAL PRIMARY KEY,
    qa_supervisor VARCHAR(200),
    qa_inspector VARCHAR(200),
    date_inspected DATE,
    submit_date DATE,
    wd_program_name VARCHAR(200),
    build_phase VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS descriptions_dimension(
    desc_id SERIAL PRIMARY KEY,
    critical_parameter_numbers VARCHAR(200),
    descriptions VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS statistic_dimension(
    stats_id SERIAL PRIMARY KEY,
    cp_type VARCHAR(200),
    nominal VARCHAR(200),
    tolerance REAL,
    usl REAL,
    lsl REAL,
    mc_upper_limit REAL,
    mc_lower_limit REAL,
    mean_stats REAL,
    mc_percent_error_real REAL,
    stdev REAL,
    uc_lof_hvm_cpk_estimate REAL,
    hvm_cpk_point_estimate REAL,
    lc_lof_hvm_cpk_estimate REAL,
    min_stats REAL,
    max_stats REAL,
    range_stats REAL,
    count_stats SMALLINT
);

CREATE TABLE IF NOT EXISTS fact_temp(
    supplier_codeand_name VARCHAR(200),
    supplier_factory_location VARCHAR(200),
    qa_supervisor VARCHAR(200),
    qa_inspector VARCHAR(200),
    date_inspected DATE,
    submit_date DATE,
    wd_program_name VARCHAR(200),
    build_phase VARCHAR(200),
    wd_part_number VARCHAR(200),
    commodity_codeand_name VARCHAR(200),
    supplier_part_numberand_revision VARCHAR(200),
    wdsqe VARCHAR(200),
    critical_parameter_numbers VARCHAR(200),
    descriptions VARCHAR(200),
    cp_type VARCHAR(200),
    nominal VARCHAR(200),
    tolerance REAL,
    usl REAL,
    lsl REAL,
    mc_upper_limit REAL,
    mc_lower_limit REAL,
    mean_stats REAL,
    mc_percent_error_real REAL,
    stdev REAL,
    uc_lof_hvm_cpk_estimate REAL,
    hvm_cpk_point_estimate REAL,
    lc_lof_hvm_cpk_estimate REAL,
    min_stats REAL,
    max_stats REAL,
    range_stats REAL,
    count_stats SMALLINT,
    sample_value REAL

);

CREATE TABLE IF NOT EXISTS sample_fact (
    supplier_id INT REFERENCES suppliersDim(supplierId),
    part_id INT REFERENCES partsDim(partId),
    inspect_id INT REFERENCES inspectionDim(inspectId),
    desc_id INT REFERENCES descriptionsDim(descId),
    stats_id INT REFERENCES statisticDim(statsId),
    sample_value REAL

);