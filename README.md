# 🧠 PC Brain AI

> A lightweight AI-powered personal PC monitoring and anomaly detection system built with Python, SQLite, and Machine Learning.

PC Brain AI continuously collects system information, stores historical performance data, learns the normal behavior of a computer, and uses machine learning to detect unusual system activity.

When an anomaly is detected, the system provides statistical explanations and analyzes captured processes to identify possible contributors.

---

## 🚀 Features

### 🖥️ System Monitoring

PC Brain AI collects:

- CPU usage
- CPU frequency
- RAM usage
- RAM used and available
- Disk usage
- Disk space
- Battery percentage
- Battery charging status
- Network statistics
- System uptime
- Running processes
- Multiple storage drives

---

### 🗄️ Data Storage

System information is stored locally using **SQLite**.

The database keeps:

- System metrics
- Process information
- Drive information
- Timestamps for historical analysis

This allows PC Brain AI to analyze the computer's behavior over time.

---

## 🤖 Machine Learning

PC Brain AI uses **Isolation Forest** from Scikit-learn for anomaly detection.

The model analyzes:

- CPU usage
- RAM usage
- Disk usage

and identifies system records that differ from the learned dataset.

Example:

```text
Records analyzed : 44

Anomalies detected : 5
Normal records     : 39

📊 Personal Baseline

PC Brain AI calculates a statistical baseline from historical system data.

Example:

CPU Average : 17.90%
CPU Std Dev : 20.86%

RAM Average : 84.97%
RAM Std Dev : 3.06%

Disk Average : 66.06%
Disk Std Dev : 0.44%

Detected anomalies are compared against this baseline to provide additional context.

⚠️ Anomaly Explanation

PC Brain AI doesn't simply report:

ANOMALY DETECTED

It also attempts to explain why the record is unusual.

Example:

ANOMALY DETECTED

CPU      : 91.1%
RAM      : 86.8%
Disk     : 66.3%
Severity : HIGH

Analysis:
  CPU usage is significantly above normal

The system classifies anomalies using the statistical deviation of the monitored metrics.

🔍 Process Correlation

When process information is available for an anomalous record, PC Brain AI analyzes the captured processes.

Example:

CPU Contributors:

python.exe
CPU: 50.7%
Relative contribution: 53.8%

System
CPU: 13.3%
Relative contribution: 14.1%

Code.exe
CPU: 13.2%
Relative contribution: 14.0%

RAM contributors are also analyzed.

Process contributors are reported as possible contributors based on the captured snapshot. They are not treated as proof of causation.

🧮 Contributor Scoring

PC Brain AI calculates relative CPU and RAM contribution among the processes captured in an anomaly snapshot.

This helps answer:

Which processes were using the most resources when unusual activity was detected?

The scoring is relative to the captured process data and should not be interpreted as the exact percentage of total system resource usage.

🏗️ System Architecture
                    PC SYSTEM
                        │
                        ▼
               SYSTEM COLLECTOR
                        │
                        ▼
                 SQLITE DATABASE
                        │
                        ▼
                HISTORICAL DATA
                        │
                        ▼
          ML ANOMALY DETECTOR
             (Isolation Forest)
                        │
                        ▼
          PERSONAL BASELINE
             + STATISTICS
                        │
                        ▼
             ANOMALY EXPLANATION
                        │
                        ▼
             PROCESS CORRELATION
                        │
                        ▼
             CONTRIBUTOR SCORING
📁 Project Structure
PC BRAIN AI/
│
├── app/
│   ├── __init__.py
│   ├── collector.py
│   ├── database.py
│   ├── logger.py
│   ├── analyzer.py
│   └── anomaly_detector.py
│
├── data/
│   └── pc_brain.db
│
├── models/
│
├── logs/
│
├── .gitignore
├── README.md
└── requirements.txt
🔄 How It Works

The complete workflow is:

1. Collect system information
          ↓
2. Store data in SQLite
          ↓
3. Build historical dataset
          ↓
4. Analyze system statistics
          ↓
5. Train Isolation Forest
          ↓
6. Detect unusual records
          ↓
7. Compare anomalies with personal baseline
          ↓
8. Explain unusual metrics
          ↓
9. Analyze captured processes
          ↓
10. Calculate possible contributors
🛠️ Technologies Used
Technology	Purpose
Python	Main programming language
psutil	System and process monitoring
SQLite	Local database
Scikit-learn	Machine learning
Isolation Forest	Anomaly detection
PowerShell	Development and execution environment
Git	Version control
GitHub	Project hosting
⚙️ Installation
1. Clone the repository
git clone https://github.com/M-Danish17-art/PC-Brain-AI.git
2. Enter the project directory
cd PC-Brain-AI
3. Create a virtual environment
python -m venv .venv
4. Activate the virtual environment

Windows PowerShell:

.\.venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
▶️ Running the Project
System Collector

Run:

python app/collector.py

This collects the current system information.

Automatic Logger

Run:

python app/logger.py

The logger continuously collects system information and stores it in the SQLite database.

The current collection interval is 30 seconds.

Press:

CTRL + C

to stop the logger.

Data Analyzer

Run:

python app/analyzer.py

The analyzer calculates statistics from the collected historical data.

It reports:

Average CPU usage
RAM usage
Disk usage
Process statistics
Drive statistics
ML Anomaly Detector

Run:

python app/anomaly_detector.py

The anomaly detector:

Loads historical metrics
Calculates a personal baseline
Runs Isolation Forest
Detects unusual records
Calculates anomaly severity
Explains unusual metrics
Checks available process information
Calculates possible CPU and RAM contributors
📊 Example Result

Example output from the anomaly detector:

=======================================================
              PC BRAIN AI
           ML ANOMALY DETECTOR
=======================================================

Records analyzed : 44

PERSONAL BASELINE

CPU Average : 17.90%
CPU Std Dev : 20.86%

RAM Average : 84.97%
RAM Std Dev : 3.06%

Disk Average : 66.06%
Disk Std Dev : 0.44%

-------------------------------------------------------

ANOMALY RESULTS

5 anomalies / 39 normal

#15
CPU  : 91.1%
RAM  : 86.8%
Disk : 66.3%

Severity : HIGH

Analysis:
  CPU usage significantly above normal

🔎 Process Contributor Example

For an anomaly where process information is available:

CPU Contributors:

python.exe
CPU: 50.7%
Relative contribution: 53.8%

System
CPU: 13.3%
Relative contribution: 14.1%

Code.exe
CPU: 13.2%
Relative contribution: 14.0%


RAM Contributors:

Code.exe
RAM: 9.50%
Relative contribution: 22.7%

chrome.exe
RAM: 8.55%
Relative contribution: 20.4%

These values represent the captured processes associated with that snapshot.

They should be interpreted as possible contributors, not definitive causes.

🧠 Machine Learning Approach

The project uses the Isolation Forest algorithm.

Isolation Forest is an unsupervised machine learning algorithm designed to identify unusual observations within a dataset.

In PC Brain AI, the model uses system performance metrics such as:

CPU Usage
RAM Usage
Disk Usage

The model identifies records that differ from the general behavior found in the collected historical data.

A statistical personal baseline is then used to provide additional explanation and context.

📈 Current Project Results

The current development dataset contains:

Records analyzed : 44
Anomalies        : 5
Normal records   : 39

The system successfully demonstrates:
Automated system monitoring
Historical data collection
SQLite database storage
Statistical analysis
Machine learning anomaly detection
Personal baseline calculation
Anomaly severity classification
Anomaly explanation
Process correlation
Relative contributor scoring

⚠️ Current Limitations

PC Brain AI is currently a lightweight personal monitoring and anomaly detection system.

Current limitations include:
Process monitoring captures a limited number of processes per snapshot.
Process contributors are based only on captured process data.
Contributor scores do not represent exact total system resource usage.
Process contribution does not prove causation.
Temperature monitoring depends on hardware and operating-system support.
The anomaly model works with the historical data available to it.
A larger and more diverse dataset can improve the usefulness of anomaly detection.

🚀 Future Improvements

Possible future versions could include:
Real-time monitoring dashboard
Web-based interface
Historical performance graphs
Automatic anomaly alerts
Email or desktop notifications
More advanced personal baselines
More detailed process tracking
Model persistence
Performance prediction
Automatic anomaly reports
System health scoring
Cloud-based monitoring
REST API integration

📌 Version History
v0.1 — System Scanner

Initial system information collector.

v0.2 — SQLite Database

Added persistent local data storage.

v0.3 — Automatic Logger

Added continuous automatic system monitoring.

v0.4 — Process & Multi-Drive Monitoring

Added process monitoring and multiple drive information.

v0.5 — Data Analyzer

Added historical statistical analysis.

v0.6 — ML Anomaly Detection

Added Isolation Forest based anomaly detection.

v0.6.1 — Anomaly Explanation

Added explanations for detected anomalies.

v0.6.2 — Statistical Anomaly Explanation

Added personal baseline and statistical deviation analysis.

v0.6.3 — Process Correlation

Connected anomaly records with captured process information.

v0.6.4 — Process Contributor Scoring

Added relative CPU and RAM contributor scoring.

🎯 Project Goal

The goal of PC Brain AI is to build a lightweight personal AI system that can understand normal computer behavior and identify unusual system activity.

Instead of only monitoring raw numbers, the project combines:

System Monitoring
       +
Historical Data
       +
Statistics
       +
Machine Learning
       +
Process Analysis

to provide more meaningful information about PC performance.

👨‍💻 Author

M. Danish

Artificial Intelligence Student

GitHub:

https://github.com/M-Danish17-art

📜 License

This project is intended for educational, experimental, and portfolio purposes.