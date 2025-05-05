# import streamlit as st
# from db import delete_all_users, get_all_users, update_user_name, delete_user_by_email
# from utils import load_css,centered_form
# def show_admin_panel(switch_page):

#     load_css("styles/base.css")
#     load_css("styles/admin.css")
    
#     users=get_all_users()
#     st.title("👩‍💼 Admin Panel")

#     if st.checkbox("📋 Show All Users"):
#         users = get_all_users()
#         st.subheader("Registered Users")
#         for user in users:
#             st.write(f"ID: {user[0]} | Name: {user[1]} | Email: {user[2]}")

#     st.markdown("---")

#     st.subheader("✏️ Update User Name")
#     email_to_update = st.text_input("Enter user email to update")
#     new_name = st.text_input("Enter new name")

#     if st.button("Update Name"):
#         if email_to_update and new_name:
#             update_user_name(email_to_update, new_name)
#             st.success("User name updated successfully.")
#         else:
#             st.warning("Please fill in both fields.")

#     st.markdown("---")

#     st.subheader("❌ Delete User")
#     email_to_delete = st.text_input("Enter user email to delete")

#     if st.button("Delete User"):
#         if email_to_delete:
#             delete_user_by_email(email_to_delete)
#             st.success("User deleted successfully (if exists).")
#         else:
#             st.warning("Please enter an email.")
#     st.markdown("---")

#     if st.button("⚠️ Delete All Users"):
#         delete_all_users()
#         st.success("All users have been deleted")
    

#     st.button("⬅️ Back to Home", on_click=lambda: switch_page("home"))
import streamlit as st
from db import delete_all_users, get_all_users, update_user_name, delete_user_by_email
from utils import load_css

def show_admin_panel(switch_page):

    load_css("styles/base.css")
    load_css("styles/admin.css")

    st.title("👩‍💼 Admin Panel")

    # --- Create columns for top navigation ---
    col1, col2, col3, col4, col5 = st.columns(5)

    if "admin_section" not in st.session_state:
        st.session_state.admin_section = "show_users"

    # --- Top buttons to control view ---
    if col1.button("📋 Show Users"):
        st.session_state.admin_section = "show_users"
    if col2.button("✏️ Update Name"):
        st.session_state.admin_section = "update_user"
    if col3.button("❌ Delete User"):
        st.session_state.admin_section = "delete_user"
    if col4.button("⚠️ Delete All"):
        st.session_state.admin_section = "delete_all"
    if col5.button("⬅️ Back to Home"):
        switch_page("home")

    st.markdown("---")

    # --- Content Based on Active Section ---
    if st.session_state.admin_section == "show_users":
        users = get_all_users()
        st.subheader("👥 Registered Users")
        if users:
            for user in users:
                st.write(f"ID: {user[0]} | Name: {user[1]} | Email: {user[2]}")
        else:
            st.info("No users found.")

    elif st.session_state.admin_section == "update_user":
        st.subheader("✏️ Update User Name")
        email_to_update = st.text_input("Enter user email to update")
        new_name = st.text_input("Enter new name")
        if st.button("Update Now"):
            if email_to_update and new_name:
                update_user_name(email_to_update, new_name)
                st.success("User name updated successfully.")
            else:
                st.warning("Please fill in both fields.")

    elif st.session_state.admin_section == "delete_user":
        st.subheader("❌ Delete User")
        email_to_delete = st.text_input("Enter user email to delete")
        if st.button("Delete Now"):
            if email_to_delete:
                delete_user_by_email(email_to_delete)
                st.success("User deleted successfully (if exists).")
            else:
                st.warning("Please enter an email.")

    elif st.session_state.admin_section == "delete_all":
        st.subheader("⚠️ Delete All Users")
        if st.button("Confirm Delete All"):
            delete_all_users()
            st.success("All users have been deleted.")