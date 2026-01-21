"""
Main Flask application for Bibliometric Analysis System
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Bibliometric Analysis System API'})


@app.route('/api/classify-fields', methods=['POST'])
def classify_fields():
    """
    Classify research fields from paper title and abstract
    
    Expected JSON payload:
    {
        "title": "Paper title",
        "abstract": "Paper abstract"
    }
    """
    try:
        data = request.get_json()
        title = data.get('title', '')
        abstract = data.get('abstract', '')
        
        # TODO: Integrate field classifier
        # from services.field_classifier import FieldClassifier
        # classifier = FieldClassifier()
        # fields = classifier.classify(title, abstract, top_n=6)
        
        return jsonify({
            'status': 'success',
            'title': title,
            'fields': []  # Will be populated by classifier
        })
    except Exception as e:
        logger.error(f"Error in classify_fields: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/process-authors', methods=['POST'])
def process_authors():
    """
    Process a batch of authors for bibliometric analysis
    
    Expected JSON payload:
    {
        "author_ids": ["author1", "author2", ...]
    }
    """
    try:
        data = request.get_json()
        author_ids = data.get('author_ids', [])
        
        # TODO: Implement author processing pipeline
        
        return jsonify({
            'status': 'success',
            'message': f'Processing {len(author_ids)} authors'
        })
    except Exception as e:
        logger.error(f"Error in process_authors: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
