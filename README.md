# API Automation Framework (PyCharm + PyTest)

This repository contains a **generic API automation framework** built using **Python 3.9+**, **PyTest**, and **Postman collections**.  
It is designed to be easily reusable across projects.  

For demonstration, this framework currently uses the **Naehas Offer Fulfillment API collection**.  
You can replace this collection with any Postman collection by following the steps described below.

---

## Features

- **Postman collection integration** – Run and validate API test collections directly.
- **Automated response verification** – Empty responses are updated with actual responses at runtime, which are then used to determine test results.
- **Reusable base framework** – Can be used across projects with minimal changes.
- **Command line and PyCharm support** – Run tests with one script or full PyTest command.
- **Virtual environment (venv)** – Easy environment isolation.
- **Customizable scenario sets** – Control which tests to run using YAML configs.
- **HTML and XML reports** – Test results are auto-generated and stored.

---

## Prerequisites

- **Python 3.9.x**  
  Verify installation:  
  ```bash
  python3 --version
  ```

- **PyCharm IDE** (optional but recommended for development)

---

## 1. Install Dependencies

### Option 1 – Using Command Line
```bash
./install.sh
```

### Option 2 – Using PyCharm
1. Press `Cmd + Shift + A` (Mac) or `Ctrl + Shift + A` (Windows/Linux) to open **Search Everywhere**.  
2. Type `requirements`.  
3. Select **Sync Python Requirements**.  
4. In **Package Requirements File**, choose `requirements.txt`.

---

## 2. Using a Virtual Environment (venv)

After cloning this repository, navigate to its directory and run:
```bash
./activate.sh
```

