package com.redsmart.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.navigation.NavType
import androidx.navigation.compose.*
import androidx.navigation.navArgument
import com.redsmart.app.ui.screens.*
import com.redsmart.app.ui.theme.RedsmartTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            var userId by remember { mutableStateOf(-1) }
            var isAdmin by remember { mutableStateOf(false) }
            
            RedsmartTheme {
                if (userId == -1) {
                    LoginScreen(onLoginSuccess = { id, admin -> 
                        userId = id
                        isAdmin = admin
                    })
                } else {
                    if (isAdmin) {
                        AdminAppScaffold(onLogout = { userId = -1; isAdmin = false })
                    } else {
                        MainAppScaffold(userId = userId, onLogout = { userId = -1; isAdmin = false })
                    }
                }
            }
        }
    }
}

@Composable
fun AdminAppScaffold(onLogout: () -> Unit) {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    Scaffold(
        bottomBar = {
            NavigationBar {
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Home, contentDescription = "Dashboard") },
                    label = { Text("Dashboard") },
                    selected = currentRoute == "admin_dashboard",
                    onClick = { navController.navigate("admin_dashboard") }
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Add, contentDescription = "Upload") },
                    label = { Text("Upload") },
                    selected = currentRoute == "admin_upload",
                    onClick = { navController.navigate("admin_upload") }
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.List, contentDescription = "Books") },
                    label = { Text("Manage") },
                    selected = currentRoute == "admin_books",
                    onClick = { navController.navigate("admin_books") }
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.ExitToApp, contentDescription = "Logout") },
                    label = { Text("Logout") },
                    selected = false,
                    onClick = onLogout
                )
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = "admin_dashboard",
            modifier = Modifier.padding(innerPadding)
        ) {
            composable("admin_dashboard") { AdminDashboardScreen() }
            composable("admin_upload") { AdminUploadScreen() }
            composable("admin_books") { AdminManageBooksScreen() }
        }
    }
}

@Composable
fun MainAppScaffold(userId: Int, onLogout: () -> Unit) {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    Scaffold(
        bottomBar = {
            if (currentRoute in listOf("home", "library", "friends", "profile", "more")) {
                NavigationBar {
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Home, contentDescription = "Home") },
                        label = { Text("Home") },
                        selected = currentRoute == "home",
                        onClick = { navController.navigate("home") { popUpTo("home") { inclusive = true } } }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Menu, contentDescription = "Library") },
                        label = { Text("Library") },
                        selected = currentRoute == "library",
                        onClick = { navController.navigate("library") }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Person, contentDescription = "Friends") },
                        label = { Text("Friends") },
                        selected = currentRoute == "friends",
                        onClick = { navController.navigate("friends") }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.AccountCircle, contentDescription = "Profile") },
                        label = { Text("Profile") },
                        selected = currentRoute == "profile",
                        onClick = { navController.navigate("profile") }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.MoreVert, contentDescription = "More") },
                        label = { Text("More") },
                        selected = currentRoute == "more",
                        onClick = { navController.navigate("more") }
                    )
                }
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = "home",
            modifier = Modifier.padding(innerPadding)
        ) {
            composable("home") { HomeScreen() }
            composable("library") { LibraryScreen(onBookClick = { bookId -> navController.navigate("book_details/$bookId") }) }
            composable("friends") { FriendsScreen(userId = userId) }
            composable("profile") { ProfileScreen(userId = userId) }
            composable("more") { 
                MoreScreen(
                    onNavigate = { route -> navController.navigate(route) },
                    onLogout = onLogout
                )
            }
            composable(
                "book_details/{bookId}",
                arguments = listOf(navArgument("bookId") { type = NavType.IntType })
            ) { backStackEntry ->
                val bookId = backStackEntry.arguments?.getInt("bookId") ?: 0
                BookDetailsScreen(bookId = bookId, onBack = { navController.popBackStack() })
            }
            composable("about_us") { AboutUsScreen(onBack = { navController.popBackStack() }) }
            composable("contact_us") { ContactUsScreen(onBack = { navController.popBackStack() }) }
            composable("privacy_policy") { PrivacyPolicyScreen(onBack = { navController.popBackStack() }) }
            composable("terms_of_service") { TermsScreen(onBack = { navController.popBackStack() }) }
        }
    }
}
