================================================================================
AETHER-1 RAG KNOWLEDGE BASE — README
================================================================================

OVERVIEW
--------
This knowledge base contains synthetic but realistic mission operations
documents for AETHER-1 spacecraft. It is designed for ingestion into Qdrant
vector database to power the Research Agent (RAG) in OrbitalOps AI.

DIRECTORY STRUCTURE
-------------------
aether1-knowledge-base/
│
├── incident-reports/
│   ├── IR-001-battery-temperature-anomaly.txt
│   ├── IR-002-signal-loss-event.txt
│   ├── IR-003-fuel-pressure-drop.txt
│   ├── IR-004-solar-panel-degradation.txt
│   ├── IR-005-cpu-temperature-attitude-instability.txt
│   └── IR-006-to-IR-009-summaries.txt
│
├── operational-procedures/
│   └── OPS-MANUAL-001-operating-procedures.txt
│
└── mission-knowledge/
    ├── MK-001-historical-patterns-knowledge.txt
    └── MK-002-engineering-lessons-learned.txt

DOCUMENT SUMMARY
----------------
Total Documents : 8 files
Total Coverage  :

  Incident Reports (6 major + 4 summary incidents):
  - IR-001 : Battery Temperature Anomaly (CRITICAL)
  - IR-002 : Signal Loss Event / Communication Blackout (CRITICAL)
  - IR-003 : Fuel Pressure Drop (WARNING)
  - IR-004 : Solar Panel Output Degradation (WARNING)
  - IR-005 : CPU Temperature + Attitude Instability (CRITICAL)
  - IR-006 : Battery Depletion During Eclipse (CRITICAL)
  - IR-007 : CPU Spike During Blackout (WARNING)
  - IR-008 : Thruster Performance Degradation (WARNING)
  - IR-009 : Signal Degradation During Solar Storm (WARNING)

  Operational Procedures:
  - Normal operating ranges for all 10 telemetry parameters
  - 6 standard response procedures (one per major anomaly type)
  - Safe mode entry criteria
  - Maintenance schedules
  - Alert escalation protocols

  Mission Knowledge:
  - 4 known failure pattern signatures with historical occurrences
  - System interdependency map (validated in-mission)
  - Anomaly classification guide
  - 15 engineering lessons learned across all subsystems

TELEMETRY PARAMETERS COVERED
------------------------------
1.  Battery Temperature       (°C)
2.  Battery Charge Level      (%)
3.  Solar Panel Output        (W)
4.  Fuel Pressure             (kPa)
5.  Signal Strength           (dBm)
6.  Data Transmission Rate    (kbps)
7.  CPU Temperature           (°C)
8.  Altitude                  (km)
9.  Velocity                  (km/s)
10. Attitude Stability        (degrees)

QDRANT INGESTION GUIDANCE
--------------------------

Recommended Chunking Strategy:
  - Chunk size     : 500-800 tokens
  - Chunk overlap  : 100 tokens
  - Splitter       : RecursiveCharacterTextSplitter
  - Split on       : Section headers, then paragraphs

Recommended Metadata per Chunk:
  {
    "source_file"    : "IR-001-battery-temperature-anomaly.txt",
    "document_type"  : "incident_report",  // or "procedure", "knowledge"
    "severity"       : "CRITICAL",          // if incident report
    "system"         : "thermal",           // affected system
    "mission_day"    : 47,                  // if incident report
    "parameters"     : ["battery_temperature", "attitude_stability"]
  }

Collection Name Suggestion: "aether1_knowledge"

Embedding Model Recommendation: text-embedding-3-small (OpenAI)
  - Cost-effective for portfolio project
  - Good semantic performance for technical text

Retrieval Strategy:
  - Top-K: 3-5 chunks per query
  - Score threshold: 0.7 minimum similarity
  - Query expansion: include parameter name + anomaly type in query

QUERY EXAMPLES FOR TESTING
----------------------------
"What should I do when battery temperature exceeds 75 degrees?"
"What are the historical causes of signal loss on AETHER-1?"
"What are the normal operating ranges for fuel pressure?"
"What happens when CPU temperature is high and attitude is unstable?"
"How do I recognize a thermal cascade pattern?"
"What is the procedure for fuel line pressure drop?"

================================================================================
END OF README
================================================================================
