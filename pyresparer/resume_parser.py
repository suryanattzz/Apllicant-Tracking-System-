import os
import multiprocessing as mp
import io
import spacy
import pprint
from spacy.matcher import Matcher
from . import utils   # make sure utils.py exists in the same folder


class ResumeParser:
    def __init__(self, resume, skills_file=None, custom_regex=None):
        """
        Resume Parser to extract structured information from resumes.
        """
        # Load spaCy model
        self._nlp_model = spacy.load("en_core_web_sm")

        self.__skills_file = skills_file
        self.__custom_regex = custom_regex
        self.__matcher = Matcher(self._nlp_model.vocab)

        self.__details = {
            'name': None,
            'email': None,
            'mobile_number': None,
            'skills': None,
            'degree': None,
            'no_of_pages': None,
        }

        self.__resume = resume

        # Handle file type
        if not isinstance(self.__resume, io.BytesIO):
            ext = os.path.splitext(self.__resume)[1].split('.')[-1]
        else:
            ext = self.__resume.name.split('.')[-1]

        # Extract raw text from resume file
        self.__text_raw = utils.extract_text(self.__resume, '.' + ext)
        self.__text = ' '.join(self.__text_raw.split())

        # Process with spaCy
        self.__nlp = self._nlp_model(self.__text)
        self.__custom_nlp = self._nlp_model(self.__text)   # fallback to same model

        self.__noun_chunks = list(self.__nlp.noun_chunks)

        # Populate details
        self.__get_basic_details()

    def get_extracted_data(self):
        """Return extracted structured resume data."""
        return self.__details

    def __get_basic_details(self):
        """Extracts basic details like name, email, phone, skills, degree, pages."""
        # Custom entities from utils
        try:
            cust_ent = utils.extract_entities_wih_custom_model(self.__custom_nlp)
        except Exception:
            cust_ent = {}

        # Extract basic fields
        name = utils.extract_name(self.__nlp, matcher=self.__matcher)
        email = utils.extract_email(self.__text)
        mobile = utils.extract_mobile_number(self.__text, self.__custom_regex)
        skills = utils.extract_skills(
            self.__nlp, self.__noun_chunks, self.__skills_file
        )

        # Extract education-related entities
        entities = utils.extract_entity_sections_grad(self.__text_raw)

        # Fill details dictionary
        try:
            self.__details['name'] = cust_ent.get('Name', [None])[0]
        except Exception:
            self.__details['name'] = name

        self.__details['email'] = email
        self.__details['mobile_number'] = mobile
        self.__details['skills'] = skills

        # Pages
        try:
            self.__details['no_of_pages'] = utils.get_number_of_pages(self.__resume)
        except Exception:
            self.__details['no_of_pages'] = None

        # Degree
        try:
            self.__details['degree'] = cust_ent.get('Degree')
        except Exception:
            self.__details['degree'] = None

        return


# Wrapper for multiprocessing
def resume_result_wrapper(resume):
    parser = ResumeParser(resume)
    return parser.get_extracted_data()


if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())

    resumes = []
    data = []

    for root, directories, filenames in os.walk('resumes'):
        for filename in filenames:
            file = os.path.join(root, filename)
            resumes.append(file)

    results = [
        pool.apply_async(resume_result_wrapper, args=(x,))
        for x in resumes
    ]

    results = [p.get() for p in results]
    pprint.pprint(results)
