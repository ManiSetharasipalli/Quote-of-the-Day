document.addEventListener("DOMContentLoaded", function() {
    // Initial fetch of a random quote on page load
    fetchRandomQuote();

    // Function to fetch a random quote
    async function fetchRandomQuote() {
        try {
            const response = await fetch('/api/quote/random');
            const data = await response.json();
            updateQuote(data);
        } catch (error) {
            handleFetchError();
        }
    }

    // Function to fetch quotes by a specific author
    async function fetchQuotesByAuthor(authorName) {
        try {
            const response = await fetch(`/api/quote/search?author=${authorName}`);
            const data = await response.json();
            if (data.length > 0) {
                // Pick a random quote from the results (if multiple)
                const randomIndex = Math.floor(Math.random() * data.length);
                updateQuote(data[randomIndex]);
            } else {
                document.getElementById('quote').textContent = "No quotes found for author.";
                document.getElementById('author').textContent = "";
            }
        } catch (error) {
            handleFetchError();
        }
    }

    // Function to update the displayed quote
    function updateQuote(quoteData) {
        document.getElementById('quote').textContent = quoteData.quote_text;
        document.getElementById('author').textContent = `- ${quoteData.quote_author}`;
    }

    // Function to handle fetch errors
    function handleFetchError() {
        console.error('Error fetching quote.');
        document.getElementById('quote').textContent = "Failed to load quote. Please try again.";
        document.getElementById('author').textContent = "";
    }

    // Button click event to fetch a new random quote
    document.getElementById('new-quote-btn').addEventListener('click', fetchRandomQuote);

    // Event listener for author search input
    document.getElementById('author-search').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            const authorName = event.target.value.trim();
            if (authorName !== '') {
                fetchQuotesByAuthor(authorName);
            }
        }
    });

    // Make fetchRandomQuote function globally available (if needed outside of this scope)
    window.fetchRandomQuote = fetchRandomQuote;
});
