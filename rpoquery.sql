CREATE TABLE IF NOT EXISTS suppliersDim(
    supplierId SERIAL PRIMARY KEY,
    supplierCodeandName VARCHAR(200),
    supplierFactoryLocation VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS partsDim(
    partId SERIAL PRIMARY KEY,
    WDPartNumber VARCHAR(200),
    commodityCodeandName VARCHAR(200),
    supplierPartNumberandRevision VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS inspectionDim(
    inspectId SERIAL PRIMARY KEY,
    QASupervisor VARCHAR(200),
    QAInspector VARCHAR(200),
    dateInspected DATE,
    submitDate DATE,
    WDProgramName VARCHAR(200),
    buildPhase VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS descriptionsDim(
    descId SERIAL PRIMARY KEY,
    criticalParameterNumbers VARCHAR(200),
    descriptions VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS statisticDim(
    statsId SERIAL PRIMARY KEY,
    CPType VARCHAR(200),
    nominal VARCHAR(200),
    tolerance REAL,
    USL REAL,
    LSL REAL,
    MCUpperLimit REAL,
    MCLowerLimit REAL,
    mean REAL,
    MCPercentError REAL,
    Stdev REAL,
    UCLofHVMCpkEstimate REAL,
    HVMCpkPointEstimate REAL,
    LCLofHVMCpkEstimate REAL,
    minStats REAL,
    maxStats REAL,
    rangeStats REAL,
    countStats SMALLINT
);