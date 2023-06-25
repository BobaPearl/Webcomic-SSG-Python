//the footer of the site would be handled in this javascript file, so you don't have to copypaste the whole thing onto every page.
//at the bottom of your page, but before the js script calls and the closing body tag, put an empty div with a class of "writeFooter"
document.querySelector(".writeFooter").innerHTML = `
    <footer align="center">
        <p>This is a comic by Boba Pearl, I own all the art and stuff, feel free to make any fanworks</p>
        <p>I made this site with the Rarebit template. I strongly recommend just learning how to do the HTML and not using wordpress. It's not worth the effort to learn all that stuff just to make a comic site.</p>
		<p>This suggestions comes from like wrestling with Wordpress and Drupal and Hugo and Jekyll for weeks and weeks. Start with the rarebit and every change just google how to do each small part bit by bit in HTML. </p>
        <p><strong>Powered by</strong></p>
        <a href="https://rarebit.neocities.org"><img src="img/rarebitlogo_small.png" height = "30" /></a>
    </footer>
`;
