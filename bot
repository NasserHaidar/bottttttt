import os
import logging
import requests
import time
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup , ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters , CallbackContext
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker


# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine("sqlite:///bot_database.db")  # SQLite database
Session = sessionmaker(bind=engine)
session = Session()


# Define the UserInteraction model
class UserInteraction(Base):
    __tablename__ = "user_interactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String, nullable=True)
    prompt = Column(Text, nullable=False)
    generated_image_url = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


# Create tables if not already present
Base.metadata.create_all(engine)


# Define user data model for SQLite
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    balance = Column(Integer, default=0)


# Create the users table if not present
Base.metadata.create_all(engine)


# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_record = session.query(User).filter_by(id=user.id).first()

    # Define inline keyboard buttons
    keyboard = [
        [InlineKeyboardButton("Help", callback_data='help')],
        [InlineKeyboardButton("Generate", callback_data='generate')],
        [InlineKeyboardButton("Profile", callback_data='profile')],
        [InlineKeyboardButton("Balance", callback_data='balance')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if user_record:  # User exists
        await update.message.reply_text(f"Welcome back, {user_record.username}! What would you like to do?",
                                        reply_markup=reply_markup)
    else:  # New user, prompt for username
        await update.message.reply_text("Welcome! Please enter your username to register:")
        context.user_data['awaiting_username'] = True  # Flag for waiting username entry


# Define the /profile command
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_record = session.query(User).filter_by(id=user.id).first()

    if user_record:
        user_id = user_record.id
        username = user_record.username
        balance = user_record.balance

        interactions = session.query(UserInteraction).filter_by(user_id=user_id).order_by(UserInteraction.timestamp.desc()).limit(5).all()

        message = f"User ID: {user_id}\nUsername: {username}\nBalance: {balance}\n\nRecent Images:"
        if interactions:
            for interaction in interactions:
                message += f"\n- {interaction.timestamp}: {interaction.generated_image_url}"
        else:
            message += "\nNo images generated yet."

        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Profile not found. Use /start to register.")


# Define the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the custom keyboard
    keyboard = [
        ["/profile", "/balance"],
        ["/generate", "/help"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Available commands:\n"  
                                     "/start - Start the bot\n"  
                                     "/profile - Register or view your profile\n"  
                                     "/balance - Check your current balance\n"  
                                     "/generate - Write what you want to generate",
                                     reply_markup=reply_markup)


# Handle username input
async def handle_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = update.message.text.strip()

    # Register the user in the database
    new_user = User(id=user.id, username=username)
    session.add(new_user)
    session.commit()

    await update.message.reply_text(f"Thank you for registering, {username}! You can now use the bot.",
                                    reply_markup=InlineKeyboardMarkup([
                                        [InlineKeyboardButton("Help", callback_data='help')],
                                        [InlineKeyboardButton("Generate", callback_data='generate')],
                                        [InlineKeyboardButton("Profile", callback_data='profile')],
                                        [InlineKeyboardButton("Balance", callback_data='balance')],
                                    ]))
    context.user_data['awaiting_username'] = False  # Reset flag


# Define the /balance command
async def check_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the custom keyboard
    keyboard = [
        ["/profile", "/balance"],
        ["/generate", "/help"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    user = update.effective_user
    user_record = session.query(User).filter_by(id=user.id).first()  # Use SQLAlchemy to query the user

    if user_record:
        await update.message.reply_text(f"Your current balance is: {user_record.balance} credits.",
                                        reply_markup=reply_markup)
    else:
        await update.message.reply_text("You don't have an account yet. Use /start to register.",
                                        reply_markup=reply_markup)



async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    try:
        # Check if the user provided a prompt
        if context.args:
            user_prompt = " ".join(context.args)
        else:
            await update.message.reply_text(
                "Please provide a prompt after /generate. Example:\n/generate a futuristic city at night")
            return

        # Acknowledge the prompt
        await update.message.reply_text(f"Received your prompt: {user_prompt}\nGenerating an image, please wait...")

        # Prepare the API payload
        payload = {
            "height": 512,
            "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",  # Replace with your Leonardo model ID
            "prompt": user_prompt,
            "width": 512
        }

        # Call Leonardo API to start generation
        response = requests.post(
            "https://cloud.leonardo.ai/api/rest/v1/generations",
            json=payload,
            headers=LEONARDO_HEADERS
        )
        response.raise_for_status()

        # Extract generation ID
        generation_id = response.json()['sdGenerationJob']['generationId']

        # Wait for image generation to complete
        time.sleep(20)

        # Retrieve the generated image URL
        result_response = requests.get(
            f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}",
            headers=LEONARDO_HEADERS
        )
        result_response.raise_for_status()
        generated_image_url = result_response.json()['images'][0]['url']

        # Log the interaction in the database
        interaction = UserInteraction(
            user_id=user.id,
            username=user.username,
            prompt=user_prompt,
            generated_image_url=generated_image_url
        )
        session.add(interaction)
        session.commit()

        # Send the generated image back to the user
        await update.message.reply_photo(generated_image_url,
                                         caption=f"Here is your image based on the prompt: {user_prompt}")
    except Exception as e:
        logger.error(f"Error during image generation: {e}")
        await update.message.reply_text("An error occurred while generating the image. Please try again later.")


# Function to handle image uploads
async def handle_image(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Image uploads are not supported in this version of the bot.")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower().strip()

    if user_message.startswith("generate"):
        # Extract the prompt after the word "generate"
        user_prompt = user_message[len("generate"):].strip()

        if not user_prompt:
            await update.message.reply_text(
                "Please provide a description of what you want to generate. Example:\ngenerate a futuristic city at night"
            )
            return

        await update.message.reply_text(f"Received your prompt: {user_prompt}\nProcessing...")

        # Add logic to handle the prompt (e.g., call Leonardo API or other actions)
        await update.message.reply_text(f"Image generation for '{user_prompt}' is not yet implemented.")
    else:
        # Respond to other text inputs
        await update.message.reply_text("Unrecognized command or input. Use /help to see available commands.")


async def process_generate_request(update: Update, context: ContextTypes.DEFAULT_TYPE, user_prompt: str) -> None:
    """Process the user's image generation request."""
    await update.message.reply_text(f"Processing your request: {user_prompt}")
    # Add the logic for image generation here.



# Button handler for inline buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    if query.data == "generate":
        await query.edit_message_text("Please enter your image prompt to generate an image:")
        context.user_data['awaiting_prompt'] = True  # Flag for waiting prompt input
    elif query.data == "profile":
        user = context.user_data.get('user')  # Get user info if available
        if user:
            user_record = session.query(User).filter_by(id=user.id).first()
            await query.edit_message_text(f"Your profile: {user_record.username}")
        else:
            await query.edit_message_text("No profile data found.")
    elif query.data == "balance":
        user = context.user_data.get('user')  # Get user info if available
        if user:
            user_record = session.query(User).filter_by(id=user.id).first()
            await query.edit_message_text(f"Your current balance is: {user_record.balance}")
        else:
            await query.edit_message_text("No balance data found.")
    elif query.data == "help":
        await query.edit_message_text("Here is how you can use the bot: ...")

    # Handle text input for prompts or username


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if context.user_data.get('awaiting_username'):
        await handle_username(update, context)
    elif context.user_data.get('awaiting_prompt'):
        user_prompt = update.message.text.strip()
        # Call the function to generate the image (implementation depends on your requirements)
        await update.message.reply_text(f"Processing image generation for: {user_prompt}")
        context.user_data['awaiting_prompt'] = False  # Reset flag
    else:
        await update.message.reply_text("Unrecognized command or input. Use the menu to see available commands.")

    # Define the main function to run the bot


def main():
    # Create the Application and the command handlers
    application = Application.builder().token('7667227066:AAGy9ibE511zCBk_tKjhlaoNJFeX6whV6ds').build()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("generate" , generate))
    application.add_handler(CommandHandler("balance", check_balance))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run the bot
    application.run_polling()


if __name__ == '__main__':
    main()
