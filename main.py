from flask import Flask, render_template

app = Flask(__name__)

# All posters data
ALL_POSTERS = [

    {
        'id': 'poster_1',
        'name': 'Mountain Vista',
        'price': 299,
        'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=400&fit=crop'
    },
    {
        'id': 'poster_2',
        'name': 'Forest Path',
        'price': 199,
        'image_url': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=300&h=400&fit=crop'
    },
    {
        'id': 'poster_3',
        'name': 'Ocean Waves',
        'price': 249,
        'image_url': 'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=300&h=400&fit=crop'
    },
    {
        'id': 'poster_4',
        'name': 'Desert Sunset',
        'price': 279,
        'image_url': 'https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=300&h=400&fit=crop'
    },
    {
        'id': 'poster_5',
        'name': 'Geometric Flow',
        'price': 199,
        'image_url': 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=300&h=400&fit=crop'
    },
    {
        'id': 'poster_6',
        'name': 'Color Burst',
        'price': 229,
        'image_url': 'https://images.unsplash.com/photo-1520637836862-4d197d17c39a?w=300&h=400&fit=crop'
    },
    {
        'id': 'poster_7',
        'name': 'Digital Dreams',
        'price': 259,
        'image_url': 'https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?w=300&h=400&fit=crop'
    },
    {
        'id': 'poster_8',
        'name': 'Simple Lines',
        'price': 179,
        'image_url': 'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=300&h=400&fit=crop'
    },
    {
        'id': 'poster_9',
        'name': 'Clean Space',
        'price': 159,
        'image_url': 'https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=300&h=400&fit=crop'
    },
    {
        'id': 'poster_10',
        'name': 'Zen Garden',
        'price': 189,
        'image_url': 'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=300&h=400&fit=crop'
    },
    {
        'id': 'poster_11',
        'name': 'Retro Car',
        'price': 219,
        'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=400&fit=crop'
    },
    {
        'id': 'poster_12',
        'name': 'Old Camera',
        'price': 199,
        'image_url': 'https://images.unsplash.com/photo-1495121553079-4c61bcce1894?w=300&h=400&fit=crop'
    },
    {
        'id': 'poster_13',
        'name': 'Dream Big',
        'price': 149,
        'image_url': 'https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=300&h=400&fit=crop'
    },
    {
        'id': 'poster_14',
        'name': 'Stay Strong',
        'price': 149,
        'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=400&fit=crop'
    },
    {
        'id': 'poster_15',
        'name': 'Galaxy Spiral',
        'price': 299,
        'image_url': 'https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=300&h=400&fit=crop'
    }
]

@app.route('/')
def index():
    """Homepage with posters button"""
    return render_template('index.html')

@app.route('/posters')
def posters():
    """Posters page displaying all posters"""
    return render_template('posters.html', posters=ALL_POSTERS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
