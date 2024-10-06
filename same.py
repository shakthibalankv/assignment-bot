import logging
import requests
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define constants
TELEGRAM_BOT_TOKEN = '7635823175:AAGgk5qiDsCiozHmvNRn_JIO5IEkr8iWFd8'  # Replace with your bot token

# Rotate User-Agents to avoid bot detection
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Please send your cookies in the format: 'cookie_name=cookie_value'")

async def apply_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    # Extract cookies from user input
    cookies = {}
    try:
        for cookie in user_input.split(';'):
            name, value = cookie.strip().split('=')
            cookies[name] = value
    except ValueError:
        await update.message.reply_text("Invalid cookie format! Please use 'cookie_name=cookie_value'.")
        return

    # Apply for jobs on LinkedIn
    linkedin_response = apply_linkedin(cookies)
    if linkedin_response:
        await update.message.reply_text("Successfully applied for a job on LinkedIn!")
    else:
        await update.message.reply_text("Failed to apply for a job on LinkedIn.")

def apply_linkedin(cookies):
    # Define LinkedIn job application URL (replace with actual job ID)
    linkedin_url = "https://www.linkedin.com/jobs/view/[job-id]"  # Replace [job-id] with actual LinkedIn job ID

    # Example job application payload (adjust as per LinkedIn's requirements)
    payload = {
        'jobId': 'specific-job-id',  # Replace with actual job ID
        'resume': 'your-resume-path',  # Replace with resume path or content
    }

    # Set proper headers (mimic browser request, include CSRF token if needed)
    headers = {
        'User-Agent': random.choice(USER_AGENTS),  # Randomize User-Agent
        'Referer': 'https://www.linkedin.com/jobs/view/[job-id]',  # Replace with the actual job URL
        'csrf-token': cookies.get('JSESSIONID', ''),  # Add CSRF token from cookies if necessary
    }

    try:
        # Make request to apply
        response = requests.post(linkedin_url, cookies=cookies, headers=headers, data=payload, timeout=30)
        logging.info(f"LinkedIn Response Status Code: {response.status_code}")
        logging.info(f"LinkedIn Response Text: {response.text}")  # Logs the raw response for debugging
        return response.ok
    except requests.exceptions.RequestException as e:
        logging.error(f"Error applying to LinkedIn: {e}")
        return False

def main():
    # Create the Application and pass it your bot's token
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, apply_job))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
