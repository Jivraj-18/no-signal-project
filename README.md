# Create a .env file for environment variables
GOOGLE_CLIENT_ID="your-client-id"
GOOGLE_CLIENT_SECRET="your-google-secret"
GOOGLE_REDIRECT_URI="http://127.0.0.1:8000/auth/callback"
Syn_LLM_URL="https://quchnti6xu7yzw7hfzt5yjqtvi0kafsq.lambda-url.eu-central-1.on.aws/"
Syn_LLM_API_KEY="your-api-key"

# Add users of differnet types into database (backend/users_data.db)

# start backend server  
`cd backend`
`uv run main.py`

# start frontend 
`npm run serve`