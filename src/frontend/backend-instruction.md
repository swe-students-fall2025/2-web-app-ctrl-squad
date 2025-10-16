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

### deleting user account

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
      - do it later

## add/update/delete posts

### singlePost.html
* **Endpoint:** `/post/<id>`
* **Functionality:**
    - Display a single post.
    - Allow users to edit or delete their own posts.
        - If the user is the author of the post, show "Edit" and "Delete" buttons.
        - If the user clicks "Edit", redirect to the edit post page.
        - If the user clicks "Delete", remove the post from the database and redirect to the home page.

        <br>

    - Allow users to favorite/unfavorite the post.
        - If the user has already favorited the post, show "Unfavorite" button.
        - If the user clicks "Unfavorite", remove the post ID from their "favorites" array in the "users" collection.
        - If the user has not favorited the post, show "Favorite" button.
        - If the user clicks "Favorite", add the post ID to their "favorites" array in the "users" collection.

        <br>


    - Allow users to initiate a trade for item posts.
        - If the post type is "item", show "Initiate Trade" button.
        - If the user clicks "Initiate Trade", create a new trade document in the "trades" collection
        - Redirect to the trade page.

### addRoommate.html
* **Endpoint:** example: `/post/roommate/new`
* **Functionality:**
    - Allow users to create a new roommate post.  
    - Save the new post to the database.
        `- Create a new document in the "posts" collection.
        - find the user in the "users" collection and add the post ID to their "posts" array.
    - Redirect to the newly created post page.

### addItem.html
* **Endpoint:** example: `/post/item/new`
* **Functionality:**
    - Allow users to create a new item post.  
    - Save the new post to the database.
        - Create a new document in the "posts" collection.
        - find the user in the "users" collection and add the post ID to their "posts" array.
    - Redirect to the newly created post page.

