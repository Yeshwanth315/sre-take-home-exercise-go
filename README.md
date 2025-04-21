# 🩺 Uptime Checker

A Python app that checks the availability of web endpoints and reports their uptime percentage at regular intervals.

---

## 🔧 Installation and Running the Code

Follow the steps below to install and run the Uptime Checker app on your machine.

---

### 📁 Clone or Download the Project

```bash
git clone https://github.com/Yeshwanth315/sre-take-home-exercise-go.git
cd sre-take-home-exercise-go
```

### 📦 Pre requirements to run the applications

- Python 3.7+
- pip

### 📥 Install Dependencies

```bash
pip install -r requirements.txt

```

### ▶️ 5. Run the Uptime Checker
```bash
### without input 
python dev.py 
ERROR:root:Usage: python main.py <config_file>

### With input yaml config
python main.py sample.yaml

dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com - 25% availability (1 successful / 4 total requests)
2025-04-21 11:35:47,407 [INFO] dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com - 25% availability (1 successful / 4 total requests)
dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com - 25% availability (1 successful / 4 total requests)
2025-04-21 11:35:49,035 [INFO] dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com - 25% availability (1 successful / 4 total requests)
2025-04-21 11:35:49,035 [INFO] 🛑 Gracefully stopped by user (Ctrl+C)

```

# CHANGES.md

## [v1.2.0] - 2025-04-21
### Added
- ✅ **Graceful termination support using `KeyboardInterrupt` handler**:
  - `try-except` block in `main()` to catch `Ctrl+C` and log a friendly exit message.
  - Final stats are optionally logged when the script is interrupted.
- 🛠️ **Logging configuration using `logging.basicConfig`**:
  - Added `logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')` for consistent and timestamped log formatting.
- 🔒 **Error handling for file and YAML issues**:
  - Added `FileNotFoundError` check for missing config file.
  - Added `yaml.YAMLError` exception handling for malformed YAML.

### Changed
- Updated `main()` to wrap the full endpoint loading and monitoring logic in error-safe blocks.

---

## [v1.1.0] - 2025-04-21
### Added
- **Made `method`, `headers`, and `body` optional in the `Endpoint` class constructor**:
  - Default values provided for missing fields (e.g., `method` defaults to `"GET"`, `headers` and `body` default to empty dictionaries).
  
### Fixed
- **Fixed TypeError in `Endpoint` initialization**:
  - The issue was caused by missing required arguments (`method`, `headers`, `body`) when they were not present in the input YAML.
  
### Changed
- **Updated `Endpoint` class constructor**:
  - The `__init__` method now supports optional arguments (`method`, `headers`, and `body`).
  
### Removed
- No changes removed in this version.

---

## [v1.0.0] - 2025-04-20
### Initial Release
- Endpoint monitoring script to check the health of multiple endpoints via HTTP requests.
- YAML-based configuration for endpoints.
- Logs success rates for each domain and endpoint.
