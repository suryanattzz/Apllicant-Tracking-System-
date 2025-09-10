# pyresparer/utils.py
import os
import re
import io

# Prefer pdfminer.six; fall back to pdfminer3 if that's what you installed
try:
    from pdfminer.high_level import extract_text as pdf_extract_text
    from pdfminer.pdfpage import PDFPage
except Exception:  # pragma: no cover
    from pdfminer3.high_level import extract_text as pdf_extract_text
    from pdfminer3.pdfpage import PDFPage

# Optional docx support
try:
    import docx2txt
except Exception:
    docx2txt = None


# --------------------
# File helpers
# --------------------
def _detect_ext(path_or_file, ext_hint=None):
    if ext_hint:
        e = ext_hint.lower()
        if not e.startswith("."):
            e = "." + e
        return e
    if isinstance(path_or_file, io.BytesIO):
        name = getattr(path_or_file, "name", "") or ""
        return os.path.splitext(name)[1].lower()
    if isinstance(path_or_file, str):
        return os.path.splitext(path_or_file)[1].lower()
    return ""


def extract_text(file_path_or_bytes, ext=None):
    """
    Extract plain text from a file path or BytesIO.
    Supports .pdf, .docx, .txt (best-effort for others).
    """
    e = _detect_ext(file_path_or_bytes, ext)

    # PDF
    if e in (".pdf", "pdf"):
        return pdf_extract_text(file_path_or_bytes)

    # DOCX
    if e in (".docx", "docx"):
        if docx2txt is None:
            return ""  # docx2txt not installed
        if isinstance(file_path_or_bytes, io.BytesIO):
            # docx2txt expects a path; write temp if BytesIO
            tmp = "_tmp_resume.docx"
            with open(tmp, "wb") as f:
                f.write(file_path_or_bytes.getbuffer())
            try:
                return docx2txt.process(tmp) or ""
            finally:
                try:
                    os.remove(tmp)
                except Exception:
                    pass
        else:
            return docx2txt.process(file_path_or_bytes) or ""

    # TXT
    if e in (".txt", "txt"):
        if isinstance(file_path_or_bytes, io.BytesIO):
            return file_path_or_bytes.getvalue().decode("utf-8", errors="ignore")
        with open(file_path_or_bytes, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    # Fallback: try PDFMiner anyway (some libs pass no ext)
    try:
        return pdf_extract_text(file_path_or_bytes)
    except Exception:
        return ""


def get_number_of_pages(file_path_or_bytes):
    """
    Return number of pages for PDFs; 1 for non-PDF/unknown.
    """
    e = _detect_ext(file_path_or_bytes)
    if e != ".pdf":
        return 1

    # Count PDF pages using PDFPage
    if isinstance(file_path_or_bytes, io.BytesIO):
        fh = file_path_or_bytes
        close_after = False
    else:
        fh = open(file_path_or_bytes, "rb")
        close_after = True

    try:
        count = sum(1 for _ in PDFPage.get_pages(fh, caching=True, check_extractable=True))
        return count or 1
    except Exception:
        return 1
    finally:
        if close_after:
            fh.close()


# --------------------
# Text extraction helpers
# --------------------
def extract_email(text):
    m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return m.group(0) if m else None


def extract_mobile_number(text, custom_regex=None):
    """
    Basic phone matcher; customize with your own regex if needed.
    """
    if custom_regex:
        pattern = re.compile(custom_regex)
    else:
        # Matches +XX-XXXX-XXXX, (XXX) XXX-XXXX, 10+ digits, etc.
        pattern = re.compile(r"(\+?\d[\d\-\s\(\)]{8,}\d)")
    m = pattern.search(text)
    if not m:
        return None
    # Normalize: keep digits and +
    raw = m.group(0)
    digits = re.sub(r"[^\d+]", "", raw)
    return digits


def extract_name(nlp_doc, matcher=None):
    # Try PERSON entity
    for ent in nlp_doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()

    # Fallback: first two capitalized tokens at the beginning
    tokens = [t.text for t in nlp_doc if t.is_alpha]
    caps = [t for t in tokens[:10] if t[:1].upper() == t[:1]]
    if len(caps) >= 2:
        return f"{caps[0]} {caps[1]}"
    if caps:
        return caps[0]
    return None


def extract_skills(nlp_doc, noun_chunks, skills_file=None):
    """
    Very simple skill extraction: intersection of known skills and text.
    `skills_file` can be a newline-separated list of skills.
    """
    skills_list = set()

    if skills_file and os.path.exists(skills_file):
        with open(skills_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                s = line.strip().lower()
                if s:
                    skills_list.add(s)
    else:
        # Minimal default list; extend as needed
        skills_list.update(map(str.lower, [
            "python","java","c++","c#","javascript","typescript","react","angular",
            "node js","node","django","flask","sql","mysql","postgresql","mongodb",
            "aws","azure","docker","kubernetes","git","html","css",
            "tensorflow","keras","pytorch","machine learning","deep learning",
            "streamlit","pandas","numpy","scikit-learn","nlp","tableau",
            "android","kotlin","swift","xcode","figma","adobe xd",
        ]))

    text = nlp_doc.text.lower()
    found = set()

    # token-level
    for s in skills_list:
        if s in text:
            found.add(s)

    # noun-chunk-level (multi-word bonuses)
    for nc in noun_chunks:
        n = nc.text.lower().strip()
        if n in skills_list:
            found.add(n)

    # Return capitalized-ish
    return sorted({s if " " not in s else s for s in found})


def extract_entities_wih_custom_model(nlp_doc):
    """
    Return a dict similar to the original project's custom NER output:
      {'Name': [..], 'Degree': [..], ...}
    """
    data = {}
    # Name from PERSON
    names = [ent.text.strip() for ent in nlp_doc.ents if ent.label_ == "PERSON"]
    if names:
        data["Name"] = [names[0]]

    # Degrees via keyword search (simple heuristic)
    degree_keywords = [
        "b.e", "b.e.", "btech", "b.tech", "bsc", "b.sc", "bca", "b.com", "bachelor",
        "m.e", "m.e.", "mtech", "m.tech", "msc", "m.sc", "mca", "m.com", "master",
        "phd", "ph.d", "doctorate", "mba"
    ]
    text = nlp_doc.text.lower()
    degrees = []
    for k in degree_keywords:
        if k in text:
            degrees.append(k.upper())
    if degrees:
        data["Degree"] = sorted(set(degrees))

    return data


def extract_entity_sections_grad(text):
    """
    Placeholder for original util; return {} if you don't need it downstream.
    """
    return {}
