import re
from kbrainsdk.validation.ingest import validate_ingest_onedrive, validate_ingest_sharepoint, validate_ingest_status, validate_ingest_rfp_responses, validate_ingest_pipeline_status
from kbrainsdk.apibase import APIBase
from docx import Document
import PyPDF2
import pandas as pd

class Ingest(APIBase):

    def __init__(self, *args, **kwds):
        self.FILE_HANDLER = {
            "pdf": self.pdf_handler,
            "txt": self.txt_handler,
            "docx": self.docx_handler
        }
        self.TXT_CHARACTERS_PER_PAGE = 2000  # Adjust this value based on your assumption
        return super().__init__(*args, **kwds)

    def get_supported_file_types(self):
        return list(self.FILE_HANDLER.keys())

    def ingest_onedrive(self, email, token, client_id, oauth_secret, tenant_id, environment):

        payload = {
            "email": email,
            "token": token,
            "environment": environment,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id
        }

        validate_ingest_onedrive(payload)

        path = f"/ingest/onedrive/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def ingest_sharepoint(self, host, site, token, client_id, oauth_secret, tenant_id, environment):

        payload = {
            "host": host,
            "site": site,
            "token": token,
            "environment": environment,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id
        }

        validate_ingest_sharepoint(payload)

        path = f"/ingest/sharepoint/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response
    
    def ingest_rfp_responses(self, proposal_id, email, assertion_token, client_id, oauth_secret, tenant_id, environment):

        payload = {
            "proposal_id": proposal_id,
            "email": email,
            "token": assertion_token,
            "environment": environment,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id
        }

        validate_ingest_rfp_responses(payload)

        path = f"/ingest/rfp/responses/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def get_status(self, datasource):

        payload = {
            "datasource": datasource 
        }

        validate_ingest_status(payload)

        path = f"/ingest/status/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response
    
    def get_pipeline_status(self, run_id):

        payload = {
            "run_id": run_id 
        }

        validate_ingest_pipeline_status(payload)

        path = f"/ingest/pipeline/run/status/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def convert_site_to_datasource(self, site):
        # Remove special characters and replace spaces with hyphens
        site_name = re.sub(r'[^a-zA-Z0-9\s]', '', site)
        site_name = site_name.replace(' ', '-')
        return f"sharepoint-{site_name.lower().replace('.', '-')}"

    def convert_email_to_datasource(self, email):
        return f"drive-{email.lower().replace('@', '-at-').replace('.', '-')}"

    def pdf_handler(self, local_filepath, document_df, filename):
        with open(local_filepath, 'rb') as book:
            with PyPDF2.PdfReader(book, strict=False) as book_reader:
                number_of_pages = len(book_reader.pages)
                page_list = book_reader.pages
                for page in range(number_of_pages):
                    paragraph_count = {"count": 0}
                    extracted_page = page_list[page]
                    text = extracted_page.extract_text()
                    sections = re.split(r'\t+|\n{2,}|\s{2,}', text)
                    sections = list(filter(lambda x: x.strip() != '', sections))
                    section_count = range(1, len(sections) + 1)
                    page_df = pd.DataFrame({"text": sections, "section": section_count})
                    page_df['file'] = filename
                    page_df['page'] = page + 1
                    page_df['text'] = page_df['text'].apply(lambda x: x.strip().replace("\n", " "))
                    page_df['type'] = page_df['text'].apply(lambda x: "header" if len(x) < 100 else "paragraph")
                    page_df['paragraph'] = page_df['type'].apply(lambda x: self.count_paragraphs(x, paragraph_count))

                    document_df = pd.concat([document_df, page_df], axis='rows')
        return document_df

    def estimate_pages(self, character_count, average_characters_per_page):
        return character_count // average_characters_per_page + 1


    def txt_handler(self, local_filepath, document_df, filename):
        with open(local_filepath, 'r') as file:
            text = file.read()
            character_count = len(text)
            estimated_pages = self.estimate_pages(character_count, self.TXT_CHARACTERS_PER_PAGE)
            paragraphs = re.split(r'\t+|\n{2,}|\s{2,}', text)
            paragraphs = list(filter(lambda x: x.strip() != '', paragraphs))
            section_count = [i + 1 for i in range(len(paragraphs))]
            page_df = pd.DataFrame({"text": paragraphs, "section": section_count})
            page_df['file'] = filename
            page_df['page'] = page_df.index // estimated_pages + 1
            page_df['text'] = page_df['text'].apply(lambda x: x.strip().replace("\n", " "))
            page_df['type'] = page_df['text'].apply(lambda x: "header" if len(x) < 200 else "paragraph")
            page_df['paragraph'] = page_df['section']  # Count paragraphs based on section number

            document_df = pd.concat([document_df, page_df], axis='rows')
        return document_df

    def docx_handler(self, local_filepath, document_df, filename):
        doc = Document(local_filepath)
        paragraphs = 1
        sections = 1
        for paragraph in doc.paragraphs:
            text = paragraph.text
            section_type = "header" if len(text) < 200 else "paragraph"
            page_df = pd.DataFrame({ "text": [text], "section": [sections], "file": [filename], "page": [1], "type": [section_type], "paragraph": [paragraphs] })
            document_df = pd.concat([document_df, page_df], axis='rows')
            sections += 1
            if section_type != "header":
                paragraphs += 1
        return document_df

    def count_paragraphs(self, x, paragraph_count):
        if x == "header":
            if paragraph_count["count"] == 0:
                return 1
            return paragraph_count["count"]
        
        paragraph_count["count"] += 1
        return int(paragraph_count["count"])

    def process_document(self, local_filepath, document_name, extension):
        try:
            document_df = pd.DataFrame({"file":[], "page":[], "section":[], "text":[], "type":[], "paragraph": []})
            filename = f"{document_name.strip()}.{extension}"
            document_df = self.FILE_HANDLER[extension.lower()](local_filepath, document_df, filename)
            metafile = f"{local_filepath.replace(f'.{extension}','')}_meta.csv"
            document_df.reset_index(inplace=True, drop=True)
            document_df.to_csv(metafile, escapechar="\\", index=False)                
            return metafile
        except Exception as ex:
            return str(ex)