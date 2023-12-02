# Bookmarks
#### Video Demo:  <https://youtu.be/9I35fvPIIZw?si=C1WsBtnsjEKGWKeS>
#### Description:

"Bookmarks" is a web application where you can save any links into separate folders in an organized structure.
It is developed using Flask Web Framework from Python, SQLite Database, HTML, CSS, and Bootstrap Framework.
You have to create an account first to log in, after which you can add, edit, and delete the folders and bookmarks.

If there is no folder or bookmark, you will see a message saying "No Bookmarks".

When you try to add a new bookmark, you can choose to add it in a new folder, or in an existing folder.
All the existing folder names will be there as options.
Or you can simply choose "None", which means no folder.

Add an empty new folder by clicking "Add Folder" button as well.
All bookmarks and folders will be displayed in descending order according to their timestamp.

If you click the folder name in the bookmark row, you will see just all the bookmarks in that single folder.
Bookmarks with the folder name as "None" will not be shown in "My Folders".

No matter how long the url you added it, only the base link will be displayed.
For instance, https://www.google.com will be displayed as www.google.com.
This allows you to know which website the link belongs to.

You can edit or delete any bookmarks or folders by simply clicking the buttons on the left side.
You will be able to change the name and url for bookmarks, but only the name for folders.
If you delete a folder, all the bookmarks contained in that folder will also be deleted.

The application handles any possible user errors such as empty username or password as well as
incorrect confirmation password.
You cannot register again if the username is already registered.

### Objective:

Of course there is already a Browser Bookmark. Why do we even need this?
With this web application, you can save your favourite websites in folders by creating an account.
The data will be stored in a database, and you can retrieve them anytime you want.
It is like your own personal place from where you can go to any website you like just by one click.


## Installation
Install required libraries using

```
pip install <libraryName>
```

### Libraries

1. flask
2. cs50
3. requests
4. werkzeug
5. pytz
6. DateTime


## Usage 
Download the project and run the program either by

```
$ flask run
```

or

```
$ python app.py
```
in the project directory.

## Contribution
I do expect any suggestions for the improvement of my web application.


    