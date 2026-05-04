package com.redsmart.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.redsmart.app.api.Friend
import com.redsmart.app.api.FriendsResponse
import com.redsmart.app.api.RetrofitClient
import kotlinx.coroutines.launch

@Composable
fun FriendsScreen(userId: Int) {
    var friendsData by remember { mutableStateOf<FriendsResponse?>(null) }
    var isLoading by remember { mutableStateOf(true) }
    val scope = rememberCoroutineScope()

    LaunchedEffect(Unit) {
        scope.launch {
            try {
                friendsData = RetrofitClient.instance.getFriends(userId)
            } catch (e: Exception) {
                // Handle error
            } finally {
                isLoading = false
            }
        }
    }

    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Text(
            text = "Social",
            style = MaterialTheme.typography.headlineMedium,
            color = MaterialTheme.colorScheme.primary,
            fontWeight = FontWeight.Bold
        )
        
        if (isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        } else {
            TabbedFriendsContent(friendsData)
        }
    }
}

@Composable
fun TabbedFriendsContent(data: FriendsResponse?) {
    var selectedTab by remember { mutableIntStateOf(0) }
    val tabs = listOf("Friends", "Requests", "Invites")

    Column {
        TabRow(selectedTabIndex = selectedTab) {
            tabs.forEachIndexed { index, title ->
                Tab(
                    selected = selectedTab == index,
                    onClick = { selectedTab = index },
                    text = { Text(title) }
                )
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        when (selectedTab) {
            0 -> FriendsList(data?.friends ?: emptyList())
            1 -> RequestsList(data?.requests ?: emptyList())
            2 -> InvitesList(data?.invites ?: emptyList())
        }
    }
}

@Composable
fun FriendsList(friends: List<Friend>) {
    if (friends.isEmpty()) {
        Text("No friends yet. Start searching!")
    } else {
        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            items(friends) { friend ->
                Card(modifier = Modifier.fillMaxWidth()) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(Icons.Default.Person, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                        Spacer(modifier = Modifier.width(16.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(friend.username, fontWeight = FontWeight.Bold)
                            Text(
                                if (friend.is_online) "Online" else "Offline",
                                style = MaterialTheme.typography.labelSmall,
                                color = if (friend.is_online) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.secondary
                            )
                        }
                        Button(onClick = { /* Invite to read */ }) {
                            Text("Invite")
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun RequestsList(requests: List<com.redsmart.app.api.FriendRequest>) {
    if (requests.isEmpty()) {
        Text("No pending requests.")
    } else {
        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            items(requests) { req ->
                Card(modifier = Modifier.fillMaxWidth()) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(req.sender_username, modifier = Modifier.weight(1f), fontWeight = FontWeight.Bold)
                        Button(onClick = { /* Accept */ }) {
                            Text("Accept")
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun InvitesList(invites: List<com.redsmart.app.api.ReadingInvite>) {
    if (invites.isEmpty()) {
        Text("No reading invites.")
    } else {
        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            items(invites) { inv ->
                Card(modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("${inv.sender_name} invited you to read", style = MaterialTheme.typography.bodySmall)
                        Text(inv.book_title, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(8.dp))
                        Button(onClick = { /* Accept */ }, modifier = Modifier.fillMaxWidth()) {
                            Text("Join Session")
                        }
                    }
                }
            }
        }
    }
}
