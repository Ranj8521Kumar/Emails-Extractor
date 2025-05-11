/**
 * Email Extractor - Frontend JavaScript
 *
 * This script handles the client-side functionality of the Email Extractor application.
 * It manages user interactions, API calls, and displaying results.
 *
 * Author: Your Name
 * Date: May 2025
 */

// Execute code when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements - Get references to all the elements we need to interact with
    const extractForm = document.getElementById('extractForm');           // The main form
    const websiteUrlInput = document.getElementById('websiteUrl');        // URL input field
    const maxPagesInput = document.getElementById('maxPages');            // Max pages input
    const extractButton = document.getElementById('extractButton');       // Submit button
    const buttonText = extractButton.querySelector('.button-text');       // Button text
    const spinner = extractButton.querySelector('.spinner');              // Loading spinner
    const resultsContainer = document.getElementById('resultsContainer'); // Results section
    const emailList = document.getElementById('emailList');               // List of emails
    const emailCount = document.getElementById('emailCount');             // Email counter
    const pagesCount = document.getElementById('pagesCount');             // Pages counter
    const copyAllButton = document.getElementById('copyAllButton');       // Copy all button
    const downloadButton = document.getElementById('downloadButton');     // Download button
    const errorContainer = document.getElementById('errorContainer');     // Error container
    const errorMessage = document.getElementById('errorMessage');         // Error message
    const settingsToggle = document.getElementById('settingsToggle');     // Settings toggle
    const advancedSettings = document.getElementById('advancedSettings'); // Advanced settings

    /**
     * API URL Configuration
     *
     * Dynamically determine the API URL based on the current location.
     * This ensures the frontend works in both development and production environments.
     */
    const API_URL = window.location.protocol + '//' + window.location.host;

    /**
     * Advanced Settings Toggle
     *
     * Show/hide the advanced settings panel when the user clicks the gear icon.
     */
    settingsToggle.addEventListener('click', () => {
        advancedSettings.classList.toggle('visible');
    });

    /**
     * Form Submission Handler
     *
     * Process the form submission, validate inputs, and call the API.
     */
    extractForm.addEventListener('submit', async (e) => {
        e.preventDefault();  // Prevent the default form submission

        // Get and process form values
        const url = websiteUrlInput.value.trim();
        const maxPages = parseInt(maxPagesInput.value);

        // Validate the URL format
        if (!isValidUrl(url)) {
            showError('Please enter a valid URL including http:// or https://');
            return;
        }

        // Reset the UI state for a new request
        hideError();
        emailList.innerHTML = '';
        resultsContainer.classList.add('hidden');

        // Show loading indicators
        setLoadingState(true);

        try {
            // Call the API to extract emails
            const result = await extractEmails(url, maxPages);

            // Display the results in the UI
            displayResults(result);
        } catch (error) {
            // Handle and display any errors
            showError(error.message || 'An error occurred while extracting emails');
        } finally {
            // Always reset the loading state when done
            setLoadingState(false);
        }
    });

    /**
     * Copy All Emails Button Handler
     *
     * Copies all extracted emails to the clipboard when the user clicks the "Copy All" button.
     * Shows feedback to the user when the operation is complete.
     */
    copyAllButton.addEventListener('click', () => {
        // Get all email elements
        const emailItems = document.querySelectorAll('.email-item .email');
        if (emailItems.length === 0) return;  // Do nothing if no emails found

        // Extract the text content from each email element
        const emails = Array.from(emailItems).map(item => item.textContent);
        // Join emails with newlines and copy to clipboard
        copyToClipboard(emails.join('\\n'));

        // Show visual feedback to the user
        copyAllButton.textContent = 'Copied!';
        // Reset the button text after 2 seconds
        setTimeout(() => {
            copyAllButton.innerHTML = '<i class="fas fa-copy"></i> Copy All';
        }, 2000);
    });

    /**
     * Download CSV Button Handler
     *
     * Creates and downloads a CSV file containing all extracted emails
     * when the user clicks the "Download CSV" button.
     */
    downloadButton.addEventListener('click', () => {
        // Get all email elements
        const emailItems = document.querySelectorAll('.email-item .email');
        if (emailItems.length === 0) return;  // Do nothing if no emails found

        // Extract the text content from each email element
        const emails = Array.from(emailItems).map(item => item.textContent);
        // Generate and download a CSV file
        downloadCsv(emails);
    });

    /**
     * API Call Function
     *
     * Makes a POST request to the server API to extract emails from the provided URL.
     * Includes timeout handling to prevent the request from hanging indefinitely.
     *
     * @param {string} url - The website URL to extract emails from
     * @param {number} maxPages - Maximum number of pages to crawl
     * @returns {Promise<Object>} - The API response containing extracted emails
     * @throws {Error} - If the request fails or times out
     */
    async function extractEmails(url, maxPages) {
        try {
            // Set a timeout for the fetch request (30 seconds)
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 30000);

            // Make the API request
            const response = await fetch(`${API_URL}/extract-emails`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    url: url,
                    max_pages: maxPages
                }),
                signal: controller.signal  // For timeout handling
            });

            // Clear the timeout since the request completed
            clearTimeout(timeoutId);

            // Handle non-successful responses
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to extract emails');
            }

            // Parse and return the JSON response
            return await response.json();
        } catch (error) {
            // Special handling for timeout errors
            if (error.name === 'AbortError') {
                throw new Error('Request timed out. The website might be too large or slow to process.');
            }
            // Re-throw other errors
            throw error;
        }
    }

    /**
     * Display Results Function
     *
     * Processes the API response and displays the extracted emails in the UI.
     * Updates statistics and creates interactive elements for each email.
     *
     * @param {Object} result - The API response object
     */
    function displayResults(result) {
        // Check for errors in the result
        if (result.error) {
            showError(result.error);
            return;
        }

        // Extract data from the result
        const emails = result.emails || [];
        const pagesCrawled = result.pages_crawled || 0;

        // Update statistics in the UI
        emailCount.textContent = emails.length;
        pagesCount.textContent = pagesCrawled;

        // Create and display email items
        if (emails.length > 0) {
            emails.forEach(email => {
                // Create a container for each email
                const emailItem = document.createElement('div');
                emailItem.className = 'email-item';
                emailItem.innerHTML = `
                    <span class="email">${email}</span>
                    <button class="copy-btn" title="Copy email">
                        <i class="fas fa-copy"></i>
                    </button>
                `;

                // Add copy functionality to each email's copy button
                const copyBtn = emailItem.querySelector('.copy-btn');
                copyBtn.addEventListener('click', () => {
                    copyToClipboard(email);
                    // Show visual feedback
                    copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                    // Reset after 1.5 seconds
                    setTimeout(() => {
                        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                    }, 1500);
                });

                // Add the email item to the list
                emailList.appendChild(emailItem);
            });
        } else {
            // Display a message if no emails were found
            emailList.innerHTML = '<div class="email-item">No emails found</div>';
        }

        // Show the results container
        resultsContainer.classList.remove('hidden');
    }

    /**
     * Helper Functions
     *
     * These utility functions handle common tasks throughout the application.
     */

    /**
     * Set Loading State
     *
     * Updates the UI to show or hide loading indicators.
     *
     * @param {boolean} isLoading - Whether the application is in a loading state
     */
    function setLoadingState(isLoading) {
        if (isLoading) {
            // Show loading state
            buttonText.textContent = 'Extracting...';
            spinner.classList.remove('hidden');
            extractButton.disabled = true;  // Prevent multiple submissions
        } else {
            // Reset to normal state
            buttonText.textContent = 'Extract Emails';
            spinner.classList.add('hidden');
            extractButton.disabled = false;
        }
    }

    /**
     * Show Error Message
     *
     * Displays an error message to the user.
     *
     * @param {string} message - The error message to display
     */
    function showError(message) {
        errorMessage.textContent = message;
        errorContainer.classList.remove('hidden');
    }

    /**
     * Hide Error Message
     *
     * Hides the error message container.
     */
    function hideError() {
        errorContainer.classList.add('hidden');
    }

    /**
     * Validate URL Format
     *
     * Checks if a string is a valid URL.
     *
     * @param {string} url - The URL to validate
     * @returns {boolean} - True if the URL is valid, false otherwise
     */
    function isValidUrl(url) {
        try {
            // Attempt to create a URL object
            new URL(url);
            return true;
        } catch (e) {
            // If it throws an error, the URL is invalid
            return false;
        }
    }

    /**
     * Copy Text to Clipboard
     *
     * Copies the provided text to the user's clipboard.
     *
     * @param {string} text - The text to copy to the clipboard
     */
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).catch(err => {
            console.error('Failed to copy text: ', err);
        });
    }

    /**
     * Download Emails as CSV
     *
     * Creates and triggers download of a CSV file containing the emails.
     *
     * @param {string[]} emails - Array of email addresses to include in the CSV
     */
    function downloadCsv(emails) {
        // Create a data URI for the CSV content
        const csvContent = 'data:text/csv;charset=utf-8,' + emails.join('\\n');
        const encodedUri = encodeURI(csvContent);

        // Create a temporary link element to trigger the download
        const link = document.createElement('a');
        link.setAttribute('href', encodedUri);
        link.setAttribute('download', 'extracted_emails.csv');

        // Append to the document, click it, and remove it
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
});
