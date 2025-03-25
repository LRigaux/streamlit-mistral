"""
Tests unifiés pour l'application Mistral AI Chat.

Ce fichier regroupe les tests d'API et de chat en un seul endroit,
permettant de vérifier rapidement que tout fonctionne correctement.

Usage:
    python test.py api    # Pour tester uniquement la connexion API
    python test.py chat   # Pour tester une conversation avec le modèle
    python test.py        # Pour exécuter tous les tests
"""
import os
import sys
import logging
from dotenv import load_dotenv
from mistralai import Mistral
from app.utils.mistral_client import get_mistral_client, test_api_connection

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_api():
    """Test de connexion à l'API Mistral."""
    logger.info("=== Test de connexion à l'API Mistral ===")
    
    # Charger les variables d'environnement
    load_dotenv()
    
    # Récupérer la clé API
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        logger.error("MISTRAL_API_KEY non trouvée dans les variables d'environnement")
        return False
    
    logger.info(f"Clé API trouvée (premiers 4 caractères: {api_key[:4]}...)")
    
    # Test d'initialisation du client
    try:
        logger.info("Initialisation du client Mistral...")
        client = get_mistral_client()
        logger.info("✓ Client initialisé avec succès")
    except Exception as e:
        logger.error(f"✗ Échec de l'initialisation du client: {str(e)}")
        return False
    
    # Test de connexion à l'API
    try:
        logger.info("Test de connexion à l'API...")
        connection_status = test_api_connection()
        
        if connection_status:
            logger.info("✓ Connexion à l'API réussie")
            return True
        else:
            logger.error("✗ Échec de la connexion à l'API")
            return False
    except Exception as e:
        logger.error(f"✗ Erreur lors du test de connexion: {str(e)}")
        return False

def test_chat():
    """Test de conversation avec le modèle Mistral."""
    logger.info("=== Test de conversation avec le modèle Mistral ===")
    
    # Charger les variables d'environnement
    load_dotenv()
    
    # Récupérer la clé API
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        logger.error("MISTRAL_API_KEY non trouvée dans les variables d'environnement")
        return False
    
    try:
        # Initialiser le client
        logger.info("Initialisation du client Mistral...")
        client = Mistral(api_key=api_key)
        
        # Test d'une conversation simple
        logger.info("Test d'une conversation simple...")
        
        # Conversation
        conversation = []
        
        # Premier message
        user_message = "Bonjour ! J'aimerais en savoir plus sur les saisons. Quelle est ta saison préférée et pourquoi?"
        logger.info(f"User: {user_message}")
        
        conversation.append({"role": "user", "content": user_message})
        
        # Obtenir la réponse
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=conversation,
            max_tokens=10

        )
        
        assistant_message = response.choices[0].message.content
        logger.info(f"Assistant: {assistant_message}")
        
        # Ajouter à la conversation
        conversation.append({"role": "assistant", "content": assistant_message})
        
        # Deuxième message pour tester le contexte
        user_message = "Peux-tu me parler des couleurs typiques de l'automne?"
        logger.info(f"User: {user_message}")
        
        conversation.append({"role": "user", "content": user_message})
        
        # Obtenir la réponse
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=conversation,
            max_tokens=10
        )
        
        assistant_message = response.choices[0].message.content
        logger.info(f"Assistant: {assistant_message}")
        
        logger.info("✓ Test de conversation réussi")
        return True
    except Exception as e:
        logger.error(f"✗ Erreur inattendue: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Démarrage des tests...")
    
    # Déterminer quels tests exécuter en fonction des arguments
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "api":
            # Exécuter uniquement le test API
            success = test_api()
        elif sys.argv[1].lower() == "chat":
            # Exécuter uniquement le test de chat
            success = test_chat()
        else:
            logger.error(f"Argument invalide: {sys.argv[1]}")
            logger.info("Options valides: 'api', 'chat'")
            sys.exit(1)
    else:
        # Exécuter tous les tests
        api_success = test_api()
        
        if api_success:
            chat_success = test_chat()
            success = api_success and chat_success
        else:
            logger.error("Le test API a échoué, test de chat annulé")
            success = False
    
    # Afficher le résultat final
    if success:
        logger.info("✅ Tous les tests ont réussi!")
        sys.exit(0)
    else:
        logger.error("❌ Certains tests ont échoué")
        sys.exit(1) 