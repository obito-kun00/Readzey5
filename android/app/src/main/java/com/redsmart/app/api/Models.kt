package com.redsmart.app.api

data class Book(
    val id: Int,
    val title: String,
    val author: String?,
    val description: String?,
    val cover_url: String?,
    val pdf_url: String?,
    val total_pages: Int
)

data class BookResponse(
    val books: List<Book>
)

data class LoginResponse(
    val success: Boolean,
    val message: String?,
    val token: String?,
    val user_id: Int?,
    val username: String?,
    val is_admin: Boolean?
)

data class ProfileResponse(
    val success: Boolean,
    val username: String,
    val email: String,
    val friends_count: Int,
    val profile_photo: String?,
    val stats: UserStats,
    val activities: List<UserActivity>,
    val badges: List<UserBadge>
)

data class UserStats(
    val total_books: Int,
    val pages_read: Int,
    val total_pages_goal: Int
)

data class UserActivity(
    val type: String,
    val desc: String,
    val date: String
)

data class UserBadge(
    val name: String,
    val icon: String?
)

data class FriendsResponse(
    val success: Boolean,
    val friends: List<Friend>,
    val requests: List<FriendRequest>,
    val invites: List<ReadingInvite>,
    val active_sessions: List<ActiveSession>
)

data class Friend(
    val id: Int,
    val username: String,
    val is_online: Boolean
)

data class FriendRequest(
    val id: Int,
    val sender_id: Int,
    val sender_username: String
)

data class ReadingInvite(
    val id: Int,
    val sender_name: String,
    val book_title: String,
    val book_id: Int
)

data class ActiveSession(
    val id: Int,
    val book_id: Int,
    val book_title: String,
    val partner_name: String,
    val partner_id: Int
)
