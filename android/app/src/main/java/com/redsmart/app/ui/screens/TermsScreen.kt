package com.redsmart.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TermsScreen(onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Terms of Service") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
                .verticalScroll(rememberScrollState())
        ) {
            Text("Welcome to Redsmart", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(16.dp))
            
            TermSection("1. Acceptance of Terms", "By accessing or using Redsmart, you agree to be bound by these Terms of Service and all applicable laws and regulations.")
            TermSection("2. User Accounts", "You are responsible for maintaining the confidentiality of your account and password. You agree to accept responsibility for all activities that occur under your account.")
            TermSection("3. Content", "Our service allows you to access various books and documents. You may not distribute or reproduce copyrighted material without permission.")
            TermSection("4. Termination", "We may terminate or suspend your account and bar access to the service immediately, without prior notice, for any reason whatsoever.")
            TermSection("5. Changes to Terms", "We reserve the right to modify or replace these terms at any time. We will provide notice of significant changes.")
        }
    }
}

@Composable
fun TermSection(title: String, content: String) {
    Column(modifier = Modifier.padding(vertical = 8.dp)) {
        Text(text = title, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
        Spacer(modifier = Modifier.height(4.dp))
        Text(text = content, style = MaterialTheme.typography.bodyMedium)
    }
}
