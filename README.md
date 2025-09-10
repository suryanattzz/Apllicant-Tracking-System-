**Applicant Tracking System** 


````markdown
# Applicant Tracking System

A Python-based Applicant Tracking System (ATS) that automates resume parsing and candidate shortlisting. Utilizes NLP via spaCy, SQL database storage, and advanced resume matching.

---

##  Features

- Parse and extract information from resumes (`resume_processing.py`)
- Match job descriptions to resumes (`jd_matcher.py`)
- SQL-backed storage of candidate and course data (`db.py`, `Courses.py`)
- Web interface via `app.py` (Flask-based likely)
- Support for file uploads (`uploads/`), templates (`templates/`), and static assets (`static/`)

---

##  Prerequisites

- Python **3.11**
- Dependencies listed in `requirements.txt`
- SQLite (or any supported SQL DB) for storage
- Optional: spaCy model (e.g., `en_core_web_sm`)

---

##  Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/suryanattzz/Apllicant-Tracking-System-.git
cd Apllicant-Tracking-System-
````

### 2. Create and Activate Virtual Environment

```bash
python -m venv environment3.11
```

* **Windows**:

  ```bash
  environment3.11\Scripts\activate
  ```
* **macOS/Linux**:

  ```bash
  source environment3.11/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Optional**: If spaCy model is not included, install it:

```bash
python -m spacy download en_core_web_sm
```

### 4. Configure Environment Variables

* Copy `.env.example` to `.env`:

  ```bash
  copy .env.example .env      # Windows
  cp .env.example .env        # macOS/Linux
  ```
* Fill in your custom values (e.g., database credentials).

### 5. Initialize the Database (if needed)

If there's a database setup script or instructions in `db.py`, run it:

```bash
python db.py
```

Alternatively, manually ensure your SQL database is created and configured per the codebase.

---

## Running the Application

```bash
python app.py
```

* Open your browser and navigate to `http://localhost:5000` (or specified port).
* Interface supports resume uploads and applicant-job matching.

---

## Project Structure

```
├── app.py
├── db.py
├── jd_matcher.py
├── resume_processing.py
├── Courses.py
├── requirements.txt
├── .env.example
├── templates/
├── static/
└── uploads/
```

* `app.py`: Starts the web application (Flask)
* `db.py`: Handles database operations
* `jd_matcher.py`: Matches job descriptions to resumes
* `resume_processing.py`: Parses resumes
* `Courses.py`: Manages courses or tags in DB

---

## Common Commands

| Action                | Command                                               |
| --------------------- | ----------------------------------------------------- |
| Activate virtualenv   | `source environment3.11/bin/activate`                 |
| Deactivate virtualenv | `deactivate`                                          |
| Add a new dependency  | `pip install <package>` and update `requirements.txt` |
| Commit changes        | `git add . && git commit -m "message"`                |

---

## Screenshots / Visuals

*(Include screenshots or UI images here if available)*

---

## License & Contributing

* **License**: *Specify license if available.*
* **Contributing**: Fork the repo, work on a branch, and submit a Pull Request.

---

## Contact

Created and maintained by \[Your Name].
Questions or feedback? \[Your email or profile link].

```

---

###  Next Steps
- Review and tweak filenames or commands to fit your actual project.
- Add sections for deployment, testing, or API docs if needed.
- Feel free to ask if you'd like this made into a PDF or enhanced with visuals!
::contentReference[oaicite:0]{index=0}
```
