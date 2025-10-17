# Backend Instruction

## user collection structure
* user_data 
    - `_id`: ObjectId(),
    - `email`: email,
    - `username`: username,
    - `nyu_id`: nyu_id
    - `password_hash`: generate_password_hash(password)
    - `bio`: bio or ''
    - `posts`: [] &nbsp;
    - `favorites`: [] &nbsp;
    - `trades`: [] &nbsp;
    - `created_at`: datetime.utcnow()
        

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

* **Endpoint:** `/profile/<username>`
* **Functionality:**
    - Display user profile information from database.
    - button to edit profile => profile_edit.html
    - button to manage user's posts => profile_posts.html
    - button to manage user's trades => manage_order.html
    - button to exchange request pending => seller_trade_page.html
    - list of user's posts with links to single post pages.


### profile_edit.html

* **Endpoint:** `/profile/<username>/edit`
* **Functionality:**
    - Retrieve the post data from the database.
    - Allow user to edit their profile information.
    - Save updated information to the database.

### profile_posts.html

* **Endpoint:** `/profile/<username>/posts`
* **Functionality:**
    - find all posts by the user from the database.
    - click view button to view the post. => post/<id> => singlePost.html
    - click delete button to delete the post.
        - remove the post from the "posts" collection.
        - remove the post ID from the user's "posts" array in the "users" collection.
        - if the post is an item post and is involved in any trades, remove the user from those trades as well.
        - if the trade has no other members, delete the trade as well.
        

### deleting user account (html not ready yet)

* **Endpoint:** `/profile/<username>/delete`
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

### searchResults.html
* **Endpoint:** `/search/keyword`
* **Functionality:**
    - Accept search queries from the user again
    - send search queries again and redirect to search results page with updated results.
        - Display search results with pagination. 


    - click filter button to filter search results.
        - filter by post type (roommate/item)
        - roommate：
          - filter by years to be roommates (shortest/longest)
        
        - item：
          - filter by category (for item posts)
          - filter by status (available/unavailable)
          - filter by trade location (manhattan/brooklyn/off-campus)

    - click sort button to sort search results.

        - roomate posts:
          - sort by years to be roommates (shortest/longest)
          - sort by number of favorites (most to least/least to most)
          - sort by date posted (newest/oldest)
          - sort by date updated (newest/oldest)

        - item posts:
          - sort by price (low to high/high to low)
          - sort by number of favorites (most to least/least to most)
          - sort by date posted (newest/oldest)
          - sort by date updated (newest/oldest)

    - (future) show pagination controls at the bottom of the page.
        - click on a page number to go to that page.
        - click on next/previous buttons to go to the next/previous page.

## add/update/delete posts

### single page: exchange_post.html
* **Endpoint:** `/post/<id>`
* **Functionality:**
    - Display a single post.
    - Allow users to edit or delete their own posts.
        - If the user is the author of the post, show "Edit" and "Delete" buttons.
        - If the user clicks "Edit", redirect to the edit post page.

        <br>

    - Allow users to favorite/unfavorite the post.
        - If the user has already favorited the post, show "Unfavorite" button.
        - If the user clicks "Unfavorite", remove the post ID from their "favorites" array in the "users" collection.
        - If the user has not favorited the post, show "Favorite" button.
        - If the user clicks "Favorite", add the post ID to their "favorites" array in the "users" collection.

        <br>


    - Allow users to initiate a trade for item posts.
        - If the post type is "item", show "exchange" button.
        - If the user clicks "exchange", create a new trade document in the "trades" collection
          - mark the trade status as "pending"
          - add the buyer (current user) and seller (post author) to the trade document
          - add the post ID to the trade document
          - add the trade ID to both users' "trades" array in the "users" collection.
        - Redirect to the request_sent.html page.

