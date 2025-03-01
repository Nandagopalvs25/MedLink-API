from django.shortcuts import render
from rest_framework import generics
from .models import Patient,Record,CustomUser,Post,Comment
from django.http import HttpResponse,JsonResponse
from .serializers import PatientSerializer,RecordSerializer,UserSerializer,PostSerializer
from rest_framework.parsers import JSONParser 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
import requests
import os
import google.generativeai as genai
import json
from rest_framework.authtoken.models import Token
from dotenv import load_dotenv
from api.utils import pinecone_utils
from uuid import uuid4
from langchain_core.documents import Document

#load_dotenv()


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class PatientList(generics.ListCreateAPIView):
   serializer_class=PatientSerializer
   filter_backends = [DjangoFilterBackend,filters.SearchFilter]
   search_fields = ['name']
   
   def get_queryset(self):
    user = self.request.user
    return Patient.objects.filter(doctor=user)
   
class PostView(APIView):
   
    def post(self, request, format=None):
           user_id = Token.objects.get(key=request.auth.key).user_id
           user = CustomUser.objects.get(id=user_id)
           posts= Post.objects.create(author=user,title=request.data['title'],desc=request.data['desc'])
           genai.configure(api_key=os.getenv("api_key"))
           model = genai.GenerativeModel("gemini-1.5-flash",generation_config={"response_mime_type": "application/json"})
           response = model.generate_content(request.data['desc']+"Analyze this question and generate suitable tags related to it")
           print(response.text)
           geminidata=json.loads(response.text)
           for i in geminidata['tags']:
               posts.tags.add(i.lower())
           #print(posts.tags.names())
           records=Record.objects.filter(tags__name__in=[posts.tags.names()]).distinct()
           for i in records:
               print(i.patient.doctor)
               posts.doctors_related.add(i.patient.doctor)
           return HttpResponse("Sucess")
           
    def get(self,request,*args, **kwargs):
        posts=Post.objects.all()
        serializer=PostSerializer(posts,many=True)
        return JsonResponse(serializer.data, safe=False) 

class RecordView(APIView):
   
    def post(self, request, format=None):
           patientr=Patient.objects.get(id=request.data['id'])
           geminikey = os.getenv("GOOGLE_API_KEY")
           genai.configure(api_key=geminikey)
           drive_link = request.data['url']
           local_pdf_path = "downloaded_file.pdf"
           download_pdf_from_drive(drive_link, local_pdf_path)
           img_file = genai.upload_file(path=local_pdf_path)
           print(f"Uploaded file '{img_file.display_name}' as: {img_file.uri}")
           model = genai.GenerativeModel(
                     model_name="gemini-2.0-flash",
                     system_instruction=(
                            "You are an advanced AI-powered medical assistant designed to analyze medical documents and provide structured insights. "
                            "Your primary function is to extract all relevant medical details and generate a comprehensive, well-structured summary. "
                            "Ensure that no critical medical information is omitted, and highlight any abnormalities, diagnoses, test results, and treatments. "
                            "You must always adhere to medical privacy regulations (e.g., HIPAA, ABHA) and ensure patient confidentiality. "
                            "Your responses should be formatted strictly as valid JSON to maintain consistency and readability. "
                            "Additionally, if no relevant medical data is found in the document, return an empty summary and an empty list of keywords."
                        ),
                    generation_config={"response_mime_type": "application/json"}
                        )
           
           prompt = (
                    "Analyze the provided medical document and extract all relevant details. "
                    "Generate a **comprehensive and structured summary** under the key 'summary'. "
                    "Ensure that the summary includes all medical history, symptoms, diagnoses, test results, prescribed medications, treatments, and doctor's notes. "
                    "Highlight any **irregularities, critical observations, or important insights** explicitly. "
                    "Additionally, extract **key medical terms** such as diseases, conditions, symptoms, medications, and test names under the key 'tags'. "
                    "The response **must be formatted as a valid JSON object** with the following structure:\n\n"
                    "```json\n"
                    "{\n"
                    '    "summary": "<detailed medical summary>",\n'
                    '    "tags": ["keyword1", "keyword2", "keyword3"]\n'
                    "}\n"
                    "```\n"
                    "If the document does not contain relevant medical data, return:\n"
                    "```json\n"
                    "{\n"
                    '    "summary": "",\n'
                    '    "tags": []\n'
                    "}\n"
                    "```\n"
                    "Ensure accuracy, maintain clarity, and strictly follow the required JSON format."
                    )
           response = model.generate_content([prompt, img_file])
           geminidata=json.loads(response.text)
           vector_store=pinecone_utils.get_vector_store()
           document_1 = Document(
            page_content=geminidata['summary'],
              metadata={"userid": str(request.data['id'])},
                )
           documents = [document_1,]
           uuids = [str(uuid4()) for _ in range(len(documents))]
           vector_store.add_documents(documents=documents, ids=uuids)
           record=Record.objects.create(patient=patientr,name=request.data['name'],url=request.data['url'],summary=geminidata['summary'])
           for i in geminidata['tags']:
               record.tags.add(i.lower())
               print(record)
           return HttpResponse("Succesfully Created")
    def get(self,request,*args, **kwargs):
        records=Record.objects.filter(patient=Patient.objects.get(id=self.kwargs["id"]))
        serializer=RecordSerializer(records,many=True)
        return JsonResponse(serializer.data, safe=False) 
      
