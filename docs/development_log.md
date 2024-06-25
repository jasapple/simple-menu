# Development Log

Here is rough timeline of my research and development progress over the project.

## Initial Version

For the first version, I started with a dummy database in a CSV file to setup an internal data structure for the business logic. I started with separating items into sections with different prices for different 'catagories' such as 'half' vs 'full' sub lengths. Once a simple display page was created I then worked on an admin page to add new sections and items to said sections. This version was not able to save data into the CSV but loading new data into the CSV was parsed properly into the admin and display pages. Once this concept was working, I pivoted to using python's sql library as the underlying data structure.

### Resources:

#### Flask forms
- https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
- https://stackoverflow.com/questions/34446877/how-to-handle-a-put-request-from-the-browser-in-flask
- https://stackoverflow.com/questions/67038472/jinja2-exceptions-templatesyntaxerror-encountered-unknown-tag-do
- https://jinja.palletsprojects.com/en/3.0.x/templates/#jinja-filters.default

#### CSS DIsplay
- https://stackoverflow.com/questions/16964294/how-to-evenly-space-many-inline-block-elements
- https://codeburst.io/how-to-position-html-elements-side-by-side-with-css-e1fae72ddcc
- https://stackoverflow.com/questions/3942254/how-to-specify-font-attributes-for-all-elements-on-an-html-web-page

#### Flask SQL
- https://www.geeksforgeeks.org/python-sqlite-connecting-to-database/?ref=lbp
- https://www.reddit.com/r/learnpython/comments/l4qdsx/which_database_to_use_with_python_for_beginners/

## Alpha 1:
Once a sql version was up, I needed to be able to add and remove sections. Instead of writing this by hand, I utilized chatGPT with the following prompts:

- make me jinja2 webpage for a flask app to add new data to a database
- build a flask app to show menu items on a display with an admin page to add items and sections for the display
- for the admin page, let me add an option description section
- can we edit the items on the admin page as well
- can we also edit the sections
- now lets be able to delete items and entire sections. provide a confirmation warning for sections
- this is great! can we add a toggle for an item to strike it out on the menu for when we're out of stock?
- can we have multiple prices for each item that is customizable via the admin page and shown evenly on the display
- can we change the display to be a table rather then lists
- can we make the table header change, per section, to be grouped by the kind of prices per items

From here, I tweaked a few things for styling and filled in some gaps to make everything work together. Once the database is initialized, the app cam up and I was able to add, edit, and delete items, sections, and prices. Changes were reflected on the display page on reload.


## Beta 1
Styling
