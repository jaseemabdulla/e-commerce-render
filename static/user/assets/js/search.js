$(document).ready(function() {
    const searchInput = $('#myInput');
    const suggestionsList = $('#menu_search');
    
    searchInput.on('input', function() {
        const query = $(this).val();
        $.ajax({
            url: '/search/suggestions/', // Update the URL to your Django endpoint
            data: { query: query },
            success: function(response) {
                const suggestions = response.suggestions;
                suggestionsList.empty();
                if (suggestions.length === 0) {
                    suggestionsList.append('<li>No products found</li>');
                } else {
                    suggestions.forEach(function(suggestion) {
                        const url = '/user_product_search/?key=' + encodeURIComponent(suggestion);
                        suggestionsList.append(`<li><a href="${url}">${suggestion}</a></li>`);
                    });
                }
                
                
            }
        });
    });
});