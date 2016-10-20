#Stack Overflow: A Code Laundering Platform?

###Requirements
- Python 2.7 or newer
- NiCad clone detection tool

###Research questions
- RQ1: Do developers release apps with code copied from Stack Overflow?
- RQ2: Do developers respect the copyright terms of code reused from Stack Overflow?
- RQ3: Do Stack Overflow users respect copyright terms when publishing code snippets on Stack Overflow?
- RQ4: How long does a Stack Overflow code remains in released versions of an app?

###File description
- **data_mining_scripts** folder contains the scripts to mine raw data.
	- **extract2json.py**: extract Java and Android related code snippets from the Stack Exchange dump (please set Posts.xml's path in line 45).
    - **write_snippets.py**: extract the results of **extract2json.py** (in JSON) into separate Java files (please set the input path in line 10).
    - **run_nicad**: run NiCad clone detection tool between Stack Overflow snippets and the _Android inconsistent files_ [1].

- **analytic_scripts** folder contains the scripts to analyze the clone detection results and to answer the research questions.
  - **case_study.py**: compute code reuse occurrences for the researh questions.
  - **overlap.py**: compute the _overlap rate (proportion)_ between a code reuse snippet and a license inconsistent snippet for RQ1.
  - **migrating.py**: identify the "migrated code snippets" (in RQ3) in which the 1st app's file and the 2nd app's file are released under different licenses.
  - **evolution_snippet.py**: extract input files for RQ4.
  - **RQ4_analysis** folder contains scripts and data to compute code reuse snippets' lifespan.
- **match_names** folder cotains scripts and data for matching developer names between the studied Android apps and Stack Overflow posts.
- **raw_data** folder contains Android snippets' creation date and raw data of RQ2 & RQ3.
- **data** folder contains clone detection results and some intermediate data for analyses.

###Data source
- Inconsistent files: http://swat.polymtl.ca/data/SANER16/AndroidAppsDataONF-DroidJanv2015.7z
- Stack Exchange data dump: https://archive.org/details/stackexchange
- NiCad tool: http://www.txl.ca/nicaddownload.html

###How to user the analytic scripts
1. Download the Stack Exchange data dump and inconsistent files.
2. Run **extract2json.py**, **write_snippets.py**, and **run_nicad** consecutively to obtain the clone code pairs between Stack Overflow posts and Android inconsistent files.
3. Use the scripts in **analytic_scripts** and **match_names** to obtain results of the four research questions.

###Reference
1. Ons Mlouki, Foutse Khomh and Giuliano Antoniol, On the Detection of Licenses Violations in Android Ecosystem, in _Proceedings of the 23rd IEEE International Conference on Software Analysis, Evolution, and Reengineering (SANER)_.

###For any questions
Please send email to le.an@polymtl.ca