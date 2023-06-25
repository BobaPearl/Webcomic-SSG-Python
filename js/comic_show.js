//comic_show.js was created by geno7, with much needed assistance from Dannarchy



//this is the script that actually displays the comics, nav and comic title on the page. 



//below are what's called some "function calls", each one is responsible for making an element of the page. to get something to actually show up on the page, all you'd need to do is make a div with a class that has the same name as the function call. i.e. writeNav shows comic navigation, to show it on a page youd use <div class="writeNav"></div> wherever you want it to be. You can even put multiple divs with that same class name and it'll display multiple instances of the navigation.



//a couple of the function calls have toggles too.







writeNav(true); //show navigation for comic pages. to toggle either images or text for nav, set this to true or false.



//debug

console.log(pg)



writePageTitle(".writePageTitle", true, " - "); //write title of page. true/false



writePageClickable(".writePageClickable",false); //show the current page. to toggle whether pages can be clicked to move to the next one, set this to true or false.



writeAuthorNotes(".writeAuthorNotes");



//keyNav(); //enables navigation through the comic with the arrow keys and WSAD. It doesn't need a div with a class name, it automatically works. delete or comment out (add // at the beginning) here to disable.



// below this point is more under-the-hood type stuff that we only encourage messing with if you're more familiar with js, 

// but it's still commented as extensively as possible anyway just in case



//SHOW COMIC PAGE, with clickable link


function writePageClickable(div, clickable) {
  if (!clickable) {
    document.querySelector(div).innerHTML = `<div class="comicPage">${writePage()}</div>`;
  } else if (pg < maxpg) {
    // Create an image element and set its `src` to the path of the image
    let img = new window.Image();
    img.src = path;

    // Set the `onload` event handler to a function that will insert the image into the DOM
    img.onload = function() {
      document.querySelector(div).innerHTML = `<div class="comicPage"><a href="?pg=${pg + 1}${navScrollTo}"/>${writePage()}</a></div>`;
    }
  } else {
    document.querySelector(div).innerHTML = `<div class="comicPage">${writePage()}</div>`;
  }
}



function writePageTitle(div,toggleNum, char) {

  if (pgData.length >= pg) {

    //display title of current page

    document.querySelector(div).innerHTML = `<h1>${pgData[pg - 1].title}</h1>`;

    if (toggleNum) {

        //toggle whether you want to display the page number

        document.querySelector(div).innerHTML = `<h1>${pgData[pg - 1].pgNum + char + pgData[pg - 1].title}</h1>`; //char denotes a separating character between the number and the title

    }

  }

}



function writeAuthorNotes(div) { //display author notes

  if (pgData.length >= pg) {

    return document.querySelector(div).innerHTML = `${pgData[pg-1].authorNotes}`

  }

}



//function used to split pages into multiple images if needed, and add alt text

function writePage() {
  let partExtension = "";
  let altText = "";
  let path = (folder != "" ? folder + "/" : "") + image + pg + partExtension + "." + ext;
  let page = ``;

  if (pgData.length < pg) {
    console.log("page code to insert - " + page);
    console.log("alt text to insert - " + altText);
    return `<img alt="` + altText + `" title="` + altText + `" src="` + path + `" loading="eager"` + `" />`;
  } else if (pgData.length >= pg) {
    altText = pgData[pg - 1].altText;

    if (pgData[pg-1].imageFiles > 1) {
      for (let i = 1; i < pgData[pg-1].imageFiles+1; i++) {
        partExtension = imgPart + i.toString();
        path = (folder != "" ? folder + "/" : "") + image + pg + partExtension + "." + ext;
        if (i > 1) {page += `<br/>`}
        page += `<img alt="` + altText + `" title="` + altText + `" src="` + path + `" loading="eager"` + `" />`;

        // Delay the loading of the next image by 1 second
      }
    } else {
      page = `<img alt="` + altText + `" title="` + altText + `" src="` + path + `" loading="eager"` + `" />`;
    }

    console.log("page code to insert - " + page);
    console.log("alt text to insert - " + altText);
    return page;
  }
}


//debug

console.log("array blank/not long enough? " + (pgData.length < pg));

console.log("array length - " + pgData.length);

console.log("current page - " + pg);

console.log("number of page segments - " + pgData[pg-1].imageFiles);

console.log("alt text - " + `"` + pgData[pg - 1].altText + `"`);



console.log("nav text - " + navText);

console.log("nav image file extension - " + navExt);



function imgOrText(setImg,navTextSet) { //function that writes the indicated nav button as either an image or text



  if (setImg) { //if its an image

    return `<img src="` + navFolder + `/nav_` + navText[navTextSet].toLowerCase() + `.` + navExt + `" alt="` + navText[navTextSet] + `" />`;

  } else {

    return navText[navTextSet];

  }

}



function writeNav(imageToggle) {

    let writeNavDiv = document.querySelectorAll(".writeNav");

    writeNavDiv.forEach(function(element) {

      element.innerHTML = `<div class="comicNav">

        ${firstButton()}

        ${divider()}

        ${prevButton()}

        ${divider()}

        ${nextButton()}

        ${divider()}

        ${lastButton()}

        </div>

        `;})



    function firstButton() {

        //FIRST BUTTON

        if (pg > 1) {

            //wait until page 2 to make button active

            return `<a href="?pg=` + 1 + navScrollTo + `"/>` + imgOrText(imageToggle, 0) + `</a>`;

        } else {

            if (!imageToggle) {

                return imgOrText(imageToggle, 0);

            } else {

                return ``;

            }

        }

    }



    function divider() {

        //divider

        if (!imageToggle) {

            return ` | `;

        }

        return ``;

    }



    function prevButton() {

        //PREV BUTTON

        if (pg > 1) {

            //wait until page 2 to make button active

            return `<a href="?pg=` + (pg - 1) + navScrollTo + `"/>` + imgOrText(imageToggle, 1) + `</a>`;

        } else {

            if (!imageToggle) {

                return imgOrText(imageToggle, 1);

            } else {

                return ``;

            }

        }

    }



    function nextButton() {

        //NEXT BUTTON

        if (pg < maxpg) {

            //only make active if not on the last page

            return `<a href="?pg=` + (pg + 1) + navScrollTo + `"/>` + imgOrText(imageToggle, 2) + `</a>`;

        } else {

            if (!imageToggle) {

                return imgOrText(imageToggle, 2);

            } else {

                return ``;

            }

        }

    }



    function lastButton() {

        //LAST BUTTON

        if (pg < maxpg) {

            //only make active if not on last page

            return `<a href="?pg=` + maxpg + navScrollTo + `"/>` + imgOrText(imageToggle, 3) + `</a>`;

        } else {

            if (!imageToggle) {

                return imgOrText(imageToggle, 3);

            } else {

                return ``;

            }

        }

    }

}



//KEYBOARD NAVIGATION

function keyNav() {

  document.addEventListener("keydown", (e) => {

  if ((e.key == 'ArrowRight' || e.key.toLowerCase() == 'd') && pg < maxpg) { //right arrow or D goes to next page

    window.location.href = "?pg=" + (pg + 1) + navScrollTo;

  } else if ((e.key == "ArrowLeft" || e.key.toLowerCase() == "a") && pg > 1) { //left arrow or A goes to previous page

    window.location.href = "?pg=" + (pg - 1) + navScrollTo;

  } else if (e.key.toLowerCase() == "w") { //W scrolls up

    window.scrollBy({ top: -30 });

  } else if (e.key.toLowerCase() == "s") { //S scrolls down

    window.scrollBy({ top: 30 });

  }

});};

