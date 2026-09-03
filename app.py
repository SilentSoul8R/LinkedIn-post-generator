import os
import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="LinkedIn Post Generator",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom Styling (Clean UI without emojis)
st.markdown("""
    <style>
    .main {
        padding-top: 1.5rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #0A66C2;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #004182;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar - API Credentials & Information
st.sidebar.title("API Credentials")
api_key_input = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    help="Get a free API key at console.groq.com",
    value=st.secrets.get("GROQ_API_KEY", "") if "GROQ_API_KEY" in st.secrets else ""
)

st.sidebar.markdown("---")
st.sidebar.subheader("About")
st.sidebar.write(
    "This app helps you draft tailored LinkedIn posts using Groq LLMs. "
    "Fill in the prompt parameters and click generate to create your post."
)

# Header
st.title("LinkedIn Post Generator")
st.write("Generate tailored, high-converting LinkedIn content in seconds.")
st.markdown("---")

# Form Inputs - Sensible Order
post_name = st.text_input(
    "1. Post Name / Internal Reference",
    placeholder="e.g., Q3 Product Launch Announcement"
)

post_topic = st.text_area(
    "2. Post Topic & Key Content Points",
    placeholder="Detail your main idea, key takeaways, statistics, or story elements...",
    height=130
)

col1, col2 = st.columns(2)

with col1:
    target_audience = st.selectbox(
        "3. Target Audience",
        [
            "Software Engineers & Developers",
            "Entrepreneurs & Founders",
            "Product Managers",
            "Marketing & Sales Leaders",
            "Recruiters & HR Professionals",
            "C-Suite & Executives",
            "Job Seekers & Graduates",
            "General Professional Audience"
        ]
    )

    tone = st.selectbox(
        "4. Tone of Post",
        [
            "Professional & Authoritative",
            "Conversational & Friendly",
            "Thought-Provoking & Analytical",
            "Inspirational & Motivational",
            "Storytelling & Personal",
            "Persuasive & Direct"
        ]
    )

with col2:
    length = st.selectbox(
        "5. Post Length",
        [
            "Short (50 - 100 words)",
            "Medium (100 - 250 words)",
            "Detailed (250 - 400 words)"
        ]
    )

    include_hashtags = st.radio(
        "6. Include Hashtags",
        options=["Yes", "No"],
        index=0,
        horizontal=True
    )

# Model selection expander
with st.expander("Advanced Settings"):
    model_choice = st.selectbox(
        "Groq Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=0
    )

st.markdown("<br>", unsafe_allow_html=True)

# Generation logic
if st.button("Generate Post"):
    if not api_key_input:
        st.error("Please enter a Groq API key in the sidebar to proceed.")
    elif not post_topic.strip():
        st.warning("Please provide a topic or core points for the post.")
    else:
        try:
            client = Groq(api_key=api_key_input)

            # Constructing prompt for LLM
            prompt = f"""
You are an expert LinkedIn copywriter. Generate an engaging, high-converting LinkedIn post using these parameters:

- Internal Reference: {post_name if post_name else 'N/A'}
- Topic / Key Points: {post_topic}
- Target Audience: {target_audience}
- Tone: {tone}
- Desired Length: {length}
- Include Hashtags: {include_hashtags}

Structuring Rules:
1. Hook: Create a compelling opening line that encourages reading further.
2. Structure: Use short sentences, clear line spacing, and bullet points where useful for scannability.
3. Call to Action: End with a thoughtful question or prompt for engagement.
4. Emojis: Emojis are permitted inside the post text if they suit the chosen tone.
5. Hashtags: {"Include 3 to 5 relevant hashtags at the bottom." if include_hashtags == "Yes" else "Do NOT include hashtags."}

Return ONLY the final LinkedIn post content. Do not include conversational introductory or concluding text.
"""

            with st.spinner("Generating post..."):
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a professional LinkedIn post writer."},
                        {"role": "user", "content": prompt}
                    ],
                    model=model_choice,
                    temperature=0.7,
                    max_tokens=1024
                )
                
                generated_post = response.choices[0].message.content

            st.success("Post generated successfully!")
            st.subheader("Generated LinkedIn Post")
            st.caption("Use the copy icon on the top-right corner of the code box below to copy your text:")
            
            # st.code provides built-in 1-click clipboard copying
            st.code(generated_post, language=None)

        except Exception as e:
            st.error(f"An error occurred while generating the post: {str(e)}")
