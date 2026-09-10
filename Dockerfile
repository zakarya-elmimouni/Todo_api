FROM python:3.11-slim

#sets the working directory for what follows
WORKDIR /app  
# Installation des dépendances Python d'abord (pour profiter du cache Docker)
COPY requirements.txt .
#ça veut dire:"prends le fichier requirements.txt qui est à la racine du build context (donc la racine de ton projet)
#et copie-le dans le conteneur, dans le dossier courant (. = WORKDIR, donc /app)."

RUN pip install --no-cache-dir -r requirements.txt

   
# Copie du code de l'application
COPY . .


EXPOSE 8000
# commande, file to run, host, port
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 