def drive_link_to_download_url(drive_link):
    file_id = drive_link.split('/d/')[1].split('/')[0]
    return f"https://drive.google.com/uc?export=download&id={file_id}"


def download_pdf_from_drive(drive_link, save_path):
    download_url = drive_link_to_download_url(drive_link)
    response = requests.get(download_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded PDF to '{save_path}'")
    else:
        print(f"Failed to download the PDF. Status code: {response.status_code}")


          
class UserProfileView(APIView):

     def get(self,request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = CustomUser.objects.get(id=user_id)
        serializer=UserSerializer(user)
        return JsonResponse(serializer.data,safe=False)
     

class AiChatView(APIView):
    def post(self,request, format=None):
        prompt=request.data['prompt']
        patient_id=request.data['patient_id']
        patient=Patient.objects.get(id=patient_id)
        record=Record.objects.filter(patient=patient)
        geminikey = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=geminikey)
       
        vector_store=pinecone_utils.get_vector_store()
        context = vector_store.similarity_search(prompt,k=10,filter={"userid": str(patient_id)}, )
        model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                system_instruction=(
                "You are an AI-powered medical assistant designed to assist doctors in retrieving and analyzing patient medical records. "
                "You provide structured and insightful responses based on available data while maintaining compliance with medical ethics, privacy regulations (e.g., HIPAA, ABHA), and patient confidentiality. "
                "You only retrieve patient data when explicitly requested and do not disclose information unless the query contains a valid request for medical records. "
                "If the input is a casual or general question, respond conversationally instead of fetching medical data. "
                "Your responses should be concise, clear, and medically relevant when required."
        )
        )

        query = f"""
                Determine the intent of the following user input. 
                - If the query is related to patient medical records, retrieve relevant structured data and present it clearly. 
                - If the input is a general or casual question, respond naturally without referencing medical data. 
                - Do not disclose patient information unless explicitly requested with a valid identifier.

                User Input: {prompt}
                """
        context_text = "\n".join([doc.page_content for doc in context]) if context else "No additional context available."
        response = model.generate_content([query, context_text])
        response = model.generate_content([query, context_text])
        result = response.text
        print(context)
        return JsonResponse({"response": result})



class CommentView(APIView):
   
    def post(self, request, format=None):
           user_id = Token.objects.get(key=request.auth.key).user_id
           user = CustomUser.objects.get(id=user_id)
           npost=Post.objects.get(id=request.data['id'])
           ncomment=request.data['comment']
           newcomment= Comment.objects.create(author=user,post=npost,comment=ncomment)
           return HttpResponse("Sucess")


