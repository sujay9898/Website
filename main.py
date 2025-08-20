from flask import Flask, render_template

app = Flask(__name__)

# Poster categories data
CATEGORIES = [
    {
        'id': 'nature',
        'name': 'Nature',
        'description': 'Beautiful landscapes and wildlife posters',
        'image_url': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400&h=300&fit=crop'
    },
    {
        'id': 'abstract',
        'name': 'Abstract Art',
        'description': 'Modern abstract and geometric designs',
        'image_url': 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=400&h=300&fit=crop'
    },
    {
        'id': 'minimalist',
        'name': 'Minimalist',
        'description': 'Clean and simple minimalist designs',
        'image_url': 'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400&h=300&fit=crop'
    },
    {
        'id': 'vintage',
        'name': 'Vintage',
        'description': 'Classic vintage and retro posters',
        'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop'
    },
    {
        'id': 'motivational',
        'name': 'Motivational',
        'description': 'Inspiring quotes and motivational designs',
        'image_url': 'https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=400&h=300&fit=crop'
    },
    {
        'id': 'space',
        'name': 'Space & Astronomy',
        'description': 'Cosmic and astronomical themed posters',
        'image_url': 'https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=400&h=300&fit=crop'
    }
]

# Posters data by category
POSTERS = {
    'nature': [
        {
            'id': 'nature_1',
            'name': 'Mountain Vista',
            'price': 299,
            'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=400&fit=crop'
        },
        {
            'id': 'nature_2',
            'name': 'Forest Path',
            'price': 199,
            'image_url': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=300&h=400&fit=crop'
        },
        {
            'id': 'nature_3',
            'name': 'Ocean Waves',
            'price': 249,
            'image_url': 'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=300&h=400&fit=crop'
        },
        {
            'id': 'nature_4',
            'name': 'Desert Sunset',
            'price': 279,
            'image_url': 'https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=300&h=400&fit=crop'
        }
    ],
    'abstract': [
        {
            'id': 'abstract_1',
            'name': 'Geometric Flow',
            'price': 199,
            'image_url': 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=300&h=400&fit=crop'
        },
        {
            'id': 'abstract_2',
            'name': 'Color Burst',
            'price': 229,
            'image_url': 'https://images.unsplash.com/photo-1520637836862-4d197d17c39a?w=300&h=400&fit=crop'
        },
        {
            'id': 'abstract_3',
            'name': 'Digital Dreams',
            'price': 259,
            'image_url': 'https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?w=300&h=400&fit=crop'
        }
    ],
    'minimalist': [
        {
            'id': 'minimalist_1',
            'name': 'Simple Lines',
            'price': 179,
            'image_url': 'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=300&h=400&fit=crop'
        },
        {
            'id': 'minimalist_2',
            'name': 'Clean Space',
            'price': 159,
            'image_url': 'https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=300&h=400&fit=crop'
        },
        {
            'id': 'minimalist_3',
            'name': 'Zen Garden',
            'price': 189,
            'image_url': 'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=300&h=400&fit=crop'
        }
    ],
    'vintage': [
        {
            'id': 'vintage_1',
            'name': 'Retro Car',
            'price': 219,
            'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=400&fit=crop'
        },
        {
            'id': 'vintage_2',
            'name': 'Old Camera',
            'price': 199,
            'image_url': 'https://images.unsplash.com/photo-1495121553079-4c61bcce1894?w=300&h=400&fit=crop'
        },
        {
            'id': 'vintage_3',
            'name': 'Classic Bike',
            'price': 239,
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=400&fit=crop'
        }
    ],
    'motivational': [
        {
            'id': 'motivational_1',
            'name': 'Dream Big',
            'price': 149,
            'image_url': 'https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=300&h=400&fit=crop'
        },
        {
            'id': 'motivational_2',
            'name': 'Stay Strong',
            'price': 149,
            'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=400&fit=crop'
        },
        {
            'id': 'motivational_3',
            'name': 'Never Give Up',
            'price': 169,
            'image_url': 'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=300&h=400&fit=crop'
        }
    ],
    'space': [
        {
            'id': 'space_1',
            'name': 'Galaxy Spiral',
            'price': 299,
            'image_url': 'https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=300&h=400&fit=crop'
        },
        {
            'id': 'space_2',
            'name': 'Planet Earth',
            'price': 279,
            'image_url': 'https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=300&h=400&fit=crop'
        },
        {
            'id': 'space_3',
            'name': 'Nebula Cloud',
            'price': 319,
            'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=400&fit=crop'
        }
    ]
}

@app.route('/')
def index():
    """Homepage displaying poster categories"""
    return render_template('index.html', categories=CATEGORIES)

@app.route('/category/<category_id>')
def category(category_id):
    """Category page displaying posters in a specific category"""
    # Find the category
    category_info = next((cat for cat in CATEGORIES if cat['id'] == category_id), None)
    
    if not category_info:
        return "Category not found", 404
    
    # Get posters for this category
    posters = POSTERS.get(category_id, [])
    
    return render_template('category.html', category=category_info, posters=posters)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
