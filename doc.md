change name to microArticles

Entities: [ Article, Comment, user ]

Article{
title:String
 createDate:Date
 creator: UserID
 body:Text
 
 views:int
 likes:int
 dislikes:int
 commments:CommentListID
}

User{
 username:string
 passwordL:string
}

Commnents:{
 creator: UserID
 createDate:Date
 body:text
}
user -> createUser -> metadata
article -> createArticle -> metadata

API
#articles GET /articles/<articleID> ;;Returns a article with the given articleID
# GET /articles ;;Returns a list of articles
#POST /articles ;; Create a new article, user must be login
#PUT /articles ;; Update a new article, user must be login
GET /search ;; Returns a list of articles base on the search query
#GET /articles/<articleID>/comments ;;Returns a list of comments of  the article, must be login
#POST /articles/<articleID>/comments ;;Create a new comment of the article
# GET /users/<userID> ;;Return the userName with userID, must be login and owner of the userID
POST /login ;;Login a user gets username and password
# POST /users ;;Register a new user gets username and password, username must not be exist
# PUT /user/<userID> ;; change the password of the user, must be login and owner of the userID
#POST /articles/<articleID>/like ;;increase the like count user must be login
#POST /articles/<articleID>/dislike ;;increase the dislike count user must be login
#GET /articles/<articleID>/metadata;; return the likes of the articlef
