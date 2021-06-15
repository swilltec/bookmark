# Python Bookmark CLI

This project is developed for saving and organizing bookmark. Bookmark allows
you to create bookmarks that, for now, will be made up of a few pieces of information:

- ID—A unique, numerical identifier for each bookmark
- Title—A short text title for the bookmark, like “GitHub”
- URL—A link to the article or website being saved
- Notes—An optional, long description or explanation about the bookmark
- Date added—A timestamp so you can

## Architecture
This project is divided into three layers of presentation, persistence, and actions or rules
is a common pattern. Some variations on this approach are so common, they’ve been
given names. Model-view-controller (MVC) is a way of modeling data for persistence,
providing users with a view into that data, and allowing them to control changes to
that data with some set of actions.

### Persistance
The persistence layer is the lowest level of the bookmark.
This layer will be concerned with taking information it
receives and communicating it to the database. The database module provides 
most of what you need to manage bookmark data, including the following:
- reating a table (for initializing the database)
- Adding or deleting a record
- Listing the records in a table
- Selecting and sorting records from a table based on some criteria
- Counting the number of records in a table


## Technologies
 - Sqlite
