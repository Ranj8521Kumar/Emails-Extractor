document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const extractForm = document.getElementById('extractForm');
    const websiteUrlInput = document.getElementById('websiteUrl');
    const maxPagesInput = document.getElementById('maxPages');
    const extractButton = document.getElementById('extractButton');
    const buttonText = extractButton.querySelector('.button-text');
    const spinner = extractButton.querySelector('.spinner');
    const resultsContainer = document.getElementById('resultsContainer');
    const emailList = document.getElementById('emailList');
    const emailCount = document.getElementById('emailCount');
    const pagesCount = document.getElementById('pagesCount');
    const copyAllButton = document.getElementById('copyAllButton');
    const downloadButton = document.getElementById('downloadButton');
    const errorContainer = document.getElementById('errorContainer');
    const errorMessage = document.getElementById('errorMessage');
    const settingsToggle = document.getElementById('settingsToggle');
    const advancedSettings = document.getElementById('advancedSettings');

    // API URL - Points to the Flask API
    const API_URL = window.location.protocol + '//' + window.location.host;

    // Toggle advanced settings
    settingsToggle.addEventListener('click', () => {
        advancedSettings.classList.toggle('visible');
    });

    // Form submission
    extractForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get form values
        const url = websiteUrlInput.value.trim();
        const maxPages = parseInt(maxPagesInput.value);

        // Validate URL
        if (!isValidUrl(url)) {
            showError('Please enter a valid URL including http:// or https://');
            return;
        }

        // Clear previous results and errors
        hideError();
        emailList.innerHTML = '';
        resultsContainer.classList.add('hidden');

        // Show loading state
        setLoadingState(true);

        try {
            // Call the API
            const result = await extractEmails(url, maxPages);

            // Display results
            displayResults(result);
        } catch (error) {
            showError(error.message || 'An error occurred while extracting emails');
        } finally {
            setLoadingState(false);
        }
    });

    // Copy all emails
    copyAllButton.addEventListener('click', () => {
        const emailItems = document.querySelectorAll('.email-item .email');
        if (emailItems.length === 0) return;

        const emails = Array.from(emailItems).map(item => item.textContent);
        copyToClipboard(emails.join('\\n'));

        // Show feedback
        copyAllButton.textContent = 'Copied!';
        setTimeout(() => {
            copyAllButton.innerHTML = '<i class="fas fa-copy"></i> Copy All';
        }, 2000);
    });

    // Download as CSV
    downloadButton.addEventListener('click', () => {
        const emailItems = document.querySelectorAll('.email-item .email');
        if (emailItems.length === 0) return;

        const emails = Array.from(emailItems).map(item => item.textContent);
        downloadCsv(emails);
    });

    // API call function
    async function extractEmails(url, maxPages) {
        const response = await fetch(`${API_URL}/extract-emails`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: url,
                max_pages: maxPages
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to extract emails');
        }

        return await response.json();
    }

    // Display results function
    function displayResults(result) {
        if (result.error) {
            showError(result.error);
            return;
        }

        const emails = result.emails || [];
        const pagesCrawled = result.pages_crawled || 0;

        // Update stats
        emailCount.textContent = emails.length;
        pagesCount.textContent = pagesCrawled;

        // Create email items
        if (emails.length > 0) {
            emails.forEach(email => {
                const emailItem = document.createElement('div');
                emailItem.className = 'email-item';
                emailItem.innerHTML = `
                    <span class="email">${email}</span>
                    <button class="copy-btn" title="Copy email">
                        <i class="fas fa-copy"></i>
                    </button>
                `;

                // Add copy functionality
                const copyBtn = emailItem.querySelector('.copy-btn');
                copyBtn.addEventListener('click', () => {
                    copyToClipboard(email);
                    copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                    setTimeout(() => {
                        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                    }, 1500);
                });

                emailList.appendChild(emailItem);
            });
        } else {
            emailList.innerHTML = '<div class="email-item">No emails found</div>';
        }

        // Show results container
        resultsContainer.classList.remove('hidden');
    }

    // Helper functions
    function setLoadingState(isLoading) {
        if (isLoading) {
            buttonText.textContent = 'Extracting...';
            spinner.classList.remove('hidden');
            extractButton.disabled = true;
        } else {
            buttonText.textContent = 'Extract Emails';
            spinner.classList.add('hidden');
            extractButton.disabled = false;
        }
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorContainer.classList.remove('hidden');
    }

    function hideError() {
        errorContainer.classList.add('hidden');
    }

    function isValidUrl(url) {
        try {
            new URL(url);
            return true;
        } catch (e) {
            return false;
        }
    }

    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).catch(err => {
            console.error('Failed to copy text: ', err);
        });
    }

    function downloadCsv(emails) {
        const csvContent = 'data:text/csv;charset=utf-8,' + emails.join('\\n');
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement('a');
        link.setAttribute('href', encodedUri);
        link.setAttribute('download', 'extracted_emails.csv');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
});