This script will create and activate a Python virtual environment.  
[Read more about venv](https://docs.python.org/3/tutorial/venv.html).

---

## 3. Setting Up Postman Collections

### Steps to Prepare Your Collection
1. **Start with an existing Postman collection.**  
2. **Manually add or update:**
   - **Auth headers** (if required for your project)
   - **Environment variables** or collection variables as needed.
3. Place the modified collection inside:  
   ```
   data/<PROJECT_NAME>/public-api/
   ```

**Example (for this repo):**
```
data/Naehas-API/public-api/Naehas Offer Fulfilment.json
```

---

## 4. Running Tests

Activate the virtual environment and run:
```bash
pytest --scenario-set-file=scenario_set.yaml --debug-test --numprocesses=auto --junitxml=xml_report.xml --html=report.html
```

### Using a Custom Scenario Set
To specify a different scenario set file:
```bash
pytest --scenario-set-file=scenario_set_sanity.yaml --debug-test --numprocesses=auto --junitxml=xml_report.xml --html=report.html
```
> **Note:** All scenario set files must be placed inside the `configs/` directory.

---

## 5. Test Execution Workflow

1. The framework reads the **Postman collection**.
2. Any **empty responses** in the collection are replaced with **actual responses** during execution.
3. A **new collection file** with updated responses is generated automatically.
4. Test statuses are determined based on **actual vs. expected responses**.
5. **Action after execution:**
   - Option A: **Replace your old Postman collection with the newly generated one** (recommended for keeping test data current), or  
   - Option B: **Manually update your old collection using changes from the new file**, then delete the generated file.  
6. **Re-run the tests** to validate against the updated collection.  

---

## 6. Test Results and Logs

- **HTML report:** `report.html`  
- **JUnit XML report:** `xml_report.xml`  
- **Log files:** Stored under the `logs/` directory.  
- **API call trace:** `logs/naehas-public-api.Naehas-API/api_calls.csv`

These artifacts help debug issues and review API call history.

---

## 7. Reusing This Framework for Other Projects

1. Clone this repository.
2. Replace the **Postman collection** in:
   ```
   data/<NEW_PROJECT>/public-api/
   ```
3. Update or create your own **scenario set file(s)** in:
   ```
   configs/
   ```
4. Adjust **auth headers, variables, or test logic** as needed.
5. Run:
   ```bash
   pytest --scenario-set-file=<your_scenario_file>.yaml --debug-test --numprocesses=auto --junitxml=xml_report.xml --html=report.html
   ```
6. Follow the same workflow of **reviewing generated collections** and **updating test data**.

---

## Extending and Integrating the Framework

### 1. Extend Test Validation Logic for New APIs
- Add or update **validation rules** inside:
  ```
  common/item.py
  common/scenario.py
  common/utilities.py
  ```
- For each new API endpoint:
  1. Modify or add **Postman test scripts** to define expected responses.
  2. Update `scenario_set.yaml` (or create a new scenario file) to reference these tests.
  3. If additional logic is needed (e.g., complex response verification), extend Python methods inside the framework rather than relying solely on Postman assertions.

---

### 2. CI/CD Integration (Jenkins or Other Pipelines)
- A `Jenkinsfile` is already included as an example.
- Key steps to integrate:
  1. Install dependencies using:
     ```bash
     ./install.sh
     ```
  2. Activate virtual environment:
     ```bash
     ./activate.sh
     ```
  3. Run tests with:
     ```bash
     pytest --scenario-set-file=scenario_set.yaml --debug-test --numprocesses=auto --junitxml=xml_report.xml --html=report.html
     ```
  4. Archive the following artifacts for each pipeline build:
     - `report.html` (HTML test report)
     - `xml_report.xml` (JUnit XML for CI test reporting)
     - Any logs under `logs/`
- Integrate with **Jenkins JUnit plugin** (or any CI tool supporting JUnit XML):
  - Point to `xml_report.xml` to automatically display test results in the pipeline dashboard.

---

### 3. Use HTML and XML Reports for Build Dashboards
- **HTML Report (`report.html`)**  
  - Can be opened directly in a browser to review full test run details.
  - Add to CI build artifacts for easy access by developers and QA teams.
  
- **JUnit XML Report (`xml_report.xml`)**  
  - Consumed by CI/CD dashboards (Jenkins, GitLab, GitHub Actions, Azure DevOps, etc.).
  - Enables test history tracking, pass/fail metrics, and build health indicators.

- **Example Jenkins Post-build Actions**:
  - **Publish JUnit Test Result Report** → `xml_report.xml`
  - **Archive Artifacts** → `report.html, logs/**`

---

## Repository Structure

```
.
├── assets/
│   └── style.css
├── common/
│   ├── constants.py
│   ├── item.py
│   ├── scenario.py
│   ├── scenario_set.py
│   ├── test_config.py
│   ├── test_logger.py
│   ├── test_run_error.py
│   └── utilities.py
├── configs/
│   ├── scenario_set.yaml
│   └── test_config.yaml
├── data/
│   └── Naehas-API/public-api/
│       ├── Naehas Offer Fulfilment.json
│       ├── OLD_Naehas Offer Fulfilment.postman_collection.json
│       └── Test-DS-OPS API Collection.postman_collection.json
├── logs/
│   ├── naehas-public-api.Naehas-API/
│   │   ├── api_calls.csv
│   │   └── Naehas Offer Fulfilment.log
│   └── test_config.log
├── tests/
│   ├── test_scenario.py
│   └── conftest.py
├── Jenkinsfile
├── pytest.ini
├── pytest.sh
├── install.sh
├── activate.sh
├── requirements.txt
├── README.md
├── report.html
└── xml_report.xml
```

---

## Example Commands

- **Default run (main scenario):**
  ```bash
  pytest --scenario-set-file=scenario_set.yaml --debug-test --numprocesses=auto --junitxml=xml_report.xml --html=report.html
  ```

- **Run a specific scenario file:**
  ```bash
  pytest --scenario-set-file=scenario_set_sanity.yaml --debug-test --numprocesses=auto --junitxml=xml_report.xml --html=report.html
  ```

- **View Python version:**
  ```bash
  python3 --version
  ```

---

## Next Steps

- Extend test validation logic to suit new APIs.
- Integrate this framework with **CI/CD** pipelines (example: Jenkinsfile included).
- Use **HTML and XML reports** for build dashboards.
- Leverage this as a **base repository** to quickly bootstrap API test automation in other projects.

---
