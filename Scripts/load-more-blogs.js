document.getElementById('load-more').addEventListener('click', function() {
    // Select all hidden posts
    const hiddenPosts = document.querySelectorAll('.blogpost-box.hidden');
    
    // Define the number of posts to show per click
    const postsToShow = 3;

    // Loop through the hidden posts and reveal the defined number of them
    for (let i = 0; i < postsToShow; i++) {
        if (hiddenPosts[i]) {
            hiddenPosts[i].classList.remove('hidden');
            hiddenPosts[i].classList.add('unhidden');
            void hiddenPosts[i].offsetHeight;
        }
    }

    // Check if all posts are now visible
    if (document.querySelectorAll('.blogpost-box.hidden').length === 0) {
        this.disabled = true; // Disable the "Load More" button
        this.title = "No more posts"; // Set the tooltip message
    }
});