### itemPost_edit.html and roommatePost_edit.html
* **Endpoint:** example: `/post/<id>/edit`
* **Functionality:**
    - check type of post (roommate/item)
    - if roommate post, redirect to roommatePost_edit.html
    - if item post, redirect to itemPost_edit.html
    - roommatePost_edit.html and itemPost_edit.html share similar functionality:
    - if item post, display item edit form.
        - Retrieve the post data from the database.
        - Allow user to edit their post.
        - Save updated information to the database.

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

## trades

### trade collection structure
* trade_data
    - `_id`: ObjectId(),
    - `post_id`: ObjectId of the post involved in the trade
    - `buyer_id`: ObjectId of the user initiating the trade (buyer)
    - `seller_id`: ObjectId of the user offering the item (seller)
    - `item_name`: Name of the item being traded
    - `images`: List of image URLs or paths (optional)
    - `status`: Trade status (`open`, `pending`, `accepted`, `completed`, `cancelled`)
    - `created_at`: Timestamp when the trade was created
    - `updated_at`: Timestamp when the trade was last updated

### manage_order.html
* **Endpoint:** `user/<user_id>/trades`
* **Functionality:**
    - Display a list of trades the user is involved in.
    - click on acknowledge receipt button to see the trade details.

### buyer_trade.html
* **Endpoint:** `user/<user_id>/trades/buyer`
* **Functionality:**
    - Display a list of trades the user is involved in as a buyer.
    - Separated ongoing and completed trades.

    - ongoing trades:
        - if the trade status is "pending"
            - mean the trade request is sent but not yet accepted by the seller.
            - click on the trade to view trade details.
        - if the trade status is "accepted"
            - mean the trade request is accepted by the seller.
            - click on the trade to view trade details.

    - completed trades:
        - if the trade status is "completed"
            - click on the trade to view trade details.
        - if the trade status is "cancelled"
            - click on the trade to view trade details.

### buyer-trade-page.html
* **Endpoint:** `user/<user_id>/trades/buyer/<trade_id>`
* **Functionality:**
    - Display the details of a specific trade the user is involved in as a buyer.
     - if the trade status is "pending"
            - mean the trade request is sent but not yet accepted by the seller.
            - click on cancel button to cancel the trade request.
                - popup a confirmation dialog to confirm the cancellation.
                - if confirmed go to route: `/trade/<trade_id>/cancel`
                    - remove the trade ID from both users' "trades" array in the "users" collection.
                    - delete the trade document from the "trades" collection.
                    - redirect to manage_order.html page.
        - if the trade status is "accepted"
            - mean the trade request is accepted by the seller.
            - click on acknowledge receipt button to acknowledge the receipt of the item.
                - update the trade status to "accepted".
                - update the post status to "unavailable".
                - redirect to manage_order.html page.
    - if the trade status is "completed"
        - go to 

### request_sent.html
* **Endpoint:** `user/<user_id>/trades/request`
* **Functionality:**
    - Display a message indicating that the trade request has been sent.
    - Provide a button to go back to the post page.

### seller_trade.html
* **Endpoint:** `user/<user_id>/trades/seller`
* **Functionality:**
    - Display a list of trades the user is involved in as a seller.

### seller-trade-page.html
* **Endpoint:** `user/<user_id>/trades/seller/<trade_id>`
* **Functionality:**
    - Display the details of a specific trade the user is involved in as a seller.
    - if the trade status is "pending"
        - mean the trade request is sent but not yet accepted by the seller.
        - click on accept button to accept the trade request.
            - update the trade status to "accepted".
            - redirect to manage_order.html page.
        - click on decline button to decline the trade request.
            - popup a confirmation dialog to confirm the decline.
            - if confirmed go to route: `/trade/<trade_id>/cancel`
                - remove the trade ID from both users' "trades" array in the "users" collection.
                - delete the trade document from the "trades" collection.
                - redirect to manage_order.html page.
    - if the trade status is "accepted"
        - the trade should be viewed as not-available on the post page.
    - if the trade status is "completed"
        - go to trade completion page.

### tradeComplete.html