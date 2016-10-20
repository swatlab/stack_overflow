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
    - **run_nicad**: run NiCad clone detection tool between Stack Overflow snippets and the inconsistent files [1].

- **analytic_scripts** folder contains the scripts to analyze the clone detection results and to answer the research questions.
  - **case_study.py**: compute code reuse occurrences for the researh questions.
  - **overlap.py**: compute the overlap proportion (rate) between a code reuse snippet and a license inconsistent snippet for RQ1.
  - **migrating**: identify the "migrated code snippets" (in RQ3) in which the 1st app's file and the 2nd app's file are released under different licenses.
  - **evolution_snippet.py**: extract input files for RQ4.
  - **RQ4_analysis** folder contains scripts and data to compute code reuse snippets' lifespan.
- **match_names** folder cotains scripts and data for matching developer names between the studied Android apps and Stack Overflow posts.
- **raw_data** folder contains Android snippets' creation date and raw data of RQ2 & RQ3.
- **data** folder contains clone detection results and some intermediate data for analyses.

###How to user the analytic scripts
1. Clone a project's Git repository. For systems originally managed by SVN, please follow this tutorial to clone the repository as Git:
   https://www.atlassian.com/git/tutorials/migrating-convert/.
2. Use the following command to extract the project's commit logs:
	```git log --pretty=format:"%H,%ae,%ai,%s"```.
3. Uncompress the folder ```output_data.zip```.
4. Run **detect_clones.py** and **extract_clone_results.py** to detect clone classes for a subject system using a clone detection tool.
6. Run **build_genealogies.py** to extract clone pairs from the JSON file, then build clone genealogies for each clone pair.
7. Run **commit_bug_mapping.py** and **fault_inducing.py** to identify bug-inducing commits.
8. Run **analyse_genealogies.py** to perform Fisher's exact test for RQ1 and RQ2.
9. Run **independant_variables.py** to extract explanatory variables for RQ3.
10. Build __GLM__ models with the R script in the **statistics/modelling** folder for RQ3.

###Data source
- Inconsistent files: http://swat.polymtl.ca/data/SANER16/AndroidAppsDataONF-DroidJanv2015.7z
- Stack Exchange data dump: https://archive.org/details/stackexchange

###Reference
1. Ons Mlouki, Foutse Khomh and Giuliano Antoniol, On the Detection of Licenses Violations in Android Ecosystem, in _Proceedings of the 23rd IEEE International Conference on Software Analysis, Evolution, and Reengineering (SANER)_.

###For any questions
Please send email to le.an@polymtl.ca