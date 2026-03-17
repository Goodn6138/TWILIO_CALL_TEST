from app import create_app

# Create Flask app
app = create_app()

if __name__ == "__main__":
    # Run on port 5000, debug mode on for development
    app.run(host="0.0.0.0", port=5000, debug=True)
