import streamlit as st
from groq import Groq
import getpass
import os
from dotenv import load_dotenv

print("Çalışma dizini:", os.getcwd())
load_dotenv()

if "GROQ_API_KEY" not in os.environ:
    api_key = st.text_input("Enter your Groq API Key:", type="password")
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
        st.success("API Key set successfully! You can now generate posts.")
    else:
        st.warning("Please enter a valid API Key.")
    if not api_key:
        st.stop()    


# API anahtarını doğrula ve kaydet


# API anahtarı olmadan devam edemez


ingredients_list = (
    "Turkish",
    "English",
    "French",
    "German")

# Uygulama başlığı
st.title("🍽️ AI Chef: Gourmet Recipe Generator")

# Dil seçimi
language = st.selectbox("🌍 Choose Language:", list(ingredients_list))

# Kullanıcı için autocomplete önerileri
ingredients = st.text_input("🍅 Enter an ingredient:", "")

# Kullanıcı girdisine göre öneri listesi gösterme

# Kullanıcının seçtiği malzemeler
#ingredients = st.text_area("📝 Enter ingredients (comma separated):")

prompt = f"""
        You are a world-class chef known for creating gourmet and restaurant-quality recipes. Your task is to generate a **single, highly detailed** recipe based on the ingredients provided by the user. Ensure that this recipe is of **chef-standard quality**, with clear and structured instructions. Follow these guidelines:  

    1️ **Recipe Name**: Provide an elegant, professional-sounding name for the dish.  

    2️⃣ **Introduction**: Briefly describe the dish, its inspiration, and the type of cuisine it belongs to. If applicable, mention any interesting facts about the dish or its ingredients.  

    3️⃣ **Ingredients List**: Clearly list all required ingredients in a structured format. If necessary, add common supporting ingredients (like oil, salt, or spices) to enhance the recipe, ensuring a balanced and flavorful dish. Include exact **measurements (grams, milliliters, teaspoons, tablespoons, etc.)** for accuracy.  

    4️⃣ **Step-by-Step Cooking Instructions**: Provide a detailed, **logical sequence** of instructions, ensuring that even a beginner can follow them easily. Use numbered steps and include professional cooking techniques where necessary. **Explain the reasoning** behind each technique (e.g., searing for better caramelization, resting meat for juiciness, etc.).  

    5️⃣ **Plating & Presentation**: Describe how to present the dish attractively, including plating techniques, garnishes, and serving suggestions. If applicable, suggest complementary side dishes or wine pairings.  

    6️⃣ **Tips & Variations**: Provide **expert-level tips** to improve the dish, substitute ingredients if needed, and offer variations for different dietary preferences (e.g., vegetarian, gluten-free, or dairy-free options).  

    7️⃣ **Language Adaptation**: The user will specify a language in the {language} variable. Ensure that the entire recipe, including the introduction and instructions, is written in that language. Use **natural, fluent, and professional** phrasing, avoiding direct word-for-word translations if they sound unnatural Variables, like ingredients, must also be in {language}..  

    ### Example Input:  
    - Ingredients: **Chicken breast, garlic, olive oil, lemon, parsley, butter**  
    - Language: **English**  

    ### Example Output:  
    - Recipe Name: **Poulet au Beurre Citronné avec Ail et Persil**  
    - Introduction: *A delicate yet flavorful dish inspired by English cuisine, featuring pan-seared chicken infused with garlic, lemon, and butter, bringing out a perfect balance of richness and freshness...*  
    - Ingredients:  
    - 2 boneless, skinless chicken breasts  
    - 2 cloves of garlic, finely minced  
    - 2 tablespoons olive oil  
    - 1 tablespoon unsalted butter  
    - Juice of 1 lemon  
    - Fresh parsley, finely chopped  
    - Salt and black pepper, to taste  

    - Instructions:  
    1. **Prepare the Chicken:** Pat the chicken breasts dry with a paper towel, ensuring they brown properly when seared.  
    2. **Marinate:** In a small bowl, mix olive oil, minced garlic, lemon juice, salt, and black pepper. Coat the chicken evenly and let it marinate for at least 15 minutes.  
    3. **Searing:** Heat a pan over medium-high heat. Add a drizzle of olive oil and sear the chicken on each side for about 4-5 minutes until golden brown.  
    4. **Butter Infusion:** Lower the heat, add butter, and baste the chicken continuously for extra flavor and moisture.  
    5. **Resting & Serving:** Remove from heat, let the chicken rest for 5 minutes, then garnish with fresh parsley. Serve with a light salad or roasted vegetables.  

    - **Chef's Tips:**  
    - For extra depth, add a splash of white wine while cooking the garlic.  
    - Pair with a crisp Sauvignon Blanc for a perfect dining experience.  
    - For a healthier twist, grill the chicken instead of pan-searing.  

    Ensure that your response is **structured, detailed, and professional**, with rich descriptions that elevate the dish to a gourmet level.  

    """

# Butona basılınca çalışacak fonksiyon
if st.button("Generate Recipes"):
    if not ingredients:
        st.warning("⚠️ Please enter some ingredients.")
    else:
        client = Groq()
        completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": ingredients
            },
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

        # Yanıtı ekrana yazdır
        content = ""
        for chunk in completion:
            print(chunk.choices[0].delta.content or "", end="")
            content += chunk.choices[0].delta.content or ""
        st.subheader("🍽️ Here are your gourmet recipes:")
        st.write(content)