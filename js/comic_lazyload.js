function lazyLoadComicImages() {
    // Get all of the images from the /imgs/comics/ directory
    var comicImages = document.querySelectorAll('img[src^="/img/comics/"]');
  
    // Iterate over the images and set their src attributes to the actual image URL
    // one at a time, using the load event to trigger the loading of the next image
    comicImages.forEach(function(image, index) {
      image.addEventListener('load', function() {
        // Load the next image in the array if there is one
        if (index < comicImages.length - 1) {
          comicImages[index + 1].src = comicImages[index + 1].dataset.src;
        }
      });
  
      // Set the initial src attribute to trigger the loading of the first image
      if (index === 0) {
        image.src = image.dataset.src;
      }
    });
  }