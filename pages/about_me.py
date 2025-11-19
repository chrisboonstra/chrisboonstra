import streamlit as st
from forms.contact import contact_form




  
@st.dialog("Get in touch")
  
def show_contact_form():
      st.write('Reach out to me via the contact form')
      contact_form()



# -- about me section
st.title(':material/account_circle: About Me')
st.subheader("Analytics / Data Engineer")

col1, col2 = st.columns([2, 8], gap="medium", vertical_alignment="top")

with col1:
  st.image("assets/about_me.png", width=275, caption="Chris Boonstra", use_container_width=True)

  st.markdown("📍 Den Haag, Nederland")
  
  st.markdown("<br>", unsafe_allow_html=True)
  st.subheader("Interests")
  st.markdown("🏑 Field Hockey<br>🏃‍♂️ Running<br>📺 Watching Netflix<br>🧑‍🍳 Cooking<br>📖 Reading<br>👨‍👩‍👧‍👧 Family Activities", unsafe_allow_html=True)



with col2:
  
  st.html(
  """
  <aside>
  Hi I’m Chris,</br>
  An Analytics / Data Engineer from The Netherlands.
  </br>
  I specialize in building and designing robust data pipelines that drive impactful insights.</br>
  With a solid foundation in system analysis, ETL development, and dimensional modeling, I thrive at the intersection of Business and IT.</br>
  </br>
  My diverse business background allows me to bridge the gap between technical solutions and strategic goals, creating business value.</br>
  </br>
  I’m passionate about tackling new challenges, learning cutting-edge technologies, and leveraging data to optimize processes and drive innovation.</br>
  Whether it’s solving complex problems or crafting efficient data systems, I’m dedicated to helping organizations succeed through the power of IT and data.  
  </aside>
    """ 
)
  if st.button( "📧 Get in touch", key='green'):
    show_contact_form()



  st.markdown("<br>", unsafe_allow_html=True)
  # --- Experience & Qualifications
  st.empty()
  st.subheader("Experience & Qualifications", anchor= False)
  st.write(
    """
    - 7+ years of experience in data analytics
    - Strong hands-on experience in SQL and Python
    - Good understanding of data modelling
    - Critical thinker, constantly challenging the norm and seeking innovative ways to drive improvement. 
    """
  )
  st.markdown("<br>", unsafe_allow_html=True)
  # --- Skills
  st.empty()
  st.subheader("Hard Skills", anchor= False)
  st.write(
    """
    - :material/thumb_up: programming in Python and SQL
    - :material/favorite: working with Snowflake and dbt
    """
  )

