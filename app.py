from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Mock data: Newspaper articles
ARTICLES = [
    {"id": i, "title": f"Article {i}", "content": f"Content of article {i}"} for i in range(1, 101)
]

# Dictionary to track bad response count per user
bad_response_count = {}

@app.route('/articles', methods=['GET'])
def get_articles():
    try:
        # Simulate user identification (e.g., via a header or token)
        user_id = request.headers.get('Authorization', 'anonymous')

        # Track bad responses per user
        bad_response_count[user_id] = bad_response_count.get(user_id, 0)

        # Limit bad responses to a maximum of 5 per user
        if bad_response_count[user_id] < 5 and random.choice([True, False]):
            bad_response_count[user_id] += 1
            return jsonify({"error": "Internal Server Error"}), 500

        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Calculate start and end indices
        start = (page - 1) * per_page
        end = start + per_page

        # Paginate data
        paginated_articles = ARTICLES[start:end]
        total_pages = (len(ARTICLES) + per_page - 1) // per_page
        is_next = page < total_pages

        # Return paginated response
        return jsonify({
            "page": page,
            "per_page": per_page,
            "is_next": is_next,
            "data": paginated_articles
        }), 200

    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
