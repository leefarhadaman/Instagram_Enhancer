import instaloader
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape_instagram():
    # Get the 'username' parameter from the URL query
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username parameter is required"}), 400
    
    # Initialize Instaloader
    L = instaloader.Instaloader()

    try:
        # Get the profile from the given username
        profile = instaloader.Profile.from_username(L.context, username)

        # Fetch profile details
        user_details = {
            "username": profile.username,
            "full_name": profile.full_name,
            "bio": profile.biography,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount,
            "is_verified": profile.is_verified,
            "is_private": profile.is_private,
            "profile_pic_url": profile.profile_pic_url,
            "external_url": profile.external_url,
            "posts_details": []  # To store post details (images, likes, comments, etc.)
        }

        # Variables for calculating engagement stats
        total_likes = 0
        total_comments = 0
        post_count = 0

        # Loop through posts and fetch details
        for post in profile.get_posts():
            post_details = {
                "image_url": post.url,
                "likes": post.likes,
                "comments": post.comments,
                "caption": post.caption,
                "date_posted": post.date_utc.strftime('%Y-%m-%d %H:%M:%S')  # Formatting the date
            }
            user_details["posts_details"].append(post_details)

            # Calculate total likes and comments for engagement rate calculation
            total_likes += post.likes
            total_comments += post.comments
            post_count += 1

        # Calculate engagement rate (simplified formula)
        engagement_rate = (total_likes + total_comments) / (user_details["followers"] * post_count) * 100 if post_count > 0 else 0
        user_details["engagement_rate"] = round(engagement_rate, 2)

        return jsonify(user_details)
    
    except instaloader.exceptions.InstaloaderException as e:
        # Return error if Instagram profile fetching fails
        return jsonify({"error": f"Could not fetch details: {str(e)}"}), 404

    except Exception as e:
        # Generic error handler
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)
