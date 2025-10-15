# Backend Instruction

## register-login-reset

### register.html

* **Endpoint:** `/register`
* **Functionality:**
    - Accept user registration data.
    - (Future) Verify email address.
    - (Future) Verify NYU ID.
    - If the user does not exist (check NYU ID), create a new user account.
    - If the user already exists, show an error message and prompt to log in instead.

### login.html

* **Endpoint:** `/login`
* **Functionality:**
    - Authenticate user credentials.
    - If credentials are valid, log the user in.
    - If user does not exist, remind them and prompt to register.
    - If credentials are invalid, show an error message and ask whether they forgot their password.

### reset.html

* **Endpoint:** `/reset`
* **Functionality:**
    - Allow users to reset their password.
    - (Future) Send password reset email.
    - (Future) Check verification code.
    - Update user password upon verification.
    - Show success message after password reset.

## user profile 

### profile.html

* **Endpoint:** `/profile`
* **Functionality:**
    - Display user profile information from database.
    - Show user's posts.

### profile_edit.html

* **Endpoint:** `/profile/edit`
* **Functionality:**
    - Retrieve the post data from the database.
    - Allow user to edit their profile information.
    - Save updated information to the database.

### profile_posts.html

* **Endpoint:** `/profile/posts`
* **Functionality:**
    - find all posts by the user from the database.

* **Endpoint:** `/profile/delete`
* **Functionality:**
    - Delete user account and all associated data from the database, including:
        - user profile
        - all posts made by the user
        - all favorites made by the user
        - keep trade and chats made by others with the user
        - if the user is the only member of a trade, delete the trade as well
        - if the other user involved in past trade click on the user's profile inside of trade, show a message indicating the user discarded their account.

## home - search - single post

### home.html
* **Endpoint:** `/home`
* **Functionality:**
    - handle search queries.
    - redirect to search results page.
    - Display a list of curated posts.
    - curate posts based on user preferences and interactions.eg.



## add/update/delete posts

* **Endpoints:**
    - `/post/add`: Create a new post.
    - `/post/<id>/edit`: Update an existing post.
    - `/post/<id>/delete`: Delete a post.

