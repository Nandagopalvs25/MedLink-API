# MedLink Platform

MedLink is an advanced Retrieval-Augmented Generation (RAG)-based health repository system designed to revolutionize how healthcare providers access and analyze patient medical records. By leveraging AI-driven retrieval and generative capabilities, the system allows doctors to seamlessly interact with a smart chatbot, enabling instant access to comprehensive patient histories through natural language queries.

## Features

- **AI-Driven Retrieval**: Efficiently retrieve patient records using AI-powered search.
- **Generative Capabilities**: Generate comprehensive summaries and insights from medical documents.
- **Smart Chatbot**: Interact with a chatbot to access patient histories and medical records.
- **Secure and Compliant**: Adheres to medical privacy regulations (e.g., HIPAA, ABHA).

## Tools and Technologies

- **Django Rest**: REST Api implementation.
- **PostgreSQL**: Relational database for storing data.
- **Pinecone**: Vector database for fast and scalable similarity search.
- **Hugging Face Models**: Pre-trained models for generating Embeddings.
- **Gemini**: Advanced AI model for generative tasks.


## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/Nandagopalvs25/MedLink-API.git
    cd medConnect
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv medenv
    source medenv/bin/activate  # On Windows use `medenv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the [`medConnect`](medConnect ) directory and add the following variables:
        ```
        DJANGO_SECRET_KEY=your_secret_key
        DEBUG=True
        DEVELOPMENT_MODE=True
        PINECONE_API_KEY=your_pinecone_api_key
        GOOGLE_API_KEY=your_google_api_key
        ```

5. **Apply migrations**:
    ```sh
    python manage.py migrate
    ```

6. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

## Usage

- **Admin Interface**: Access the Django admin interface at `/admin/` to manage users, patients, records, and posts.
- **API Endpoints**:
    - Register: `/api/auth/register/`
    - Login: `/api/auth/login/`
    - Logout: `/api/logout/`
    - User Details: `/api/user/`
    - Patients: `/api/patients/`
    - Posts: `/api/posts/`
    - Comments: `/api/comment/`
    - Records: `/api/records/`
    - User Profile: `/api/userProfile/`
    - AI Chat: `/api/chat/`
