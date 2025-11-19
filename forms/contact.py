import streamlit as st
from app.functions import is_valid_email, send_email

# --- settings ---

password = st.secrets["password"]
sender = 'chris.boonstra@gmail.com'
recipients = ['chris.boonstra@gmail.com']
subject = "Contact Form (MyStreamlit App)"



def contact_form():
  with st.form("contact_form", clear_on_submit=True):
  
    name = st.text_input("First Name", key='form')
    email = st.text_input("Email adddress")
    message = st.text_area("Your Message")
    submit_button = st.form_submit_button("Submit")

    if submit_button:
      if not name:
        st.error("Please provide your name", icon="📧")
        st.stop
      if not email:
        st.error("Please provide your email address", icon="📧")
        st.stop
      if not message:
        st.error("Please provide a message", icon="💬")
        st.stop

      # --- text settings --- 
      # write the text/plain part
      text = """\
      Hi,
      """

      # write the HTML part
      html = f"""\
        <h3>Contact Form</h3>
        <p><strong>MyStreamlit App</strong></p>
        <p><strong>Naam</strong>: &nbsp;{name}
        <p><strong>Email: &nbsp;</strong>{email}</p>
        <p><strong>Message:</strong></p>
        <p>{message}</p>
        <p>&nbsp;</p>
      """
      
      
        
      try:
        send_email(subject, text, html, sender, recipients, password)
        st.success("Your message has ben sent!", icon="🚀")
      except:  
        st.error("There was an error sending your message", icon= "❌")