# CUSTOM CSV PROCESSING
import os
from typing import List
from pathlib import Path
import pandas as pd
import sqlite3
from langchain_core.documents import Document
from langchain_unstructured import UnstructuredLoader
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class Data_Ingestion:
    def __init__(self,chunk_size=1000,chunk_overlap=100):
        self.chunk_size=chunk_size,
        self.chunk_overlap=chunk_overlap,
        self.text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[" "]
        )
    
    #PDF
    def pdf_custom_process(self,filepath: str)->List[Document]:
        loader = PyMuPDF4LLMLoader(file_path=filepath)
        pages = loader.load()
        processed_chunks=[]
        for page_num,page in enumerate(pages):
            cleaned_text=" ".join(page.page_content.split())
            if len(cleaned_text)<50:
                continue
            
            #Create a chunks with enhanced metadata
            chunks=self.text_splitter.create_documents(
                texts=[cleaned_text],
                metadatas=[{
                    **page.metadata,
                    "page":page_num+1,
                    "total_pages":len(pages),
                    "Chunk_method":"pdf_custom_process",
                    "Char_count":len(cleaned_text)
                }]
            )
            processed_chunks.extend(chunks)
        return processed_chunks
    
    #DOCX
    def docx_custom_process(self,filepath:str)->List[Document]:
        """Process PDF with smart chunking and metadata enhancement"""
        #Load PDF
        loader = UnstructuredLoader(file_path=filepath,mode="elements")
        docs = loader.load()
        processed_chunks = []

        for doc_index, doc in enumerate(docs):
            cleaned_text = " ".join(doc.page_content.split())

            if len(cleaned_text) < 50:
                continue

            chunks = self.text_splitter.create_documents(
                texts=[cleaned_text],
                metadatas=[{
                    **doc.metadata,
                    "source": filepath,
                    "file_name": os.path.basename(filepath),
                    "file_type": "docx",
                    "element_index": doc_index,
                    "total_elements": len(docs),
                    "chunk_method": "docx_custom_process",
                    "char_count": len(cleaned_text),
                    "word_count": len(cleaned_text.split())
                }]
            )

            processed_chunks.extend(chunks)
        return processed_chunks
        
    #CSV
    def csv_custom_process(filepath: str, data_type: str = "csv_row") -> List[Document]:
        df=pd.read_csv(filepath)
        documents=[]

        for idx,row in df.iterrows():
            row_data = row.dropna().to_dict()
            content = "\n".join(
                [f"{key}: {value}" for key, value in row_data.items()]
            )
            metadata = {
                "source": filepath,
                "row_index": idx,
                "data_type": data_type,
                "columns": list(row_data.keys())
            }
            doc=Document(page_content=content,metadata=metadata)
            documents.append(doc)
        return documents

    #Excel(.xlsx)
    def excel_custom_process(filepath: str) -> List[Document]:
        excel_data = pd.read_excel(filepath, sheet_name=None)
        documents = []
        for sheet_name, df in excel_data.items():
            for idx, row in df.iterrows():
                row_data = row.dropna().to_dict()
                if not row_data:
                    continue
                content = "\n".join(
                    [f"{key}: {value}" for key, value in row_data.items()]
                )
                metadata = {
                    "source": filepath,
                    "file_name": os.path.basename(filepath),
                    "file_type": "excel",
                    "sheet_name": sheet_name,
                    "row_index": int(idx),
                    "columns": ", ".join(row_data.keys()),
                    "column_count": len(row_data),
                    "document_type": "excel_row",
                }
                doc = Document(
                    page_content=content,
                    metadata=metadata
                )

                documents.append(doc)
        return documents


    def sql_data_process(db_path: str)->List[Document]:

        """" Converting SQL Database into Documents with context"""
        con=sqlite3.connect(db_path)
        cursor=con.cursor()
        documents=[]

        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
            tables=cursor.fetchall()

            for table in tables:
                table_name=table[0]

                #Schema
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns=cursor.fetchall()
                column_name=[col[1] for col in columns]

                #table data
                cursor.execute(f"SELECT * FROM {table_name}")
                rows=cursor.fetchall()

                #Create table overview document
                table_content = f"Table: {table_name}\n"
                table_content += f"Columns: {','.join(column_name)}\n"
                table_content += f"Total Records : {len(rows)}\n\n"

                table_content += "Sample Records: \n"
                for row in rows[:5]:
                    records=dict(zip(column_name,row))
                    table_content += f"{records}\n"
                
                doc=Document(
                    page_content=table_content,
                    metadata={
                        'source':db_path,
                        'table_name':table_name,
                        'num_records':len(rows),
                        'data_type':'sql_tables'
                    }
                )
                documents.append(doc)

            # Strategy that create realationship document
            cursor.execute("""
            SELECT e.name,e.role,p.name as project_name,p.status 
            FROM employees e 
            JOIN projects p
            ON e.id=p.lead_id 
            """)
            relationship=cursor.fetchall()
            rel_content="Employees -Project RelationShip : \n\n"
            for rel in relationship:
                rel_content+=f"{rel[0]} ({rel[1]}) leads {rel[2]} - Status : {rel[3]}\n"

            rel_docs=Document(
                page_content=rel_content,
                metadata={
                    'source':db_path,
                    'data_type':'sql_relationship',
                    'quary':'employee_project_join'
                }
            )
            documents.append(rel_docs) 
        finally:
            con.close()
        return documents


    